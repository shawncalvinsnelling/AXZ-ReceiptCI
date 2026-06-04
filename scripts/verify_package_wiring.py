#!/usr/bin/env python3
"""Verify AXZ ReceiptCI packaging metadata and CLI entry-point wiring."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
EXPECTED_VERSION = "1.2.1"
EXPECTED_ENTRY = "axz_receiptci.cli:main"


def read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    sys.path.insert(0, str(SRC))

    package = importlib.import_module("axz_receiptci")
    cli = importlib.import_module("axz_receiptci.cli")

    assert getattr(package, "__version__") == EXPECTED_VERSION, package.__version__
    assert callable(getattr(cli, "main", None)), "axz_receiptci.cli.main is not callable"

    pyproject = read_text(ROOT / "pyproject.toml")
    assert 'name = "axz-receiptci"' in pyproject
    assert f'version = "{EXPECTED_VERSION}"' in pyproject
    assert f'axz-receiptci = "{EXPECTED_ENTRY}"' in pyproject
    assert 'where = ["src"]' in pyproject

    setup_py = read_text(ROOT / "setup.py")
    assert f'version="{EXPECTED_VERSION}"' in setup_py
    assert f'"axz-receiptci={EXPECTED_ENTRY}"' in setup_py
    assert 'packages=find_packages(where="src")' in setup_py

    publishing = read_text(ROOT / "docs" / "PUBLISHING.md")
    assert "TestPyPI" in publishing
    assert "twine check" in publishing
    assert "not yet confirmed live on production PyPI" in publishing

    print("PASS: AXZ_RECEIPTCI_PACKAGE_WIRING_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
