# TLY Methodology v0.1

Principle: every published figure must be reproducible by anyone, from keyless
public endpoints, by running open code. The script `tly_v0_calc.py` is the
methodology; this document explains it. No number without a source URL and a
runnable path.

## 1. Definition

S(t) = sum over age bands a of N(a, t) x e(a, t)

where N is world population in the band and e is remaining life expectancy at
the band's mean exact age. v0 is a single global aggregate; v1 (see SPEC.md)
computes it per country and week.

## 2. Data sources (all keyless, all public)

- Population by 5-year age band, World, 2023 (8,091,734,933 people):
  Our World in Data grapher CSV, underlying source UN World Population
  Prospects 2024.
  https://ourworldindata.org/grapher/population-by-five-year-age-group
- Crude birth rate, World, 2023 (16.327 per 1,000):
  https://ourworldindata.org/grapher/crude-birth-rate
- Global abridged life table, both sexes, 2000-2021: WHO Global Health
  Observatory OData API, indicator LIFE_0000000035 (ex, expectation of life
  at exact age x), SpatialDim = GLOBAL.
  https://ghoapi.azureedge.net/api/LIFE_0000000035

## 3. Estimator

Band mean age: uniform-within-band (0-4 -> 2.5, ..., 80-84 -> 82.5; open
100+ band -> 101). e at the mean age: piecewise-linear interpolation on the
WHO exact-age anchors {0, 1, 5, 10, ..., 85}; flat at e(85) beyond 85.

Life-table vintage: WHO's latest global table is 2021, a COVID-anomaly year
(e0 = 71.37). WPP 2024 reports world e0 recovered to 73.3 by 2024 - almost
exactly the 2019 table (e0 = 73.12). The 2019 table is therefore primary and
the 2021 table is reported as a lower bound.

Result (population 2023, table 2019):
- S = 362,412,641,743 = 362.4126 billion remaining life-years
- lower bound (2021 table): 348.1905 billion
- E-bar (average remaining years per living person) = 44.7880

## 4. The issuance identity

With age density N(a, t), force of mortality mu(a), births B, and a fixed
life table, two standard identities -

  de/da = mu(a) e(a) - 1          (remaining expectancy along age)
  dN/dt + dN/da = -mu N           (population transport)

- give, integrating by parts with boundary flux N(0) e(0) = B e(0):

  dS/dt = B e(0) - N

The mu terms cancel exactly: expected deaths do not change S because they are
already priced into e(x). The full accounting is therefore

  dS/dt = B e(0)  -  N  +  N dEbar/dt  -  (excess deaths) x e(age at death)
          [mint]   [spend] [table-revision drift]   [shocks only]

- Mint: 132,113,756 births x 73.1234 = +9.6606 B/yr
- Spend: every living person uses one year per year = -8.0917 B/yr
- Drift: table revisions 2015 -> 2019 (pre-COVID window, current population
  weights held fixed) give dEbar/dt = +0.1285/yr -> +1.0394 B/yr
- Net organic growth: +2.6083 B/yr, g = +0.7197% per year

Correction log: an earlier working estimate of +2.9%/yr was wrong twice over -
it omitted the spend term and subtracted GBD YLL (which uses an aspirational
reference table and double-counts against our own e). The open recomputation
caught it. This is the point of the openness rule.

Trajectory: g decays with fertility. WPP 2024 medium variant has population
peaking around 10.3 billion in the mid-2080s; S peaks earlier (the aging of
the pyramid drags E-bar down before headcount turns), then declines - a
built-in demographic halving-and-reversal schedule. Exact peak year is a v1
computation from the WPP projection variants.

## 5. Shock scenarios

