# Math and Computer Science Positioning

AXZ ReceiptCI is deliberately positioned as a bridge between computational proof practice and commercial software infrastructure.

## Mathematical skill signal

The project uses finite deterministic verification:

```text
finite input set
canonical ordering
SHA-256 state hash
explicit receipt object
pass/fail truth label
re-checkable certificate
```

This mirrors the structure of the AXZ finite exact proof repositories: define the universe, compute the object, hash the state, and publish the verifier.

## Computer science skill signal

The project demonstrates:

- CLI design,
- package structure,
- deterministic file scanning,
- cryptographic hashing,
- JSON certificate design,
- GitHub Actions integration,
- test-driven validation,
- failure labels for drift and command failure.

## State-of-the-art but truth-safe framing

Strong public wording:

```text
AXZ ReceiptCI is a deterministic CI receipt engine for cryptographic proof-of-run certificates.
```

Avoid overclaiming:

```text
Do not claim it replaces all CI/CD systems.
Do not claim it proves all code correct.
Do not claim it solves supply-chain security by itself.
```
