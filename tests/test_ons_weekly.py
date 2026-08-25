"""B-uc2-18: the ONS England & Wales weekly-deaths adapter, against the
committed 2025-v45 + 2026-v20 fixture (E92000001 + W92000004 rows)."""

from __future__ import annotations

from decimal import Decimal as D
from pathlib import Path

import pytest

from tly.ons_weekly import (
    GEO_ENGLAND,
    OCCURRENCES,
    OnsFormatError,
    ew_weekly_totals,
    parse_ons_weekly,
)

FIXTURE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "snapshots"
    / "2026-08-25"
    / "fixtures"
    / "ons_weekly_deaths_ew_2025_2026.csv.gz"
)


def _cells():
    return parse_ons_weekly(FIXTURE)


def test_parse_shape_and_decimal():
    cells = _cells()
    assert len(cells) == 21252
    assert {c.geography for c in cells} == {"E92000001", "W92000004"}
    assert {c.basis for c in cells} == {"registrations", "occurrences"}
    assert all(isinstance(c.deaths, D) for c in cells)


def test_ew_registration_totals_full_2025_plus_partial_2026():
    totals = ew_weekly_totals(_cells())
    weeks_2025 = [w for (y, w) in totals if y == 2025]
    weeks_2026 = [w for (y, w) in totals if y == 2026]
    assert sorted(weeks_2025) == list(range(1, 53))  # mature full year
    assert sorted(weeks_2026) == list(range(1, 26))  # in-progress edition
    # sanity magnitude: E&W weekly all-cause deaths run ~8-14k
    assert all(D(7000) < v < D(16000) for v in totals.values())


def test_occurrence_basis_is_a_distinct_series():
    reg = ew_weekly_totals(_cells())
    occ = ew_weekly_totals(_cells(), basis=OCCURRENCES)
    assert set(occ) == set(reg)
    assert any(occ[k] != reg[k] for k in reg)  # bases genuinely differ


def test_partial_national_total_refused():
    cells = [c for c in _cells() if not (c.geography == GEO_ENGLAND and c.week == 7)]
    with pytest.raises(OnsFormatError, match="missing national half"):
        ew_weekly_totals(cells)


def test_malformed_rows_raise(tmp_path):
    import gzip

    header = (
        "v4_0,calendar-years,Time,administrative-geography,Geography,"
        "week-number,Week,sex,Sex,age-groups,AgeGroups,"
        "registration-or-occurrence,RegistrationOrOccurrence"
    )
    bad = (
        header
        + "\nxx,2025,2025,E92000001,England,week-1,Week 1,all,All,all-ages,All ages,registrations,Registrations\n"
    )
    p = tmp_path / "bad.csv.gz"
    p.write_bytes(gzip.compress(bad.encode()))
    with pytest.raises(OnsFormatError, match="non-integer count"):
        parse_ons_weekly(p)
