# AXZ-ReceiptCI v1.2.0 Benchmarks

AXZ-ReceiptCI v1.2.0 adds a deterministic benchmark and stress-test suite for measuring source-tree scanning, canonical hashing, and drift detection on large simulated repositories.

## What the benchmark does

The benchmark script lives at:

```text
tests/benchmark_suite.py
```

It performs four steps:

1. Generates a deterministic mock repository with a configurable number of files.
2. Runs the real AXZ ReceiptCI `scan_files()` and `source_tree_hash()` path.
3. Mutates exactly one file deep inside the generated tree.
4. Re-runs the canonical scan/hash path and verifies that the source-tree hash changes.

## Run locally

```bash
python tests/benchmark_suite.py --files 10000 --subdirs 10 --out certificates/benchmark_report.json
```

For a faster smoke test:

```bash
python tests/benchmark_suite.py --files 1000 --subdirs 10
```

## Expected behavior

A successful run prints:

```text
Status                           : BENCHMARK_PASS
Drift detected                   : True
```

The JSON report includes:

```text
schema_version
benchmark_version
total_files
subdirectories
file_count
total_bytes_before_drift
total_bytes_after_drift
generation_seconds
scan_seconds
drift_scan_seconds
initial_source_tree_hash
mutated_source_tree_hash
drift_file
drift_detected
status
```

## Performance interpretation

The benchmark is intentionally hardware-sensitive. Local disk speed, CPU speed, runner virtualization, and file-system cache state can change the reported timing. The important invariant is not a fixed speed claim. The important invariant is:

```text
same generated tree -> deterministic source-tree hash
one-file mutation -> different source-tree hash
```

AXZ ReceiptCI's file traversal and hashing scale approximately linearly with the number of included files because each file is read once and every canonical manifest record is sorted deterministically before the root hash is computed.

## Truth boundary

This benchmark does not claim that AXZ ReceiptCI replaces SLSA, Sigstore, GitHub Artifact Attestations, Bazel, Nix, or enterprise CI systems. It shows that the AXZ ReceiptCI canonical scan/hash path can process a large simulated repository and detect a controlled one-file drift event under the stated test conditions.
