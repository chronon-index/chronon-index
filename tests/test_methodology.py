"""B-uc1-07 / AC-1.4: policy changes require a methodology version bump.

The registry pins each version to its exact policy strings. These tests ARE
the CI guard: edit a policy without a new registry entry + version move and
the suite fails.
"""

from __future__ import annotations

from tly import estimator
from tly.methodology import (
    METHODOLOGY_VERSION,
    VERSION_POLICY_REGISTRY,
    current_policies,
    output_metadata,
)


def test_policy_change_requires_version_bump():
    """Live policies must equal the registry entry for the CURRENT version.

    Changing any policy string without appending a new registry entry and
    moving METHODOLOGY_VERSION to it fails here — this is the AC-1.4 gate.
    """
    assert METHODOLOGY_VERSION in VERSION_POLICY_REGISTRY, (
        f"METHODOLOGY_VERSION {METHODOLOGY_VERSION!r} has no registry entry — "
        "append one (never edit past entries) and update the changelog"
    )
    assert current_policies() == VERSION_POLICY_REGISTRY[METHODOLOGY_VERSION], (
        "live policy strings differ from the registry pin for "
        f"{METHODOLOGY_VERSION} — a policy change requires a version bump "
        "(new registry entry + docs/METHODOLOGY_CHANGELOG.md entry)"
    )


def test_registry_is_append_only_v010_pin():
    """The v0.1.0 entry is history; editing it is forbidden. Byte-pin it."""
    assert VERSION_POLICY_REGISTRY["v0.1.0-reconstruction"] == {
        "interpolation": "linear-on-anchors, flat-tail",
        "band_midpoint": "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)",
        "decimal": "Decimal prec 34, ROUND_HALF_EVEN",
    }


def test_estimator_uses_canonical_policy():
    assert estimator.INTERPOLATION_POLICY == current_policies()["interpolation"]


def test_output_metadata_stamp_shape():
    meta = output_metadata()
    assert meta["methodology_version"] == METHODOLOGY_VERSION
    assert set(meta["policies"]) == {
        "interpolation",
        "band_midpoint",
        "decimal",
        "baseline",
        "p6_closure",
        "quanta",
        "excess_age_profile",
    }


def test_changelog_documents_current_version():
    from pathlib import Path

    changelog = (
        Path(__file__).resolve().parent.parent / "docs" / "METHODOLOGY_CHANGELOG.md"
    ).read_text(encoding="utf-8")
    assert METHODOLOGY_VERSION in changelog, (
        "current methodology version missing from docs/METHODOLOGY_CHANGELOG.md"
    )
