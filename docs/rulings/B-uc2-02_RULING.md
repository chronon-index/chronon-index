# B-uc2-02 — Ruling: option (c), keyless-only. G6 stands unamended.

**Decision.** HMD is removed as a pipeline dependency. No account, no credential,
no manual snapshot, no version gate. Neither (a) nor (b) as framed — both require a
human (a: someone logs in and downloads; b: someone registers and holds a secret).

## Why (a) and (b) both fail the brief
- **(b)** breaks G6 for a marginal gain and adds a rotation/expiry failure mode with no
  monitoring. A read-only account is still a secret in the pipeline.
- **(a)** is worse than it looks. A "periodic manual snapshot" is an unowned recurring
  human task. It decays silently: the vintage goes stale, nothing alerts, and the
  first symptom is a Lee-Carter fit quietly running on 2024 data in 2027.

## Verified state (2026-08-20, from this container)
| Endpoint | Result |
|---|---|
| `mortality.org/File/GetDocument/Public/STMF/Outputs/stmf.csv` | **302 → /Account/Login** |
| `mortality.org/.../all_hmd/hmd_statistics.zip` | **302 → /Account/Login** |
| Eurostat `demo_r_mwk_ts` | 200, keyless, max week 2026-W32 |
| Eurostat `demo_magec` (deaths, 1-yr age) | 200, keyless, 1960–2024, 60 geos |
| Eurostat `demo_pjan` (pop 1 Jan, 1-yr age) | 200, keyless, 1960–2025 |
| CDC SODA `r8kw-7aab` | 200, keyless, weekly to w/e 2026-08-08 |
| UN WPP 2024 complete life tables | 200, keyless, 200 MB gz, 1950–2023 |
| CDC WONDER `datarequest/D176`,`D158` | **403 Access Denied** from datacenter IP |

## Replacement source map
- **STMF weekly → Eurostat `demo_r_mwk_ts` (EU/EFTA) + CDC `r8kw-7aab` (US).**
- **HMD single-age life tables (D-01 / Lee-Carter) → build them.** `demo_magec`
  (deaths by single year of age) + `demo_pjan` (population 1 Jan by single year of age)
  give raw registry Dx and Ex. We do the graduation HMD would have done.
- **Non-Eurostat geographies → UN WPP complete life tables**, explicitly second-tier.

## Validation — the reconstruction is not a downgrade
Reconstructed IT life tables vs Eurostat's independently published ones:

| year | e0 ours | e0 published | Δ | e65 ours | e65 published | Δ |
|---|---|---|---|---|---|---|
| 2018 | 83.1251 | 83.1 | +0.0251 | 20.9908 | 21.0 | −0.0092 |
| 2020 | 82.2444 | 82.2 | +0.0444 | 20.0452 | 20.0 | +0.0452 |
| 2022 | 82.7576 | 82.8 | −0.0424 | 20.5235 | 20.5 | +0.0235 |
| 2024 | 83.6964 | 83.7 | −0.0036 | 21.3802 | 21.4 | −0.0198 |

Max |Δ| = 0.0452 years across 2018–2024, i.e. inside the 1-dp rounding of the
published series. Lee-Carter on IT 1990–2024: drift −2.0330, σ 2.4981, first
component explains 0.9270 of variance. Nothing here needed HMD.

## What we actually give up (state it, don't hide it)
1. **Lexis triangles.** HMD builds exposures from triangles + monthly births;
   Eurostat publishes neither. We use Ex = (P(1 Jan t) + P(1 Jan t+1))/2. Second-order
   bias from cohort-size curvature, material only at age 0 and in the open interval.
   Age-0 is patched by the Andreev–Kingkade a0 rule; the open interval by Kannisto.
2. **Old-age smoothing is now ours.** Implemented as a weighted Kannisto logistic
   fitted from 80 and extrapolated to 110. This is not optional — raw Eurostat rates
   at 95+ are noise-dominated and will detonate Lee-Carter's b_x.
3. **US age detail is gone.** `muzy-jte6`, `y5bj-9g5w`, `u6jv-9ijr`, `xkkf-xrst` were
   all frozen on 2025-04-21. The only live keyless US weekly all-cause feed is
   `r8kw-7aab`, and it carries no age breakdown. US age-specific work runs annual off
   WPP until a live keyless age feed reappears.
4. **Cross-country method consistency.** HMD's real product is a uniform protocol.
   Ours is uniform across Eurostat geos and different for WPP geos. Never pool the two
   tiers inside one Lee-Carter fit.

## Two edge-cases the old backlog note got wrong
- **The EU panel does not run to 2026-W31.** On 2026-08-20, W32 had exactly one
  reporting country (FI); W30 had 2; W27 had 26. Aggregating at the nominal max week
  prints a fabricated ~80% collapse in EU deaths. Cut at `eu_weekly_edge(min_geos=20)`.
- **US weeks backfill for ~8 weeks.** w/e 2026-08-08 printed 23,458 against 48,683 for
  w/e 2026-07-25. Censor the immature tail; do not model it. To ever *correct* rather
  than censor, persist a dated vintage per pull and build the lag triangle — that is a
  prerequisite, not a nice-to-have.

## Follow-ups worth opening
- **Vintage store** for both weekly feeds (append-only, one row per pull date) — the
  only route to chain-ladder backfill correction, and it costs nothing to start now.
- **WONDER is unusable unattended** (403 from cloud IPs). If US single-age annual data
  is required, the candidate is NCHS published life tables, not WONDER.
- **UK**: Eurostat UK coverage stops post-Brexit; ONS is keyless and should be a
  separate adapter rather than a WPP fallback.
