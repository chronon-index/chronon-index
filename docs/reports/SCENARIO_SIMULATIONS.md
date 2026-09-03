# 1000-event index simulations — 20-year stress grid

*Ben directive 2026-09-04. Engine: `tly/scenario_engine.py` (model
layer); catalog: `tly/scenario_catalog.py` — exactly 1000 events,
generated as deterministic parameter grids, reproducible from those two
files alone. Full per-event results: `scenario_results.json`. Anchor
check: the COVID-shaped event (1.25× elder qx, 2y) produces a −4.4%
drawdown — the real COVID drew ~−4%.*

**Read this correctly: it is a STRESS GRID, not a probability
distribution.** Extreme tails (up to 200× mortality — civilization-scale
engineered pathogens, full nuclear exchanges) are deliberately included
and deliberately over-represented; a median over the grid is not an
expectation about the future.

## The one-line result

Across 1000 events spanning pandemics, wars, nuclear exchange, AMR,
climate, famine, natural catastrophe, engineered biology, fertility
swings, systemic decay, longevity breakthroughs and compounds: **the
index is extraordinarily hard to kill and structurally biased to
recover** — because S is a stock of remaining time, and every mechanism
that destroys it is bounded by the people it can reach, while the
mechanisms that grow it (births, mortality improvement) compound.

## Headline numbers

**Realistic core** (946 events — excluding the deliberate
civilization-collapse tail of ≥25× engineered pathogens and full/worst
nuclear exchanges):

| statistic | value |
|---|---|
| median max drawdown vs baseline | **−3.3%** |
| 5th-percentile drawdown | −32.6% |
| worst core drawdown | −59.9% (major nuclear exchange + deep winter) |
| median S deviation at 2043 | −0.5% |
| p5 / p95 S deviation at 2043 | −9.4% / **+8.9%** |
| baseline supply growth g | +0.37% to +0.80% per year |

Full grid including the tail: worst event (200× pathogen, 3 years)
destroys 97% of S — i.e., the index fails only when civilization does,
which is the correct behavior for an asset defined as humanity's
remaining time.

## Per-category profile (median / worst drawdown, best 2043 outcome)

| category | n | med dd | worst dd | best dS@2043 |
|---|---|---|---|---|
| pandemic | 238 | −9.7% | −39.1% | ~0 |
| breakthrough | 195 | **0.0%** | 0.0% | **+20.9%** |
| climate | 84 | −7.2% | −18.5% | −0.1% |
| engineered-bio | 72 | −65.5% | −97.4% | −0.2% |
| compound | 72 | −3.6% | −13.6% | **+37.6%** |
| fertility | 72 | −0.9% | −23.6% | **+42.6%** |
| nuclear | 54 | −32.4% | −61.8% | −2.4% |
| war | 51 | −1.6% | −10.8% | ~0 |
| amr | 46 | −2.5% | −13.4% | −0.2% |
| natural | 42 | −21.7% | −45.5% | ~0 |
| baseline-variant | 38 | −1.4% | −8.3% | +3.9% |
| systemic | 36 | −1.8% | −6.0% | −0.3% |

## The five findings that matter

1. **The asymmetry runs upward.** Mortality shocks are one-shot and
   bounded (a death removes one person's remaining years, once);
   fertility and longevity gains **compound** (a birth adds ~73 years
   that then survive and reproduce). The best outcomes (+20 to +43%)
   all come from breakthrough/fertility scenarios; no mortality
   catastrophe short of the civilization tail produces a symmetric
   loss. For a holder this is a long-biased payoff profile on human
   flourishing.

2. **Wars barely move the world index.** Even a "great-power war"
   parameterization (7 years) draws under −11%, and a WWII-scale world
   war ~−10% at trough — young combatant deaths are a small share of a
   362B-life-year stock. The index is a poor war-fear trade and a good
   war-recovery one (post-war fertility booms overshoot the baseline).

3. **What actually hurts: anything that kills the old *and* keeps
   killing.** The worst non-tail categories are nuclear-with-winter,
   asteroid/supervolcano, and severe multi-year pandemics — broad
   age profiles sustained for years. One-year spikes, however violent,
   mean-revert (the 2043 median deviation across ALL pandemics is
   −0.5%).

4. **Fertility is the slow master-variable.** A 20-year deep fertility
   collapse (×0.55) out-damages most pandemics by 2043 (−23.6%) with
   no visible "event" — and a pronatal-tech boom is the single biggest
   upside in the grid (+42.6%). The index is, at horizon, a bet on
   birth rates more than on death rates.

5. **Supply growth stays orderly outside the tail.** Baseline g is
   +0.4–0.8%/yr; in 95% of the realistic core the worst single year
   stays above −32%, and the median scenario's worst year is ~−1% —
   i.e., the monetary rule stays boring in almost every world where
   money still matters. (This is also the manipulation paper's result
   from the other direction: it takes a world-historical catastrophe,
   not a data attack, to move the supply meaningfully.)

## Limitations (stated, not hidden)

- **No prices.** These are index paths, not P&L: trading backtests
  need a demand/price model, and no market exists yet. What CAN be
  said: supply-side volatility is low outside catastrophe, so token
  price variance would be dominated by demand, not by the index.
- Model layer: float engine, world-aggregate only (no migration —
  world-closed), CBR baseline is a documented assumption (16.3→14.0 by
  2045), and the engine's baseline level sits ~0.9% above the
  settlement print (period-e from qx vs WPP's published ex) — all
  results are DEVIATIONS vs the engine's own baseline, which cancels
  the level bias.
- Grid weights are design choices, not probabilities.
