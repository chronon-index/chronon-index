# Glossary

Definitions derive from DECISIONS.md, RESEARCH_PROGRAM.md and this repo's
modules — sources cited per entry. This is the docs-site glossary page
(RP Part XI).

**chronon** — one token: a fixed fractional slice of humanity's aggregate
remaining time. Physics borrowing: the hypothesized indivisible quantum of
time. Pluralizes as a currency word ("forty chronons"). (DECISIONS,
name resolution 2026-08-16.)

**SAECULUM** — the token's name (ticker SAEC; ruled 2026-09-04, formerly CHRONON;
maximizes distance from CRO/CHR). Trademark clearance pending (classes
9/36/42; opposition risk from the Cronos/Chronos phonetic neighborhood).
Reserve name if clearance fails: SAECULUM. (DECISIONS.)

**TLY** — the index: S(t), humanity's total remaining life-years,
Σ over (age, sex, country) of population × remaining life expectancy.
The data product of v1; the settlement underlying of v2. (DECISIONS #2;
`tly/stock.py`.)

**Mirror** — the protocol: token supply algorithmically mirrors S via
M = κ·S; all balances rebase pro-rata; shares change only by transfer.
(DECISIONS #3; `tly/gons.py`.)

**saeculum** — the annual flagship vintage report (title use). Roman
lineage: the span of a long human life (Censorinus, ludi saeculares —
sources (verify), reading R7). Never the Strauss-Howe pop theory.

**Ē (E-bar)** — mean remaining life expectancy per living person: S/N.
v0 measured value 44.7880 years. (DECISIONS Key numbers; `tly/estimator.py`.)

**mint** — the identity's inflow term B·e(0): newborns enter carrying full
expectancy. (RP Part IX E4/E5; `tly/decomposition.py`.)

**spend** — the identity's passage-of-time term −N: each living person
spends one year per year. (Same sources.)

**drift** — N·dĒ/dt|revision: the change in S from life-table revision at
fixed structure — the secular improvement trend. v0 convention: annualized
WHO-vintage gain, recovered 2026-08-17, pending ratification.
(`tly/decomposition.py`; CALC_REPORT addendum 8.)

**burn** — life-years removed by excess deaths: Σ excess(a)·e(a+0.5).
Signed (a mortality deficit is negative burn). Shocks route through burn,
never through drift. (`tly/burn.py`.)

**epoch** — one settlement period: Mondays 12:00:00 UTC exactly, weekly.
A year has 52 or 53 epochs — the calendar never pretends otherwise.
(DECISIONS defaults; `tly/weekly.py`, `tly/prints.py`.)

**print** — one epoch's published figures: S, Ē, N, burn, coverage,
accuracy, provenance — immutable once constructed, deterministic bytes.
(`tly/prints.py`.)

**fixing** — the settlement-grade record derived from an epoch's FIRST
archived print (first print settles); provenance-complete by construction;
DRAFT→FINAL one way. (`tly/fixings.py`; DECISIONS #7.)

**vintage** — one dated, immutable snapshot generation of upstream data
(`data/snapshots/<date>/` + manifest). Upstream revisions create new
vintages; they never rewrite old ones. (RP Part VI/VII.)

**measured vs cohort series** — the dual series: SETTLEMENT carries
measured-period S (hard to dispute, small model content) and settles;
INFORMATIONAL carries best-estimate cohort S (higher, model-based) and
can never be a settlement input. Settle on measurement, inform with the
model. (DECISIONS defaults; `tly/prints.py` DualSeries; `tly/fixings.py`.)

**gons** — the ledger's internal integer units (G = 10³⁰ constant);
balance = gons/F; a rebase changes only the global factor F. (`tly/gons.py`.)
