"""B-uc2-07 / AC-2.2 / invariant P7: coverage honesty is schema-enforced.

The named test builds a REAL print — WMD feed, kk-linear baselines, real
CoverageRecords for Germany and Albania — and proves that stripping the
measured-vs-imputed share makes schema validation fail. A print may not
omit its own honesty.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.baseline import coverage_block, coverage_metadata, fit_baseline
from tly.prints import PrintSchemaError, WeeklyPrint, validate_print_dict
from tly.stock import stamp
from tly.wmd import parse_wmd

REPO = Path(__file__).resolve().parent.parent
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"
WMD = REPO / "data" / "snapshots" / "2026-08-17" / "wmd_world_mortality.csv"

D = Decimal


def _real_coverage() -> dict:
    cells = parse_wmd(WMD, countries={"DEU", "ALB"})
    records = []
    for iso3 in ("DEU", "ALB"):
        bl = fit_baseline(cells, iso3)
        records.append(coverage_metadata(cells, bl, 2021))
    return coverage_block(records)


def _real_print(coverage: dict) -> WeeklyPrint:
    return WeeklyPrint(
        epoch_utc="2026-08-17T12:00:00+00:00",
        series_label="SETTLEMENT",
        s_life_years=D("362412641743.467008807750"),
        e_bar_years=D("44.7880"),
        n_persons=D("8091734933"),
        burn_life_years=D("0"),
        coverage=coverage,
        provenance=stamp([SNAP16]),
    )


def test_p7_coverage_honesty():
    """Named per RP Part X: a print without the measured-vs-imputed share
    fails schema validation; with it, the same print passes."""
    coverage = _real_coverage()
    good = _real_print(coverage).to_json_dict()
    validate_print_dict(good)  # honest print passes

    dishonest = _real_print(coverage).to_json_dict()
    del dishonest["coverage"]["measured_share"]
    with pytest.raises(PrintSchemaError, match="measured_share is required"):
        validate_print_dict(dishonest)

    coverless = _real_print(coverage).to_json_dict()
    del coverless["coverage"]
    with pytest.raises(PrintSchemaError, match="missing required fields"):
        validate_print_dict(coverless)


def test_coverage_block_real_values():
    """DEU (weekly, near-complete 2021) and ALB (monthly, complete 2021):
    the block carries each country's own share plus the plain aggregate."""
    block = _real_coverage()
    assert set(block["by_country"]) == {"ALB", "DEU"}
    assert block["period_universe"] == {"ALB": "monthly", "DEU": "weekly"}
    assert block["by_country"]["ALB"] == D(1)  # all 12 months measured
    assert block["by_country"]["DEU"] > D("0.9")
    # aggregate is measured/total across both period universes
    assert D("0.9") < block["measured_share"] <= D(1)


def test_coverage_block_rejects_empty():
    with pytest.raises(ValueError, match="at least one CoverageRecord"):
        coverage_block([])
