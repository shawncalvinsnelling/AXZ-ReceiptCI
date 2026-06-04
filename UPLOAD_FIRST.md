# Upload AXZ ReceiptCI v1.2.0 Patch

Use this patch to upgrade the existing `AXZ-ReceiptCI` repository from v1.1.0 to v1.2.0.

## Upload steps

1. Open the existing GitHub repository: `AXZ-ReceiptCI`.
2. Upload every file in this patch.
3. Commit directly to `main`.

Commit message:

```text
Add v1.2 benchmark suite
```

## Critical files

Make sure these files exist after upload:

```text
.github/workflows/verify.yml
.github/workflows/receipt_engine.yml
tests/benchmark_suite.py
tests/test_benchmark_suite.py
docs/BENCHMARKS.md
docs/RELEASE_NOTES_v1.2.0.md
```

If GitHub misses hidden workflow files, manually create them from the visible backup files:

```text
VISIBLE_GITHUB_ACTIONS_verify.yml
VISIBLE_GITHUB_ACTIONS_receipt_engine.yml
```

## Release

After Actions passes, publish release:

```text
Tag: v1.2.0
Title: AXZ ReceiptCI v1.2.0 — benchmark and stress-test suite
```


## v1.2.1 patch note

After uploading this patch, ensure `.github/workflows/verify.yml` and `.github/workflows/receipt_engine.yml` are updated from their visible backup copies if GitHub does not upload hidden workflow files.
