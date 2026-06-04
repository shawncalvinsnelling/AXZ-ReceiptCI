from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

TRUTH_LABEL = "CERTIFIED_BUILD_RECEIPT_ENGINE_V0"
SCHEMA_VERSION = "axz.receiptci.v1"

DEFAULT_IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".ipynb_checkpoints",
    "dist",
    "build",
    "htmlcov",
    "node_modules",
    "certificates",
}

DEFAULT_IGNORE_FILES = {
    ".DS_Store",
    "Thumbs.db",
}

PASS_STATUS = "CERTIFIED_REPRODUCIBLE_PASS"
FAILED_TESTS = "FAILED_TESTS"
HASH_DRIFT = "HASH_DRIFT_DETECTED"
MISSING_FILE = "MISSING_FILE"
CERT_MISMATCH = "CERTIFICATE_MISMATCH"


@dataclass(frozen=True)
class FileRecord:
    path: str
    bytes: int
    sha256: str

    def canonical_line(self) -> str:
        return f"{self.path}\0{self.sha256}\0{self.bytes}\n"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def should_ignore(path: Path, root: Path, out_dir: Path | None = None) -> bool:
    rel_parts = path.relative_to(root).parts
    if any(part in DEFAULT_IGNORE_DIRS for part in rel_parts):
        return True
    if path.name in DEFAULT_IGNORE_FILES:
        return True
    if path.name.endswith(".pyc"):
        return True
    if out_dir is not None:
        try:
            path.relative_to(out_dir)
            return True
        except ValueError:
            pass
    return False


def scan_files(root: Path, out_dir: Path | None = None) -> list[FileRecord]:
    root = root.resolve()
    out_dir = out_dir.resolve() if out_dir is not None else None
    records: list[FileRecord] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if should_ignore(path, root, out_dir):
            continue
        rel = path.relative_to(root).as_posix()
        records.append(FileRecord(path=rel, bytes=path.stat().st_size, sha256=sha256_file(path)))
    records.sort(key=lambda r: r.path)
    return records


def source_tree_hash(records: Iterable[FileRecord]) -> str:
    canonical = "".join(record.canonical_line() for record in records).encode("utf-8")
    return sha256_bytes(canonical)


def run_verifier(command: str | Sequence[str] | None, cwd: Path) -> dict:
    if not command:
        return {
            "test_command": None,
            "test_exit_code": 0,
            "test_status": "SKIPPED_BY_REQUEST",
            "test_duration_seconds": 0.0,
            "stdout_tail": "",
            "stderr_tail": "",
        }
    start = time.monotonic()
    if isinstance(command, str):
        completed = subprocess.run(command, cwd=str(cwd), shell=True, text=True, capture_output=True)
        command_repr = command
    else:
        completed = subprocess.run(list(command), cwd=str(cwd), shell=False, text=True, capture_output=True)
        command_repr = " ".join(command)
    duration = round(time.monotonic() - start, 6)
    return {
        "test_command": command_repr,
        "test_exit_code": completed.returncode,
        "test_status": "PASS" if completed.returncode == 0 else "FAIL",
        "test_duration_seconds": duration,
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
    }


def artifact_records(root: Path, artifacts: Sequence[str] | None) -> list[FileRecord]:
    records: list[FileRecord] = []
    for item in artifacts or []:
        path = (root / item).resolve()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"Artifact not found: {item}")
        records.append(FileRecord(path=item, bytes=path.stat().st_size, sha256=sha256_file(path)))
    records.sort(key=lambda r: r.path)
    return records


