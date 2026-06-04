from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import PASS_STATUS, check_receipt, create_receipt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="axz-receiptci", description="Deterministic CI receipt engine.")
    parser.add_argument("--version", action="version", version=f"axz-receiptci {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify", help="Generate a CI receipt.")
    verify.add_argument("--root", default=".", help="Project root. Default: current directory.")
    verify.add_argument("--out", default="certificates", help="Output directory. Default: certificates.")
    verify.add_argument("--project-name", default="AXZ-ReceiptCI", help="Project name for the certificate.")
    verify.add_argument("--test-cmd", default="python -m pytest -q", help="Verifier/test command to run.")
    verify.add_argument("--no-run", action="store_true", help="Do not run a test command; generate a scan-only receipt.")
    verify.add_argument("--artifact", action="append", default=[], help="Artifact file to hash; may be repeated.")

    check = sub.add_parser("check", help="Check a previously generated receipt.")
    check.add_argument("certificate", help="Path to certificate.json")
    check.add_argument("--root", default=None, help="Project root. Default: parent of certificate directory.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "verify":
        root = Path(args.root)
        out = Path(args.out)
        command = None if args.no_run else args.test_cmd
        cert = create_receipt(root=root, out_dir=out, project_name=args.project_name, test_command=command, artifacts=args.artifact)
        print(json.dumps({
            "status": cert["status"],
            "certificate": str((out / "certificate.json").resolve()),
            "source_tree_hash": cert["source_tree_hash"],
            "certificate_hash": cert["certificate_hash"],
        }, indent=2, sort_keys=True))
        return 0 if cert["status"] == PASS_STATUS else 1
    if args.command == "check":
        root = Path(args.root) if args.root else None
        result = check_receipt(Path(args.certificate), root=root)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == PASS_STATUS else 1
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
