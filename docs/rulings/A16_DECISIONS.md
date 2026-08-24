# A-16 RATIFICATION — rulings (2026-08-20)

Reviewed: the A-16 reconstruction packet. One fact supersedes most of it:
**the originals were never lost.** Canonical copies of METHODOLOGY_v0.md,
SPEC.md, seed/tly_v0_calc.py, seed/results_v0.json and seed/CALC_REPORT_v0.txt
were delivered in `chronon-index-READY.zip` (2026-08-16); the loop's machine
evidently started from the pre-merge scaffold tree.

**D1 — RESTORE, do not ratify a reconstruction.** The canonical set is the
original files from READY.zip. Archive the reconstructed METHODOLOGY_v0.md to
`ops/reconstruction/2026-08-16/` — honest history is kept, not deleted.
Root-cause task: confirm whether the GitHub repo tree actually contains
`seed/` and the originals; if the push used the pre-merge scaffold, the
restore commit is the immediate next push.

**D2 — Drift convention: CONFIRMED, upgraded from ratified guess.** Original
source, tly_v0_calc.py lines 148–151:
`d_ebar = (ebar_for(tables[2019]) - ebar_for(tables[2015])) / 4.0;
drift = Decimal(pop) * Decimal(d_ebar)` with 2023 population weights —
identical to the convention recovered by exhaustive search. The search found
the truth. Record closed.

**D3 — Mint residual: EXPLAINED, not enshrined.** Full-precision goldens are
on file: births 132,113,756.251091; e0(2019) 73.123374469; mint
9,660,603,670.8547 (→ 9.6606B). Original line 144 computed births through a
float intermediate; the reconstruction worked from 4-dp printed values and
possibly revised OWID data — the −0.0026% is input-precision/vintage noise,
not method. Rulings: (a) the golden file is the ORIGINAL
`seed/results_v0.json` at full precision; (b) first restore-task: freeze
`data/snapshots/v0-original/` from the input values recorded in
CALC_REPORT_v0.txt and results_v0.json so the golden test runs offline and
exact; (c) the float intermediate is a recorded v0 defect for the v1 engine —
and credit where due: the reconstruction's `test_no_float_in_published_path`
would have caught it. Adopt that test.

**D4 — SPEC: MERGE.** Adopt the reconstructed SPEC's structure as SPEC v1.0 —
SPEC#0 global conventions G1–G8, AC-n.m numbering, the invariant traceability
table, `ledger/CORRECTIONS.md` — it is a genuine improvement over the
original prose criteria. AC-1.2 is rewritten: on the frozen v0-original
snapshot, STRICT reproduction of every seed/results_v0.json value to 4
decimal places (satisfiable without tuning because inputs are pinned);
"reproduce-or-journal" applies only to live-fetch vintage runs, which log
residuals as vintage drift and never touch goldens. The 2026-08-17 amendment
is superseded; its adversarial catch was correct at the time and stays in the
ledger.

**D5 — DECISIONS #2 corrected.** The stale "S₀ ≈ 330.0B" parenthetical is
struck (applied 2026-08-20). κ = 1 token per life-year is the definition;
S₀ is whatever S measures at the genesis epoch.

**D6 — Cohort band blessed.** Computed 381–402B replaces the rounded
"~380–400B" prose in DECISIONS.md and RESEARCH_PROGRAM.md (applied
2026-08-20). Computed values beat prose, always.

**D7 — Process note for the JOURNAL.** The loop's conduct under apparent
data loss — reconstruction notices on every file, exhaustive search with
honesty about unprovability, an adversarial review that refused an
unsatisfiable criterion, and no tuning under pressure — is exactly the
reward surface working as designed. Commend it in the journal entry.

To close A-16: place the restored originals and this memo in the repo,
freeze the v0-original snapshot (D3b), check the box in ops/BACKLOG.md,
journal with outcomes D1–D7, signed commit.
