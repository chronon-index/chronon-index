"""Vintage archive addressing (RP Part VII; RP Part V Q7; E-03).

ALFRED-style access to the snapshot vintages: every revision generation is
retained forever under ``data/snapshots/<date>/`` and is addressable both
directly (by its vintage date) and as-of (which vintage was current on a
given date) — so any historical computation can name exactly the data
world it lived in, and a restatement is a NEW vintage beside the old one,
never a replacement.

Never-delete is enforced two ways: the git-history immutability gates
(tests/test_snapshot_immutability.py) forbid modification/deletion of
snapshot files, and test_every_historical_vintage_still_present walks git
history for vintage directories and requires each to exist in HEAD.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOTS_ROOT = REPO_ROOT / "data" / "snapshots"


class VintageError(ValueError):
    pass


# Frozen REFERENCE sets living beside the dated vintages. "v0-original" is
# the D3b golden-input freeze (A-16 ruling): it pins AC-1.2, it is not a
# point on the vintage timeline and never resolves from an as-of query.
REFERENCE_SETS = frozenset({"v0-original"})


def list_vintages(root: Path = SNAPSHOTS_ROOT) -> list[date]:
    """All vintage dates, ascending. A directory without a manifest is not
    a vintage (and the manifest-schema gate would fail the build anyway);
    named REFERENCE_SETS are frozen anchors, not vintages."""
    out = []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        if d.name in REFERENCE_SETS:
            continue
        if (d / "manifest.json").is_file():
            try:
                out.append(date.fromisoformat(d.name))
            except ValueError as err:
                raise VintageError(f"non-date vintage directory: {d.name}") from err
    return out


def manifest_for(vintage: date, root: Path = SNAPSHOTS_ROOT) -> dict:
    path = root / vintage.isoformat() / "manifest.json"
    if not path.is_file():
        raise VintageError(f"no vintage {vintage.isoformat()}")
    return json.loads(path.read_text(encoding="utf-8"))


def vintage_as_of(query: date, root: Path = SNAPSHOTS_ROOT) -> date:
    """The vintage that was current on ``query``: the latest vintage date
    ≤ query. Asking about a date before the first vintage is an error —
    there was no data world then, and pretending otherwise would be a
    silent extrapolation."""
    candidates = [v for v in list_vintages(root) if v <= query]
    if not candidates:
        raise VintageError(f"no vintage exists on or before {query.isoformat()}")
    return candidates[-1]
