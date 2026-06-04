# Upload First

Create GitHub repository:

```text
AXZ-ReceiptCI
```

Description:

```text
Deterministic CI receipt engine that verifies tests, hashes artifacts, and emits reproducible JSON release certificates.
```

Create with:

```text
Add README: Off
Add .gitignore: Off
License: None / Off
```

Upload all files from this folder.

Make sure these hidden files are present after upload:

```text
.github/workflows/verify.yml
.gitignore
```

If GitHub misses hidden files, use:

```text
VISIBLE_GITHUB_ACTIONS_verify.yml
VISIBLE_GITIGNORE.txt
```

## v1.1.0 patch upload notes

For the v1.1.0 provenance pack, ensure these files are present after upload:

```text
.github/workflows/receipt_engine.yml
ROADMAP.md
CONTRIBUTING.md
SECURITY.md
docs/PROVENANCE_WORKFLOW_PACK.md
docs/RECEIPT_SCHEMA.md
docs/RELEASE_NOTES_v1.1.0.md
examples/use_receipt_engine.yml
examples/sample_axz_receipt.json
```

If GitHub's browser uploader does not preserve hidden workflow files, create `.github/workflows/receipt_engine.yml` manually using `VISIBLE_GITHUB_ACTIONS_receipt_engine.yml`.
