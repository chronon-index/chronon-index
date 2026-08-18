# IOSCO Principles for Financial Benchmarks — mapping table

Filled 2026-08-18 from the PRIMARY document: *Principles for Financial
Benchmarks — Final Report*, FR07/13, July 2013 (IOSCOPD415.pdf,
snapshotted `data/snapshots/2026-08-18/`, sha256 in manifest; © IOSCO
2013, all rights reserved — brief excerpts with source stated; the PDF is
excluded from Zenodo redistribution). Principle titles are verbatim; the
Principles chapter is pp. 15–29 of the report. Rule: no row claims
compliance without naming the artifact that evidences it; gaps carry the
phase (P1–P7) that closes them.

Standing context: TLY today is a pre-launch research series with no
administrator entity — one person plus a public repo whose CI is the
computation. Entity-dependent Principles are honest GAPs until the P5
administrator work (RP Part XI).

| # | Principle (verbatim) | Mapped to | Evidence artifact | Gap / phase |
|---|---|---|---|---|
| 1 | Overall Responsibility of the Administrator | Partially: development/determination/operation are repo mechanisms; the accountable administrator ENTITY does not exist | Methodology + registry (`tly/methodology.py`), CI-as-computation (`.github/workflows/print.yml`), archive chain | GAP: administrator entity + accountable oversight function — P5 (RP Part XI entity work) |
| 2 | Oversight of Third Parties | No third parties currently participate in determination; data comes from official statistical agencies (note: the Principle's own carve-out covers Regulated Market/Exchange data sources — ours are analogous public authorities, stated as analogy not equivalence) | `docs/LICENSING.md` (source roles) | GAP when E-14 external recomputers join: written arrangements per (a)–(d) — P5 |
| 3 | Conflicts of Interest for Administrators | Planned disclosure: RP Part XI mandates a conflict-of-interest statement ("you hold SAEC; disclose from day one") | — | GAP: COI statement is D-15 (drafts for counsel); remuneration/segregation clauses moot until an entity exists — P5 |
| 4 | Control Framework for Administrators | Documented, published control framework = the test-suite gates: manifest schema, snapshot immutability, publish gate, licensing gate, P1–P10 invariants | `tests/` (all gates), `tly/publish.py`, `tly/licensing_gate.py` | GAP: whistleblowing mechanism (4c) — needs an entity and a channel — P5 |
| 5 | Internal Oversight | None: a separate oversight committee cannot exist in a one-person project | — | GAP: oversight function with documented terms of reference — P5; interim mitigant: everything is public and externally recomputable |
| 6 | Benchmark Design | Design factors documented: estimator, banding, interpolation, error budget; the Interest (remaining life-years) is demographic, not market-traded | `METHODOLOGY_v0.md`, `tly/error_budget.py`, `docs/METHODOLOGY_CHANGELOG.md` | Ratification pending (A-16) |
| 7 | Data Sufficiency | TLY is a non-transactional index by nature — covered by the Principle's own clause for indices "not designed to represent transactions" whose data reflects what the index measures; inputs are official vital statistics; sufficiency is measured and published per print | P7 coverage block (`tly/baseline.py` coverage_block; `tests/test_p7_coverage.py`) | — (clause fit documented here; keep under review at P5 gap analysis) |
| 8 | Hierarchy of Data Inputs | Published input hierarchy: WPP = licensed source of record; WHO GHO/IHME = triangulation only; feed roles per source; expert judgment excluded from the settlement series by design (measured-period settles) | `docs/LICENSING.md` (roles column), DECISIONS G5, dual-series discipline (`tly/prints.py`, `tly/fixings.py`) | — |
| 9 | Transparency of Benchmark Determinations | Every print publishes: methodology version + policies, per-file input hashes, coverage share, accuracy statement with typed uncertainty; full reproduction instructions; Annex C guidance noted for the P5 gap review | print schema (`tly/prints.py`), `docs/REPRODUCE_FIXING.md`, `docs/API_REFERENCE.md` | — |
| 10 | Periodic Review | Partially: upstream revisions surface via the vintage archive; methodology changes via the governed process; but no SCHEDULED review of whether the Interest/design remains apt | `tly/vintages.py`, `docs/METHODOLOGY_CHANGE_PROCESS.md` | GAP: a documented periodic-review cadence (natural fit: the annual saeculum report) — P5 |
| 11 | Content of the Methodology | (a)–(h) substantially present: definitions (glossary), criteria/procedures (methodology+registry), stress/absent-source procedures = the failure ladder, error handling = correction ledger, limitations = §8 + error budget | `METHODOLOGY_v0.md`, `docs/GLOSSARY.md`, `tly/failure_ladder.py`, `ledger/CORRECTIONS.md` | (f) internal-review frequency: subsumed by GAP at #10 |
| 12 | Changes to the Methodology | Direct hit: proposal → public comment window (14d/7d, pre-P1 shortcut expires at launch) → one-commit version bump; CI-enforced registry pairing | `docs/METHODOLOGY_CHANGE_PROCESS.md`, `tests/test_methodology.py`, `tests/test_version_bump_guard.py` | — |
| 13 | Transition | None: no cessation policy exists | — | GAP (predicted by the skeleton): cessation/transition policy with fall-back guidance — P5, before any settlement product |
| 14 | Submitter Code of Conduct | Self-scoping: "only applicable to a Benchmark based on Submissions" — TLY takes no submissions; all inputs are published official statistics | print provenance shows all inputs | N/A by the Principle's own scope; revisit only if a submission-based input ever enters (methodology bump would flag it) |
| 15 | Internal Controls over Data Collection | Source selection documented and license-verified; collection integrity = sha256 manifests verified before every compute; transmission integrity = offline-only compute over verified snapshots | `tly/snapshot.py` (verify_manifest), `tly/loader.py` (AC-1.5), `docs/LICENSING.md`, network policy in manifests | — |
| 16 | Complaints Procedures | Published complaints channel: the 48h log-only dispute window (permanent record, alters/delays nothing); substantiated disputes resolve via the forward-only correction ledger; records retained forever (immutable git + chain) | `tly/disputes.py`, `ledger/CORRECTIONS.md`, `docs/REPRODUCE_FIXING.md` §7 | Partial GAP: investigation by personnel independent of the subject (16b) impossible solo — P5 |
| 17 | Audits | None: no independent internal or external auditor engaged | — | GAP: external audit — P5/P6 (RP budgets contract audits; index-methodology audit natural at P5); partial interim: E-14 external recomputers independently verify determinations |
| 18 | Audit Trail | Strong: immutable git history, content-hashed snapshot manifests, append-only archive hash chain, append-only journal/ledgers — written records retained indefinitely (≥ the 5-year requirement) | `tests/test_snapshot_immutability.py`, `tly/archive.py`, `loop/JOURNAL.md` | — |
| 19 | Cooperation with Regulatory Authorities | Everything a Regulatory Authority could request is already public by design (radical verifiability); nothing exists to withhold | the public repo + static API + reproduction doc | Formal cooperation procedures follow entity existence — P5 |

## Summary for the P5 gap analysis

Satisfied by architecture today: **7, 8, 9, 11, 12, 15, 18, 19** (+ 14 N/A).
Partial: **1, 4, 6 (ratification), 10, 16**.
Open gaps, all entity-shaped, all P5-phase: oversight function (5),
COI statement (3/D-15), whistleblowing (4c), periodic-review cadence
(10), cessation policy (13), external audit (17), third-party/recomputer
arrangements (2/E-14). This confirms RESEARCH_PROGRAM's sequencing: the
remaining IOSCO distance is the administrator-entity work, not the
computation.
