"""B-uc4-10 / AC-4.1: the three named negative classes — an orphan number,
a missing provenance block, and a negative value — each blocks PUBLISH.

test_p9_lineage covers the lineage checker in isolation; these tests prove
the same classes cannot get past the full publish gate either, and that
each failure names its cause in the PublishBlocked violations.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.pipeline import build_settlement_print
from tly.publish import PublishBlocked, publish_prints

REPO = Path(__file__).resolve().parent.parent
SNAPSHOTS = REPO / "data" / "snapshots"
EPOCH = "2026-08-17T12:00:00+00:00"


def _corrupt(print_obj, field, value):
    object.__setattr__(print_obj, field, value)
    return print_obj


def test_orphan_number_blocks_publish(tmp_path):
    """A print citing zero snapshots is an orphan number at publish time."""
    bad = build_settlement_print(EPOCH)
    prov = dict(bad.provenance)
    prov["snapshots"] = {}
    _corrupt(bad, "provenance", prov)
    with pytest.raises(PublishBlocked) as exc:
        publish_prints([bad], tmp_path / "site", SNAPSHOTS)
    assert any("orphan print" in v for v in exc.value.violations)
    assert not (tmp_path / "site").exists()


def test_missing_provenance_block_blocks_publish(tmp_path):
    """No provenance at all: caught by the schema gate before lineage."""
    bad = _corrupt(build_settlement_print(EPOCH), "provenance", {})
    with pytest.raises(PublishBlocked) as exc:
        publish_prints([bad], tmp_path / "site", SNAPSHOTS)
    assert any("provenance" in v for v in exc.value.violations)
    assert not (tmp_path / "site").exists()


def test_negative_value_blocks_publish(tmp_path):
    """A negative stock value is caught by the lineage non-negativity rule."""
    bad = _corrupt(build_settlement_print(EPOCH), "n_persons", Decimal("-8091734933"))
    with pytest.raises(PublishBlocked) as exc:
        publish_prints([bad], tmp_path / "site", SNAPSHOTS)
    assert any("n_persons is negative" in v for v in exc.value.violations)
    assert not (tmp_path / "site").exists()


def test_all_three_reported_together(tmp_path):
    """One print carrying all three defects: the gate reports every
    violation at once (CI legibility), not just the first."""
    bad = build_settlement_print(EPOCH)
    _corrupt(bad, "provenance", {})
    _corrupt(bad, "n_persons", Decimal("-1"))
    with pytest.raises(PublishBlocked) as exc:
        publish_prints([bad], tmp_path / "site", SNAPSHOTS)
    text = "\n".join(exc.value.violations)
    assert "provenance" in text
    assert "n_persons is negative" in text
