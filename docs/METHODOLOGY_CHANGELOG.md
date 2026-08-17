# Methodology changelog

Append-only. A methodology version bump is the ONLY sanctioned way to
change a numerical policy (SPEC#1 AC-1.4). The full procedure — proposal →
public comment window → version bump — is docs/METHODOLOGY_CHANGE_PROCESS.md.
Each entry lists the policies that version is defined by; the registry in
`tly/methodology.py` pins them and CI enforces the pairing.

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
