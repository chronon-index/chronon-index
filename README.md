# TLY / CHRONON

A demographically-ruled monetary asset. **TLY** is the index: humanity's total
remaining life-years, S(t) = Σ over (age, sex, country) of population ×
remaining life expectancy. **Mirror** is the protocol whose token supply
algorithmically mirrors S. **CHRONON** is the token. Price floats; the formula
governs supply only.

Layered rollout (DECISIONS.md #1): v1 index → v2 cash-settled derivatives →
v3 Mirror token → v4 Ledger.

## Governing documents

| File | Role |
|---|---|
| `DECISIONS.md` | Locked design decisions. Never contradicted. |
| `RESEARCH_PROGRAM.md` | The full map: math, data, phases, gates, governance. |
| `SPEC.md` | The seven build capabilities with acceptance criteria. |
| `METHODOLOGY_v0.md` | The v0 math: estimator, transport identity, error budget. |
| `RALPH_LOOP.md` | The autonomous build loop protocol. |

> **Reconstruction notice:** `SPEC.md`, `METHODOLOGY_v0.md` and everything in
> `seed/` are 2026-08-16 reconstructions of lost originals, pending
> ratification (`loop/BACKLOG.md` task A-16). Treat their numbers as
> anchors-to-confirm, not truth. No public print before ratification.

## Principles (non-negotiable)

- **Radical verifiability.** Every published figure is computed by open code
  from keyless public endpoints, prints its source URLs, and is reproducible
  by any third party. No number ships without a runnable path.
- **First print settles.** Corrections are forward-only, in
  `ledger/CORRECTIONS.md`. No historical value is ever restated.
- **Decimal everywhere** supply- or index-adjacent (precision 34,
  ROUND_HALF_EVEN). Floats never touch published numbers.
- **Snapshot-first.** Fetch to `data/snapshots/<date>/` with a sha256
  manifest, then compute offline. Small v0 snapshots are committed; large
  snapshots move to object storage with manifests committed in-repo
  (RESEARCH_PROGRAM Part VII).
- **Licensing gate.** `docs/LICENSING.md` must be cleared before the first
  public print.

## Layout

```
tly/              the package (index computation)
seed/             v0 calculator and its golden output (ground truth)
tests/            pytest suite; the golden test anchors every refactor
data/snapshots/   content-hashed input snapshots
docs/             licensing table, governance artifacts
ledger/           forward-only correction ledger
loop/             Ralph-loop state: BACKLOG.md, JOURNAL.md, LEARNINGS.md
.github/          CI (tests on push) + weekly Monday 12:00 UTC print job
```

## Run

```bash
python3.12 -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Autonomous build: `./ralph.sh` (see RALPH_LOOP.md).

## Licensing

Code: Apache-2.0 (`LICENSE`). Documentation and published index data:
CC BY 4.0. Upstream data licenses: `docs/LICENSING.md`.
