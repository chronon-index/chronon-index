# Live-burn dual run — what weekly prints would do with the burn active

*Item 3 of the 2026-10-03 resume. Module `tly/liveburn_dualrun.py`;
per-week numbers in `liveburn_dualrun.json`; every figure recomputes
from committed snapshots. This is the evidence base for the activation
proposal. The settlement path is UNTOUCHED until a governed bump that
Ben signs.*

## Setup

Eurostat weekly panel (38 geographies, all with full 2015-2019
kk-linear baselines), 2026 weeks through the ≥20-country edge
(2026-W27). Conversion: **9.2890 life-years per excess death** on the
live WPP-2023 settlement table (registered age profile). World
scaling: the panel covers a measured **9.52% of world deaths** (2019
reference, measured over measured), so world estimates are
panel ÷ 0.0952.

## Result — four findings

**1. Magnitude: single-digit ppm per week.** Normal-times weekly
burns land between −1.3 and +4.1 ppm of S. Cumulative 2026 through
W27: **−8.1 ppm** of S (−12.3 excluding the edge week). Weekly prints
would finally move every week — at the sixth decimal of a percent.
The supply stays glacial exactly as designed; what changes is that
the print's burn line becomes a measured number instead of 0.

**2. The sign question is live, not hypothetical.** 2026 mortality in
the panel is running BELOW baseline — the measured "excess" is
negative in 16 of 27 weeks and cumulatively. The identity treats
expected deaths as already priced into e(x); a mortality deficit is
information of exactly the same kind as a surplus. **A symmetric rule
(deficits credit what surpluses debit) follows the identity; an
asymmetric burn-only rule would have silently removed ~12 ppm of
true S this year.** The proposal will recommend symmetric; the
decision is Ben's at sign-off.

**3. Burns post in arrears — by construction, not by choice.** The
mature panel edge is W27 while prints run at W40: reporting lag means
the burn term posts ~8–13 weeks behind the epoch it measures.
Convention for the proposal: forward-only postings at maturity (the
week's burn enters the first print after that week reaches the
maturity rule), never restatement — first-print-settles untouched.

**4. Two instabilities the activation must fence.**
- *Coverage amplification:* at 9.52% coverage, world-scaling
  multiplies panel noise ~10.5×. Widening the live panel (CDC ~ +6%,
  ONS ~ +1% of world deaths — their excess machinery already exists)
  roughly halves the amplification; the proposal should make panel
  composition a registered policy.
- *Edge-week composition:* W27 flips the cumulative by 4 ppm because
  the reporting set changed (31 → 26 countries). The ≥20-country
  aggregate guard is not enough for POSTING; the maturity rule must be
  per-country (a week posts when the SAME country set as the baseline
  fit has reported), which the winsorization from the manipulation
  paper's hardening also complements.

## What the proposal will say (draft skeleton, for the refutation pass)

v0.8.0: settlement burn = coverage-adjusted panel excess, symmetric,
per-country maturity rule, E11-quantized postings in arrears,
panel composition and coverage reference as registered policies,
DEFER via the failure ladder when the panel edge stalls. Archived
prints stand; the golden is untouched; activation turns the burn line
from a structural 0 into a measured series worth ~±1 ppm/week.
