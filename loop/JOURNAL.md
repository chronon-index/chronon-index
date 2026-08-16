# loop/JOURNAL.md — append-only iteration journal

One entry per iteration: `## <iso-datetime> | <task-id> | DONE|BLOCKED|PARTIAL`
then 3–6 lines. Never edit or delete old entries. The first four entries
record what the 2026-08-16 bootstrap session actually did, at the real
timestamps, before the loop existed.

## 2026-08-16T18:19:45+02:00 | A-01..A-07 | DONE
- Scaffold commit 27e4dac (15 files, 1163 insertions): governing docs
  (DECISIONS.md, RESEARCH_PROGRAM.md, RALPH_LOOP.md), pyproject + tly/
  skeleton, ci.yml + print.yml (print job honestly labeled not-official until
  SPEC#4), pre-commit config, Apache-2.0 LICENSE + README (docs CC BY 4.0),
  docs/LICENSING.md (all rows (verify); ACLED/EM-DAT HUMAN), ledger/CORRECTIONS.md with C-0001.
- Verifier: files on disk + `git show --stat 27e4dac`.
- The original SPEC.md, METHODOLOGY_v0.md and seed/ artifacts were not
  recoverable from disk anywhere; reconstruction follows in A-08..A-10.

## 2026-08-16T18:25:00+02:00 | A-08 | DONE
- SPEC.md reconstructed from DECISIONS.md + RESEARCH_PROGRAM.md +
  RALPH_LOOP.md; reconstruction note in the header; pending Ben's review (A-16).
- Seven capabilities with AC-n.m acceptance criteria, global conventions
  G1–G8, and the P1–P10 / gates traceability table.
- Verifier: document task — cross-read against the three surviving governing
  docs; lost-anchor figures taken only from DECISIONS.md "Key numbers".

## 2026-08-16T18:28:00+02:00 | A-09 | DONE
- METHODOLOGY_v0.md reconstructed with reconstruction notice; section
  numbering kept load-bearing (RP cites METH §4 transport identity, §6
  wealth-neutrality proof — do not renumber).
- Every number is (a) verbatim from DECISIONS.md/CORRECTIONS.md, (b) a
  Decimal-reverified arithmetic consequence, or (c) marked (verify).
- Pending Ben's ratification (A-16); not ground truth until re-anchored.

## 2026-08-16T18:31:00+02:00 | A-10 | DONE
- Reconstructed seed/tly_v0_calc.py (Python 3.12, stdlib, Decimal prec 34),
  snapshot data/snapshots/2026-08-16/ (6 requests, UA, manifest with sha256 +
  URL + timestamp per file), seed/results_v0.json, seed/CALC_REPORT_v0.txt,
  tests/test_golden.py.
- Verifier: pytest 2 passed; offline recompute run twice, byte-identical (P5).
- Achieved vs target (CALC_REPORT §3): S 362.4126B (2019) / 348.1905B (2021),
  E-bar 44.7880, N 8.0917B, spend −8.0917B all exact at 4 dp; mint 9.6603B vs
  target 9.6606B (−0.0026%, hypotheses h1–h3 recorded unverified); drift
  +1.0394B and g +0.7197%/yr NOT REPRODUCED — need the vintage-pair
  convention lost with the original METHODOLOGY (backlog B-uc1-12).

## 2026-08-16T18:40:00+02:00 | A-11 | DONE
- Iteration 0 (RALPH_LOOP §4): created loop/BACKLOG.md (118 tasks, phases
  A–E, deps + refs per line, 13 HUMAN tasks incl. ratification A-16),
  loop/JOURNAL.md, loop/LEARNINGS.md (§6 hard rules verbatim + gotchas).
- Every [x] in Phase A verified against the filesystem/git this iteration;
  noted: pre-commit hooks NOT installed (A-15 open), tly/ holds only
  __init__.py (port is A-12/A-13), CI has never run (no remote, A-17 HUMAN).
- Verifier: full suite re-run this iteration — 2 passed
  (`~/.venvs/main/bin/python -m pytest -q`).
- Next iteration: A-12 (port seed parsers + Decimal context into tly/) —
  local, no accounts needed.

## 2026-08-17T00:14+02:00 | bootstrap-commit | DONE
- Committed the 2026-08-16 reconstruction bundle (seed+snapshots+golden test;
  SPEC.md; METHODOLOGY_v0.md; loop state). Verifier: suite re-run pre-commit
  this iteration — 2 passed.
- Adversarial consistency review of the reconstructed artifacts (planned
  verify:critic agent) did NOT run — hit the session usage limit 2026-08-16
  18:31 CEST before reading any artifact. No review claims exist. Rescheduled
  as the next iteration's task; A-16 (Ben ratifies reconstructions) still
  gates the first public print regardless.

## 2026-08-17T00:35+02:00 | verify-critic | DONE
- Adversarial consistency review of the reconstructions ran to completion
  (5 findings: 1 high, 1 medium, 3 low). Critic independently re-ran the
  suite: 2 passed; independently recomputed mint from the raw snapshot
  (132,110,264 × 73.123374469 = 9,660,348,305.670449816) confirming the
  committed golden value.
- Fixes applied this iteration: SPEC AC-1.2 amended (golden-anchor conflict:
  now S/Ē/N/spend exact at 4 dp; mint/drift/g reproduce-or-journal per
  B-uc1-11/12; results_v0.json declared THE anchor until B-uc1-13 post-A-16;
  amendment note in-place, flagged for A-16). SPEC dangling refs fixed
  (DECISIONS 13→removed at G5; DECISIONS 11→Key-numbers bullet at AC-5.3;
  grep confirms no DECISIONS n>10 refs remain). METHODOLOGY §1.1 and §5
  "exactly" claims reworded to mutual-consistency-at-4dp. README gained the
  reconstruction/ratification notice.
- CORRECTION to the 2026-08-17T00:14 entry (append-only, not edited): the
  2026-08-16 session limit was hit ~18:41 CEST (per .claude/RESUME.md
  checkpoint 16:41:16Z), not 18:31; and iterations A-08..A-11 were committed
  as one bundle at 2026-08-17T00:12:54+02:00, not per-iteration.
- Verifier: full suite re-run after all edits — see next line for result.
- Suite green after review fixes: 2 passed (2026-08-17T00:35+02:00).

## 2026-08-17T00:45+02:00 | A-12 | DONE
- Ported parsers into the package: tly/numeric.py (Decimal prec-34
  ROUND_HALF_EVEN context, BILLION/Q4 quanta) and tly/parsers.py (GHO ex
  life tables with scope+completeness validation, OWID population bands as
  frozen dataclass with uniform-within-band midpoints, OWID births).
  seed/tly_v0_calc.py untouched (frozen ground truth).
- Verifier: 9 new unit tests cross-check parsed values against
  seed/results_v0.json (e0 anchors, N_persons total, band midpoints/counts
  vs golden band_detail, births) plus error-path tests. Full suite:
  11 passed. ruff check tly/ tests/ seed/: all checks passed.
- Next: A-13 (port E2 estimator; package golden test to 4 dp).

## 2026-08-17T00:52+02:00 | A-13 | DONE
- tly/estimator.py: e_interp (linear-on-anchors, flat-tail — policy string
  versioned per AC-1.4), compute_stock returning frozen StockResult with
  full per-band decomposition, total_population, e_bar, mint.
- Verifier: package golden test at THREE strengths — 4-dp match on
  S/N/Ē/spend/mint (AC-1.2 core), full-precision prec-34 string equality
  vs golden, and per-band term equality vs golden band_detail for both
  years; plus e_interp unit properties. Full suite: 15 passed. ruff clean.
- Next: A-14 (snapshot fetcher module) or A-15 (install pre-commit hooks).

## 2026-08-17T00:58+02:00 | A-14 | DONE
- tly/snapshot.py: fetch_url (User-Agent, exponential backoff + jitter,
  injectable sleep), fetch_snapshot (injectable fetcher — manifest logic
  testable offline; sha256/URL/UTC-timestamp/bytes per file), and
  verify_manifest — the offline integrity gate (SnapshotIntegrityError on
  missing/mismatched files) that AC-1.5 compute paths must call first.
- Verifier: 7 network-free tests — fetch/manifest roundtrip, committed
  2026-08-16 snapshot verifies intact (6 files), tamper + missing-file +
  missing-manifest detection, backoff sequencing (2 sleeps for 3 attempts,
  exponential base). Full suite: 22 passed. ruff clean.
- Next: A-15 (install pre-commit hooks; ruff green already verified).
