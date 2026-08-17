"""B-uc2-10 / AC-2.5: dual series — settlement never depends on the cohort model."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.prints import DualSeries, PrintSchemaError, WeeklyPrint
from tly.stock import stamp

REPO = Path(__file__).resolve().parent.parent
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"

D = Decimal
EPOCH = "2026-08-17T12:00:00+00:00"


def _print(label: str, s: str, epoch: str = EPOCH) -> WeeklyPrint:
    return WeeklyPrint(
        epoch_utc=epoch,
        series_label=label,
        s_life_years=D(s),
        e_bar_years=D("44.7880"),
        n_persons=D("8091734933"),
        burn_life_years=D("0"),
        coverage={"measured_share": D("0.92")},
        accuracy={
            "statement": "test accuracy statement",
            "uncertainty": {"type": "convention", "note": "test fixture"},
        },
        provenance=stamp([SNAP16]),
    )


def test_settlement_value_reads_settlement_print_only():
    settlement = _print("SETTLEMENT", "362412641743.4670")
    cohort = _print("INFORMATIONAL", "390000000000.0000")  # cohort estimate, higher
    dual = DualSeries(settlement=settlement, informational=cohort)
    assert dual.settlement_value == D("362412641743.4670")
    # the cohort print's value appears nowhere in the settlement accessor
    assert dual.settlement_value != cohort.s_life_years


def test_informational_slot_optional_pre_p2():
    dual = DualSeries(settlement=_print("SETTLEMENT", "362412641743.4670"))
    assert dual.settlement_value == D("362412641743.4670")
    data = dual.to_json_dict()
    assert data["informational"] is None
    assert data["settlement"]["series_label"] == "SETTLEMENT"


def test_label_discipline_both_slots():
    with pytest.raises(PrintSchemaError, match="settlement slot requires"):
        DualSeries(settlement=_print("INFORMATIONAL", "1"))
    with pytest.raises(PrintSchemaError, match="informational slot requires"):
        DualSeries(
            settlement=_print("SETTLEMENT", "1"),
            informational=_print("SETTLEMENT", "2"),
        )


def test_epoch_must_match():
    with pytest.raises(PrintSchemaError, match="must share one epoch"):
        DualSeries(
            settlement=_print("SETTLEMENT", "1"),
            informational=_print("INFORMATIONAL", "2", epoch="2026-08-24T12:00:00+00:00"),
        )


def test_render_orders_settlement_first_and_is_deterministic():
    dual = DualSeries(
        settlement=_print("SETTLEMENT", "362412641743.4670"),
        informational=_print("INFORMATIONAL", "390000000000.0000"),
    )
    assert dual.render() == dual.render()
    data = dual.to_json_dict()
    assert data["settlement"]["s_life_years"] == "362412641743.4670"
    assert data["informational"]["s_life_years"] == "390000000000.0000"