Only excess deaths versus the table burn stock. WHO estimates 14.83 million
excess deaths associated with COVID-19 across 2020-2021
(https://www.who.int/news/item/05-05-2022-14.9-million-excess-deaths-were-associated-with-the-covid-19-pandemic-in-2020-and-2021).
Burn = excess x mean e at age of death:

- e at death 10 (older skew):  148.3M life-years = 0.0409% of S
- e at death 12 (central):     178.0M            = 0.0491%
- e at death 15 (younger skew): 222.4M           = 0.0614%
- WHO YLL-paper implied 22.7:  336.6M            = 0.0929%

A century-scale pandemic moves supply by less than a tenth of a percent.
Supply is glacially smooth; essentially all price variance will be
demand-side.

## 6. Wealth-neutrality of rebases (proof)

Let wallet i hold share s_i of supply M(t), so balance b_i = s_i M(t). A
rebase multiplies M by k and every balance by the same k; s_i is unchanged.
Market value of the wallet = s_i x (market capitalization), which contains no
M term. Therefore rebases transfer nothing and create nothing; all holder
returns come from the market price of the share. Deaths never enrich a
holder (mortality neutrality) and longevity gains never dilute one.

## 7. Vision-consistent asymptote

Burger = 15 minutes at $6.00 implies $24.0000/hour, x 8,766 h/yr =
$210,384.00 per life-year. Across S that is a $76.2458 quadrillion
capitalization. Anchor for scale: UBS Global Wealth Report base of USD 454.4T
(end-2022) grown by UBS's published rates (+4.2%, +4.6%, +10.8%) gives ~USD
549T of global personal wealth - the asymptote is ~138.9x all personal wealth
on Earth. The Mirror token requires no particular price to function; the v4
Ledger only pays people more than dust near the asymptote. This is why Mirror
ships first.

## 8. Known limitations (v0), in order of size

1. Period vs cohort expectancy: period tables ignore future mortality
   improvement, understating true cohort remaining years - plausibly +3-8%
   for young cohorts. Scheduled as a v1.x methodology factor (projected
   cohort tables), per the versioned-expansion rule.
2. Population vintage: bands are 2023; at ~+0.9%/yr headcount growth the
   2026 stock is roughly 2-3% above the stated S.
3. Global aggregation: no country split in v0; aggregation error order
   +-1-2%. v1 computes per country.
4. Flat e beyond 85 overstates the 90+ bands' e; those bands are 0.288% of
   population; bias on S < +0.05%.
5. Uniform-within-band mean ages; drift window is pre-COVID by construction;
   shock age-profile is parameterized (three-point sensitivity shown), not
   observed.

## 9. Versioning

- v0.1 = this document + `tly_v0_calc.py` + `results_v0.json`. First-print
  discipline applies from v1.0 onward (see SPEC.md capabilities 3 and 7).
- Changes land only as version bumps with a changelog entry; corrections are
  forward-only. This file's correction log (section 4) is the seed of that
  ledger.

## 10. Extension ladder: v0 to the ceiling

v0 is the minimal defensible estimator. Each rung below is a strict upgrade,
ordered by impact; estimated level effects are working figures, to be
computed when each rung lands.

- Rung 1 (= SPEC v1). Country x sex x single year of age, weekly nowcast.
  Population: WPP2024 single-age files, 237 locations; life tables: WHO GHO
  per country (183), HMD full single-age tables 0-110 for ~40 countries.
  Level correction est. +-1-3%; coverage from one aggregate to per-country
  sub-indices with a reconciliation constraint (country deltas sum to global,
  exactly, in Decimal).
- Rung 2. Old-age closure: replace flat e(85+) with Kannisto/logistic
  extension fit on HMD supercentenarian data. Est. +0.1-0.3%.
- Rung 3. Period -> cohort tables (the biggest single move). Period tables
  freeze today's mortality; cohort tables project each cohort's future
  improvement via Lee-Carter, Cairns-Blake-Dowd, or UN probabilistic
  projections (actuarial practice: CMI model, SOA MP scales). Young cohorts
  gain the most; est. +3-8% on S. From this rung on, the index is partly a
  forecast, not a measurement - acceptable (CPI is also a model) but it must
  enter through the versioned-methodology gate.
- Rung 4. Stochastic S. Model mortality improvement as a stochastic factor
  (Lee-Carter kappa as random walk with drift) plus a jump component for
  pandemics/conflict: S becomes a jump-diffusion with published 80/95%
  intervals and a forward term structure S(t,T) - forward life-years. No
  level change; it creates the variance objects that make v2 derivatives
  (vol, forwards) well-defined.
- Rung 5. Shock nowcast mesh. HMD STMF weekly deaths (~40 countries) plus
  conflict feeds (UCDP, ACLED), pandemic surveillance, famine early warning,
  and ML excess-mortality models for unregistered regions, each with an
  age-at-death distribution per shock type instead of a scalar. Latency for
  covered regions drops from years to days; burn gets cause-attributed
  sub-indices.
- Rung 6. Heterogeneity. Frailty models, socioeconomic mortality gradients
  (top-vs-bottom income percentile differ by ~10+ years in the US), and at
  the limit personalized survival curves (insurer-grade covariates,
  biomarker/epigenetic-clock inputs). Moves the aggregate barely at all;
  transforms the v4 Ledger, where per-person issuance needs per-person e.
- Rung 7. Quality weighting (HALE/QALY). Redefines the unit from life-years
  to healthy-life-years. A governance decision about what the asset measures,
  not an accuracy improvement.

## 11. Hard ceilings no math removes

1. Registration coverage: a large share of world deaths (very roughly 4 in
   10) are never registered; below that floor, "data" is imputation. More
   coverage means more model, not more measurement.
2. Cohort truth is unknowable in real time: any e beyond the period table is
   a forecast and will be revised. Handled by first-print settlement and
   forward-only corrections, never by pretending otherwise.
3. State-published statistics are manipulable. Mitigation is triangulation
   (WPP vs IHME GBD vs national vs HMD) and capped epoch adjustments;
   elimination is impossible.

## 12. Prior art

JPMorgan's LifeMetrics (2007) was an open-methodology longevity index later
transferred to the Life & Longevity Markets Association; the index worked,
the derivatives market died of one-sided demand and basis risk. Lesson
encoded here: the index layer must be self-sustaining as a data product
(v1), and the Mirror token supplies a permissionless second side that swap
markets never had. Academic base: Lee-Carter (1992), Cairns-Blake-Dowd,
UN probabilistic projections, Human Mortality Database.
