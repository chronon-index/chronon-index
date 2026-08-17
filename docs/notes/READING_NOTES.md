# Reading notes — R1–R7 templates (D-11)

Rule (RALPH §5 Phase D, verbatim in spirit): **never write summaries of
papers you have not read — fetch and read first, or leave the slot
empty.** Every entry below starts UNREAD with an empty summary. Citations
are transcribed from RESEARCH_PROGRAM Part III (the repo's own reading
list) and carry (verify) until the actual work is fetched — RP itself
warns its records must be re-checked at execution time.

Entry format on completing a reading (HUMAN, or an iteration that fetched
and actually read the text):

```
Status: READ <date> | Source: <URL or edition, fetched/owned>
Summary: <yours, from the text>
Key results for TLY: <what changes in this repo because of it>
```

## R1 — Foundations (est. 3–4 weeks part-time)

- Preston, Heuveline & Guillot, *Demography: Measuring and Modeling
  Population Processes* (verify) — Status: UNREAD. Summary: (empty).
  Note: THE textbook; do the life-table and decomposition exercises.
- Keyfitz & Caswell, *Applied Mathematical Demography* (verify) —
  Status: UNREAD. Summary: (empty). Note: the transport identity's
  natural habitat — read against METHODOLOGY_v0.md §4.
- Wachter, *Essential Demographic Methods* (verify) — Status: UNREAD.
  Summary: (empty).
- Vaupel 2009, "Life lived and left: Carey's equality", Demographic
  Research 20(3): 7-10, DOI 10.4054/DemRes.2009.20.3 —
  Status: READ 2026-08-17 | Source: demographic-research.org open access,
  snapshotted (vaupel_2009_life_lived_and_left.pdf; CC BY-NC 2.0 DE — NC:
  excluded from Zenodo deposits).
  Summary: In a STATIONARY population the age composition equals the
  distribution of remaining lifespans: c(a) = g(a) — a randomly chosen
  individual is as likely to have lived a years as to have exactly a
  years left. Four-line proof: c(a) = ℓ(a)/e(0); the death-in-n-years
  density given age a is μ(a+n)ℓ(a+n)/ℓ(a); integrating over the
  population gives g(n) = ℓ(n)/e(0) = c(n). Corollaries: mean age equals
  mean remaining lifespan (∫a·c = ∫a·g), and via Goldstein's companion
  result (DemRes 20(2)) both equal mean remaining life EXPECTANCY
  ∫e(a)c(a)da. Concept due to Carey's medfly work (Müller et al. 2004,
  2007 — estimating age structure from residual lifespans of individuals
  of unknown age); also derivable from renewal theory (Cox 1962).
  Striking application: in the US 2005 lifetable >48% of individuals are
  41+, i.e. nearly half the stationary population is still alive in 2050.
  Key results for TLY: (1) this is the correct citation and content for
  the whitepaper §1 claim "a population's past mirrors its future" — but
  it holds EXACTLY only in stationary populations; the estimator rightly
  computes Σ N(a)·e(a) directly instead of assuming stationarity. (2) The
  Goldstein/Vaupel identity means: in a stationary world our Ē would
  equal the population's mean age; in the real world Ē = 44.79 vs world
  mean age ≈ low 30s — that gap is a clean, citable measure of how
  non-stationary (young + still-improving) humanity is; belongs in
  whitepaper §1 as the honest caveat. (3) Müller et al.'s statistical
  adjustments for non-stationary populations are the thread to pull if a
  residual-demography cross-check of S is ever wanted.

## R2 — Mortality modeling (est. 2–3 weeks)

- Lee & Carter 1992 (JASA) (verify) — Status: UNREAD. Summary: (empty).
  Note: gates C-uc6-03's replication targets.
- Cairns, Blake & Dowd 2006 (JRI) (verify) — Status: UNREAD. Summary: (empty).
- Renshaw & Haberman 2006 (verify) — Status: UNREAD. Summary: (empty).
- Plat 2009 (verify) — Status: UNREAD. Summary: (empty).
- Cairns et al. 2009, eight-model comparison (NAAJ) (verify) — Status:
  UNREAD. Summary: (empty). Note: its backtest protocol is adopted by
  C-uc6-04 — read before running the 1990-vintage backtest.
- Raftery et al., Bayesian population projections (PNAS) (verify) —
  Status: UNREAD. Summary: (empty). Note: our upstream's machinery.
- Barbi et al. 2018 (Science) + responses (verify) — Status: UNREAD.
  Summary: (empty). Note: the plateau debate; affects old-age closure.

## R3 — Longevity markets (est. 1–2 weeks)

- Blake, Cairns, Dowd, MacMinn, "The New Life Market" (JRI 2013) (verify)
  — Status: UNREAD. Summary: (empty).
- Loeys et al., "Longevity: a market in the making" (JPMorgan 2007)
  (verify) — Status: UNREAD. Summary: (empty).
- Wang 2000, the Wang transform (verify) — Status: UNREAD. Summary: (empty).
- OWN WORK, blocked on the above: the LifeMetrics/LLMA failure postmortem
  (one-sided demand, basis risk, no retail leg) — gates whitepaper §4.

## R4 — Index governance (est. 1 week; before any settlement product)

- IOSCO Principles for Financial Benchmarks 2013 (verify) — Status:
  UNREAD (fetch BLOCKED: site 403s curl — see D-06b). Summary: (empty).
- EU Benchmark Regulation 2016/1011 + third-country regime (verify) —
  Status: UNREAD. Summary: (empty).
- The Wheatley Review of LIBOR (verify) — Status: UNREAD. Summary:
  (empty). Note: the manipulation case study our dispute/fixing design
  already gestures at — read to check the design against the record.

## R5 — Token and securities law (est. 1–2 weeks; WITH COUNSEL)

- MiCA final Level 2 texts + ESMA guidance (verify) — Status: UNREAD.
  Summary: (empty).
- Howey line + CFTC/Kalshi event-contract cases (verify) — Status:
  UNREAD. Summary: (empty).
- Jurisdiction memo inputs (FINMA/Zug vs Cayman vs UK) (verify) —
  Status: UNREAD. Summary: (empty). HUMAN: counsel engagement.

## R6 — Mechanism design precedents (est. 3–4 days)

- Ampleforth docs + audits (verify) — Status: UNREAD. Summary: (empty).
  Note: our gons engine follows its pattern — read to confirm divergences
  are deliberate.
- Basis Cash + Terra postmortems (verify) — Status: UNREAD. Summary: (empty).
- Worldcoin PoP papers + critiques (verify) — Status: UNREAD. Summary:
  (empty). Note: gates the v4 Ledger PoP decision.
- Circles UBI postmortem; Chilean UF history; Fureai kippu studies;
  Ithaca HOURS (verify) — Status: UNREAD. Summary: (empty).

## R7 — Positioning and philosophy (est. 2–3 days)

- Becker 1965, "A Theory of the Allocation of Time" (verify) — Status:
  UNREAD. Summary: (empty). Note: gates whitepaper §6.
- Censorinus / ludi saeculares sources (verify) — Status: UNREAD.
  Summary: (empty). Note: branding footnote only for Strauss-Howe; never
  load-bearing.
