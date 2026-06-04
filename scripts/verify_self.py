#!/usr/bin/env python3
from pathlib import Path
from axz_receiptci.core import PASS_STATUS, check_receipt, create_receipt


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    cert = create_receipt(
        root=root,
        out_dir=root / "certificates",
        project_name="AXZ-ReceiptCI",
        test_command="python -m pytest -q",
    )
    if cert["status"] != PASS_STATUS:
        print("FAIL: tests did not pass")
        return 1
    result = check_receipt(root / "certificates" / "certificate.json", root=root)
    if result["status"] != PASS_STATUS:
        print("FAIL:", result)
        return 1
    print("PASS: AXZ_RECEIPTCI_SELF_VERIFICATION")
    print("source_tree_hash:", cert["source_tree_hash"])
    print("certificate_hash:", cert["certificate_hash"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
