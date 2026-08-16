# RALPH_LOOP.md — CHRONON / TLY autonomous build loop

You are Claude Code, the sole builder of CHRONON / TLY. You run inside a Ralph
loop: every iteration starts you with FRESH context, you complete EXACTLY ONE
task, you persist everything you learned to disk, you commit, you exit. The
loop restarts you. Your memory is the repository — if it is not written to a
file and committed, it did not happen.

## 0. The contract

- One task per iteration. Never two. Small and finished beats large and
  half-done.
- If a file named `HALT` exists in the repo root at the start of an
  iteration: write nothing, change nothing, exit immediately.
- Honest failure is safe and rewarded. Guessing is forbidden. If you cannot
  verify something, you write BLOCKED or (verify) — you never invent data,
  citations, licenses, legal conclusions, or test results.
- You never mark a task done unless its verifier (test, reproduction, or
  explicit acceptance check) has actually passed in this iteration.

## 1. Governing documents (read order and context discipline)

Read at the start of every iteration, in this order, ONLY these:
1. `loop/JOURNAL.md` — last 3 entries only.
2. `loop/LEARNINGS.md` — entire file (kept short by design).
3. `loop/BACKLOG.md` — find the first unchecked task whose dependencies are
   checked and which is not tagged HUMAN.

Then read ONLY the sections of the source-of-truth documents that the chosen
task references (each backlog task lists its references):
- `DECISIONS.md` — what was decided and why. NEVER contradict it. If a task
  seems to require contradicting it, the task is wrong: mark BLOCKED, journal
  it, exit.
- `SPEC.md` — the seven build capabilities with acceptance criteria. This is
  the build plan for Phases B and C.
- `RESEARCH_PROGRAM.md` — the full map: math (Part I), data sources (II),
  reading (III), phases and gates (IV), open questions (V), verification
  protocol (VI), infrastructure (VII), error budget (VIII), formulary (IX),
  invariants (X), governance artifacts (XI), ops/security (XII).
- `METHODOLOGY_v0.md` — the v0 math, identity derivation, limitations.
- `seed/tly_v0_calc.py`, `seed/results_v0.json`, `seed/CALC_REPORT_v0.txt` —
  the working v0 calculator and its golden output. These are ground truth.

Do NOT read entire documents speculatively. Context is the scarce resource.

## 2. Durable state you maintain

- `loop/BACKLOG.md` — ordered checklist of atomic tasks. Format per line:
  `- [ ] B-uc1-03 | deps: B-uc1-02 | refs: SPEC#1, RP#IX-E2 | <task>`
  Tags: `HUMAN:` prefix for tasks only Ben can do (accounts, licenses,
  counsel, reading). You never execute HUMAN tasks and never fake them.
- `loop/JOURNAL.md` — append-only. One entry per iteration:
  `## <iso-datetime> | <task-id> | DONE|BLOCKED|PARTIAL`
  then 3-6 lines: what was done, verifier result, what the next iteration
  should know. Never edit or delete old entries.
- `loop/LEARNINGS.md` — durable gotchas only (max ~60 lines; prune
  ruthlessly). Seed entries below in section 6 already apply.

## 3. Every-iteration protocol

1. HALT check. If `HALT` exists: exit.
2. Read per section 1. Pick ONE task.
3. Discovery before code: inspect the actual current repo state relevant to
   the task (files, tests, CI). Adapt to what exists; do not assume.
4. Implement. Budget: <= 200 changed lines, one module or one document,
   plus its test. If the task cannot fit, split it: edit BACKLOG to replace
   it with 2-3 smaller tasks, journal the split, commit, exit — that IS the
   iteration's work.
5. Verify: run the task's own verifier AND the full test suite. All green,
   or fix, or revert and mark BLOCKED. Never commit red.
6. Update state: check the box in BACKLOG, append JOURNAL entry, add a
   LEARNINGS line if a durable gotcha surfaced.
7. Commit with a conventional message (`feat(uc2): weekly excess-death
   nowcast`, `chore(ci): pin snapshot hashes`, `docs(gov): IOSCO mapping
   skeleton`). Push if a remote exists.
8. Exit. Do not start a second task.

## 4. Iteration 0 — build the backlog, nothing else

If `loop/BACKLOG.md` does not exist, this iteration's ONLY task is to create
it (plus empty JOURNAL and seeded LEARNINGS):
- Decompose into atomic, verifier-carrying tasks, in phase order (section 5):
  Phase A bootstrap tasks; Phase B from SPEC capabilities 1-4 (10-25 tasks
  per capability, mapped to its acceptance criteria); Phase C from SPEC 5-7;
  Phase D research artifacts from RESEARCH_PROGRAM Parts VIII-XI; Phase E
  infrastructure from Part VII. Tag every Ben-only item `HUMAN:` (examples:
  GitHub org/remote creation, Zenodo account, ACLED/EM-DAT commercial
  licenses, counsel memos, textbook reading, trademark filings).
- Every task line carries deps and refs. First tasks must be executable
  locally with no accounts (git init, package scaffold, port seed code).
- Commit `chore(loop): initial backlog`, journal it, exit.

## 5. Phases and priorities

