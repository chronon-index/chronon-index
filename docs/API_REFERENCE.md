# API reference

The API is static JSON — committed files, no server, no keys (RP Part VII;
`tly/api.py`). Any dumb host or mirror can serve it; `index.json` lets you
verify a mirror byte-for-byte.

## Layout

```
api/v1/
  latest.json          the newest epoch's print
  prints/<date>.json   one file per epoch (date = the Monday, UTC)
  countries.json       per-country S / E-bar / N breakdown
  index.json           every artifact above with its sha256
```

## The print object (`latest.json`, `prints/*.json`)

Fields (all numbers are Decimal-as-string; schema: `tly/prints.py`):

- `schema_version` — currently `print-v1`.
- `epoch_utc` — Monday 12:00:00 UTC exactly, explicit UTC offset.
- `series_label` — `SETTLEMENT` (measured-period S; the series
  derivatives settle on) or `INFORMATIONAL` (cohort best-estimate;
  never a settlement input).
- `s_life_years`, `e_bar_years`, `n_persons`, `burn_life_years`.
- `coverage` — invariant P7: `measured_share` plus per-country shares;
  a print without this block does not validate.
- `accuracy` — RP Part VI rule 6: a statement plus typed uncertainty —
  an `interval` whose bounds bracket the published S, or a `convention`
  label with a reason. Produced by `tly.error_budget`, never hand-typed.
- `provenance` — methodology version, policy strings, and the sha256 of
  every input snapshot file (resolvable against the committed manifests;
  invariant P9).

## Integrity

1. Fetch `index.json`; hash every artifact you mirror; compare.
2. Nothing may exist in the tree that `index.json` does not describe.
3. Each print's provenance hashes resolve into `data/snapshots/*/
   manifest.json` in the repo — see the reproduction instructions
   (`docs/REPRODUCE_FIXING.md`) to recompute the values themselves.

## Stability

`print-v1` fields are append-only; removing or renaming a field is a
schema version bump. Consumers should reject unknown `schema_version`
values (the reference validator does).
