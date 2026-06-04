from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def test_cli_entrypoint_module_exists_and_is_callable():
    sys.path.insert(0, str(SRC))
    cli = importlib.import_module("axz_receiptci.cli")
    assert callable(cli.main)


def test_pyproject_entrypoint_matches_package_layout():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "axz-receiptci"' in pyproject
    assert 'version = "1.2.1"' in pyproject
    assert 'axz-receiptci = "axz_receiptci.cli:main"' in pyproject
    assert 'where = ["src"]' in pyproject


def test_setup_py_fallback_matches_src_layout():
    setup_py = (ROOT / "setup.py").read_text(encoding="utf-8")
    assert 'packages=find_packages(where="src")' in setup_py
    assert 'package_dir={"": "src"}' in setup_py
    assert '"axz-receiptci=axz_receiptci.cli:main"' in setup_py


def test_publishing_docs_state_testpypi_boundary():
    publishing = (ROOT / "docs" / "PUBLISHING.md").read_text(encoding="utf-8")
    assert "TestPyPI" in publishing
    assert "production PyPI" in publishing
    assert "not yet confirmed live on production PyPI" in publishing
