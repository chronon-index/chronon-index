"""Methodology versioning (SPEC#1 AC-1.4; RP Part I M5; RP Part XI).

Every published output is stamped with the methodology version and the
numerical policies it was computed under. Policies may change ONLY together
with a version bump recorded in docs/METHODOLOGY_CHANGELOG.md — the
VERSION_POLICY_REGISTRY below pins each version to its exact policy
strings, and test_policy_change_requires_version_bump enforces the pairing
in CI. Editing a policy without adding a new registry entry (and moving
METHODOLOGY_VERSION to it) fails the suite by construction.
"""

from __future__ import annotations

from tly.numeric import PRECISION, ROUNDING

METHODOLOGY_VERSION = "v0.2.0-reconstruction"

INTERPOLATION_POLICY = "linear-on-anchors, flat-tail"
BAND_MIDPOINT_POLICY = "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)"
DECIMAL_POLICY = f"Decimal prec {PRECISION}, {ROUNDING}"
BASELINE_POLICY = "kk-linear: per-period linear trend fit on 2015-2019 (Karlinsky-Kobak)"

# version -> the exact policy strings that version is defined by.
# Append-only: past entries are history and must never be edited.
VERSION_POLICY_REGISTRY: dict[str, dict[str, str]] = {
    "v0.1.0-reconstruction": {
        "interpolation": "linear-on-anchors, flat-tail",
        "band_midpoint": "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)",
        "decimal": "Decimal prec 34, ROUND_HALF_EVEN",
    },
    # v0.2.0: ADDS the nowcast baseline policy (B-uc2-04); prior policies
    # unchanged. See docs/METHODOLOGY_CHANGELOG.md.
    "v0.2.0-reconstruction": {
        "interpolation": "linear-on-anchors, flat-tail",
        "band_midpoint": "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)",
        "decimal": "Decimal prec 34, ROUND_HALF_EVEN",
        "baseline": "kk-linear: per-period linear trend fit on 2015-2019 (Karlinsky-Kobak)",
    },
}


def current_policies() -> dict[str, str]:
    """The live policy strings, as the code actually computes them."""
    return {
        "interpolation": INTERPOLATION_POLICY,
        "band_midpoint": BAND_MIDPOINT_POLICY,
        "decimal": DECIMAL_POLICY,
        "baseline": BASELINE_POLICY,
    }


def output_metadata() -> dict[str, object]:
    """Stamp block for every published artifact (AC-1.4)."""
    return {
        "methodology_version": METHODOLOGY_VERSION,
        "policies": current_policies(),
    }
