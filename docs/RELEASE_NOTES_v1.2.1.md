# AXZ ReceiptCI v1.2.1 — PyPI Packaging Prep

AXZ ReceiptCI v1.2.1 prepares the project for safe Python package distribution without claiming a production PyPI release.

Added:

- Corrected package metadata version `1.2.1`.
- Verified console script entry point: `axz-receiptci = axz_receiptci.cli:main`.
- Backward-compatible `setup.py` shim.
- Package wiring verifier script.
- Package wiring tests.
- Distribution preflight SHA-256 audit script.
- `docs/PUBLISHING.md` with TestPyPI-first staging checklist.

Truth label:
`PYPI_PACKAGING_PREP / TESTPYPI_STAGING_REQUIRED`

Boundary:
AXZ ReceiptCI is publicly released on GitHub. It should not be described as live on production PyPI until the production package page exists and a clean install from PyPI succeeds.
