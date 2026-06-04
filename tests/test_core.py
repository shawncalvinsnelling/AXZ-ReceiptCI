from pathlib import Path
import sys

from axz_receiptci.core import PASS_STATUS, check_receipt, create_receipt, scan_files, source_tree_hash


def test_scan_and_hash_are_stable(tmp_path: Path):
    (tmp_path / "a.txt").write_text("alpha", encoding="utf-8")
    (tmp_path / "b.txt").write_text("beta", encoding="utf-8")
    records1 = scan_files(tmp_path)
    records2 = scan_files(tmp_path)
    assert [r.path for r in records1] == ["a.txt", "b.txt"]
    assert source_tree_hash(records1) == source_tree_hash(records2)


def test_create_and_check_receipt(tmp_path: Path):
    (tmp_path / "pkg.py").write_text("x = 1\n", encoding="utf-8")
    cert = create_receipt(
        root=tmp_path,
        out_dir=tmp_path / "certificates",
        project_name="demo",
        test_command=[sys.executable, "-c", "print('ok')"],
    )
    assert cert["status"] == PASS_STATUS
    result = check_receipt(tmp_path / "certificates" / "certificate.json", root=tmp_path)
    assert result["status"] == PASS_STATUS


def test_hash_drift_detected(tmp_path: Path):
    f = tmp_path / "pkg.py"
    f.write_text("x = 1\n", encoding="utf-8")
    create_receipt(
        root=tmp_path,
        out_dir=tmp_path / "certificates",
        project_name="demo",
        test_command=[sys.executable, "-c", "print('ok')"],
    )
    f.write_text("x = 2\n", encoding="utf-8")
    result = check_receipt(tmp_path / "certificates" / "certificate.json", root=tmp_path)
    assert result["status"] == "HASH_DRIFT_DETECTED"