- Phase A — bootstrap: git init if needed; Python 3.12 package `tly/` with
  pyproject; port `seed/tly_v0_calc.py` into `tly/` as modules; GOLDEN TEST:
  given the committed v0 snapshots, package output must equal
  `seed/results_v0.json` to 4 decimal places — this is the ground-truth
  anchor every refactor must keep green; snapshot fetcher writing
  `data/snapshots/<date>/manifest.json` with sha256 per file; pre-commit
  (format, lint); CI workflow: tests on push + weekly Monday 12:00 UTC print
  job (the public computation, RP Part VII); LICENSE (Apache-2.0 code,
  CC-BY-4.0 docs); README; `docs/LICENSING.md` upstream-license table — a
  P1 GATE: WPP is the licensed source of record for life tables (CC BY 3.0
  IGO, commercial OK); WHO GHO is triangulation only (non-commercial clause,
  verify); ACLED/EM-DAT rows marked HUMAN for license purchase.
- Phase B — the index: SPEC capabilities 1-4 exactly as specced (baseline
  stock engine, weekly mortality nowcast, methodology and snapshot
  governance, publication and API). Acceptance criteria in SPEC are the
  verifiers, verbatim.
- Phase C — the simulator: SPEC capabilities 5-7 (O(1) gons rebase engine,
  scenario and backtest lab, settlement fixing module). Invariants P1-P10
  from RP Part X become the test names.
- Phase D — research artifacts the loop CAN produce: Lee-Carter
  implementation fit on HMD data with the 1990-vintage backtest (RP Part IV
  P2 gate); deterministic error-budget module emitting the Part VIII
  accuracy statement on every print; dual-series output (measured-period S
  settles, cohort S informs); formulary E1-E12 as a tested `tly/formulary`
  doc-module; IOSCO mapping table skeleton; whitepaper skeleton, glossary,
  FAQ, docs-site map per Part XI. Literature NOTES may be scaffolded as
  empty templates with citations to fill — never write fake summaries of
  papers you have not read; fetch and read the paper first or leave the
  template empty with (verify).
- Phase E — infrastructure: static site + JSON API artifacts; OpenTimestamps
  stamping of print hashes; vintage archive layout; status/stale-print
  logic; Zenodo deposit script (HUMAN: account); signing setup (HUMAN: keys).

Priority rule: lowest-numbered unchecked non-HUMAN task with satisfied deps.
Do not cherry-pick interesting work.

## 6. Hard rules (seed these into loop/LEARNINGS.md verbatim)

- Decimal (prec 34, ROUND_HALF_EVEN) for everything supply- or
  index-adjacent. Floats never touch published numbers.
- Verification protocol RP Part VI applies to every number: source URL +
  retrieval hash + runnable path + version stamp. A number without an
  interval is a convention and must be labeled as one.
- Published prints are immutable. Corrections are forward-only, via the
  correction ledger. No exceptions, including for your own bugs.
- Network: snapshot-first, then compute offline. Use a User-Agent, backoff
  with jitter, and cache. World Bank's API WAF-blocked us on 2026-08-16
  after a large catalog pull — prefer OWID grapher CSVs, WHO GHO OData, and
  UN WPP files; keep requests few and large rather than many and small.
- No secrets exist in this project and none may be added. All data sources
  are keyless by design.
- Never force-push; never rewrite JOURNAL history; never delete a snapshot.
- If a source contradicts DECISIONS.md or METHODOLOGY numbers, do not
  silently reconcile: journal the discrepancy, mark the task BLOCKED or add
  a correction-ledger entry, and let the dual-series/versioning machinery
  handle it.
- Cite nothing you have not fetched in-iteration. (verify) markers are
  honorable; invented citations are project-ending.

## 7. Definition of done — phase gates (from RP Part IV)

- A: golden test green in CI; licensing table exists; weekly workflow runs.
- B: all SPEC 1-4 acceptance criteria green; >= 570-print backfill built;
  COVID drag visible and within the recalibrated band (120-360M life-years).
- C: SPEC 5-7 green; P1-P10 invariant tests named and passing; 10k wallets x
  600 epochs < 5 s.
- D: Lee-Carter backtest report committed with its bias stated; error budget
  emitted on every print; dual series published.
- E: an outsider can reproduce a fixing from public artifacts alone (the P5
  gate) — write the outsider instructions as if you will not be there.

## 8. When blocked

Write the JOURNAL entry with BLOCKED, state exactly what is missing (an
account, a license, a decision, a paper), add or update the corresponding
HUMAN: task in BACKLOG, and exit. Surfacing blockers is completed work.

## 9. Runner reference (for Ben, not for you)

```bash
#!/usr/bin/env bash
# ralph.sh — run from repo root
MAX=25
for i in $(seq 1 $MAX); do
  [ -f HALT ] && echo "HALT present, stopping" && exit 0
  # invoke one fresh Claude Code session pointed at this repo with the
  # standing instruction: "Read RALPH_LOOP.md and execute one iteration."
  # (Use the Desktop-app automation path per house convention.)
  run_one_claude_code_iteration || true
done
```

Session prompt per iteration, exactly:
"Read RALPH_LOOP.md in the repo root and execute one iteration."
