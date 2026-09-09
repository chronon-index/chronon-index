# Proposal: model-risk governance — the fixed-weight ensemble rule (RP Part V Q1)

**Status: DRAFTED for adoption at the next model-content version bump.
Changes nothing today** — the SETTLEMENT series contains no forecast
(measured-period only, by construction), so this rule governs the
INFORMATIONAL surfaces (cohort-S, the stochastic fan) now and becomes
load-bearing only if model content ever feeds settlement (it should
not; this proposal also says why).

## The question

Beyond P2 the informational series embed a mortality forecast. Who
picks the model? Discretion here is the same evil the monetary rule
exists to remove: a maintainer who can choose the model can steer the
number.

## The rule (the monetary-rule philosophy applied to model choice)

1. **A fixed-weight ensemble of ≥3 published, independently-specified
   mortality models.** Candidates already in or adjacent to the repo:
   Lee-Carter (implemented, backtested, bias published), the WPP
   medium-variant projection itself (an external institution's model —
   maximal independence), and a CBD/Cairns-Blake-Dowd-family model for
   old-age dynamics (to implement at adoption). Each model's forecast
   of the qx surface is computed separately and published separately.
2. **Weights are constants in the methodology registry.** Initial
   proposal: equal weights (1/3 each) — any unequal choice must argue
   itself through the change process. Changing a weight, adding, or
   removing a model is a VERSION BUMP with the full public-window
   process; the registry pairing test makes a silent change fail CI,
   exactly as it does for every other policy.
3. **No in-sample reweighting, ever.** Backtest performance is
   published (each model's bias, per era, in the open) but never feeds
   an automatic weight update — automatic "performance" weighting is
   discretion wearing a formula, and it overfits the last shock.
4. **The ensemble never touches settlement.** Settlement is
   measured-period arithmetic on published statistics; the identity
   requires no forecast. Any future proposal to let forecasts into the
   settlement path must survive the change process AND an external
   recomputer cycle first. This line is the whole point of the
   dual-series design.
5. **Disagreement is data.** The published informational print carries
   the ensemble spread (min/max across members) alongside the
   combined value — model disagreement is disclosed as part of the
   number, not averaged into silence.

## Adoption path

Implement CBD (stdlib, same discipline as leecarter.py) → backtest all
three on the vintage store → publish the comparison → version bump
adopting this rule with equal weights. Effort: one focused build
iteration; sensible to schedule after the first external recomputers
exist so the machinery is verified independently before it carries
published uncertainty.
