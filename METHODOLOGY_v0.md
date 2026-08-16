# METHODOLOGY_v0.md — TLY v0 mathematics

> **Reconstruction notice.** Reconstructed 2026-08-16 from DECISIONS.md,
> RESEARCH_PROGRAM.md and RALPH_LOOP.md after loss of the original; pending
> Ben's review. The original METHODOLOGY_v0.md, SPEC.md and the seed artifacts
> (`seed/tly_v0_calc.py`, `seed/results_v0.json`, `seed/CALC_REPORT_v0.txt`)
> no longer exist on this machine. Every number below is either (a) reproduced
> verbatim from DECISIONS.md "Key numbers" or ledger/CORRECTIONS.md, (b) an
> arithmetic consequence of those numbers re-verified in Decimal during this
> reconstruction, or (c) marked (verify). Structural conventions of the v0
> estimator that lived only in the lost seed code are reconstructed from the
> formulary (RESEARCH_PROGRAM Part IX) and flagged where the seed was the only
> authority. Nothing here may be treated as ground truth until the seed
> calculator is rebuilt and its output re-anchored.

Companion documents: DECISIONS.md (locked decisions), RESEARCH_PROGRAM.md
(cited below as RP; formulary E1–E12 in Part IX, invariants P1–P10 in Part X,
error budget in Part VIII). Section numbering in this file is load-bearing:
RP cites "METHODOLOGY_v0.md section 4" for the transport-identity derivation
and "METHODOLOGY section 6" for the wealth-neutrality proof. Do not renumber.

---

## 1. Definitions and the v0 estimator

### 1.1 The index quantity

TLY measures humanity's total remaining life-years:

**E1 (RP Part IX):**

    S(t) = Σ_{a,c} N(a, c, t) · e(a, c, t)

where the sum runs over age `a` and cell `c` (sex × country in the full
index), `N(a,c,t)` is the population count of the cell, and `e(a,c,t)` is the
remaining life expectancy at age `a` for that cell at time `t`.

`e` is **period** life expectancy in v0: the expected remaining lifetime if
the mortality rates of the reference table were frozen and experienced
forever. In continuous form, with force of mortality `μ(a)`,

    e(a) = ∫₀^∞ exp( −∫₀^s μ(a+u) du ) ds .

Period expectancy understates the true cohort quantity when mortality is
improving; this is a deliberate conservatism, quantified in section 7 and
addressed by the cohort series at P2 (RP Part IV, E6).

The mean remaining expectancy per living person is

    Ē(t) = S(t) / N(t),   N(t) = Σ_{a,c} N(a,c,t)  (total headcount).

Recorded v0 values (DECISIONS.md Key numbers): **S = 362.4126 B life-years**
on the WHO 2019 global table × WPP 2024 population (348.1905 B on the
COVID-depressed 2021 table), **Ē = 44.7880 years**. Consistency check
performed during this reconstruction, in Decimal (prec 34, ROUND_HALF_EVEN):
S / Ē = 362.4126 / 44.7880 = 8.0917 B persons, which matches the spend term
of the issuance decomposition (section 5) exactly as the identity requires.

### 1.2 The v0 estimator

v0 collapses `c`: one global, both-sexes cell. Population is available by
age **band**, expectancy by **exact-age anchors**, so:

**E2 (RP Part IX):**

    S = Σ_{bands b} N_b · e( mid(b) )

with the following conventions, in order of application:

1. **Uniform-within-band midpoint.** Ages within a closed band
   `[x, x+n)` (in completed years) are assumed uniformly distributed, so the
   band's representative exact age is `mid(b) = x + n/2`.
2. **Piecewise-linear interpolation on exact-age anchors.** The life table
   publishes `e(x)` at exact ages `x ∈ {0, 1, 5, 10, …, 85}` (the WHO
   abridged layout; exact anchor set per the retrieved table — (verify)
   against the rebuilt snapshot). For `x_k ≤ a ≤ x_{k+1}`:

       e(a) = e(x_k) + (a − x_k) · ( e(x_{k+1}) − e(x_k) ) / ( x_{k+1} − x_k )

