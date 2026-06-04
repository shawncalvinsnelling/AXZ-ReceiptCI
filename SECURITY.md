# Security Policy

AXZ ReceiptCI is a deterministic receipt layer. It records and verifies file hashes, artifact hashes, and verifier command outcomes. It is not a complete security boundary by itself.

## Supported versions

| Version | Supported |
|---|---|
| 1.1.x | Yes |
| 1.0.x | Maintenance only |

## Reporting a vulnerability

Please open a private security advisory on GitHub if available, or open an issue without exploit details and request a secure contact path.

## Security scope

In scope:

- Hash drift not detected when it should be.
- Certificate tampering not detected.
- Unsafe default ignore behavior.
- Receipt mismatch accepted as valid.

Out of scope:

- Claims that ReceiptCI prevents all supply-chain attacks.
- Compromised GitHub runner infrastructure.
- Malicious verifier commands supplied by the user.
- Semantic bugs in the project being tested.

## Safe security posture

AXZ ReceiptCI can support provenance and audit workflows, but should be combined with established signing, attestation, access-control, and CI hardening systems for production security.
