# CHRONON / TLY — Master Research & Build Program
From v0.1 to the most extensive version possible. Companion to DECISIONS.md,
SPEC.md, METHODOLOGY_v0.md. Status: parked behind TrancheBook; this document
exists so that when unparked, nothing has to be rediscovered.

Convention: (verify) marks facts/URLs recorded as of Aug 2026 that must be
re-checked at execution time. Effort figures are focused-work estimates.

---

## Part I — The mathematics to own

You should be able to derive every result below from scratch before v2 ships.
Order matters; each block builds on the last.

**M1. Demographic accounting core (est. 25-35 h)**
- Life table construction end to end: m(x) -> q(x) via a(x) separation
  factors, l(x), d(x), L(x), T(x), e(x); abridged vs complete tables;
  closure of the open age interval. Reproduce the WHO 2019 global table's
  e(x) column from its m(x) inputs to 3 decimals as the exercise.
- Stationary and stable population theory: Lotka's equation, intrinsic
  growth rate, and Carey's equality (in a stationary population the
  distribution of ages equals the distribution of remaining lifetimes —
  Vaupel 2009, "Life lived and left"). This is the theoretical heart of the
  asset: a population's past mirrors its future.
- The transport identity. From the McKendrick–von Foerster equation
  dN/dt + dN/da = -mu(a,t) N and de/da = mu e - 1, derive
  dS/dt = B e(0) - N (+ migration per country, + revision drift, - excess
  burn), and show the mortality terms cancel exactly. Already sketched in
  METHODOLOGY_v0.md section 4; produce the full worked version with the
  migration term and per-country reconciliation (sum of country dS = global
  dS, exactly, in Decimal — the fund-proofs conservation discipline).
- Exact discrete-time accounting: within-year fractions, mid-year exposure,
  and the reconciliation of weekly prints to annual identities.
- Decomposition methods (Arriaga, Pollard, stepwise replacement) for
  attributing changes in S to ages and causes — this powers the
  cause-attributed burn sub-indices of rung 5.

**M2. Mortality projection: period to cohort (est. 40-60 h)**
- Lee-Carter (1992): log m(x,t) = a(x) + b(x) k(t) + e; SVD fit; k(t) as
  random walk with drift; jump-off bias correction. Implement from scratch
  on HMD data for 3 countries; replicate published parameter estimates.
- Extensions: Renshaw-Haberman cohort effect, Plat (2009), Cairns-Blake-Dowd
  M5-M7 family. Read Cairns et al. (2009), the quantitative comparison of
  eight models, and adopt its backtest protocol.
- The UN's own machinery: Bayesian hierarchical probabilistic projections
  (Raftery et al., PNAS) — this is what generates the WPP variants you
  already consume; understanding it means understanding your upstream.
- Old-age closure: Gompertz-Makeham, Kannisto logistic; the mortality
  plateau debate (Barbi et al. 2018, Science, and the Newman critiques).
- Cohort expectancy from a projected mortality surface:
  e_cohort(a, t) = integral over s of exp(-integral of mu(a+u, t+u) du) ds.
  This replaces the period e in S and is the single largest level change
  (+3-8% est.). Backtest gate: fit on data through 1990 only, project
  1990-2020, compare to realized — publish the bias.