3. **Flat beyond the last anchor.** For `a ≥ x_last`: `e(a) = e(x_last)`.
   In particular the open-ended population band (85+) evaluates at
   `e(85)` regardless of its assumed interior age distribution, since every
   candidate midpoint lies at or beyond the last anchor. This overstates the
   open band's expectancy slightly (true `e` keeps falling with age); the
   effect is inside the ±0.5 % banding/closure term of section 7.

All estimator arithmetic is Decimal (section 9). The estimator is
deliberately model-free: no smoothing, no projection, no fitted parameters —
every number in E2 is a published input or a linear combination of two of
them. That is what makes v0 disputable only at the level of its sources.

### 1.3 Interfaces to the asset layer

The supply rule (DECISIONS.md #2) is `M(t) = κ·S(t)` with κ = 1 token per
life-year at genesis. This document covers `S`; the mapping from `S` to
balances is section 6. Denomination convention (DECISIONS.md defaults):
1 token = 1 life-year; 1 year = 8,766 h (= 365.25 × 24, re-verified).

---

## 2. v0 data sources

Two inputs, two roles. Full catalog and roadmap: RP Part II. License status
for every source lives in `docs/LICENSING.md` and is a P1 gate — the caveats
are not repeated here.

| Input | Source | Role |
|---|---|---|
| `e(x)` anchors | WHO Global Health Estimates life tables, 2019 global both-sexes abridged table, via the GHO API (verify URL at execution) | The expectancy curve. The 2021 table (COVID-depressed) is computed as a sensitivity, not the headline: 348.1905 B. |
| `N_b` age-band population | UN World Population Prospects 2024, via the Our World in Data grapher CSV mirror (verify URL at execution) | The population structure (2023 vintage structure; see the vintage-lag term, section 7). |

Notes:

- WHO GHO is v0's research-phase expectancy source. For v1 the licensed
  source of record for life tables becomes WPP itself (which publishes them),
  with WHO retained as triangulation only — RP Part VII, mirrored in
  `docs/LICENSING.md`.
- Snapshot-first discipline applies (RALPH_LOOP §6): fetch once into
  `data/snapshots/<date>/` with sha256 manifest, compute offline. The v0
  snapshots must be re-fetched as part of rebuilding the seed calculator;
  until then no figure in this document has a live runnable path, which is
  why the reconstruction notice governs.
- Two-source rule (RP Part VI item 4): the 2019-vs-2021 table pair is the
  v0 instance of "two independent sources for any level claim" — the spread
  (362.4126 vs 348.1905, −3.9 %) is published, not averaged.

---

## 3. Exact discrete-time accounting

The continuous identity of section 4 must be bookable in discrete epochs.

**E5 (RP Part IX):**

    S_{t+1} − S_t = B_t · e_t(0)  −  N_t  +  N_t · (Ē_{t+1} − Ē_t)|revision  −  Burn_t

with within-year `a(x)` separation factors. Term by term:

- **Mint** `B_t·e_t(0)`: births during `[t, t+1)` each enter carrying the
  newborn expectancy of the table in force.
- **Spend** `−N_t`: every person alive spends remaining time at rate exactly
  1 year per year. The exact spend is person-years of exposure,
  `PY_t = ∫_t^{t+1} N(s) ds`, not the start-of-period headcount; the two are
  reconciled with separation factors (below). At v0's stated precision,
  mid-year population is the estimator of `PY_t`.
- **Drift** `N_t·(Ē_{t+1} − Ē_t)|revision`: the change in `S` caused by the
  life table itself being revised (mortality improvement or deterioration),
  weighted by who is alive. The `|revision` qualifier is essential: total
  `dĒ/dt` also contains composition effects (population aging shifts weight
  toward lower `e(a)`), and those are already inside the mint and spend
  terms. Only the table-revision part enters here — section 4.3 makes this
  precise.
- **Burn** `Burn_t = Σ_a D_a^excess · e(a)`: deaths in excess of the table's
  expectation, each removing the expectancy the decedent carried. Expected
  deaths do NOT appear — they cancel exactly (section 4.2). This is the
  single most important structural fact about the index: normal mortality is
  already priced into `e`, so only *surprises* burn.

### 3.1 Within-year separation factors

Deaths inside an interval do not occur at its end. The standard demographic
accounting (Preston, Heuveline & Guillot, life-table chapters — (verify),
per RP Part III R1) writes person-years lived in `[x, x+n)` as

    L_x = n · l_{x+n} + a_x · d_x

where `l` is survivors, `d` deaths in the interval, and `a_x` the average
years lived within the interval by those dying in it. Conventions: interior
ages `a_x = n/2` (uniform deaths); infancy `a_0` well below one half-year,
because infant deaths concentrate near birth (value taken from the source
table where published — (verify)). The same factors time-place flows within
an epoch: births contribute `e(0)` on arrival but only `~half` an epoch of
their own spend; decedents spend `a_x` before their (expected or excess)
exit. v0 is an annual-step calculation and uses these factors implicitly
through the source table's own `L_x` construction; the weekly machinery
below must apply them explicitly.

### 3.2 Weekly-to-annual reconciliation

Epochs are weekly (DECISIONS.md defaults: Monday 12:00 UTC prints). Let
epoch `k` have exact length `h_k` days and weight `w_k = h_k / 365.25`
(convention, versioned). The weekly print books

    ΔS_k = w_k · ( B·e(0) − N + N·ΔĒ|rev )  −  Burn_k

with the flow terms at their current annual rates and `Burn_k` measured from
the epoch's own excess-death feed (v1: HMD STMF; v0 has no weekly feed and
prints the annual identity only). Invariant **P6** (RP Part X): 52 (or 53)
weekly prints must reconcile to the annual E5 identity within the stated
tolerance; the residual (rate-updating between epochs, leap conventions,
late registrations) is published, never silently absorbed. Per-country
accounting must additionally satisfy **P3**: Σ country ΔS = global ΔS,
exactly, in Decimal — the migration convention that makes this exact is
section 4.4.

