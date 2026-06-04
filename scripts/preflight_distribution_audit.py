#!/usr/bin/env python3
"""Print SHA-256 receipts for built distribution files in dist/."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    files = sorted(p for p in DIST.glob("*") if p.is_file())
    if not files:
        print("FAIL: no distribution files found in dist/")
        return 1
    print("AXZ ReceiptCI distribution preflight audit")
    for path in files:
        print(f"{path.relative_to(ROOT)}  bytes={path.stat().st_size}  sha256={sha256_file(path)}")
    print("PASS: AXZ_RECEIPTCI_DIST_PREFLIGHT_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
