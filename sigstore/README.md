# Sigstore signatures (E-12)

One `<epoch>.json.sigstore.json` bundle per archived print, produced
KEYLESSLY in the print workflow via GitHub OIDC (no long-lived signing
key exists to steal). Each bundle proves: this exact record was
produced by this repo's `weekly-print` workflow at that time, logged in
the public Rekor transparency log. Verify any record:

```bash
cosign verify-blob archive/<epoch>.json \
  --bundle sigstore/<epoch>.json.sigstore.json \
  --certificate-identity-regexp "https://github.com/chronon-index/chronon-index/" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

Together with the hash chain (tamper linkage), OTS (Bitcoin time
anchoring), and the outsider-sim (recomputability), this closes the
provenance triangle: WHAT was printed, WHEN, and BY WHICH code path.
Bundles begin with the first print after 2026-09-04; earlier epochs
carry OTS + chain only (stated, not backfilled — keyless signatures
cannot be honestly backdated).
