# AXZ ReceiptCI v1.2.0 Release Notes

AXZ ReceiptCI v1.2.0 adds the Benchmark and Stress-Test Suite.

## Added

- `tests/benchmark_suite.py`
- `tests/test_benchmark_suite.py`
- `docs/BENCHMARKS.md`
- GitHub Actions benchmark execution
- 10,000-file simulated repository stress test
- one-file drift mutation benchmark
- structured JSON benchmark output

## Core capability

The benchmark suite measures the real AXZ ReceiptCI canonical source-tree scan and hash path, then mutates one file and verifies that the root hash changes.

## Truth label

```text
CERTIFIED_BUILD_RECEIPT_ENGINE_V0
```

## Boundary

AXZ ReceiptCI v1.2.0 is still a deterministic receipt layer. It does not replace SLSA, Sigstore, GitHub Artifact Attestations, Bazel, Nix, or enterprise CI systems.
