from pathlib import Path

from axz_receiptci.cli import main


def test_cli_verify_no_run(tmp_path: Path):
    (tmp_path / "main.py").write_text("print('hi')\n", encoding="utf-8")
    code = main(["verify", "--root", str(tmp_path), "--out", str(tmp_path / "certificates"), "--project-name", "demo", "--no-run"])
    assert code == 0
    assert (tmp_path / "certificates" / "certificate.json").exists()


def test_cli_check(tmp_path: Path):
    (tmp_path / "main.py").write_text("print('hi')\n", encoding="utf-8")
    assert main(["verify", "--root", str(tmp_path), "--out", str(tmp_path / "certificates"), "--project-name", "demo", "--no-run"]) == 0
    assert main(["check", str(tmp_path / "certificates" / "certificate.json"), "--root", str(tmp_path)]) == 0
