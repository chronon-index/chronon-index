"""B-uc2-12 (backfill engine) + B-uc2-13 (COVID-drag gate, AC-2.3).

The gate test is the Phase B milestone: 570 consecutive weekly rows
ending at the current epoch, the COVID drag visible, and the cumulative
measured burn inside the recalibrated 120–360M life-year band.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

from tly.backfill import (
    backfill_series,
    load_annual_structures,
)

REPO = Path(__file__).resolve().parent.parent
FIXTURE = (
    REPO / "data" / "snapshots" / "2026-08-17" / "fixtures" / "wpp_world_annual_2010_2023.json"
)
WMD = REPO / "data" / "snapshots" / "2026-08-17" / "wmd_world_mortality.csv"
OWID_BD = REPO / "data" / "snapshots" / "2026-08-16" / "owid_births_deaths_world.csv"
END_EPOCH = "2026-08-24T12:00:00+00:00"  # the latest ARCHIVED real epoch

D = Decimal
B = D(10) ** 9


def test_annual_structures_pin():
    s = load_annual_structures(FIXTURE)
    assert set(s) == set(range(2010, 2024))
    # cross-check against the independently pinned engine values
    assert str((s[2023].s_life_years / B).quantize(D("0.0001"))) == "363.5117"
    assert str((s[2019].s_life_years / B).quantize(D("0.0001"))) == "354.4515"


def test_covid_drag_in_annual_deltas():
    """First visibility channel: the annual deltas do not merely slow in
    the COVID years — S FALLS. deltas[y] = S(y+1) − S(y): the delta INTO
    2020 and INTO 2021 are both negative against a ~+3.7B/yr pre-COVID
    trend, then 2022 rebounds hard (mortality recovery + WPP structure)."""
    s = load_annual_structures(FIXTURE)
    deltas = {y: s[y + 1].s_life_years - s[y].s_life_years for y in range(2010, 2023)}
    pre = sum(deltas[y] for y in range(2014, 2019)) / 5  # into 2015..2019
    assert pre > D(3) * B  # healthy pre-COVID growth ≈ +3.7B/yr
    assert deltas[2019] < 0  # S falls INTO 2020 (−4.2B)
    assert deltas[2020] < 0  # and again INTO 2021 (−6.0B)
    assert deltas[2021] > pre  # the 2022 rebound overshoots trend (+14.9B)


def test_backfill_570_weeks_ending_at_current_epoch():
    rows = backfill_series(FIXTURE, WMD, END_EPOCH, weeks=570)
    assert len(rows) == 570
    assert rows[-1].epoch_utc == END_EPOCH
    # consecutive Mondays, no gaps
    for a, b_ in zip(rows, rows[1:]):
        gap = datetime.fromisoformat(b_.epoch_utc) - datetime.fromisoformat(a.epoch_utc)
        assert gap == timedelta(days=7)
    # real-time structure discipline
    for r in rows:
        year = datetime.fromisoformat(r.epoch_utc).year
        assert r.structure_year == min(year - 1, 2023)
    # plateau weeks carry, measured weeks step
    assert all(r.carried for r in rows if r.structure_year == 2023)
    assert not any(r.carried for r in rows if r.structure_year < 2023)


def test_backfill_p6_closure_within_measured_years():
    """The weekly path lands EXACTLY on the next annual structure at each
    year boundary (E11 closure at micro-quantum precision)."""
    s = load_annual_structures(FIXTURE)
    rows = backfill_series(FIXTURE, WMD, END_EPOCH, weeks=570)
    by_year: dict[int, list] = {}
    for r in rows:
        by_year.setdefault(datetime.fromisoformat(r.epoch_utc).year, []).append(r)
    for year, yr_rows in by_year.items():
        if year >= 2024 or year == min(by_year):  # plateau, or partial first year
            continue
        last = yr_rows[-1]
        if (
            datetime.fromisoformat(last.epoch_utc)
            == datetime.fromisoformat(f"{year}-12-31T12:00:00+00:00")
            or last.epoch_utc.startswith(f"{year}-12-2")
            or last.epoch_utc.startswith(f"{year}-12-3")
        ):
            target = s[year].s_life_years
            assert abs(last.s_life_years - target) < D("0.000001") * 60


def test_b_uc2_13_covid_gate():
    """THE AC-2.3 GATE. The WMD panel measures ~36% of world deaths, so
    the gate figure is the COVERAGE-ADJUSTED global estimate
    (measured / coverage — both sides data, zero free parameters), with
    the measured number and the coverage share published beside it (P7:
    measured and imputed never conflated). No profile tuning anywhere."""
    from tly.backfill import covid_gate_report

    report = covid_gate_report(FIXTURE, WMD, OWID_BD)
    measured_m = report.measured_burn_life_years / D(10) ** 6
    adjusted_m = report.adjusted_burn_life_years / D(10) ** 6
    assert D(55) < measured_m < D(75)  # the honest measured-panel figure
    assert D("0.30") < report.coverage_share < D("0.45")
    assert D(120) < adjusted_m < D(360), (
        f"coverage-adjusted 2020-21 burn {adjusted_m:.1f}M outside the gate band"
    )
    # drag visible weekly: the worst measured week burns >1M life-years
    assert report.worst_week[0] in (2020, 2021)
    assert report.worst_week_burn > D(10) ** 6
