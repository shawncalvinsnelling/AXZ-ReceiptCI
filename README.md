# AXZ ReceiptCI

**Truth label:** `CERTIFIED_BUILD_RECEIPT_ENGINE_V0`

AXZ ReceiptCI is a deterministic CI receipt engine. It runs a declared verification command, hashes the project tree, hashes selected artifacts, and emits a reproducible JSON certificate that records what ran, what passed, what files were included, and what changed.

This project is the commercial-infrastructure continuation of the AXZ finite-proof repository series: instead of certifying one arithmetic universe, it certifies a software verification run.

## Why this exists

Modern software teams need proof receipts:

- What source files were verified?
- What command was run?
- Did it pass or fail?
- What artifacts were produced?
- Did the source tree drift after certification?
- Can another person or CI runner re-check the receipt?

AXZ ReceiptCI gives a small, inspectable, open-source answer.

## What it does

```text
scan project files
run verifier/test command
hash source tree
hash optional artifacts
write certificate.json
write receipt.txt
write SHA256SUMS.txt
verify certificate later
```

## What it does not claim

AXZ ReceiptCI is **not** a full CI/CD replacement, not a universal compiler, and not a general proof of supply-chain security. It is a deterministic receipt layer that can be embedded into GitHub Actions or other build systems.

Forbidden claims:

```text
No claim of solving all software supply-chain security.
No claim of replacing SLSA, Sigstore, Bazel, Nix, or enterprise CI systems.
No claim that failed tests can be made safe by a receipt.
No claim that AI-generated code is automatically trustworthy.
```

## Install locally

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
pip install -r requirements-dev.txt
```

## Quick start

Generate a receipt for this repository:

```bash
axz-receiptci verify \
  --project-name AXZ-ReceiptCI \
  --test-cmd "python -m pytest -q" \
  --out certificates
```

Check the receipt later:

```bash
axz-receiptci check certificates/certificate.json
```

Expected status after a clean run:

```text
CERTIFIED_REPRODUCIBLE_PASS
```

## CLI commands

### `verify`

```bash
axz-receiptci verify --project-name MyProject --test-cmd "python -m pytest -q"
```

Outputs:

```text
certificates/certificate.json
certificates/receipt.txt
certificates/SHA256SUMS.txt
```

### `check`

```bash
axz-receiptci check certificates/certificate.json
```

Recomputes source hashes and returns one of:

```text
CERTIFIED_REPRODUCIBLE_PASS
HASH_DRIFT_DETECTED
MISSING_FILE
CERTIFICATE_MISMATCH
```

## Receipt status labels

```text
CERTIFIED_REPRODUCIBLE_PASS
FAILED_TESTS
HASH_DRIFT_DETECTED
UNTRACKED_ARTIFACTS
ENVIRONMENT_MISMATCH
MISSING_FILE
CERTIFICATE_MISMATCH
```

## Certificate fields

Each JSON certificate includes:

```text
schema_version
project_name
truth_label
status
generated_at_utc
platform
python_version
test_command
test_exit_code
test_duration_seconds
file_count
total_bytes
source_tree_hash
artifact_hashes
certificate_hash
receipt_text_hash
files[]
```

## Deterministic hash policy

The source tree hash is computed from sorted file records:

```text
relative_path\0sha256\0byte_count\n
```

Generated receipt outputs, `.git`, virtual environments, caches, and build directories are excluded by default. File modification times are not included in the canonical hash.

## GitHub Actions

This repository includes:

```text
.github/workflows/verify.yml
```

The workflow runs the test suite, generates a receipt, and checks the receipt.

## State-of-the-art posture

AXZ ReceiptCI is designed around ideas used in modern high-assurance infrastructure:

- deterministic build receipts
- source-tree hashing
- artifact hashing
- machine-readable provenance
- CI-verifiable certificates
- explicit truth labels
- drift detection

The first release is intentionally small and auditable. The future commercial/open-source path is a hosted dashboard for team receipts, artifact history, compliance exports, and AI-code verification logs.

## Truth label

```text
CERTIFIED_BUILD_RECEIPT_ENGINE_V0
```

This label means the tool can certify the result of a finite software verification run under its stated scan, hash, and command-execution rules. It does not certify semantic correctness of the program beyond the verifier command that was executed.

## Release posture

A safe public description:

```text
AXZ ReceiptCI is an open-source deterministic CI receipt engine that verifies tests, hashes project files and artifacts, and emits reproducible JSON release certificates.
```

## Implement AXZ-ReceiptCI in 3 minutes

After `v1.2.0`, other repositories can call the reusable provenance workflow directly.
Create `.github/workflows/verify.yml` in the target repository:

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

The called workflow emits deterministic receipt outputs:

```text
certificates/certificate.json
certificates/receipt.txt
certificates/SHA256SUMS.txt
```

For non-Python projects, change `test_cmd` to the project verifier command, for example `npm test`, `go test ./...`, or `cargo test`.

## v1.1 provenance pack

AXZ ReceiptCI v1.1 adds a reusable workflow layer and documentation pack:

- `.github/workflows/receipt_engine.yml` reusable workflow
- `ROADMAP.md` five-phase system roadmap
- `CONTRIBUTING.md` engineering contribution rules
- `SECURITY.md` vulnerability and claim-safety policy
- `docs/PROVENANCE_WORKFLOW_PACK.md` integration guide
- `docs/RECEIPT_SCHEMA.md` receipt field reference
- `examples/use_receipt_engine.yml` copyable caller workflow
- `examples/sample_axz_receipt.json` sample receipt payload

State-of-the-art posture remains truth bounded: AXZ ReceiptCI produces deterministic build receipts and provenance-style records. It does not replace SLSA, Sigstore, GitHub Artifact Attestations, Bazel, Nix, or enterprise CI systems.

## v1.2 benchmark suite

AXZ ReceiptCI v1.2 adds a benchmark and stress-test suite for large deterministic source-tree scans.

Run a 10,000-file benchmark locally:

```bash
python tests/benchmark_suite.py --files 10000 --subdirs 10 --out certificates/benchmark_report.json
```

The benchmark creates a temporary simulated repository, hashes it through the real AXZ ReceiptCI canonical scan path, mutates one file, re-hashes the tree, and verifies that the source-tree hash changes.

Added in v1.2:

- `tests/benchmark_suite.py`
- `tests/test_benchmark_suite.py`
- `docs/BENCHMARKS.md`
- GitHub Actions benchmark execution
- 10,000-file simulated repository stress test
- one-file drift mutation check
- structured benchmark JSON output

Truth boundary: benchmark timings are hardware-sensitive. The certified behavior is deterministic hashing and positive drift detection under the stated benchmark rules, not a universal speed guarantee.


## v1.2.1 PyPI packaging prep

AXZ ReceiptCI v1.2.1 adds package-distribution preparation files. This does **not** claim that AXZ ReceiptCI is live on production PyPI yet. It verifies package metadata, source layout, and CLI entry-point wiring before any production upload.

Run the packaging wiring check:

```bash
python scripts/verify_package_wiring.py
python -m pytest -q
```

Publishing guidance lives in:

```text
docs/PUBLISHING.md
```

Truth boundary: production PyPI status should only be claimed after the real PyPI project page exists and a clean `pip install axz-receiptci==1.2.1` succeeds.
