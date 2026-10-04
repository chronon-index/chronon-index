# Proposal: publish the live-burn baseline-sensitivity table

**Status: DRAFTED, awaiting adoption signature. Changes nothing until
the PR carrying it is merged after sign-off** — this adds one
INFORMATIONAL page to the publication surface and touches neither the
settlement series nor the print computation.

## What

A new site page, `liveburn-sensitivity.html`, synthesized at build
time from the committed dual-run analysis
(`docs/reports/liveburn_dualrun.json`, three refutation passes). It
shows the cumulative 2026 excess-mortality reading under eleven
expected-deaths rules, the same method applied to prior years, and the
known biases (panel ageing, provisional cells, no age standardisation
on this feed). Every figure is module output; the page contains no
hand-written numbers.

## Why

The live-burn question (should weekly prints respond to measured
excess deaths?) is downstream of a baseline-policy choice that flips
the sign of the year: defensible rules span −11 to +23 ppm of S.
Publishing the table makes that decision public BEFORE any activation
proposal, in the same spirit as the open G5 proposal page: the
decision is made in the open, with the sensitivity in front of
everyone, not asserted afterwards.

## What this is NOT

- NOT live-burn activation. Settlement remains measured-period
  arithmetic on published statistics; the INFORMATIONAL wall
  (tly/prints.py series labels, tly/fixings.py guard) is untouched.
- NOT a new weekly computation. The page rides the existing
  `build_public` step of the print workflow and re-renders only when
  the committed JSON changes. Refreshing the analysis itself requires
  a new dated snapshot vintage plus a rerun of
  `python -m tly.liveburn_dualrun` — the normal governed data path.
- NOT a methodology change. S, Ē, and every settlement value compute
  exactly as before; the methodology version is unchanged. Adoption is
  a publication-surface change recorded in the changelog at merge.

## Mechanics (all in the PR)

- `tly/site.py`: `_liveburn_markdown()` + page registration; a policy
  key the module adds without a display label still renders under its
  raw key, so a row can never silently drop.
- `tests/test_site.py`: the page renders every policy row with both
  values straight from the JSON, carries the INFORMATIONAL banner and
  "not active" wording, and is covered by the liveness proof
  (B-uc4-09) and the byte-reproducibility test.
- Committed `site/` tree rebuilt (nav gains one entry on every page).

## Adoption

Merge after sign-off; the changelog entry lands in the same merge. If
declined, the branch closes and the table remains available in the
repo at `docs/reports/LIVEBURN_DUALRUN.md` for anyone who looks.
