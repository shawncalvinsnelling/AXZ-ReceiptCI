# AXZ ReceiptCI Publishing Guide

Truth label: `PYPI_PACKAGING_PREP / TESTPYPI_STAGING_REQUIRED`

AXZ ReceiptCI is publicly released on GitHub through v1.2.0. Version v1.2.1 prepares the project for Python package distribution by verifying package metadata, package layout, and CLI entry-point wiring.

Boundary: AXZ ReceiptCI is **not yet confirmed live on production PyPI** unless the production project page exists and a clean install from PyPI succeeds. Do not claim `pip install axz-receiptci` is live until that verification is complete.

## What v1.2.1 verifies

- `pyproject.toml` uses package name `axz-receiptci`.
- The console script points to `axz_receiptci.cli:main`.
- The source package layout is `src/axz_receiptci/`.
- `setup.py` exists only as a backward-compatible setuptools shim.
- The publishing path uses TestPyPI before production PyPI.

## Local package wiring check

```bash
python scripts/verify_package_wiring.py
python -m pytest -q
```

Expected result:

```text
PASS: AXZ_RECEIPTCI_PACKAGE_WIRING_VERIFIED
```

## Build the distribution locally

Install the build tools in a local virtual environment:

```bash
python -m pip install --upgrade build twine
python -m build
```

This should create files in `dist/`, usually a source distribution and a wheel.

## Check distribution metadata

```bash
python -m twine check dist/*
```

Expected result: every file reports `PASSED`.

## Optional distribution hash audit

```bash
python scripts/preflight_distribution_audit.py
```

This prints SHA-256 hashes for the built archives so the local distribution can be recorded before upload.

## TestPyPI staging upload

Create a TestPyPI account and a TestPyPI API token. Then set temporary environment variables in your local terminal:

```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-your-testpypi-token-here"
```

Upload to TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

TestPyPI is a separate test instance of PyPI intended for trying distribution uploads before publishing to the real index.

## Verify sandbox install

Use a fresh virtual environment. Because TestPyPI may not mirror all dependencies, install with the TestPyPI index and allow PyPI fallback only if needed. AXZ ReceiptCI has no runtime dependencies.

```bash
python -m venv /tmp/axz-receiptci-test
source /tmp/axz-receiptci-test/bin/activate
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps axz-receiptci==1.2.1
axz-receiptci --version
```

Expected command output includes:

```text
axz-receiptci 1.2.1
```

## Production PyPI boundary

Only after TestPyPI succeeds should production PyPI be considered. For production upload, use a production PyPI API token and run:

```bash
python -m twine upload dist/*
```

After production upload, verify the project page exists and a clean install succeeds:

```bash
python -m venv /tmp/axz-receiptci-prod
source /tmp/axz-receiptci-prod/bin/activate
python -m pip install axz-receiptci==1.2.1
axz-receiptci --version
```

Only then is it safe to say:

```text
AXZ ReceiptCI is live on production PyPI.
```

## Forbidden claims

Do not claim:

- Production PyPI release before the package page and install are verified.
- Universal supply-chain security.
- Replacement of SLSA, Sigstore, GitHub Artifact Attestations, Bazel, Nix, or enterprise CI systems.
- Semantic correctness beyond the verifier command actually executed.
