from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_benchmark_suite_small_run(tmp_path: Path) -> None:
    out = tmp_path / "benchmark.json"
    completed = subprocess.run(
        [sys.executable, "tests/benchmark_suite.py", "--files", "120", "--subdirs", "6", "--out", str(out)],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "BENCHMARK_PASS" in completed.stdout
    metrics = json.loads(out.read_text(encoding="utf-8"))
    assert metrics["status"] == "BENCHMARK_PASS"
    assert metrics["total_files"] == 120
    assert metrics["file_count"] == 120
    assert metrics["drift_detected"] is True
    assert metrics["initial_source_tree_hash"] != metrics["mutated_source_tree_hash"]
    assert len(metrics["initial_source_tree_hash"]) == 64
    assert len(metrics["mutated_source_tree_hash"]) == 64
