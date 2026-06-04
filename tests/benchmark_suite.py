#!/usr/bin/env python3
"""AXZ ReceiptCI v1.2 benchmark suite.

This script builds a deterministic mock repository, runs the real AXZ ReceiptCI
canonical scanner and source-tree hasher, mutates one file, and verifies that the
root hash changes. It is intentionally standard-library only.
"""
from __future__ import annotations

import argparse
import json
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from axz_receiptci.core import scan_files, source_tree_hash


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def generate_mock_repository(base_path: Path, total_files: int = 10_000, subdirs: int = 10) -> None:
    """Construct a deterministic nested mock repository."""
    if total_files < 1:
        raise ValueError("total_files must be at least 1")
    if subdirs < 1:
        raise ValueError("subdirs must be at least 1")

    for i in range(subdirs):
        (base_path / f"module_zone_{i}").mkdir(parents=True, exist_ok=True)

    for file_idx in range(total_files):
        dir_bucket = file_idx % subdirs
        file_path = base_path / f"module_zone_{dir_bucket}" / f"source_file_{file_idx:05d}.py"
        file_path.write_text(
            "\n".join(
                [
                    f"# AXZ deterministic benchmark payload: {file_idx}",
                    f"VALUE_{file_idx} = {file_idx}",
                    f"def payload_{file_idx}():",
                    f"    return VALUE_{file_idx}",
                    "",
                ]
            ),
            encoding="utf-8",
        )


def execute_hashing_pass(target_dir: Path) -> tuple[str, int, int, float]:
    """Run the real AXZ ReceiptCI scan/hash path and return metrics."""
    start = time.perf_counter()
    records = scan_files(target_dir)
    root_hash = source_tree_hash(records)
    duration = time.perf_counter() - start
    total_bytes = sum(record.bytes for record in records)
    return root_hash, len(records), total_bytes, duration


def run_performance_suite(total_files: int = 10_000, subdirs: int = 10) -> dict[str, Any]:
    """Run scaling and drift benchmarks and return structured metrics."""
    with tempfile.TemporaryDirectory(prefix="axz_receiptci_benchmark_") as tmp:
        tmp_repo = Path(tmp)

        t_start_gen = time.perf_counter()
        generate_mock_repository(tmp_repo, total_files=total_files, subdirs=subdirs)
        generation_seconds = time.perf_counter() - t_start_gen

        initial_hash, file_count, total_bytes, scan_seconds = execute_hashing_pass(tmp_repo)

        drift_index = min(total_files - 1, max(0, total_files // 2 + 55))
        drift_file = tmp_repo / f"module_zone_{drift_index % subdirs}" / f"source_file_{drift_index:05d}.py"
        drift_file.write_text(
            drift_file.read_text(encoding="utf-8") + "# AXZ drift mutation insertion.\n",
            encoding="utf-8",
        )

        drift_hash, drift_file_count, drift_total_bytes, drift_scan_seconds = execute_hashing_pass(tmp_repo)

        drift_detected = initial_hash != drift_hash
        if not drift_detected:
            raise AssertionError("Drift mutation did not change source tree hash")
        if file_count != total_files or drift_file_count != total_files:
            raise AssertionError("Benchmark file count mismatch")

        return {
            "schema_version": "axz.receiptci.benchmark.v1",
            "benchmark_version": "1.2.0",
            "generated_at_utc": utc_now_iso(),
            "total_files": total_files,
            "subdirectories": subdirs,
            "file_count": file_count,
            "total_bytes_before_drift": total_bytes,
            "total_bytes_after_drift": drift_total_bytes,
            "generation_seconds": round(generation_seconds, 6),
            "scan_seconds": round(scan_seconds, 6),
            "drift_scan_seconds": round(drift_scan_seconds, 6),
            "initial_source_tree_hash": initial_hash,
            "mutated_source_tree_hash": drift_hash,
            "drift_file": drift_file.relative_to(tmp_repo).as_posix(),
            "drift_detected": drift_detected,
            "status": "BENCHMARK_PASS",
        }


def print_report(metrics: dict[str, Any]) -> None:
    print("\n" + "=" * 62)
    print("  AXZ-RECEIPTCI V1.2.0 BENCHMARK METRICS")
    print("=" * 62)
    print(f"Generated at UTC                 : {metrics['generated_at_utc']}")
    print(f"Repository scale                 : {metrics['total_files']} files")
    print(f"Subdirectories                   : {metrics['subdirectories']}")
    print(f"File population generation time  : {metrics['generation_seconds']:.6f} seconds")
    print(f"Canonical scan/hash time         : {metrics['scan_seconds']:.6f} seconds")
    print(f"Post-drift re-scan time          : {metrics['drift_scan_seconds']:.6f} seconds")
    print(f"Initial source-tree hash         : {metrics['initial_source_tree_hash']}")
    print(f"Mutated source-tree hash         : {metrics['mutated_source_tree_hash']}")
    print(f"Drift file                       : {metrics['drift_file']}")
    print(f"Drift detected                   : {metrics['drift_detected']}")
    print(f"Status                           : {metrics['status']}")
    print("=" * 62)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AXZ ReceiptCI v1.2 benchmark suite.")
    parser.add_argument("--files", type=int, default=10_000, help="Number of mock files to generate. Default: 10000.")
    parser.add_argument("--subdirs", type=int, default=10, help="Number of module subdirectories. Default: 10.")
    parser.add_argument("--out", default=None, help="Optional JSON metrics output path.")
    args = parser.parse_args()

    metrics = run_performance_suite(total_files=args.files, subdirs=args.subdirs)
    print_report(metrics)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"[AXZ-ReceiptCI] Benchmark JSON written to {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
