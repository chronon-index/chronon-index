"""B-uc2-06: weekly print object — schema, epoch discipline, determinism."""

from __future__ import annotations

import dataclasses
from decimal import Decimal
from pathlib import Path

import pytest

from tly.prints import PrintSchemaError, WeeklyPrint, validate_epoch, validate_print_dict
from tly.stock import stamp

REPO = Path(__file__).resolve().parent.parent
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"

D = Decimal
EPOCH = "2026-08-17T12:00:00+00:00"  # a Monday


def _print(**overrides) -> WeeklyPrint:
    kwargs = dict(
        epoch_utc=EPOCH,
        series_label="SETTLEMENT",
        s_life_years=D("362412641743.467008807750"),
        e_bar_years=D("44.7880"),
        n_persons=D("8091734933"),
        burn_life_years=D("0"),
        coverage={"measured_share": D("0.92"), "by_country": {"DEU": D("0.98")}},
        provenance=stamp([SNAP16]),
    )
    kwargs.update(overrides)
    return WeeklyPrint(**kwargs)


def test_valid_print_roundtrip_and_schema():
    p = _print()
    data = p.to_json_dict()
    validate_print_dict(data)  # passes the consumer-side gate
    assert data["series_label"] == "SETTLEMENT"
    assert data["s_life_years"] == "362412641743.467008807750"  # Decimal-as-string
    assert data["coverage"]["measured_share"] == "0.92"


def test_epoch_discipline():
    validate_epoch(EPOCH)
    for bad in (
        "2026-08-18T12:00:00+00:00",  # Tuesday
        "2026-08-17T12:00:01+00:00",  # not exactly 12:00:00
        "2026-08-17T12:00:00",  # naive
        "2026-08-17T14:00:00+02:00",  # explicit non-UTC offset
        "not-a-date",
    ):
        with pytest.raises(PrintSchemaError):
            validate_epoch(bad)


def test_label_and_type_discipline():
    with pytest.raises(PrintSchemaError, match="series_label"):
        _print(series_label="OFFICIAL")
    with pytest.raises(PrintSchemaError, match="must be Decimal"):
        _print(s_life_years="362.4")


def test_print_is_immutable_p4():
    p = _print()
    with pytest.raises(dataclasses.FrozenInstanceError):
        p.s_life_years = D("1")  # type: ignore[misc]


def test_render_deterministic_p5():
    a = _print().render()
    b = _print().render()
    assert a == b  # byte-identical
    assert '"s_life_years": "362412641743.467008807750"' in a
    assert "float" not in a  # no accidental float reprs


def test_missing_coverage_fails_schema():
    data = _print().to_json_dict()
    del data["coverage"]
    with pytest.raises(PrintSchemaError, match="missing required fields"):
        validate_print_dict(data)
    data2 = _print().to_json_dict()
    data2["coverage"] = {"by_country": {}}
    with pytest.raises(PrintSchemaError, match="measured_share is required"):
        validate_print_dict(data2)


def test_provenance_required():
    data = _print().to_json_dict()
    data["provenance"] = {"policies": {}}
    with pytest.raises(PrintSchemaError, match="methodology_version and snapshots"):
        validate_print_dict(data)
