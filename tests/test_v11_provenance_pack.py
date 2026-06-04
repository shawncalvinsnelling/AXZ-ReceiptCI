from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reusable_workflow_exists_and_is_call_target():
    workflow = ROOT / ".github" / "workflows" / "receipt_engine.yml"
    text = workflow.read_text(encoding="utf-8")
    assert "workflow_call:" in text
    assert "axz-receiptci verify" in text
    assert "axz-receiptci check" in text
    assert "source_tree_hash" in text


def test_v11_docs_exist():
    required = [
        "ROADMAP.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "docs/PROVENANCE_WORKFLOW_PACK.md",
        "docs/RECEIPT_SCHEMA.md",
        "docs/RELEASE_NOTES_v1.1.0.md",
        "examples/use_receipt_engine.yml",
        "examples/sample_axz_receipt.json",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_readme_contains_three_minute_integration():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Implement AXZ-ReceiptCI in 3 minutes" in readme
    assert "receipt_engine.yml@v1.1.0" in readme
