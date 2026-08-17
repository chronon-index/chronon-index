# Reproducing a TLY fixing from public artifacts alone

Audience: an outsider with no access to the authors. If any step below
requires asking someone, that is a defect — file it as an issue (or a
dispute, step 7). This document is the SPEC#7 AC-7.5 gate: the project is
not settlement-grade until a stranger succeeds with nothing but this page.

**Current-state caveats (honest):** the repository is not yet published to
a public remote (backlog A-17) and no official Monday prints have been
produced yet (the weekly CI job still runs the reproducibility gate only).
Until then, this procedure verifies the committed reference computation —
the same path official prints will use.

## 0. What you are verifying

A **fixing** is one epoch's settlement value plus complete provenance
(methodology version, snapshot sha256 hashes, source URLs), hashed over a
canonical rendering. Two independent parties agree when their 64-hex
**fixing hashes** are string-equal. Nothing else needs to be exchanged.

## 1. Prerequisites

- Python ≥ 3.12 (stdlib only for the compute path; `pytest` and `ruff`
  for the gates: `pip install -e '.[dev]'`).
- `git` and ~1 GB disk if you refetch the large snapshots.
- No accounts, no keys. Every data source is keyless (the HMD/STMF feed,
  which is not, is pending a governance decision and is NOT part of the
  fixing path).

## 2. Get the exact tree

```sh
git clone <repo-url> tly && cd tly
git log --oneline -1        # record the commit you verified
```

## 3. Verify the repository's own integrity gates

```sh
python -m pytest tests/test_manifest_schema.py tests/test_snapshot_immutability.py -q
```

Both must pass: every snapshot file matches its manifest sha256, and
history contains no rewrites. If this fails, STOP — the tree you have is
not the tree that was published.

## 4. Reproduce the computation byte-for-byte

```sh
python -m tly.pipeline 2026-08-17T12:00:00+00:00 > my_print.json
python -m tly.pipeline 2026-08-17T12:00:00+00:00 > my_print_2.json
diff my_print.json my_print_2.json        # must be empty (determinism)
```

The full P5 gate (two cold processes, different hash seeds):

```sh
python -m pytest tests/test_p5_reproducibility.py -q
```

## 5. Verify the inputs against their upstreams (optional but complete)

Every input file's `source_url`, `sha256`, and retrieval timestamp is in
`data/snapshots/<date>/manifest.json`. Refetch any URL yourself and hash
it. NOTE: upstreams revise; a hash mismatch against a **fresh** fetch
proves revision, not tampering — tampering is a mismatch between the
committed file and the committed manifest (step 3 catches that).
Files marked `"in_git": false` are large; their manifest rows are the
committed record, and your own fetch lets you verify content
independently.

## 6. Build the fixing and compare hashes

```python
from pathlib import Path
from tly.archive import PrintArchive
from tly.fixings import settle_from_archive
from tly.pipeline import build_settlement_print

archive = PrintArchive(Path("./my_archive"))
archive.append(build_settlement_print("2026-08-17T12:00:00+00:00"))
fixing = settle_from_archive(
    archive, "2026-08-17T12:00:00+00:00", Path("data/snapshots")
)
print(fixing.fixing_hash)
```

Compare your 64-hex hash with the published one (once official fixings
publish, they live in the static API tree under `api/v1/` and in the
archive's `chain.json`). String-equal = agreement.

## 7. If your hash differs

1. Re-run step 3 (is your tree intact?) and step 4 (is your run
   deterministic on your machine?).
2. Diff your `my_print.json` against the published per-epoch artifact —
   the first differing field localizes the disagreement.
3. File a dispute within 48 hours of the epoch (log-only; it alters
   nothing and delays nothing, but it is permanently on the record):
   claimant, claim, the epoch, the disputed fixing hash, and your
   computed hash. Substantiated disputes are resolved through the
   correction ledger (`ledger/CORRECTIONS.md`) in the NEXT epoch —
   published history is never rewritten.

## 8. What you may NOT conclude

- Agreement does not prove the upstream data was *true* — it proves the
  published number follows from the recorded inputs by the published
  method (see the accuracy block inside every print for what is claimed).
- A fresh-fetch mismatch (step 5) does not prove misconduct — sources
  revise; the vintage archive exists precisely because of this.
