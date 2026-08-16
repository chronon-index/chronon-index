# TLY / Mirror — Design Decisions
Locked 2026-08-16. Names: **TLY** (the index), **Mirror** (the protocol), **CHRONON** (the token — resolved 2026-08-16).

**One-liner:** A demographically-ruled monetary asset. Token supply algorithmically mirrors humanity's total remaining life-years; each token is a fixed fractional slice of humanity's aggregate remaining time; price floats.

## Locked

1. **Layered rollout.** v1 TLY index (data product) → v2 cash-settled derivatives on it → v3 Mirror token → v4 Ledger. "All of the above" is a sequence, not one asset; each layer funds and legitimizes the next.
2. **Supply rule.** M(t) = κ·S(t), where S(t) = Σ over (age, sex, country) of population × remaining life expectancy. κ = 1 token per life-year at genesis (S₀ ≈ 330.0B).
3. **Mirror model.** All balances rebase pro-rata with S. A wallet's share of supply changes only by transfer, never by demographics. The token is a permanent fractional claim-by-convention on humanity's remaining time.
4. **Symmetric down-rebase on mortality shocks.** Mass-death events shrink every balance together — nobody's share grows from war or pandemic ("mortality neutrality").
5. **FX floats.** The formula governs supply only, never price. No peg → no reserves, no reflexive defense, no Soros trade against it.
6. **Versioned methodology, index-provider style.** v1.0 core inputs: UN WPP population and life tables, HMD STMF weekly deaths, GBD YLL. Expansion roadmap (HALE weighting, spending-by-age, conflict nowcasts) lands only via governed version bumps with a dispute process. Every input is an oracle attack surface; ambition enters through versioning, not v1.
7. **First print settles.** Corrections are forward-only, folded into the next epoch. No historical value is ever restated.
8. **Computation governance path.** v1: open-source, deterministic, fully reproducible from content-hashed public data snapshots. v2+: N-of-M independent recomputation must match. Autonomous operator (Cole-class agent) is a v3+ conversation, gated on the reproducibility record.
9. **Radical verifiability.** Every published figure is computed by open code from keyless public endpoints, prints its source URLs, and is reproducible by any third party. No number ships without a runnable path. First artifacts: `tly_v0_calc.py`, `CALC_REPORT_v0.txt`, `results_v0.json`, `METHODOLOGY_v0.md`.
10. **Ledger deferred to v4** behind three explicit gates: (a) credible proof-of-personhood exists; (b) market cap high enough that the per-person drip clears dust; (c) the actuarial-vs-equal issuance question is resolved (actuarial issuance hard-codes national inequality on-chain; equal issuance breaks the formula-equals-truth premise).

## Defaults set (overridable)

- Epoch: weekly print and rebase, Mondays 12:00 UTC, aligned to HMD STMF publication cadence.
- Denomination: 1 token = 1 life-year; UI displays hours and minutes (1 year = 8,766 h).
- Dispute window on fixings: 48 h, log-only, never blocks the next print.
- Dual series from P2: settlement settles on conservative measured-period S; best-estimate cohort S (with intervals) published alongside as informational. Settle on measurement, inform with the model.

## Open — your call

- **Name/ticker — RESOLVED: CHRONON.** Physics: the hypothesized indivisible quantum of time — the smallest unit time can be divided into, which is exactly what one token is. Pluralizes naturally as a currency word ("forty chronons"). Verified 2026-08-16: no existing Chronon token. Flag for formal clearance: the phonetic neighborhood is congested — Cronos (CRO, Crypto.com's chain), Chronos (CHR, defunct), Chrono.tech (TIME) — so an EUIPO/USPTO opposition risk from Crypto.com exists in classes 9/36/42; the clearance task (Part III R5) must assess it first. Ticker: full-word CHRONON (modern convention, maximizes distance from CRO/CHR). Rejected: Horae — it is a plural (singular "hora" is the generic word for hour in half of Europe, an unregistrable weak mark), pronunciation is ambiguous, and spoken aloud it sits one slurred syllable from an English vulgarity; a financial brand that cannot be said safely on a podcast is disqualified. Retained: Saeculum as the title of the annual flagship vintage report and as reserve name if clearance kills Chronon.
- **Chain** — v3 decision, irrelevant until then.
- **Legal wrapper** — MiCA vs offshore foundation; real counsel at v3, not before.

## Key numbers (computed, open, reproducible — see METHODOLOGY_v0.md and tly_v0_calc.py)

- Stock S = 362.4126B remaining life-years (2019 WHO table x WPP2024 population; 348.1905B on the COVID-depressed 2021 table). E-bar = 44.7880 years per living person.
- Organic issuance g = +0.7197%/yr from the identity dS/dt = B·e(0) − N + N·dĒ/dt (mint +9.6606B, spend −8.0917B, drift +1.0394B). CORRECTION: the earlier napkin +2.9%/yr was wrong — it omitted the aging spend term and misused GBD YLL. Open recomputation caught it; that is the point of the openness rule.
- g decays with fertility; population peaks ~10.3B mid-2080s (WPP 2024), S peaks earlier as aging drags Ē before headcount turns.
- COVID-scale pandemic (WHO 14.83M excess deaths) burns 148–337M life-years = −0.04% to −0.09% of S. Supply is glacially smooth; price variance will be demand-side.
- Rebases are wealth-neutral by proof (share invariance ⇒ wallet value = share × market cap): mortality never enriches a holder, longevity never dilutes one.
- Vision-consistent asymptote: burger = 15 min ⇒ $210,384.00 per life-year ⇒ $76.2458 quadrillion cap ≈ 138.9× global personal wealth (~$549T, UBS GWR chain). Mirror functions at any cap; Ledger only near the asymptote — which is why Mirror ships first.

## Status

**ACTIVE — unparked by Ben 2026-08-16.** Execution runs via RALPH_LOOP.md (one-task-per-iteration autonomous loop). Pipeline alternative remains available:

```
pipeline ingest --spec ~/tly/SPEC.md
pipeline analyze --project tly
pipeline status
pipeline start
```
