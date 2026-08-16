"""B-uc3-04 / AC-3.4: the version-bump guard, completed.

Beyond the pairing check (test_methodology), this closes the remaining
gap: governed numerical constants living in CODE must be represented in
the CURRENT version's registered policy strings — so a constant cannot be
changed (or added) without the registry noticing. Plus ledger hygiene:
every registry version appears in the changelog, and version history is
append-only in file order.

Ensemble weights (RP Part V Q1) are future-governed: they do not exist
until the P2 model ensemble lands, and MUST enter this registry when they
do — recorded here as an executable reminder.
"""

from __future__ import annotations

from pathlib import Path

from tly.baseline import FIT_YEARS
from tly.burn import distribute_excess
from tly.methodology import (
    METHODOLOGY_VERSION,
    VERSION_POLICY_REGISTRY,
    current_policies,
)
from tly.numeric import PRECISION
from tly.weekly import LIFE_YEAR_QUANTUM

REPO = Path(__file__).resolve().parent.parent


def test_governed_constants_are_registered():
    """Every governed code constant appears in the current policy strings."""
    policies = current_policies()
    blob = " | ".join(policies.values())
    # baseline fit window
    assert f"{FIT_YEARS[0]}-{FIT_YEARS[-1]}" in policies["baseline"]
    # scheduling quantum (tly/weekly.py)
    assert str(LIFE_YEAR_QUANTUM) in policies["quanta"]
    # attribution quantum: the documented default of distribute_excess
    assert "0.001" in policies["quanta"]
    assert distribute_excess.__defaults__ is not None
    # decimal precision
    assert str(PRECISION) in policies["decimal"]
    # nothing registered is empty
    assert all(v.strip() for v in blob.split("|"))


def test_attribution_quantum_default_matches_registry():
    from decimal import Decimal
    from inspect import signature

    default = signature(distribute_excess).parameters["quantum"].default
    assert default == Decimal("0.001")
    assert str(default) in current_policies()["quanta"]


def test_every_registry_version_is_in_changelog():
    changelog = (REPO / "docs" / "METHODOLOGY_CHANGELOG.md").read_text(encoding="utf-8")
    for version in VERSION_POLICY_REGISTRY:
        assert version in changelog, f"{version} missing from changelog"


def test_registry_history_is_append_only_ordered():
    versions = list(VERSION_POLICY_REGISTRY)
    assert versions == sorted(versions), "registry keys must stay in ascending order"
    assert versions[-1] == METHODOLOGY_VERSION, "current version must be the newest entry"
    # policy keys only ever grow across versions (policies are added, never dropped)
    for older, newer in zip(versions, versions[1:]):
        old_keys = set(VERSION_POLICY_REGISTRY[older])
        new_keys = set(VERSION_POLICY_REGISTRY[newer])
        assert old_keys <= new_keys, f"{newer} drops policy keys {old_keys - new_keys}"


def test_ensemble_weights_not_yet_governed_reminder():
    """When the P2 model ensemble lands (D-phase), its weights MUST become
    a registered policy. Until then no policy may claim to govern them."""
    assert "ensemble" not in current_policies(), (
        "an ensemble policy appeared — ensure weights are registry-governed "
        "and delete this reminder test"
    )
