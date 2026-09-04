# SAECULUM whitepaper — working draft (D-07; renamed from CHRONON 2026-09-04)

Assembly per the skeleton's own order (3 → 2 → 5 → 7 first: their
substance is CI-verified repo artifact, so writing them is assembly,
not invention). **Sections 1, 4 and 6 remain SKELETONS by rule**: each
is gated on readings (Vaupel; Blake/LifeMetrics; Becker) that have not
been done — drafting them now would manufacture authority. The gate
markers are preserved verbatim below.

---

## 3. The Mirror monetary rule and the two neutrality proofs — DRAFT

One rule, no discretion: **M = κ·S**, with κ = 1 token per life-year.
The token supply is not managed toward the index; it *is* the index,
restated. Internally every wallet holds gons — fixed integers that no
rebase touches; the public balance is a pure rescaling
(balance = gons·M / 10³⁰). Two properties follow, and neither is
asserted on trust:

**Wealth neutrality (share invariance).** A rebase changes no wallet's
share of total supply — holding x% of SAECULUM is holding x% of
humanity's remaining time, before and after every settlement. This is
a *fuzzed, machine-checked theorem* of the reference contract
(`testFuzz_ShareInvarianceUnderRebase`, 2,000 randomized supplies per
run) and of the Python normative model, which agree byte-for-byte on
executed operation sequences.

**Mortality neutrality (path independence).** Any sequence of rebases
arriving at the same S yields identical balances: the order in which
the world's news arrives cannot advantage anyone
(`testFuzz_PathIndependence`). Expected deaths never enter the flow at
all — they are already priced inside e(x); only *excess* mortality
moves the stock (METHODOLOGY_v0.md §4).

Settlement itself is mechanical: each weekly print is archived in a
public hash chain, Bitcoin-timestamped (OpenTimestamps), keylessly
signed by the CI identity that computed it (Sigstore/Rekor), and the
on-chain rebase executes only when N-of-M independent recomputers
attest byte-identical values (`SaeculumOracle`). Disagreement stalls
the fixing — the failure ladder's DEFER, on-chain. A missed fixing
stays missed: first print settles.

## 2. The index and the identity — DRAFT

S(t) = Σ N(a,t)·e(a,t): people, weighted by the remaining years the
current period life table assigns them. The flow identity that governs
its motion (METHODOLOGY_v0.md §4; `tly/decomposition.py` with the
residual exposed, never absorbed):

  dS = births·e(0) − N·1yr + N·dĒ − Σ excess_deaths(a)·e(a)

Mint: each birth endows e(0) ≈ 73 years. Spend: every living person
uses exactly one year per year. Drift: revisions of measured longevity
re-mark the whole stock. Burn: only mortality *in excess of* the table
— the expected deaths cancel by construction. Organic growth nets to
≈ +0.4–0.8%/yr; COVID, the worst shock in the data, burned ≈ 0.05–0.09%
of the stock — measured, printed, never restated.

Discipline is the product: measured-period values settle (model
content is walled off in a separately-labeled INFORMATIONAL series);
the first print is final and corrections are forward-only in a public
ledger; every input file is content-hashed in committed manifests;
and one command reproduces any fixing byte-for-byte from public
artifacts (`docs/REPRODUCE_FIXING.md` — exercised weekly by CI against
every archived epoch, not asserted).

## 5. Governance as a mechanical rule — DRAFT

Everything discretionary is converted to procedure, and every
procedure to a test:

- **Methodology changes** ride a versioned registry: a policy cannot
  change without a version bump through a published proposal (14-day
  public window at launch); the pairing is CI-enforced, and archived
  prints reproduce forever under the version that made them —
  demonstrated live by the G5 source-of-record switch (v0.7.0), whose
  dual-run delta (+0.3033%) was published before sign-off.
- **Corrections** are forward-only ledger entries; **disputes** get a
  48-hour log-only window that alters nothing and is preserved
  forever.
- **Publication** is dumb static files behind a hash-chained archive;
  the CI run *is* the official computation (a print produced any other
  way is invalid by spec).
- **Trust is triangulated**, not requested: the hash chain links
  tampering, Bitcoin anchors the timeline, Sigstore ties each record
  to the exact workflow identity that computed it, and the weekly
  outsider-simulation plus (P5) external N-of-M recomputers make
  "verify us" a standing invitation with running code behind it. The
  IOSCO Principles mapping (docs/IOSCO_MAPPING.md) states row-by-row
  what is satisfied mechanically and what honestly awaits an
  administrator entity.

## 7. Risk factors, by the harshest critic — DRAFT (grow, never prune)

1. **Demand may simply not exist.** LifeMetrics had perfect math and
   died of a one-sided market. Nothing in this repository refutes
   that; only counterparties can. (Reading-gated section 4 owns the
   full postmortem.)
2. **The index is a bet on birth rates at horizon.** The 1000-event
   stress grid's clearest finding: a 20-year fertility collapse
   out-damages most pandemics (−24% by 2043) with no visible event.
3. **Upstream revision risk.** WPP restates biennially; the vintage
   archive and versioned level changes convert restatements into
   documented steps, not silent drift — but the steps are real
   (WHO→WPP moved the level +0.30%).
4. **Model risk beyond P2.** Cohort/stochastic content embeds
   forecasts; ensemble governance (RP Part V Q1) is unresolved. The
   stochastic fan's own backtest missed COVID *by design* — jump risk
   is priced as a 4-in-107-years overlay, which is honest and thin.
5. **Manipulation.** Quantified (MANIPULATION_ECONOMICS.md): data
   attacks are ppm-scale; the honest residual is infrastructure
   compromise until the attestor set is staffed and diverse.
6. **Regulatory.** US posture is favorable but unsettled (statutes in
   motion); the operator-residence question (German-resident founder)
   is live until counsel signs Memo C; benchmark regulation (BMR)
   applies the moment an EU-supervised entity uses the index in a
   in-scope way.
7. **Concentration.** Until launch distribution and the P6 oracle
   rotation complete, founder holdings and the deploy key are single
   points the conflict-of-interest statement discloses rather than
   hides.
8. **Ethics and communication.** Pricing life-years invites misreading
   as pricing lives; the personal page's framing (population
   statistics, not prophecy) is the standing answer and must never
   slip.
9. **Provenance history.** The 2026-08-16 loss-and-restore of the
   founding artifacts is documented (A-16, closed by verbatim restore
   with strict golden reproduction); the episode itself stays in the
   record.

---

## Reading-gated sections (skeletons preserved verbatim)

## 1. The claim: humanity's remaining time as a measurable stock

- Must argue: S(t) is a well-defined, measurable aggregate; a population's
  past mirrors its future (Carey's equality).
- Repo substance: METHODOLOGY_v0.md §1–2 (estimator), the live computed S
  with its error budget (`tly/error_budget.py` statement).
- Reading gate (HUMAN, R1): Vaupel 2009 "Life lived and left" — the
  Carey/Vaupel framing may not be characterized until read (verify).

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

## 6. The Becker 1965 anchor and the saeculum story

- Must argue: the economics of time's value; the naming lineage.
- Reading gate (HUMAN, R7): Becker 1965 must be READ before this section
  is drafted (verify); Censorinus/ludi saeculares sources for the
  saeculum story (verify). Strauss-Howe is branding footnote material
  ONLY, never load-bearing (RP Part III R7 warning, preserved here).

