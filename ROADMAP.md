# AXZ-ReceiptCI System Evolution Roadmap

This roadmap keeps AXZ ReceiptCI commercially useful while preserving strict truth labels and non-overclaiming boundaries.

## Phase 1 — Foundation

**Status:** Complete in `v1.0.0`.

Features:

- Python CLI receipt generator.
- Source-tree SHA-256 hashing.
- Optional artifact hashing.
- JSON certificate generation.
- Receipt checking and drift detection.
- GitHub Actions self-verification.

## Phase 2 — Provenance Integration

**Status:** Active in `v1.1.0`.

Features:

- Reusable GitHub Actions workflow engine.
- Canonical folder manifest sorting.
- Provenance-style metadata fields.
- Pull request drift report artifacts.
- Copyable three-minute integration template.

## Phase 3 — Ecosystem Interoperability

**Status:** Planned.

Features:

- Sigstore-compatible signing bridge.
- GitHub Artifact Attestation export helpers.
- SLSA-style provenance field mapping.
- Multi-stage artifact validation.

## Phase 4 — AI-Assisted Non-Breaking Deflection

**Status:** Research and development.

Features:

- Drift explanation mode.
- Suggested repair pull requests.
- Human-review-only remediation workflow.
- No autonomous production edits by default.

## Phase 5 — Cloud Workspace Control Plane

**Status:** Future vision.

Features:

- Multi-repository receipt dashboard.
- Team audit logs.
- Artifact history.
- Compliance exports.
- Zero-trust verification vaults.

## Forbidden roadmap claims

AXZ ReceiptCI does not claim to solve all software supply-chain security, replace existing security frameworks, prove semantic correctness of arbitrary programs, or make AI-generated code automatically trustworthy.


## Phase 2B — Benchmark and Stress-Test Suite

**Status:** Complete in v1.2.0.

AXZ ReceiptCI v1.2.0 adds deterministic large-repository benchmark coverage, including a 10,000-file simulated source tree, a one-file drift mutation, and structured benchmark JSON output.