---

## 4. The transport identity

This section derives, in full, with every step shown:

**E4 (RP Part IX):**

    dS/dt = B·e(0) − N + N·(dĒ/dt)|revision − Σ excess_deaths(a)·e(a)

and demonstrates the exact cancellation of the expected-mortality terms.

### 4.1 Setup

Work in continuous age and time. Let:

- `N(a,t)` — population density at age `a`, time `t` (persons per unit age);
  headcount `N(t) = ∫₀^∞ N(a,t) da`.
- `μ_act(a,t)` — the force of mortality actually experienced.
- `μ_tab(a,t)` — the force of mortality of the reference life table in force
  at `t` (the table from which `e` is computed).
- `B(t)` — births per unit time.
- `e(a,t)` — period remaining expectancy at age `a` under the table at `t`.

**Transport (McKendrick–von Foerster) equation** — E3, first part:

    ∂N/∂t + ∂N/∂a = −μ_act(a,t) · N(a,t)                                (4.1)

**Boundary conditions:**

    N(0,t) = B(t)                       (renewal at age zero)            (4.2)
    lim_{a→∞} N(a,t)·e(a,t) = 0         (closure of the open interval)   (4.3)

(4.3) holds because `N(a,t) → 0` at the maximum attained age ω while `e`
stays bounded; it is the continuous counterpart of closing the life table's
open age group.

**Expectancy gradient** — E3, second part. From
`e(a,t) = ∫₀^∞ exp(−∫₀^s μ_tab(a+u,t) du) ds`, write `l(a) =
exp(−∫₀^a μ_tab)` and `T(a) = ∫_a^∞ l(x) dx`, so `e(a) = T(a)/l(a)`. Then

    ∂e/∂a = ( T'(a)·l(a) − T(a)·l'(a) ) / l(a)²
          = ( −l(a)·l(a) − T(a)·(−μ_tab·l(a)) ) / l(a)²
          = −1 + μ_tab(a,t)·e(a,t)

i.e.

    ∂e/∂a = μ_tab·e − 1                                                  (4.4)

