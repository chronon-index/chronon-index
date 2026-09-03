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

> **Provenance notice (A-16 CLOSED 2026-09-03):** the 2026-08-16 loss was
> resolved by RESTORE, not ratification-of-reconstruction: `seed/` and
> `METHODOLOGY_v0.md` are the verbatim originals (delivered back in
> chronon-restore-A16.zip); the reconstructions remain archived under
> `ops/reconstruction/2026-08-16/`, still byte-runnable. AC-1.2 is strict:
> the v1 engine reproduces every original golden value to 4 dp on the
> frozen `data/snapshots/v0-original/` inputs.
>
> **Series status:** the G5 source-of-record switch (WHO → UN WPP 2024,
> CC BY 3.0 IGO) was accepted 2026-09-04 as methodology v0.7.0 — the live
> settlement path now cites only commercially cleared sources and passes
> the licensing gate with zero violations; the first v0.7.0 print is the
> 2026-09-07 epoch (archived prints stand as printed, P4). Level change
> +0.3033%, dual-run published in the proposal and changelog. Nothing here
> is investment advice; settlement-grade status still awaits the P5
> hardening (external recomputers, oversight, audits — tracked openly).

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

## Live site + API

**https://chronon-index.pages.dev** — the rendered governance pages and the
static JSON API (`/api/v1/latest.json`, `/api/v1/prints/<date>.json`,
`/api/v1/index.json` with sha256s). The API serves the archived prints
byte-verbatim; a path that was never printed returns 404 — absence is an
answer. The tree is committed under `site/` and rebuilt by CI after every
print; the suite asserts the committed tree equals a fresh build.

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
