# SAECULUM whitepaper — skeleton (D-07; renamed from CHRONON 2026-09-04)

Structure per RESEARCH_PROGRAM Part XI, pointers only. NO section contains
drafted prose: each lists what it must argue, which repo artifacts already
carry the substance, and which readings must be DONE (HUMAN, Part III)
before its claims may be written. Drafting any section before its inputs
exist would manufacture authority — the skeleton exists so the eventual
writing is assembly, not invention.

## 1. The claim: humanity's remaining time as a measurable stock

- Must argue: S(t) is a well-defined, measurable aggregate; a population's
  past mirrors its future (Carey's equality).
- Repo substance: METHODOLOGY_v0.md §1–2 (estimator), the live computed S
  with its error budget (`tly/error_budget.py` statement).
- Reading gate (HUMAN, R1): Vaupel 2009 "Life lived and left" — the
  Carey/Vaupel framing may not be characterized until read (verify).

## 2. The index and the identity

- Must argue: the transport identity and why expected mortality cancels;
  first-print discipline; dual series.
- Repo substance: METHODOLOGY_v0.md §4 (derivation), `tly/decomposition.py`
  (E4/E5 with exposed residual), dual-series plumbing (`tly/prints.py`),
  the reproduction instructions (`docs/REPRODUCE_FIXING.md`).

## 3. The Mirror monetary rule and the two neutrality proofs

- Must argue: M = κ·S; rebases touch F only; wealth + mortality neutrality.
- Repo substance: METHODOLOGY_v0.md §6 (proofs), `tly/gons.py` (E10/E12),
  the machine checks (test_p1/p2/e12) — the proofs are CI-verified, cite
  that directly.

## 4. Why supply is glacial and demand is the product

- Must argue: g ≈ +0.72%/yr organic; COVID-scale shock ≈ −0.04..−0.09%;
  variance is demand-side. The LifeMetrics postmortem (one-sided demand)
  and why the Mirror token is the answer to it.
- Repo substance: DECISIONS.md Key numbers (all reproduced or residual-
  documented — cite CALC_REPORT addenda 7–8), `tly/jumps.py` COVID entry.
- Reading gate (HUMAN, R3): Blake et al. "The New Life Market", Loeys et
  al. 2007, the LifeMetrics technical doc — the postmortem section may not
  be written until these are read (verify). RP Part V Q4 (distribution
  strategy memo) feeds this section.

## 5. Governance as a mechanical rule

- Must argue: version-gated methodology, forward-only corrections,
  log-only disputes, first-print-settles — rule, not discretion.
- Repo substance: docs/METHODOLOGY_CHANGE_PROCESS.md, ledger/, the
  dispute log, fixing lifecycle, the IOSCO mapping (docs/IOSCO_MAPPING.md
  — pending D-06b fill).

## 6. The Becker 1965 anchor and the saeculum story

- Must argue: the economics of time's value; the naming lineage.
- Reading gate (HUMAN, R7): Becker 1965 must be READ before this section
  is drafted (verify); Censorinus/ludi saeculares sources for the
  saeculum story (verify). Strauss-Howe is branding footnote material
  ONLY, never load-bearing (RP Part III R7 warning, preserved here).

## 7. Risk factors, by the harshest critic

- Must argue: everything that can kill this — enumerated honestly.
- Seed list from repo evidence (grow, never prune): WPP revision risk
  (biennial restatements; vintage archive as mitigation), the WHO→WPP
  source-of-record level change (~0.5yr e0, documented), model risk at P2+
  (ensemble governance unresolved — RP Part V Q1), manipulation economics
  (RP Part V Q3 — the attack paper), demand risk (LifeMetrics precedent,
  RP Part V Q4), benchmark-regulation risk (BMR; RP Part V Q2),
  ethics/comms of pricing life-years (RP Part V Q5), the reconstruction
  provenance of this very methodology (pending A-16 ratification), STMF
  access regression (keyless route gone), WMD staleness (data edge
  2024-12).

## Assembly order (when the reading gates clear)

3 → 2 → 1 (the mathematical core is CI-verified today) then 5 (governance
is built) then 7 (risks are enumerable today) then 4 and 6 (blocked on
readings). Sections 3, 5, 7 could be drafted from repo artifacts alone.