Interpretation: as a survivor ages, expectancy falls at rate 1 (the spend)
but is pushed up by `μ_tab·e` — the selection effect of having survived an
instant of hazard. **Note carefully**: (4.4) carries the *table* hazard
`μ_tab`, because `e` is a table quantity; (4.1) carries the *actual* hazard
`μ_act`. Keeping the two distinct is what makes the excess-burn term appear
and the expected terms cancel.

### 4.2 The derivation

`S(t) = ∫₀^∞ N(a,t)·e(a,t) da`. Differentiate under the integral:

    dS/dt = ∫₀^∞ [ (∂N/∂t)·e + N·(∂e/∂t) ] da                            (4.5)

**Step 1 — substitute the transport equation.** From (4.1),
`∂N/∂t = −∂N/∂a − μ_act·N`:

    dS/dt = ∫₀^∞ ( −∂N/∂a )·e da  −  ∫₀^∞ μ_act·N·e da  +  ∫₀^∞ N·(∂e/∂t) da   (4.6)

**Step 2 — integrate the first term by parts.**

    ∫₀^∞ (−∂N/∂a)·e da = [ −N·e ]₀^∞ + ∫₀^∞ N·(∂e/∂a) da

By boundary condition (4.3) the upper limit vanishes; by (4.2) the lower
limit contributes `+N(0,t)·e(0,t) = B(t)·e(0,t)`:

    ∫₀^∞ (−∂N/∂a)·e da = B·e(0)  +  ∫₀^∞ N·(∂e/∂a) da                    (4.7)

**Step 3 — substitute the expectancy gradient.** From (4.4):

    ∫₀^∞ N·(∂e/∂a) da = ∫₀^∞ N·( μ_tab·e − 1 ) da
                       = ∫₀^∞ μ_tab·N·e da  −  N(t)                      (4.8)

**Step 4 — assemble.** Insert (4.7)–(4.8) into (4.6):

    dS/dt = B·e(0)
            + ∫₀^∞ μ_tab·N·e da        ← selection term, from the e-gradient
            − N(t)                     ← spend term
            − ∫₀^∞ μ_act·N·e da        ← removal term, from actual deaths
            + ∫₀^∞ N·(∂e/∂t) da        ← table-revision term

**Step 5 — the exact cancellation.** Combine the two hazard integrals:

    ∫₀^∞ μ_tab·N·e da − ∫₀^∞ μ_act·N·e da = − ∫₀^∞ (μ_act − μ_tab)·N·e da

Define excess mortality `μ_exc(a,t) = μ_act(a,t) − μ_tab(a,t)` and the
excess death density `D^exc(a,t) = μ_exc(a,t)·N(a,t)`. Then:

    dS/dt = B·e(0) − N + ∫₀^∞ N·(∂e/∂t) da − ∫₀^∞ D^exc(a,t)·e(a,t) da   (4.9)

When mortality follows the table exactly (`μ_act ≡ μ_tab`), the hazard
integrals cancel **identically — pointwise in age, before integration, with
no approximation**. Expected deaths never appear in `dS/dt`. This is not a
modeling choice; it is forced by the algebra: the life-years a decedent
"removes" (`μ·N·e`) are exactly the life-years the table had already
scheduled to melt out of survivors' expectancies (`μ·e` inside `∂e/∂a`).
Only mortality that the table did not price — `μ_exc` — burns.

### 4.3 The revision term, made precise

Define the population-weighted table revision rate

    (dĒ/dt)|revision ≡ (1/N(t)) · ∫₀^∞ N(a,t) · (∂e/∂t)(a,t) da

— the partial time-derivative of `e` at *fixed age*, i.e. pure table
revision, weighted by who is alive. With this definition (4.9) is exactly E4:

    dS/dt = B·e(0) − N + N·(dĒ/dt)|revision − ∫₀^∞ D^exc(a)·e(a) da

The qualifier matters: the total derivative `dĒ/dt` of `Ē = S/N` also
contains composition change (aging shifts population weight down the `e(a)`
curve), and that composition change is already carried by the `B·e(0) − N`
transport terms. Booking total `dĒ/dt` here would double-count aging — the
precise error behind the +2.9 % napkin figure (section 8).

