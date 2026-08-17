# Upstream licensing table

**P1 GATE (RESEARCH_PROGRAM Part VII): every row must reach status CLEARED
before the first public print.** No row may be cleared from memory; each
clearance requires reading the source's current license text and recording
URL + date. All rows start (verify).

| Source | License (as recorded Aug 2026) | Commercial use | Role in TLY | Status |
|---|---|---|---|---|
| UN WPP 2024 | CC BY 3.0 IGO — the UN's own WPP index states it verbatim (wpp_downloads_index.json, snapshotted 2026-08-17) and the CC deed (cc_by_30_igo_deed.html) confirms share/adapt 'for any purpose, even commercially', irrevocable, attribution required | OK, with attribution + citation per UN suggested form | Source of record: population + life tables | CLEARED 2026-08-17 |
| Our World in Data grapher | CC BY for OWID's own charts/articles/data ('unless stated otherwise' — owid_about.html, snapshotted 2026-08-17); third-party data subject to upstream licenses, which for our WPP series is UN CC BY 3.0 IGO (CLEARED above) | OK with attribution; cite both OWID processing and UN source (citation strings are in the snapshotted grapher metadata) | Clean CSV mirror of WPP series | CLEARED 2026-08-17 |
| WHO GHO / GHE | CONFIRMED non-commercial: publications CC BY-NC-SA 3.0 IGO (who_copyright.html); data policy grants 'non-commercial, not-for-profit use... for public health purposes' (who_data-policy.html); both snapshotted 2026-08-17 | NOT usable in a commercial index product — the reason WPP is source of record | Triangulation only — never source of record; v0 research use compatible | VERIFIED-RESTRICTED 2026-08-17 |
| HMD | CC BY 4.0 for constructed data (exposure-to-risk, death rates, life tables); INPUT data 'remain under each provider's distribution license' — never redistribute inputs. Required: HMD acknowledgment, the specified citation form, and noting the download date (our manifest retrieved_utc satisfies this). Evidence: hmd_user_agreement.html | OK for constructed data with attribution + citation; inputs excluded | Research-grade life tables, exposures | CLEARED-CONSTRUCTED-ONLY 2026-08-17; access needs free account (HUMAN B-uc2-02) |
| HMD STMF | CC BY 4.0 (STMF OUTPUTS are HMD-constructed; the agreement offers an STMF-specific citation form); STMF INPUT files (STMFinput.zip) remain under provider licenses — outputs only | OK with attribution + STMF citation | Weekly deaths nowcast | CLEARED-CONSTRUCTED-ONLY 2026-08-17; NOT keyless (302→Login; HUMAN B-uc2-02); G6 conflict logged |
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

Status vocabulary: **(verify)** = recorded from memory, unconfirmed;
**VERIFIED-RESTRICTED** = terms read, source unusable commercially (role
limited accordingly); **CLEARED-CONSTRUCTED-ONLY** = cleared for the
provider's constructed outputs, inputs excluded; **CLEARED** = cleared for
the project's intended use with attribution. HUMAN = license purchase or
account action pending.