**M3. Stochastic index and derivatives mathematics (est. 40-60 h)**
- S as a functional of the mortality surface; sensitivities of S to the
  Lee-Carter factors (the index's "greeks").
- Jump component for shocks: frequency-severity calibration of pandemic and
  conflict mortality; extreme value theory (peaks over threshold) for the
  tail. Historical calibration set: 1918 flu, WWII, HIV, COVID.
- Forward life-years S(t,T) and the settlement conventions that make a
  forward curve coherent with first-print discipline.
- Pricing in an incomplete market: longevity risk is not hedgeable, so
  risk-neutral measures are not unique — study Sharpe-ratio loading and the
  Wang transform (Wang 2000) as used in the longevity bond literature.
- Basis risk: index vs any real book of lives — the mathematical reason
  LifeMetrics derivatives failed to trade. Quantify it before promising
  hedgers anything.
- Uncertainty propagation: Monte Carlo over (population estimate error x
  projection model x shock nowcast), variance reduction, interval coverage
  tests on the backtest.

**M4. Protocol mathematics (est. 15-25 h)**
- Rebase via a global scaling factor (the gons pattern): O(1) rebases,
  overflow and precision analysis in fixed point, formal proof that share
  vectors are invariant under any rebase sequence.
- Largest-remainder allocation correctness and the residual-account
  conservation proof (imported from the fund-proofs work).
- Formal statements: wealth-neutrality (done, METHODOLOGY section 6) and
  mortality neutrality; write both as machine-checkable properties for the
  SPEC capability 5 test suite.
- Oracle aggregation: N-of-M with trimmed mean vs median; cost-to-corrupt
  analysis as a function of the number of independent computers.

**M5. Numerical standards (est. 5-10 h)**
- Interpolation policy: linear vs monotone cubic Hermite on e(x) anchors
  (monotone Hermite avoids overshoot at the old-age bend); pick one,
  version it.
- Decimal contexts everywhere money- or supply-adjacent; float quarantine.
- Reproducibility: pinned snapshots, content hashes, deterministic seeds
  for all Monte Carlo, byte-identical re-runs as a CI gate.

---

## Part II — Complete data source catalog

For each source: what it is, granularity, cadence, access, and role. All
URLs (verify) at execution time.

**D1. Population stocks and structure**
- UN World Population Prospects 2024 — population by single year of age and
  sex, 237 locations, 1950-2100, medium/low/high/probabilistic variants.
  CSV downloads at population.un.org/wpp; also a data portal API. THE
  backbone. Biennial revisions (WPP 2026 due — check).
- Our World in Data grapher mirrors (ourworldindata.org) — clean CSV access
  to WPP series; already the v0 source of record.
- National statistical offices for high-weight countries: US Census Bureau
  and CDC/NCHS, Destatis (DE), ONS (UK), INSEE (FR), Statistics Bureau
  Japan, NBS China (treat with the manipulation caveat), MoSPI India.
  Monthly/quarterly estimates for nowcast anchoring.
- Eurostat — EU population and demography, including weekly deaths (demo_r_mwk*).
- Human Mortality Database exposures (mortality.org) — research-grade
  denominators for ~41 countries.

**D2. Life tables and mortality levels**
- Human Mortality Database (HMD) — single-age life tables 0-110, ~41
  countries, the gold standard; free with registration.
- WHO Global Health Estimates life tables via GHO API — 183 countries,
  abridged, 2000-2021 (v0's source). Watch for post-2021 releases.
- WPP 2024 abridged and single-age life tables — all countries, including
  projections (the cohort-table raw material).
- IHME Global Burden of Disease (ghdx.healthdata.org) — mortality, YLL,
  cause decomposition; use as triangulation, not as the e source (its YLL
  uses an aspirational reference table — the exact trap the v0 correction
  log documents).
- Actuarial tables for cross-checks: CMI (UK, Institute and Faculty of
  Actuaries, subscription (verify)), SOA tables and MP improvement scales
  (US), DAV tables (Germany). Human Life-Table Database (lifetable.de) for
  historical depth.

**D3. High-frequency mortality (the nowcast mesh)**
- HMD Short-Term Mortality Fluctuations (STMF) — weekly deaths by age band,
  ~38-40 countries. Already in SPEC v1.
- World Mortality Dataset (Karlinsky & Kobak, GitHub) — the broadest open
  excess-death compilation, ~120 countries, actively maintained (verify).
- Eurostat weekly deaths; CDC provisional deaths (US).
- The Economist's excess-mortality machine-learning model — global weekly
  estimates with intervals, code and outputs on GitHub; use as the
  imputation layer for unregistered regions, clearly labeled as model.
- WHO excess mortality estimates (the 14.83M COVID anchor).

**D4. Shock feeds by cause**
- Conflict: UCDP Georeferenced Event Dataset (Uppsala, annual + candidate
  monthly), ACLED (weekly, license terms (verify)).
- Disasters: EM-DAT (CRED, UCLouvain).
- Famine: FEWS NET, IPC classifications.
- Pandemic surveillance: WHO FluNet, national wastewater programs.
- Each feed needs an age-at-death distribution assumption per cause,
  documented and versioned (rung 5).

**D5. Fertility and births**
- WPP births and rates; Human Fertility Database (humanfertility.org) —
  HMD's companion, research-grade; national CRVS birth registrations for
  nowcasting the mint term.

**D6. Registration quality (the imputation floor)**
- UN Statistics Division CRVS coverage assessments; WHO SCORE reports; GBD
  data-quality star ratings. Purpose: publish, per country, how much of the
  index is measurement vs model — an honesty layer competitors will not have.

**D7. Health-adjusted layer (rung 7)**
- WHO HALE (healthy life expectancy); GBD YLD and disability weights.
  Governance note: switching the unit to healthy-life-years is a
  redefinition of the asset and needs its own version gate and comms.

**D8. Heterogeneity and personalization (v4 Ledger research)**
- Chetty et al. 2016 (JAMA) income-longevity gradient, public data.
- Education/SES gradients: Eurostat, national cohort studies.
- Biological-age literature: Horvath clocks, GrimAge, PhenoAge.
- Insurer-grade mortality: SOA ILEC experience studies. UK Biobank (access
  application required) for covariate-rich survival modeling.

**D9. Economic anchors**
- UBS Global Wealth Report (annual, June) — the wealth denominator.
- VSL: US DOT annual guidance memo, EPA; VSLY literature (Viscusi).
- NICE cost-per-QALY thresholds (UK) — the public price of a life-year.
- UBS Prices and Earnings — minutes-of-work purchasing power (the burger
  metric's institutional ancestor).

**D10. Market and mechanism precedents (primary documents)**
- JPMorgan LifeMetrics technical document (Coughlan et al., 2007) and the
  q-forwards papers — the direct prior art; obtain and annotate.
- LLMA (Life and Longevity Markets Association) archive material.
- EIB/BNP Paribas 2004 longevity bond documentation (the failed launch);
  Swiss Re Vita mortality cat bonds (the successful opposite side).
- Pension risk transfer market reports (LCP, Hymans Robertson, WTW) — the
  live two-sided longevity market and your eventual institutional users.
- Ampleforth docs and audits (rebase mechanics), Basis and Terra
  postmortems (peg graveyard), Worldcoin whitepaper and critiques (PoP),
  Circles postmortem (demogrant sell pressure), Chile UF history (the
  surviving formula-unit), Fureai kippu studies (time credits in practice).

---

## Part III — Reading curriculum, in order

**R1. Foundations (3-4 weeks part-time)**
- Preston, Heuveline & Guillot, "Demography: Measuring and Modeling
  Population Processes" — THE textbook; read fully, do the exercises for
  chapters on life tables and decomposition.
- Keyfitz & Caswell, "Applied Mathematical Demography" — the transport
  identity's natural habitat.
- Wachter, "Essential Demographic Methods" — lighter companion.
- Vaupel 2009, "Life lived and left: Carey's equality" (Demographic
  Research) — short, foundational for the asset's story.

**R2. Mortality modeling (2-3 weeks)**
- Lee & Carter 1992 (JASA). Cairns, Blake & Dowd 2006 (JRI). Renshaw &
  Haberman 2006. Plat 2009. Cairns et al. 2009 eight-model comparison
  (North American Actuarial Journal) — adopt its backtest design.
- Raftery et al. on Bayesian population projections (PNAS) — your upstream.
- Barbi et al. 2018 (Science) and responses — the plateau debate.

**R3. Longevity markets (1-2 weeks)**
- Blake, Cairns, Dowd, MacMinn — "The New Life Market" (JRI 2013) and the
  annual Longevity conference survey papers.
- Loeys et al., "Longevity: a market in the making" (JPMorgan 2007).
- Wang 2000 (the Wang transform) — pricing without a complete market.
- A written postmortem, by you, of why LifeMetrics/LLMA derivatives failed:
  one-sided demand, basis risk, no retail leg. The Mirror token is the
  answer to that postmortem; write it as such.

**R4. Index governance (1 week, before any settlement product)**
- IOSCO Principles for Financial Benchmarks (2013) — the global standard a
  settlement index is judged against; map every principle to a SPEC
  capability.
- EU Benchmark Regulation (BMR, 2016/1011) — determine whether TLY becomes
  a regulated benchmark if EU venues list derivatives on it (likely yes;
  administrator authorization is heavy — a reason to start non-EU) (verify
  current BMR third-country regime).
- The Wheatley Review of LIBOR — the canonical manipulation case study;
  design against it.

**R5. Token and securities law (1-2 weeks, with counsel at execution)**
- MiCA: classification analysis — SAEC has no redemption claim and no
  basket peg, so it is not an asset-referenced token; likely an "other
  crypto-asset" with whitepaper obligations (verify against final Level 2
  texts and ESMA guidance).
- SEC: Howey applied to a rebasing index token; study recent event-contract
  and commodity-classification precedents (CFTC/Kalshi line of cases).
- FINMA foundation route (Zug) vs Cayman foundation vs UK — jurisdiction
  memo with counsel.
- Trademark clearance: CHRONON in Nice classes 9, 36, 42; EUIPO and USPTO
  searches; explicit likelihood-of-confusion assessment against Cronos (CRO,
  Crypto.com) and Chronos (CHR); domain and ticker collision sweep. Reserve
  name if blocked: SAECULUM (already verified clean).

**R6. Mechanism design precedents (3-4 days)**
- Ampleforth documentation and audits; Basis Cash and Terra postmortems;
  Worldcoin PoP papers plus independent critiques; Circles UBI postmortem;
  history of the Chilean UF; Fureai kippu field studies; Ithaca HOURS.

**R7. Positioning and philosophy (2-3 days, for the whitepaper)**
- Becker 1965, "A Theory of the Allocation of Time" — the canonical
  economics of time's value; the whitepaper's intellectual anchor.
- Roman saeculum sources (Censorinus, the ludi saeculares) for the name's
  story. Note: the Strauss-Howe "saeculum" generational theory is pop
  material, not scholarship — usable as a branding footnote, never as a
  load-bearing citation.

---

## Part IV — Build phases and acceptance gates

- P0 (done): v0.1 — open calculator, methodology, corrected identity.
- P1 (2 weeks): v1.0 index per SPEC.md — country x sex x single-age,
  weekly nowcast, snapshot governance, publication, fixing module. Gates
  are the SPEC acceptance criteria.
- P2 (3-4 weeks incl. R2 reading): cohort tables. Lee-Carter implemented
  and backtested (fit through 1990, project to 2020, publish bias); Kannisto
  closure; cohort-S published alongside period-S as parallel series before
  any switch. Gate: backtest bias documented; ensemble weights versioned.
- P3 (2-3 weeks): stochastic S — intervals, forward curve S(t,T), jump
  calibration on the 1918/WWII/HIV/COVID set. Gate: interval coverage on
  backtest within stated tolerance.
- P4 (2 weeks): shock mesh — STMF + World Mortality Dataset + UCDP/ACLED +
  EM-DAT, cause-attributed burn. Gate: COVID replay using only
  real-time-vintage data (no hindsight), error vs final documented.
- P5 (research + legal): settlement hardening — IOSCO gap analysis mapped
  to capabilities, oracle N-of-M live with at least 3 independent
  recomputers, BMR/jurisdiction memo. Gate: an external party reproduces a
  fixing from public artifacts alone.
- P6: Mirror token — SPEC capability 5 hardened to contract form, audits,
  MiCA/securities memo executed, testnet with public rebase feed. Gate:
  audited share-invariance and mortality-neutrality properties.
- P7 (parallel research track, no build): Ledger — PoP landscape review,
  personalized-e ethics and issuance-equity memo, dust-threshold economics.

Cumulative focused effort to the end of P5: roughly 350-500 hours plus
counsel. P1 alone is the 2-week pipeline build already specced.

---

## Part V — Open research questions (the honest hard part)

1. Model-risk governance: beyond P2 the index embeds a forecast. Who picks
   the model? Proposal to develop: a fixed-weight ensemble of 3+ published
   models, weights changeable only by version gate — the monetary-rule
   philosophy applied to model choice.
2. Benchmark regulation: does listing an EU derivative make TLY a BMR
   benchmark requiring an authorized administrator? Sequencing implication:
   first venues likely US/offshore.
3. Manipulation economics: cost to move a national mortality statistic vs
   payoff on index derivatives; sizing of per-epoch caps and trimmed
   aggregation. Write the attack paper yourself before someone else does.
4. Demand: the question no mathematics answers. LifeMetrics had perfect
   math and no second side. Candidate legs: pension funds (long longevity
   protection), life insurers (natural opposite), crypto store-of-value
   narrative, sovereigns. A distribution strategy memo is worth more than
   rungs 6 and 7 combined.
5. Ethics and comms of publicly pricing life-years: VSL/QALY precedent as
   the shield; pre-write the criticism response before launch.
6. Ledger issuance equity: actuarial (accurate, encodes inequality) vs
   equal (egalitarian, breaks formula-truth). This is political philosophy,
   not mathematics; do the Rawls/luck-egalitarianism reading before v4.
7. WPP 2026 revision risk: the biennial update will restate the level;
   first-print discipline plus a public vintage archive (ALFRED-style)
   turns restatements from embarrassment into product.

---

## Part VI — Standing verification protocol (applies to every number, forever)

1. Source URL + retrieval timestamp + content hash recorded in the manifest.
2. A runnable code path from raw snapshot to published figure; re-run must
   be byte-identical (CI gate).
3. Methodology version stamped on every artifact; changes only by version
   bump with changelog.
4. Two independent sources minimum for any level claim; disagreements
   published, not averaged away silently.
5. Corrections forward-only, in the correction ledger; first print settles.
6. Uncertainty stated wherever it exists; a number without an interval is a
   convention, and must be labeled as one.
7. Anything recorded from memory or secondary sources carries (verify)
   until confirmed against the primary — including everything in this
   document.

---

## Part VII — Infrastructure and hosting (compute in public)

The verifiability principle dictates the architecture: the computation itself
should happen in public, not merely be reproducible in private.

- **Compute:** public GitHub repository (org under Praevex), GitHub Actions
  cron job every Monday 12:00 UTC. The CI run IS the official computation:
  logs public, artifacts hashed and committed. Anyone can watch the print
  being made. Cost: free tier suffices for v1.
- **Publication:** static site + static JSON API on Cloudflare Pages (the
  SPEC API is deliberately static-friendly). Custom domain at execution time
  (saeculum.* / tly.* sweep is part of the trademark clearance task).
- **Snapshot storage:** raw data snapshots are too large for git — object
  storage (R2/S3) with sha256 manifests committed in-repo; quarterly deposit
  of the full snapshot set to Zenodo for a DOI per vintage (citable data,
  academic credibility, free).
- **Timestamping:** OpenTimestamps each print hash (Bitcoin-anchored, free,
  no chain commitment implied). When the token chain is chosen at v3, fixings
  additionally post on-chain.
- **Independent recomputation (P5):** one-command Docker image published;
  recruit at least two external recomputers (a university demography group
  and an actuarial society student chapter are natural candidates) who sign
  and publish their hashes. N-of-M starts at 3-of-3 matching.
- **Ops:** status page, stale-print flagging (already in SPEC), disaster
  recovery = the repo itself (everything rebuilds from snapshots + code).
- **Upstream licensing audit (a P1 GATE, not a footnote):**
  - UN WPP: CC BY 3.0 IGO — commercial use OK. Make WPP the licensed source
    of record for life tables in v1 (it publishes them), with WHO as
    triangulation only, because:
  - WHO GHO carries a non-commercial clause on much content (verify) — fine
    for v0 research, a problem for a commercial index product.
  - HMD: free registration; redistribution of raw data restricted (verify) —
    publish derived indicators, link raw.
  - ACLED: commercial license required (verify). EM-DAT: license needed for
    commercial use (verify). Economist excess model: MIT-licensed code,
    check output terms (verify).
  - Deliverable: a licensing table in-repo, one row per source, cleared
    before the first public print.
- **Cost estimate pre-token:** infra < EUR 200/yr; counsel EUR 10-30k at
  P5/P6; smart-contract audits USD 50-150k at P6. Everything before P5 is
  essentially time, not money.

## Part VIII — Error budget and the accuracy statement

What v0 can honestly claim, decomposed. Propagation: for independent inputs,
Var(S) = sum of (dS/dx_i)^2 Var(x_i), with dS/dN(a) = e(a) and
dS/de(a) = N(a). Symmetric terms combine in quadrature; one-sided biases are
listed, never netted.

Symmetric (measurement) terms on the v0 level:
- Population level and age structure (WPP estimate error, world aggregate,
  worse where registration is weak): ~ +-1.0%
- Life-table level (global E-bar from an estimated table): ~ +-1.0-1.5%
- Banding, interpolation, old-age closure: ~ +-0.5%
- Quadrature total: ~ +-2%

One-sided (structural) terms:
- Vintage lag (2023 structure, 2026 today): +2 to +3% (stock is higher now)
- Period vs cohort expectancy: +3 to +8% (true cohort stock is higher)

The honest v0 statement, to appear wherever S is quoted:
"Measured-period S = 362.4B +- ~2% on 2023 structure; best-estimate current
cohort stock 381-402B (computed per the error-budget module, blessed per A-16)."

Design decision (proposed default): publish a DUAL SERIES from P2 onward —
settlement settles on the conservative measured-period S (small model
content, hard to dispute); the best-estimate cohort S with intervals is
published alongside as informational. Settle on measurement, inform with the
model. From rung 4, every print carries a Monte Carlo interval and the
deterministic budget above retires.

## Part IX — Formulary (the equations, numbered)

- E1  S(t) = sum over a, c of N(a, c, t) * e(a, c, t)
- E2  v0 estimator: S = sum over bands of N_band * e(mid(band)), mid by
      uniform-within-band, e by piecewise-linear interpolation on exact-age
      anchors, flat beyond the last anchor
- E3  Transport: dN/dt + dN/da = -mu N ;  de/da = mu e - 1
- E4  Identity: dS/dt = B e(0) - N + N dEbar/dt - sum(excess_deaths * e(a))
      (expected-mortality terms cancel exactly; derivation in METHODOLOGY 4)
- E5  Discrete accounting: S_{t+1} - S_t = B_t e_t(0) - N_t + N_t
      (Ebar_{t+1} - Ebar_t)|revision - Burn_t, with within-year a(x) factors
- E6  Cohort expectancy: e_coh(a, t) = integral_0^inf exp( -integral_0^s
      mu(a+u, t+u) du ) ds  over the projected mortality surface
- E7  Lee-Carter: ln m(x, t) = alpha(x) + beta(x) kappa(t) + eps(x, t);
      kappa(t) = kappa(t-1) + d + xi_t (random walk with drift)
- E8  Stochastic index: dS = f(kappa) dt + sigma(S) dW - J dq, J the shock
      jump (frequency-severity calibrated on 1918/WWII/HIV/COVID), giving
      S(t, T) forward term structure and interval bands
- E9  Error propagation: Var(S) = sum (e(a))^2 Var(N(a)) + (N(a))^2 Var(e(a))
      + covariance terms where sources are shared
- E10 Rebase (gons): balance_i = gons_i / F; rebase multiplies F only;
      shares gons_i / sum(gons) invariant under any F path — O(1), exact
- E11 Largest-remainder allocation: floor to quantum, distribute residual
      quanta by descending fractional part; sum of parts equals total exactly
- E12 Neutrality: wallet value = s_i * MarketCap; d(value)/d(rebase) = 0
      (wealth neutrality); d(s_i)/d(deaths) = 0 (mortality neutrality)

## Part X — Machine-checkable invariants (each maps to a CI test)

- P1  Conservation: sum of balances = M(t) after every operation, exactly
- P2  Share invariance: share vector identical across any rebase sequence
- P3  Reconciliation: sum of country dS = global dS per epoch, exactly
- P4  Immutability: no code path mutates a FINAL print (raises)
- P5  Reproducibility: identical snapshot hashes -> byte-identical outputs
- P6  Identity closure: 52 weekly prints reconcile to the annual E5 identity
      within stated tolerance
- P7  Coverage honesty: measured vs imputed share published on every print
- P8  Interval coverage: backtest realized values fall inside published
      intervals at the stated rate (rung 4 onward)
- P9  Non-negativity and monotone lineage: every published value traces to a
      manifest entry; no orphan numbers
- P10 Correction completeness: every deviation between vintages appears in
      the correction ledger, forward-applied only

## Part XI — Governance, legal, and clarity artifacts (the writing to do)

- Whitepaper outline: (1) the claim — humanity's remaining time as a
  measurable stock (Carey/Vaupel), (2) the index and identity, (3) Mirror
  monetary rule and the two neutrality proofs, (4) why supply is glacial and
  demand is the product, (5) governance as a mechanical rule, (6) the
  Becker 1965 anchor and the saeculum story, (7) risk factors written by
  the harshest critic you can simulate.
- One-pager and FAQ (includes the pre-written response to "you are pricing
  human lives": the VSL/QALY precedent — governments already do, in the
  open, and opacity is worse).
- Glossary: chronon, CHRONON, TLY, saeculum (the annual vintage report), E-bar, mint/spend/drift/burn, epoch, print,
  fixing, vintage, measured vs cohort series.
- Docs site map: home / methodology / data & licenses / API reference /
  changelog / correction ledger / governance / vintage archive.
- IOSCO mapping table: every Principle for Financial Benchmarks row-mapped
  to a SPEC capability or a governance doc; gaps listed with phase numbers.
- Methodology change process: proposal -> public comment window -> version
  bump; model-ensemble weights changeable only through this gate.
- Terms of use and disclaimer (index is information, not advice; no
  warranty), privacy statement (trivially: no personal data anywhere in the
  pipeline — individual-level data never enters, only published aggregates),
  conflict-of-interest statement (you hold SAEC; disclose from day one).
- Entity and IP: TLY/SAECULUM IP held under Praevex initially; a separate
  administrator entity at P5 for benchmark-regulation cleanliness;
  trademark filings per Part III R5.

## Part XII — Ops, security, KPIs

- Runbook: the Monday print procedure, failure ladder (source down -> carry
  rule -> stale flag -> deferred fixing), escalation = you, everything
  rebuilds from repo + snapshots.
- Security: dependencies hash-pinned; artifacts signed (sigstore/cosign);
  branch protection + signed commits; upstream anomaly detection thresholds
  documented (a hash proves what was fetched, not that upstream was sane);
  API is static so the attack surface is the repo and the data, not a server.
- KPIs by phase: P1 — third-party reproductions (target: 3), data citations;
  P2-P4 — backtest bias and interval coverage published; P5 — external
  fixing reproduction without assistance; P6 — audit findings closed,
  testnet rebase feed consumers; commercial — API consumers, data licensing
  conversations, and only then market metrics.

## Completeness statement

This program is category-complete as of 2026-08-16: mathematics, data,
sources, accuracy, infrastructure, governance, legal, licensing, security,
operations, communications, budget, KPIs. No plan enumerates its unknown
unknowns; the mechanism that catches them is the standing protocol (Part VI),
the correction ledger, and the repo issue tracker — discoveries during
execution become versioned additions here, never silent edits.
