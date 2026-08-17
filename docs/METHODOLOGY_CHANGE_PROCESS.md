# Methodology change process

The monetary-rule philosophy applied to methodology (RESEARCH_PROGRAM
Part XI; DECISIONS #6): ambition enters through versioning, never through
silent edits. This document is the governing procedure; the mechanics that
enforce it are code.

## Scope

Any change to a **methodology-governed parameter** — the policy strings in
`tly/methodology.py` (`current_policies()`): interpolation, band midpoint,
Decimal context, nowcast baseline, closure tolerances, quanta — and, when
they land, model-ensemble weights (RP Part V Q1; an executable reminder in
`tests/test_version_bump_guard.py` fires when an ensemble policy appears).

Bug fixes that change published numbers are NOT methodology changes — they
go through the correction ledger (`ledger/CORRECTIONS.md`), forward-only.

## Procedure

1. **Proposal.** A written proposal in the repo (issue or `docs/proposals/`)
   stating: the policy being changed, old and new policy strings, the
   motivation, and the expected numerical impact on S (with magnitude).
2. **Public comment window.** Minimum 14 days from proposal publication for
   index-affecting changes; 7 days for additions that do not alter existing
   published series. The window is announced wherever prints are published.
   (Pre-P1, while no external consumers exist, the window may be satisfied
   by Ben's explicit sign-off, recorded in the proposal — this shortcut
   expires at the first public print.)
3. **Version bump.** On acceptance, in ONE commit:
   - append the new version entry to `VERSION_POLICY_REGISTRY`
     (never edit past entries — byte-pinned by tests),
   - move `METHODOLOGY_VERSION` to it,
   - update the live policy constants,
   - add the changelog entry in `docs/METHODOLOGY_CHANGELOG.md`.
4. **Effective date.** The new version applies from the next epoch's print
   onward. No historical print is recomputed (DECISIONS #7); if the change
   creates a level break, both series values at the boundary epoch are
   published side by side, labeled.

## Enforcement (already live in CI)

- `test_policy_change_requires_version_bump` — live policies must equal the
  current version's registry pin; any drift fails.
- `test_registry_is_append_only_v010_pin` + `test_registry_history_is_
  append_only_ordered` — history cannot be rewritten; policy keys only grow.
- `test_every_registry_version_is_in_changelog` — no undocumented version.
- `test_governed_constants_are_registered` — governed code constants must
  appear in the registered policy strings (signature-inspected).
- `test_changelog_documents_current_version` — the changelog names the
  current version.

A change that skips any step above cannot merge with a green build; that is
the wiring.