### 4.4 Migration and per-country accounting

The global identity (4.9) has no migration term: the world is closed. For
country `c` the transport equation gains a source density:

    ∂N_c/∂t + ∂N_c/∂a = −μ_act,c·N_c + m_c(a,t)                         (4.10)

where `m_c(a,t)` is net in-migration (persons per unit age per unit time;
negative for net emigration). `m_c` passes through Steps 1–5 untouched by
the integration by parts (it carries no age-derivative), adding linearly:

    dS_c/dt = B_c·e_c(0) − N_c + N_c·(dĒ_c/dt)|rev − ∫ D_c^exc·e_c da
              + ∫₀^∞ m_c(a,t)·e_c(a,t) da                               (4.11)

**Reconciliation (invariant P3).** Closedness gives `Σ_c m_c(a,t) = 0` at
every age (headcount flows cancel), but `Σ_c ∫ m_c·e_c da ≠ 0` in general:
a migrant leaves valued at the *origin's* table and arrives valued at the
*destination's*, so a move from `o` to `d` at age `a` adds
`e_d(a) − e_o(a)` to the summed stock. Under E1 the global stock is
*defined* as `S = Σ_c S_c` (per-country tables), so `Σ_c dS_c = dS` holds
by definition — the reconciliation risk is not the total but the
*attribution*: migration revaluation silently landing inside drift or burn.
Convention adopted: each epoch books an explicit **migration revaluation
line** `R_mig = Σ_moves (e_d(a) − e_o(a))` (per country in-and-out, summed
globally), and the reconciliation test asserts, exactly, in Decimal,

    Σ_c [ demographic terms of (4.11) ]  +  R_mig  =  dS

