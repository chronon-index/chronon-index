# Methodology changelog

Append-only. A methodology version bump is the ONLY sanctioned way to
change a numerical policy (SPEC#1 AC-1.4). The full procedure — proposal →
public comment window → version bump — is docs/METHODOLOGY_CHANGE_PROCESS.md.
Each entry lists the policies that version is defined by; the registry in
`tly/methodology.py` pins them and CI enforces the pairing.

## v0.5.0-reconstruction — 2026-08-25

Adds the excess-age-profile policy (B-uc2-12/13); prior policies unchanged.

- excess_age_profile: `0.7 at exact age 75.5 + 0.3 at 85.5 on the epoch
  structure-year table` — the age-at-death assumption converting measured
  excess deaths to life-years in the backfill burn series. Implied mean
  remaining expectancy ≈ 10.5-11.5y on the 2019-2023 World tables, inside
  the DECISIONS anchor's 10.0-22.7y implied range (14.83M excess ->
  148-337M life-years), at its conservative end (COVID excess skewed old).
  Changing the profile is a version bump; per-feed profiles (RP Part II
  D4) will supersede this single global profile with their own bump.

## v0.4.0-reconstruction — 2026-08-17

Adds the quanta policy (B-uc3-04); prior policies unchanged.

- quanta: `scheduling quantum 0.000001 life-years; attribution quantum
  0.001` — the E11 quantum for weekly flow scheduling (tly/weekly.py) and
  the default quantum for age attribution (tly/burn.py) were governed
  numerical parameters living only as code constants; changing either now
  requires a bump. Registry-completeness is tested: every governed code
  constant must appear in the current version's policy strings.

## v0.3.0-reconstruction — 2026-08-17

Adds the P6 identity-closure tolerance policy (B-uc2-08); prior policies
unchanged.

- p6_closure: `exact-0: E11-scheduled weekly flows sum to the annual
  identity exactly` — annual flows split across the year's actual Mondays
  (52 or 53) by equal quantum division with largest-remainder distribution;
  closure is exact, no tolerance. Introducing any nonzero tolerance (e.g.
  for mixed-source weekly burn) requires a bump.

## v0.2.0-reconstruction — 2026-08-17

Adds the nowcast baseline policy (B-uc2-04); v0.1.0 policies unchanged.

- baseline: `kk-linear: per-period linear trend fit on 2015-2019
  (Karlinsky-Kobak)` — expected deaths for (country, period) extrapolate a
  per-period straight line fit on the five pre-pandemic years, the World
  Mortality Dataset's own published method (chosen for comparability with
  the feed's literature; alternatives like 5-year means or Serfling
  seasonal models would require a bump). Fit windows and the excess
  definition (observed − expected) are part of this policy.

## v0.1.0-reconstruction — 2026-08-17

Initial packaged methodology, reconstructed 2026-08-16 from DECISIONS.md /
RESEARCH_PROGRAM.md / RALPH_LOOP.md after loss of the originals; pending
ratification (loop/BACKLOG.md A-16).

- interpolation: `linear-on-anchors, flat-tail` — piecewise-linear e() on
  exact-age anchors, flat beyond the last anchor (RP M5; monotone-Hermite
  upgrade would require a bump).
- band_midpoint: `uniform-within-band; open-band lo+2.5 (inert beyond last
  anchor)` — band [lo, hi] covers exact ages [lo, hi+1), midpoint
  (lo+hi+1)/2.
- decimal: `Decimal prec 34, ROUND_HALF_EVEN` — floats never touch
  published numbers (G1).

## v0.6.0-reconstruction (2026-08-25)

**Changed** (the registry's FIRST parameter change, not an addition):
the period-vs-cohort one-sided error-budget upper bound moves **+8% ->
+9%**. Driver: the E6 cohort computation on the committed 2010-2100 qx
surface measured the uplift at **+8.06%** (tests/test_cohort.py), 0.06pp
above the +3-8% literature-prose band — computed-beats-prose (ruling
D6). The one-sided bounds are now GOVERNED, version-keyed parameters
(`tly.methodology.VERSION_ONE_SIDED_TERMS`): reproducing an archived
print selects the band its version was computed under, never HEAD's —
the outsider-sim recomputes each epoch under its archived version.

Effect on published text: the cohort best-estimate band becomes
~381-406B (+5%/+12% applied to measured S). The A-16 packet's blessed
**381-402B remains the correct v0.5.0 statement** and archived prints
carrying it continue to reproduce byte-exactly.

## v0.7.0 (2026-09-04)

**The G5 source-of-record switch** — proposal
`docs/proposals/2026-09-03-G5-source-of-record.md`, signed off by Ben
2026-09-04 under the pre-P1 shortcut (recorded in the proposal; the
proposal stays published on the site through 2026-09-17 regardless).

- Settlement mortality input: WHO GHO 2019 abridged (banded estimator)
  → **UN WPP 2024 complete life table, 2023, single-age estimator**;
  population single-age WPP (same N: 8,091,734,933). License basis:
  CC BY 3.0 IGO (attribution now carried in print provenance) replacing
  a non-commercial source — the commercial licensing gate passes the
  new compute path with zero violations; the WHO path remains blocked.
- Level change, dual-run on committed snapshots: S 362.4126B →
  **363.5117B = +1.0991B (+0.3033%)**; decomposed +1.1639B table
  (WPP 2023 e0 73.1694 vs WHO 2019 73.1234) − 0.0648B single-age vs
  band-midpoint. Ē 44.7880 → 44.9238. Inside the published ±1.87%
  interval. Applies from the first epoch after acceptance
  (2026-09-07); archived prints stand as printed (P4).
- **Cite-what-you-consume stamping**: v0.7.0 prints cite only the files
  the computation read (the licensing gate judges the real input set;
  prints stop growing with unrelated snapshot evidence). Pre-G5 prints
  keep their cite-everything provenance and keep reproducing under
  their own versions (the pipeline is version-keyed end to end).
- Version string drops the `-reconstruction` suffix: A-16 closed by
  restore 2026-09-03 — the series no longer computes on reconstructed
  seeds.
