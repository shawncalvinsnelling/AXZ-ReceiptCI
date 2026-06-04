from pathlib import Path
import sys

from axz_receiptci.core import TRUTH_LABEL, create_receipt


def test_certificate_has_required_fields(tmp_path: Path):
    (tmp_path / "x.py").write_text("print('x')\n", encoding="utf-8")
    cert = create_receipt(tmp_path, tmp_path / "certificates", "demo", [sys.executable, "-c", "print('ok')"])
    for field in ["schema_version", "project_name", "truth_label", "status", "source_tree_hash", "certificate_hash", "files"]:
        assert field in cert
    assert cert["truth_label"] == TRUTH_LABEL
    assert cert["files"][0]["path"] == "x.py"
