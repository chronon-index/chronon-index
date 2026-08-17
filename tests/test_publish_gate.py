"""B-uc4-05: a print failing any validation blocks publish — atomically."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tly.pipeline import build_settlement_print
from tly.publish import PublishBlocked, publish_prints

REPO = Path(__file__).resolve().parent.parent
SNAPSHOTS = REPO / "data" / "snapshots"
EPOCH_1 = "2026-08-10T12:00:00+00:00"
EPOCH_2 = "2026-08-17T12:00:00+00:00"


def _corrupt(print_obj, field, value):
    """Simulate future code drift bypassing construction-time validation:
    frozen dataclasses can still be mutated via object.__setattr__ — the
    publish gate must catch what slips past the constructor."""
    object.__setattr__(print_obj, field, value)
    return print_obj


def test_publish_happy_path(tmp_path):
    out = tmp_path / "site"
    api_root = publish_prints([build_settlement_print(EPOCH_2)], out, SNAPSHOTS)
    latest = json.loads((api_root / "latest.json").read_text())
    assert latest["series_label"] == "SETTLEMENT"
    assert not (tmp_path / "site.staging").exists()  # staging cleaned up


def test_bad_label_blocks_publish_and_preserves_previous(tmp_path):
    out = tmp_path / "site"
    publish_prints([build_settlement_print(EPOCH_1)], out, SNAPSHOTS)
    before = (out / "api" / "v1" / "latest.json").read_bytes()

    bad = _corrupt(build_settlement_print(EPOCH_2), "series_label", "OFFICIAL")
    with pytest.raises(PublishBlocked) as exc:
        publish_prints([bad], out, SNAPSHOTS)
    assert any("series_label" in v for v in exc.value.violations)
    # the previously published tree is byte-for-byte untouched
    assert (out / "api" / "v1" / "latest.json").read_bytes() == before
    assert not (tmp_path / "site.staging").exists()


def test_missing_accuracy_blocks_publish(tmp_path):
    bad = _corrupt(build_settlement_print(EPOCH_2), "accuracy", {})
    with pytest.raises(PublishBlocked) as exc:
        publish_prints([bad], tmp_path / "site", SNAPSHOTS)
    assert any("accuracy" in v.lower() for v in exc.value.violations)
    assert not (tmp_path / "site").exists()  # nothing half-published


def test_broken_lineage_blocks_publish(tmp_path):
    bad = build_settlement_print(EPOCH_2)
    prov = dict(bad.provenance)
    prov["snapshots"] = {"2099-01-01": {"ghost.csv": "0" * 64}}
    _corrupt(bad, "provenance", prov)
    with pytest.raises(PublishBlocked) as exc:
        publish_prints([bad], tmp_path / "site", SNAPSHOTS)
    assert any("unknown snapshot" in v for v in exc.value.violations)


def test_republish_retires_previous_tree(tmp_path):
    out = tmp_path / "site"
    publish_prints([build_settlement_print(EPOCH_1)], out, SNAPSHOTS)
    publish_prints(
        [build_settlement_print(EPOCH_1), build_settlement_print(EPOCH_2)],
        out,
        SNAPSHOTS,
    )
    latest = json.loads((out / "api" / "v1" / "latest.json").read_text())
    assert latest["epoch_utc"] == EPOCH_2
    prev = json.loads((tmp_path / "site.previous" / "api" / "v1" / "latest.json").read_text())
    assert prev["epoch_utc"] == EPOCH_1  # one prior tree retained
