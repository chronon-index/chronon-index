# COVID replay on true real-time vintages (C-uc6-07)

**Question** (SPEC#6 AC-6.2): if the pipeline had run through 2020-21
with first-print-settles (P4), how wrong would its real-time excess
estimates have been versus the final figures?

**No-hindsight is real, not simulated.** Each vintage is
`world_mortality.csv` exactly as a git commit published it — snapshotted
2026-08-25 with commit shas and dual (stored/wire) hashes:

| vintage | commit |
|---|---|
| 2021-01-14 | `7c245b0829` |
| 2021-06-29 | `33694fef9b` |
| 2021-12-31 | `c2fe1261b6` |
| 2022-06-29 | `a2418a18cb` |

Final figures: the committed 2026-08-17 WMD snapshot. Panel: Albania +
Germany (the settlement print's coverage panel). Machinery: the
pipeline's own `fit_baseline` (kk-linear) + `excess_series`, fit only on
the years each vintage actually contains (≥4-year floor). Reproduce:
`tly.covid_replay.run_replay()` — every number below regenerates from
committed artifacts (suite-guarded).

## Results — 2020 excess deaths, per vintage

| vintage | ALB excess | ALB err vs final | DEU excess | DEU err vs final |
|---|---|---|---|---|
| 2021-01-14 | +1,282.4 (39 wks) | **−77.9%** | **−1,598.0** (50 wks, 4y fit) | **−106.5%** |
| 2021-06-29 | +5,813.0 | 0.0% | +16,520.0 (4y fit) | −32.6% |
| 2021-12-31 | +5,813.0 | 0.0% | +24,501.8 | 0.0% |
| 2022-06-29 | +5,813.0 | 0.0% | +24,501.8 | 0.0% |
| **final** | **+5,813.0** (12 mo) | — | **+24,501.8** (52 wks) | — |

## Findings

1. **A January-2021 analyst measured NEGATIVE German excess.** The
   vintage's 50 reported weeks plus a 2016-2019 baseline (no 2015 in
   the file yet) net to −1,598 — an error of −106.5%. Real-time is not
   merely noisy; early in a shock it can carry the wrong sign.
2. **The dominant error source was baseline history, not death-count
   backfill.** Decomposing Germany's June-2021 error (−7,982): fitting
   the FINAL data on 2016-2019 gives 16,142, so the missing 2015 fit
   year explains −8,360 of it; data revisions explain only +378. The
   scarce input was history for the baseline, not fresh counts.
3. **Convergence was fast once reporting matured**: Albania exact from
   June 2021 (after its weekly→monthly series switch); Germany exact
   from December 2021, within the year.
4. **Reporting units shift under replay** (Albania weekly in Jan 2021,
   monthly after) — excess sums are comparable across vintages, period
   counts are not.

## What this means for CHRONON

P4 (first-print-settles, corrections forward-only) trades exactly this
real-time error for immutability. The replay quantifies the trade on
the pipeline's own panel: worst case −106.5% at the shock's edge,
sub-year convergence, and an error budget dominated by baseline-history
availability — which the error budget's terms and the failure ladder's
carry states are built to absorb.

## Limitations

- Two countries, one shock year: a machinery replay, not a world
  estimate.
- Our own vintage store begins 2026-08-25; future shocks replay
  natively from `data/vintages/` (Eurostat + CDC + ONS pulls, weekly).
  For 2020, WMD's git history is the only true as-of source we hold.
- The 2021-01-14 vintage predates WMD's iso3c column and carries an
  extra `date` column — normalization is recorded in the snapshot
  manifest's derivation entry.
