# AXZ ReceiptCI Verification Argument

AXZ ReceiptCI is not a mathematical theorem prover. It is a deterministic receipt generator for finite software verification runs.

## Claim

For a fixed project directory, fixed ignore policy, fixed verifier command, and fixed artifact set, AXZ ReceiptCI deterministically computes:

1. a canonical source file manifest,
2. a SHA-256 digest for each included file,
3. a canonical source-tree hash,
4. verifier command status,
5. optional artifact hashes,
6. a JSON certificate hash.

## Source-tree hash

For each included file, the engine records:

```text
relative_path
byte_count
sha256
```

The source-tree hash is computed from the sorted canonical lines:

```text
relative_path\0sha256\0byte_count\n
```

This proves that if a file path, byte count, or digest changes, the tree hash changes.

## Certificate hash

The certificate hash is computed over the JSON object with the `certificate_hash` field removed. This prevents a self-reference loop while still binding the certificate content.

## Check mode

`axz-receiptci check certificate.json` recomputes the hash of each recorded file and the full source-tree hash. If any file is missing or changed, the check fails.

## Limits

A passing receipt proves that the stated verifier command returned success under the captured environment metadata. It does not prove that the verifier command was complete, that the software has no bugs, or that future environments will behave identically.

Truth label:

```text
CERTIFIED_BUILD_RECEIPT_ENGINE_V0
```
