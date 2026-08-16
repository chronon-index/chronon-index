# Upstream licensing table

**P1 GATE (RESEARCH_PROGRAM Part VII): every row must reach status CLEARED
before the first public print.** No row may be cleared from memory; each
clearance requires reading the source's current license text and recording
URL + date. All rows start (verify).

| Source | License (as recorded Aug 2026) | Commercial use | Role in TLY | Status |
|---|---|---|---|---|
| UN WPP 2024 | CC BY 3.0 IGO (verify) | OK (verify) | Source of record: population + life tables | (verify) |
| Our World in Data grapher | CC BY 4.0 (verify) | OK (verify) | Clean CSV mirror of WPP series | (verify) |
| WHO GHO / GHE | Non-commercial clause on much content (verify) | PROBLEM for commercial product | Triangulation only — never source of record | (verify) |
| HMD | CC BY 4.0 for HMD-constructed data (User Agreement read+snapshotted 2026-08-17: hmd_user_agreement.html, sha256 in 2026-08-17 manifest); input data excluded from CC BY | OK for constructed data with attribution | Research-grade life tables, exposures | VERIFIED 2026-08-17; access needs free account (HUMAN B-uc2-02) |
| HMD STMF | CC BY 4.0 (STMF outputs are HMD-constructed; same evidence row as HMD) | OK with attribution | Weekly deaths nowcast | VERIFIED 2026-08-17; stmf.csv 302s to /Account/Login — NOT keyless, registration required (HUMAN B-uc2-02); G6 conflict logged |
| World Mortality Dataset (Karlinsky & Kobak) | MIT (LICENSE fetched+snapshotted 2026-08-17: wmd_LICENSE.txt) | OK | Broad excess-death compilation; keyless nowcast feed candidate | VERIFIED 2026-08-17; observed data ends 2024-12 (staleness (verify)) |
| Eurostat weekly deaths | Eurostat standard reuse policy (verify) | OK (verify) | EU nowcast | (verify) |
| CDC provisional deaths | US public domain (verify) | OK (verify) | US nowcast | (verify) |
| UCDP GED | Free for research; terms (verify) | (verify) | Conflict shock feed | (verify) |
| ACLED | Commercial license required (verify) | HUMAN: purchase license | Conflict shock feed | HUMAN |
| EM-DAT | License needed for commercial use (verify) | HUMAN: obtain license | Disaster shock feed | HUMAN |
| Economist excess-mortality model | MIT code; output terms (verify) | (verify) | Imputation layer, labeled as model | (verify) |
| IHME GBD | Free-of-charge non-commercial (verify) | PROBLEM — triangulation only | Cause decomposition, YLL cross-check | (verify) |
| UBS Global Wealth Report | Proprietary report; cite-only (verify) | Citation only, no data redistribution | Wealth denominator context | (verify) |

Change process: a row's status changes only with a link to the license text
and a retrieval date, committed in the same change.
