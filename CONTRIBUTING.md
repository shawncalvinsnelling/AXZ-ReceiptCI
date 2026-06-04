# Contributing to AXZ ReceiptCI

Thank you for helping improve AXZ ReceiptCI.

## Engineering rules

AXZ ReceiptCI is a deterministic receipt engine. Contributions should preserve these rules:

1. Deterministic output whenever possible.
2. Sorted manifests before hashing.
3. No file modification times in canonical source-tree hashes.
4. No hidden network calls in the core verifier.
5. No overclaiming in docs, tests, or release notes.
6. Every new receipt field should be documented in `docs/RECEIPT_SCHEMA.md`.
7. Every feature should have tests.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scriptsctivate
pip install -e .
pip install -r requirements-dev.txt
python -m pytest -q
python scripts/verify_self.py
```

## Pull request checklist

- [ ] Tests pass locally.
- [ ] `python scripts/verify_self.py` passes.
- [ ] Documentation updated if behavior changed.
- [ ] No unsupported security or supply-chain claims added.
- [ ] New files are included in the receipt scan unless intentionally ignored.

## Claim-safety policy

Safe wording:

> AXZ ReceiptCI emits deterministic CI receipts that record what ran, what passed, what files were hashed, and what artifacts were produced.

Forbidden wording:

- Guarantees total supply-chain security.
- Replaces SLSA, Sigstore, Bazel, Nix, or enterprise CI.
- Proves arbitrary program correctness.
- Makes failed tests safe.
- Makes AI-generated code automatically trustworthy.
