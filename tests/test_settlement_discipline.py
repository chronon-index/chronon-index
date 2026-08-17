"""C-uc7-05 / AC-7.4: the cohort/INFORMATIONAL series can never be a
settlement input — at the fixing gate AND at the dual-series accessor."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.archive import PrintArchive
from tly.fixings import FixingValidationError, settle_from_archive
from tly.prints import DualSeries, WeeklyPrint
from tly.stock import stamp

REPO = Path(__file__).resolve().parent.parent
SNAPSHOTS = REPO / "data" / "snapshots"
SNAP16 = SNAPSHOTS / "2026-08-16"
EPOCH = "2026-08-17T12:00:00+00:00"

D = Decimal


def _print(label: str, s: str) -> WeeklyPrint:
    return WeeklyPrint(
        epoch_utc=EPOCH,
        series_label=label,
        s_life_years=D(s),
        e_bar_years=D("44.7880"),
        n_persons=D("8091734933"),
        burn_life_years=D("0"),
        coverage={"measured_share": D("0.92")},
        accuracy={
            "statement": "x",
            "uncertainty": {"type": "convention", "note": "x"},
        },
        provenance=stamp([SNAP16]),
    )


def test_informational_print_cannot_settle(tmp_path):
    """The gap this task closes: an archived cohort print must be REFUSED
    by the fixing gate — archiving it is legitimate (it is published data),
    settling on it is not."""
    archive = PrintArchive(tmp_path)
    archive.append(_print("INFORMATIONAL", "390000000000.0000"))  # cohort estimate
    with pytest.raises(FixingValidationError, match="can never be a settlement input"):
        settle_from_archive(archive, EPOCH, SNAPSHOTS)


def test_settlement_print_still_settles(tmp_path):
    archive = PrintArchive(tmp_path)
    archive.append(_print("SETTLEMENT", "362412641743.4670"))
    fixing = settle_from_archive(archive, EPOCH, SNAPSHOTS)
    assert fixing.value == D("362412641743.4670")


def test_dual_series_settlement_value_ignores_cohort():
    """Belt to the fixing gate's braces: even inside one epoch's dual
    publication, the settlement accessor cannot see the cohort number."""
    dual = DualSeries(
        settlement=_print("SETTLEMENT", "362412641743.4670"),
        informational=_print("INFORMATIONAL", "390000000000.0000"),
    )
    assert dual.settlement_value == D("362412641743.4670")
    assert dual.settlement_value != dual.informational.s_life_years
