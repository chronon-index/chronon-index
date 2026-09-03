# Manipulation economics — the attack paper (RP Part V #3)

*"Cost to move a national mortality statistic vs payoff on index
derivatives; sizing of per-epoch caps and trimmed aggregation. Write
the attack paper yourself before someone else does." — written
2026-09-03, by the project, about the project. Every number recomputes
from committed artifacts.*

## Threat model

An attacker wants to move a published fixing in a chosen direction and
profit on an instrument that settles on it. Channels, by input:

1. **Burn channel** — fabricate or suppress weekly deaths in a source
   feed (Eurostat panel, CDC, ONS, WMD).
2. **Structure channel** — corrupt the annual population / life-table
   input (UN WPP).
3. **History channel** — alter the 2015–2019 baseline the excess
   calculation fits against.
4. **Infrastructure channel** — compromise the repo/CI to rewrite
   prints directly.

## Channel 1: the burn lever is tiny (computed)

S is a **stock** (~362.4B life-years); weekly excess deaths are a
~10⁻⁶-scale flow against it. Each excess death burns
**9.0448 life-years** under the governed age profile
(0.7·e(75.5) + 0.3·e(85.5) on the epoch table, methodology v0.5.0+):

| fabricated excess deaths | life-years burned | move in S |
|---|---|---|
| 1,000 | 9,045 | 0.025 ppm |
| 10,000 | 90,448 | 0.25 ppm |
| 100,000 | 904,476 | **2.5 ppm** |

For scale: fabricating 100,000 deaths — a fiction larger than most
countries' *total* weekly mortality, visible to every demographer with
a newspaper — moves S by 2.5 parts per million. Total fabrication of
the single largest weekly feed in the panel (US, ~60k deaths/week)
is worth ~1.5 ppm per week. The burn channel is economically dead:
the cost of corrupting a national statistical agency buys a move
inside the noise floor of the published ±1.87% interval.

Additional structural obstacles, all live in code: the baseline is fit
on frozen, hash-manifested 2015–2019 snapshots (a fabricated spike
raises measured excess but cannot bend the baseline it is measured
against); the coverage block prices measured share honestly, so a
poisoned feed's weight is visible; the vintage store records every
weekly pull, so a value that jumps between pulls leaves a permanent
lag-triangle anomaly; and the failure ladder means yanking a feed
produces a flagged CARRY, never a silent gap.

## Channel 2: the structure lever is the real one (computed)

S = Σ N(a)·e(a), so a **uniform +0.01-year shift in life expectancy**
moves S by N × 0.01 ≈ 81M life-years = **223 ppm (0.022%)** — roughly
**90× the leverage of 100,000 fabricated deaths**. A +0.1-year shift
is +0.22% of S; a full year is +2.2%. The G5 dual-run illustrates the
scale: the WHO→WPP table change moves S by +0.30%.

This is where the defense budget belongs, and where it already sits:

- **One licensed source of record** (WPP; G5), revised on the UN's
  biennial cycle — not a feed an attacker can nudge weekly. Corrupting
  it means corrupting the UN Population Division's published files
  *and* the hash-manifested snapshot discipline: the committed vintage
  is frozen at fetch time, so post-hoc file tampering upstream produces
  a NEW vintage beside the old (first-print-settles), never a silent
  restatement.
- **Level changes route through versioning** — a table revision lands
  as a governed methodology bump with a published dual-run (exactly
  what the G5 proposal does), not as an unexplained drift in the
  series.
- **Annual deltas are E11-scheduled** across the year's epochs in
  conserving quanta — a structure update cannot spike a single fixing.

## Channel 3: history — closed by construction

The baseline years live in committed, content-hashed snapshots; the
archive chain and OTS Bitcoin anchors (blocks 964013 / 964946) make
retroactive alteration detectable by anyone with the repo and a block
explorer. Rewriting history requires rewriting a public git history,
its hash chain, and a Bitcoin block — at which point the attack is on
Bitcoin, not on TLY.

## Channel 4: infrastructure — the honest weakest link

Cheaper than any statistical attack: compromise CI or a maintainer
account and publish a false print. Mitigations live: branch protection
(strict ruleset staged; deploy-key bypass only), the outsider-sim
recomputing every archived epoch weekly from public artifacts, OTS
anchoring, and — the real defense — **N-of-M external recomputers**
(E-14): a corrupted print that no independent party can reproduce is a
detected incident, not a settlement. Until E-14 is staffed, this
channel is the residual risk and is stated as such.

## Payoff side

No instrument settles on TLY today, so the current payoff is zero and
this paper is preemptive. When instruments exist: weekly fixings move
by ~ppm from measured mortality and by scheduled, pre-announced quanta
from structure updates — an attacker needs enormous notional against
near-zero engineered drift, in a market whose settlement value any
counterparty can recompute. The manipulation-economics asymmetry runs
the right way: **the cost of moving the input exceeds the move's value
by orders of magnitude on every statistical channel.**

## Proposed hardening (sized, not yet implemented — future version bumps)

1. **Per-epoch burn cap:** clamp weekly excess-burn at the historical
   COVID-peak weekly burn × 1.5, overflow E11-scheduled forward with a
   flagged status. COVID (the worst real shock on record: 175.5M
   adjusted life-years over the whole event) stays inside it;
   a single-week fabrication beyond any historical precedent cannot
   spike a fixing.
2. **Trimmed panel aggregation:** compute per-country excess z-scores
   against each country's own baseline volatility; winsorize the top
   and bottom 2.5% of country-weeks before aggregating. COVID — a
   correlated, many-country signal — survives trimming; a fabricated
   single-country spike is exactly what gets clipped. (Sizing note:
   the ≥20-country panel edge already enforced for the weekly series
   is what makes trimming meaningful.)
3. **Cross-source triangulation alarm:** where two independent feeds
   overlap (Eurostat vs ONS for E&W-adjacent geographies; WMD vs
   national feeds), a divergence beyond reporting-lag norms (from the
   vintage-store lag triangle) flags the epoch's status block.

Each lands as a governed methodology bump with tests, when accepted.

## Limitations

Static analysis, not a red-team exercise; no adversarial simulation of
the chain-ladder/backfill machinery yet; derivative-market
microstructure (where the payoff side would live) is out of scope until
an instrument exists. IOSCO Principle mapping for manipulation controls
is in `docs/IOSCO_MAPPING.md` rows 4, 15, 17.
