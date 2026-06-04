# AXZ ReceiptCI v1.1 Provenance Workflow Pack

The v1.1 provenance pack makes AXZ ReceiptCI easier to reuse from another GitHub repository.

## Reusable workflow

The reusable workflow lives at:

```text
.github/workflows/receipt_engine.yml
```

A target repository can call it like this:

```yaml
name: Security Pipeline Audit

on:
  push:
  pull_request:

jobs:
  run_receipt_engine:
    uses: shawncalvinsnelling/AXZ-ReceiptCI/.github/workflows/receipt_engine.yml@v1.2.0
    with:
      project_name: ${{ github.event.repository.name }}
      root_dir: "."
      test_cmd: "python -m pytest -q"
      out_dir: "certificates"
      enable_drift_check: true
```

## Outputs

The workflow publishes an `axz-receiptci-provenance` artifact containing:

```text
certificate.json
receipt.txt
SHA256SUMS.txt
axz_modified_files.txt   # pull requests only, when present
```

## Workflow outputs

The reusable workflow exposes:

- `source_tree_hash`
- `certificate_hash`
- `status`

## Truth boundary

This workflow provides deterministic receipts and drift evidence. It does not prove semantic correctness beyond the configured verifier command.
