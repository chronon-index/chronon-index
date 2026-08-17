"""E-03: vintage addressability + never-delete at the vintage level."""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

import pytest

from tly.vintages import VintageError, list_vintages, manifest_for, vintage_as_of

REPO = Path(__file__).resolve().parent.parent


def test_list_vintages_real_tree():
    vintages = list_vintages()
    assert date(2026, 8, 16) in vintages
    assert date(2026, 8, 17) in vintages
    assert vintages == sorted(vintages)


def test_manifest_addressable_by_vintage():
    m16 = manifest_for(date(2026, 8, 16))
    assert "gho_ex_global_btsx_2019_2021.json" in m16["files"]
    m17 = manifest_for(date(2026, 8, 17))
    assert "wmd_world_mortality.csv" in m17["files"]
    with pytest.raises(VintageError, match="no vintage 1999-01-01"):
        manifest_for(date(1999, 1, 1))


def test_as_of_resolution():
    assert vintage_as_of(date(2026, 8, 16)) == date(2026, 8, 16)
    assert vintage_as_of(date(2026, 8, 16)) != date(2026, 8, 17)
    assert vintage_as_of(date(2027, 1, 1)) == date(2026, 8, 17)  # latest ≤ query
    with pytest.raises(VintageError, match="on or before"):
        vintage_as_of(date(2020, 1, 1))  # before the first data world


def test_every_historical_vintage_still_present():
    """Never-delete at the vintage level: every snapshot directory that
    EVER appeared in git history must still exist in the worktree."""
    out = subprocess.run(
        ["git", "-C", str(REPO), "log", "--all", "--name-only", "--pretty=format:"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    historical = {
        line.split("/")[2]
        for line in out.splitlines()
        if line.startswith("data/snapshots/") and len(line.split("/")) > 3
    }
    assert historical, "expected at least one historical vintage"
    for vintage in sorted(historical):
        assert (REPO / "data" / "snapshots" / vintage).is_dir(), (
            f"vintage {vintage} appeared in history but is gone from the tree"
        )