i.e. the summed migration terms of (4.11) must equal the published `R_mig`
to the last digit, and the demographically-closed part of the world identity
(`B·e(0) − N + drift − burn`, summed over countries) must account for all
the rest. The revaluation is published, not smeared into drift. (Reconstructed
convention — the lost seed had no per-country accounting; v0 is global-only.
This subsection specifies the v1 requirement per RP Part I M1. Pending
Ben's review.)

### 4.5 What the identity buys

- **Interpretability of issuance**: section 5's mint/spend/drift language is
  (4.9) term by term.
- **Shock accounting**: a pandemic enters only through `D^exc·e(a)` — hence
  the recorded COVID sizing (WHO 14.83 M excess deaths → 148–337 M
  life-years, −0.04 % to −0.09 % of S; DECISIONS.md Key numbers). Supply is
  glacially smooth because expected mortality cancels.
- **Auditability**: E5 is (4.9) integrated over an epoch; P6 checks the
  books; P3 checks the geography.

---

## 5. Organic issuance decomposition

Recorded values (DECISIONS.md Key numbers, computed values recorded there,
reproduced by `seed/tly_v0_calc.py` — the seed is lost; the runnable path
must be rebuilt before these figures are re-published):

    g = +0.7197 %/yr
    mint   B·e(0)              = +9.6606 B life-years/yr
    spend  −N                  = −8.0917 B life-years/yr
    drift  N·(dĒ/dt)|revision  = +1.0394 B life-years/yr

Arithmetic re-verified during this reconstruction in Decimal (prec 34,
ROUND_HALF_EVEN):

    net flow = 9.6606 − 8.0917 + 1.0394 = +2.6083 B life-years/yr
    g = 2.6083 / 362.4126 = 0.0071970…  → +0.7197 %/yr   ✓ matches record
    S / Ē = 362.4126 / 44.7880 = 8.0917 B                ✓ spend = headcount, as the identity requires

Per-term contribution to g: mint +2.6656 %/yr, spend −2.2327 %/yr, drift
+0.2868 %/yr (derived here from the recorded values). Implied consistency
notes, not published figures: mint/e(0) with the table's newborn expectancy
(≈ 73 years (verify)) implies ≈ 132 M births/yr, WPP-scale (verify); drift
implies the table-revision component of Ē rising ≈ 0.128 yr/yr (verify
against the rebuilt calculator).

Trajectory (DECISIONS.md): g decays with fertility; population peaks
≈ 10.3 B mid-2080s (WPP 2024), and S peaks *earlier* than headcount because
aging drags Ē down before the headcount turns. In identity terms: the mint
shrinks with falling births while the spend keeps growing with N, so the net
flow crosses zero while headcount is still rising.

---

## 6. Neutrality proofs

The two monetary-rule guarantees of the Mirror protocol (DECISIONS.md #3,
#4), stated and proved. Both are the machine-checkable properties of RP
Part X: **P2 (share invariance)** and **P1 (conservation)** are their test
forms, named verbatim in the SPEC capability-5 suite (RP Part I M4).

### 6.1 The gons representation (E10)

- Each wallet `i` holds an integer gons count `G_i ≥ 0`. `G = Σ_i G_i`.
- `G_i` changes **only by transfer** (which moves gons between wallets and
  conserves `G`). No protocol operation other than transfer touches any
  `G_i`, and none touches `G`.
- A global scale factor `F > 0` maps gons to balances:
  `balance_i = G_i / F`, total supply `M = G / F`.
- A **rebase** is the map `R_λ : F ↦ λF` with `λ > 0`, leaving every `G_i`
  fixed. To track the supply rule `M(t) = κ·S(t)`, the protocol applies the
  rebase with `λ = S_old / S_new` each epoch (so `M_new = κ·S_new`). This is
  O(1) regardless of wallet count: one stored scalar changes.

### 6.2 Lemma — share invariance (E10, invariant P2)

**Claim.** `s_i ≡ balance_i / M = G_i / G`, independent of `F`; hence the
share vector `(s_1, …, s_n)` is invariant under any finite sequence of
rebases `R_{λ1}, …, R_{λk}`, in any order, exactly.

**Proof.** `s_i = (G_i/F) / (G/F) = G_i/G`; `F` cancels identically, so
`s_i` does not depend on `F` at all. A rebase changes only `F`
(`F ↦ F·Πλ_j` after the sequence) and no `G_i`, so `s_i' = G_i/G = s_i`.
The statement is exact — it is a cancellation in the definition, not a
limit: no arithmetic on `s_i` is ever performed, and the integers `G_i, G`
are untouched. ∎

Corollary: a wallet's share changes **only by transfer** — the DECISIONS.md
#3 statement "a wallet's share of supply changes only by transfer, never by
demographics" is this lemma.

### 6.3 Theorem — wealth neutrality (E12)

**Claim.** Let `P` be the market price per token and `C = M·P` the market
cap. Then wallet value satisfies `V_i = s_i · C`, and therefore
`∂V_i/∂(rebase) = 0` holding `C` fixed: no rebase, and no sequence of
rebases, changes any wallet's value at a given market cap, and no rebase
ever redistributes value between wallets.

**Proof.**

    V_i = balance_i · P = (s_i · M) · P = s_i · (M·P) = s_i · C .

By Lemma 6.2, `s_i` is invariant under any rebase sequence. Hence `V_i`
depends on the rebase path only through `C`: for fixed `C`,
`V_i = s_i·C` is constant, i.e. `dV_i/d(rebase)|_C = 0`. Furthermore, for
*any* market-cap path whatsoever, `V_i / V_j = s_i / s_j` is
rebase-invariant, so relative wealth is untouchable by rebases. ∎

**Reading.** A rebase relabels the unit; it cannot move value between
holders. Any change in `V_i` coincident with a rebase is a change in `C` —
a demand phenomenon, priced by the market — never a mechanical transfer.
Hence (DECISIONS.md Key numbers): mortality never enriches a holder,
longevity never dilutes one. The theorem is conditional exactly where it
should be: the protocol guarantees the distribution; the market determines
the level.

### 6.4 Theorem — mortality neutrality (E12)

**Claim.** Under the supply rule `M = κ·S` implemented by symmetric
down-rebase (DECISIONS.md #4), deaths change no wallet's share:
`d(s_i)/d(deaths) = 0` for every `i`.

**Proof.** A mortality shock removes `ΔS = Σ_a D_a^exc·e(a) > 0` from the
stock (section 4.2), so the target supply falls to `M' = κ·(S − ΔS)`. The
protocol implements this **only** through the rebase `R_λ` with
`λ = S/(S−ΔS) > 1` (equivalently `F' = G / (κ(S−ΔS))`): every balance is
scaled by the same factor `M'/M = (S−ΔS)/S < 1`, and no `G_i` is touched —
by construction the protocol has no other channel; there is no
wallet-selective seizure, exclusion, or bonus. By Lemma 6.2,
`s_i' = G_i/G = s_i`. Since this holds for every shock size `ΔS`,
`d(s_i)/d(deaths) = 0`. Combined with Theorem 6.3, `V_i = s_i·C` with
`s_i` death-invariant: nobody's *share* of the asset grows because others
died; any value change routes through `C` alone. ∎

This is the design content of "symmetric down-rebase": symmetry (one global
`λ` for all wallets) is precisely the property that makes Lemma 6.2
applicable. An asymmetric implementation — burning specific wallets — would
break the lemma's premise and with it both theorems.

### 6.5 Exactness domain and the display layer

Both proofs are exact in the integer gons domain. Displayed balances are a
quantized image of `G_i/F` and must round; the display layer uses
largest-remainder allocation (**E11**): floor every balance to the display
quantum, then distribute the remaining quanta by descending fractional part,
so that Σ displayed balances = M exactly (conservation, **P1**) with no
wallet mis-rounded by more than one quantum. Overflow and fixed-point
precision analysis for the on-chain form is SPEC capability-5 work (RP Part
I M4), out of v0 scope. The CI test forms:

- **P1**: Σ balances = M(t) after every operation, exactly.
- **P2**: share vector byte-identical across randomized rebase sequences.

---

## 7. Error budget

Reproduced faithfully from RP Part VIII; it is the v0 accuracy statement and
travels with every quotation of S.

**Propagation rule.** For independent inputs,
`Var(S) = Σ (∂S/∂x_i)² Var(x_i)`, with sensitivities `∂S/∂N(a) = e(a)` and
`∂S/∂e(a) = N(a)` (this is E9; covariance terms where sources are shared).
Symmetric terms combine in quadrature; one-sided biases are listed, never
netted.

**Symmetric (measurement) terms on the v0 level:**

| Term | Size |
|---|---|
| Population level and age structure (WPP estimate error, world aggregate; worse where registration is weak) | ~ ±1.0 % |
| Life-table level (global Ē from an estimated table) | ~ ±1.0–1.5 % |
| Banding, interpolation, old-age closure | ~ ±0.5 % |
| **Quadrature total** | **~ ±2 %** |

**One-sided (structural) terms — listed, never netted:**

| Term | Size | Direction |
|---|---|---|
| Vintage lag (2023 structure, 2026 today) | +2 to +3 % | true stock higher |
| Period vs cohort expectancy | +3 to +8 % | true cohort stock higher |

**The honest v0 statement, to appear wherever S is quoted (verbatim from RP
Part VIII):**

> "Measured-period S = 362.4B +- ~2% on 2023 structure; best-estimate current
> cohort stock ~ 380-400B."

Design decision recorded there (proposed default): publish a **dual series**
from P2 onward — settlement settles on the conservative measured-period S
(small model content, hard to dispute); the best-estimate cohort S with
intervals is published alongside as informational. Settle on measurement,
inform with the model. From rung 4, every print carries a Monte Carlo
interval and this deterministic budget retires.

---

## 8. Limitations and correction log

### 8.1 Correction C-0001 — the +2.9 % napkin error

The earliest issuance estimate was **g = +2.9 %/yr**. It was wrong, for two
compounding reasons (ledger/CORRECTIONS.md C-0001; DECISIONS.md Key
numbers):

1. **It omitted the aging spend term** — the `−N` of the identity: every
   living person burns one life-year per year. In section 4.3's language, it
   booked expectancy gains without the transport terms that offset them,
   double-counting the composition side.
2. **It misused GBD YLL**, whose years-of-life-lost are computed against an
   *aspirational* reference table, not the population's own table — a
   category error for this identity (the same trap flagged for IHME data in
   RP Part II D2).

Open recomputation via the full identity corrected it to **g = +0.7197 %/yr**
(mint +9.6606 B, spend −8.0917 B, drift +1.0394 B). Forward treatment: none
needed — the error predates all prints. It is logged because the openness
rule caught it, and that is the point of the rule. All corrections are
forward-only, per DECISIONS.md #7 and the ledger's standing rules.

### 8.2 Known v0 limitations

1. **Period, not cohort.** v0's `e` freezes today's mortality; with secular
   improvement the true cohort stock is +3–8 % higher (section 7). Cohort
   series arrives at P2 via E6 with the Lee-Carter machinery (RP Part I
   M2), gated on the 1990-vintage backtest.
2. **Vintage lag.** 2023 population structure quoted in 2026: +2–3 %
   one-sided. Cured by nowcasting (SPEC capability 2) and WPP revisions —
   which will themselves restate levels; first-print discipline plus the
   vintage archive turns restatements into product (RP Part V item 7).
3. **Global single cell.** No country/sex resolution in v0; E1's full sum,
   per-country reconciliation (P3) and the migration revaluation line
   (section 4.4) are v1 scope.
4. **Banding and closure.** Abridged anchors, linear interpolation, flat
   extrapolation past the last anchor (which overvalues the open band
   slightly); inside the ±0.5 % term. Monotone cubic Hermite is the flagged
   candidate replacement (RP Part I M5), adoptable only as a versioned
   methodology change.
5. **Deterministic.** No intervals in v0; the section-7 budget stands in
   until stochastic S (RP Part I M3) at P3.
6. **Source licensing.** WHO GHO carries a non-commercial caveat (verify) —
   acceptable for v0 research, resolved for v1 by making WPP the source of
   record (`docs/LICENSING.md`, P1 gate).
7. **Genesis constant.** DECISIONS.md #2 records κ = 1 token/life-year at
   genesis with "S₀ ≈ 330.0B", while the Key numbers record
   S = 362.4126 B; both figures appear in DECISIONS.md as written. Noted
   here without reconciliation (RALPH_LOOP §6 forbids silent
   reconciliation): S₀ is fixed at the genesis print, and the discrepancy is
   flagged for Ben's review.
8. **Reconstruction status.** Until `seed/tly_v0_calc.py` is rebuilt and
   re-anchored against fresh snapshots, the figures herein are recorded
   values without a live runnable path — a standing violation of the
   radical-verifiability rule (DECISIONS.md #9) that must be cured before
   any figure is re-published. Rebuilding the seed is therefore the highest
   priority backlog item after this reconstruction.

---

## 9. Numerical standards

1. **Decimal arithmetic.** Everything supply- or index-adjacent computes in
   Python `decimal.Decimal`, precision 34, ROUND_HALF_EVEN. Floats never
   touch published numbers; float inputs are quarantined at the parse
   boundary (convert-on-read, then Decimal-only).
2. **Interpolation policy (versioned).** v0: piecewise-linear on exact-age
   `e(x)` anchors, flat beyond the last anchor, uniform-within-band
   midpoints (section 1.2). Any change — including the monotone-Hermite
   candidate — is a methodology version bump with changelog, never a silent
   edit (RP Part XI change process).
3. **Reproducibility.** Snapshot-first: source URL + retrieval timestamp +
   sha256 recorded in `data/snapshots/<date>/manifest.json`; computation
   runs offline from the snapshot; identical snapshot hashes must yield
   byte-identical outputs (invariant P5, a CI gate). Deterministic seeds for
   any Monte Carlo (from P3). Every published value traces to a manifest
   entry (P9); a number without an interval is a convention and is labeled
   as one (RP Part VI).
4. **Immutability.** Published prints are immutable; corrections are
   forward-only via `ledger/CORRECTIONS.md` (P4, P10). This document itself
   changes only by version bump.

---

*METHODOLOGY_v0.md — reconstructed 2026-08-16; pending Ben's review and
re-anchoring against a rebuilt `seed/tly_v0_calc.py`.*