def certificate_hash(certificate: dict) -> str:
    clone = json.loads(json.dumps(certificate, sort_keys=True))
    clone.pop("certificate_hash", None)
    encoded = json.dumps(clone, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(encoded)


def receipt_text(certificate: dict) -> str:
    lines = [
        "AXZ ReceiptCI Verification Receipt",
        f"project_name: {certificate['project_name']}",
        f"truth_label: {certificate['truth_label']}",
        f"status: {certificate['status']}",
        f"generated_at_utc: {certificate['generated_at_utc']}",
        f"test_command: {certificate['test_command']}",
        f"test_exit_code: {certificate['test_exit_code']}",
        f"file_count: {certificate['file_count']}",
        f"total_bytes: {certificate['total_bytes']}",
        f"source_tree_hash: {certificate['source_tree_hash']}",
        f"certificate_hash: {certificate['certificate_hash']}",
    ]
    return "\n".join(lines) + "\n"


def write_sha256sums(out_dir: Path, files: Sequence[Path]) -> None:
    lines = []
    for path in files:
        lines.append(f"{sha256_file(path)}  {path.name}")
    (out_dir / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def create_receipt(
    root: Path,
    out_dir: Path,
    project_name: str,
    test_command: str | Sequence[str] | None,
    artifacts: Sequence[str] | None = None,
) -> dict:
    root = root.resolve()
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    run = run_verifier(test_command, root)
    records = scan_files(root, out_dir=out_dir)
    tree_hash = source_tree_hash(records)
    art_records = artifact_records(root, artifacts)

    status = PASS_STATUS if run["test_exit_code"] == 0 else FAILED_TESTS
    cert = {
        "schema_version": SCHEMA_VERSION,
        "project_name": project_name,
        "truth_label": TRUTH_LABEL,
        "status": status,
        "generated_at_utc": utc_now_iso(),
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "python_implementation": platform.python_implementation(),
        "working_directory_name": root.name,
        "test_command": run["test_command"],
        "test_exit_code": run["test_exit_code"],
        "test_status": run["test_status"],
        "test_duration_seconds": run["test_duration_seconds"],
        "stdout_tail": run["stdout_tail"],
        "stderr_tail": run["stderr_tail"],
        "ignore_policy": sorted(DEFAULT_IGNORE_DIRS),
        "file_count": len(records),
        "total_bytes": sum(record.bytes for record in records),
        "source_tree_hash": tree_hash,
        "artifact_hashes": [record.__dict__ for record in art_records],
        "files": [record.__dict__ for record in records],
    }
    cert["certificate_hash"] = certificate_hash(cert)
    text = receipt_text(cert)
    cert["receipt_text_hash"] = sha256_bytes(text.encode("utf-8"))
    cert["certificate_hash"] = certificate_hash(cert)
    text = receipt_text(cert)

    cert_path = out_dir / "certificate.json"
    receipt_path = out_dir / "receipt.txt"
    cert_path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt_path.write_text(text, encoding="utf-8")
    write_sha256sums(out_dir, [cert_path, receipt_path])
    return cert


def load_certificate(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_receipt(certificate_path: Path, root: Path | None = None) -> dict:
    cert = load_certificate(certificate_path)
    cert_clone = dict(cert)
    expected_cert_hash = cert_clone.get("certificate_hash")
    actual_cert_hash = certificate_hash(cert_clone)
    if expected_cert_hash != actual_cert_hash:
        return {"status": CERT_MISMATCH, "reason": "certificate_hash mismatch"}

    if root is None:
        root = certificate_path.resolve().parents[1]
    root = root.resolve()
    records = []
    for item in cert.get("files", []):
        path = root / item["path"]
        if not path.exists():
            return {"status": MISSING_FILE, "reason": item["path"]}
        actual = FileRecord(path=item["path"], bytes=path.stat().st_size, sha256=sha256_file(path))
        if actual.bytes != item["bytes"] or actual.sha256 != item["sha256"]:
            return {"status": HASH_DRIFT, "reason": item["path"]}
        records.append(actual)
    records.sort(key=lambda r: r.path)
    actual_tree = source_tree_hash(records)
    if actual_tree != cert.get("source_tree_hash"):
        return {"status": HASH_DRIFT, "reason": "source_tree_hash mismatch"}
    return {"status": cert.get("status", PASS_STATUS), "reason": "receipt verified"}
