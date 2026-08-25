# Conflict-of-Interest Statement — DRAFT for counsel review (D-15)

> STATUS: DRAFT. Not reviewed by counsel (D-13 pending). RP Part XI
> mandates this disclosure from day one; IOSCO Principle 3 is the
> governance reference (`docs/IOSCO_MAPPING.md` row 3).

## Disclosed interests

1. **The builder holds (or will hold) the asset.** The project's
   originator holds SAEC/CHRONON interests from inception. This is
   disclosed up front, permanently, in the repository itself. Any
   future token allocation to the originator will be published before
   any public sale or listing.
2. **One-person project (pre-entity).** Until an administrator entity
   with an oversight function exists (P5), the same person originates
   methodology proposals and operates the pipeline. The structural
   mitigants below are what make that tolerable in the interim.

## Structural mitigants (in force today, all machine-checked)

- **The computation is public and reproducible.** The weekly CI run is
  the official computation; anyone can recompute every archived epoch
  byte-for-byte (`tly/outsider_sim.py` does exactly this on a public
  schedule). Discretion in operation is minimized by construction.
- **No discretionary inputs.** The settlement series admits only
  published official statistics through hash-manifested snapshots;
  expert judgment is excluded from settlement by design (measured-
  period settles; model content is walled off as INFORMATIONAL).
- **Methodology changes are governed.** A policy cannot change without
  a version bump through the public change process (14-day comment
  window at launch); the pairing is CI-enforced
  (`tests/test_methodology.py`).
- **First-print-settles.** Archived values are immutable; the holder of
  the asset cannot retroactively improve their own history. Corrections
  are forward-only and public.
- **Bitcoin-anchored timestamps.** Archived record hashes are
  OpenTimestamps-stamped, so even a total repository compromise could
  not silently rewrite history.

## What is not yet in place (honest gaps, tracked)

- No independent oversight function (IOSCO P5 gap — needs an entity).
- No remuneration policy (moot until an entity employs anyone).
- No independent complaints investigator (Principle 16b — P5).

These gaps close at the P5 administrator-entity phase; they are listed
in the public IOSCO mapping rather than hidden.
