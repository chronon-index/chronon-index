"""D-04: cohort-S (E6) — the INFORMATIONAL series gets real values."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from tly.cohort import cohort_e, cohort_s, informational_print, load_qx_surface
from tly.prints import DualSeries, validate_print_dict
from tly.wpp import parse_population_single_age, population_by_age

REPO = Path(__file__).resolve().parent.parent
SURFACE = (
    REPO / "data" / "snapshots" / "2026-08-25" / "fixtures" / "wpp_world_qx_surface_2010_2100.json"
)
POP_FIX = (
    REPO / "data" / "snapshots" / "2026-08-17" / "fixtures" / "wpp_pop_single_age_fixture.csv.gz"
)
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"
SNAP25 = REPO / "data" / "snapshots" / "2026-08-25"

D = Decimal
B = D(10) ** 9
PERIOD_S_2023 = D("363.5117")  # the pinned WPP-table period S, billions


def _inputs():
    surface = load_qx_surface(SURFACE)
    pop = parse_population_single_age(POP_FIX, {2023}, locations={"World"})
    return surface, population_by_age(pop, "World", 2023)


def test_cohort_e_exceeds_period_e_and_declines_with_age():
    surface, _ = _inputs()
    e0 = cohort_e(surface, 0, 2023)
    assert str(e0.quantize(D("0.0001"))) == "78.0502"  # pinned
    assert e0 > D("73.17")  # period e0 on the same table year
    ages = [0, 20, 40, 65, 85]
    es = [cohort_e(surface, a, 2023) for a in ages]
    assert all(b < a for a, b in zip(es, es[1:]))  # monotone in age


def test_cohort_s_pinned_and_inside_the_blessed_band():
    surface, pop = _inputs()
    cs = cohort_s(surface, pop, 2023)
    assert str((cs / B).quantize(D("0.0001"))) == "392.8260"  # pinned
    # DECISIONS band per ruling D6 (computed 381-402B): we land inside
    assert D(381) * B < cs < D(402) * B


def test_period_vs_cohort_term_measured_finding():
    """A FINDING, recorded as a test: the computed period-vs-cohort uplift
    is +8.06% — 0.06pp ABOVE the error budget's recorded +3-8% upper
    bound. Per computed-beats-prose (ruling D6) the budget term is due a
    version-bump proposal; until then this test documents the exceedance
    honestly instead of hiding it."""
    surface, pop = _inputs()
    uplift_pct = (cohort_s(surface, pop, 2023) / B / PERIOD_S_2023 - 1) * 100
    assert D("7.9") < uplift_pct < D("8.2")  # regression pin
    assert uplift_pct > D(8)  # the exceedance IS the finding


def test_informational_print_slots_into_dual_series():
    surface, pop = _inputs()
    info = informational_print(surface, pop, 2023, "2026-08-24T12:00:00+00:00", [SNAP16, SNAP25])
    validate_print_dict(info.to_json_dict())
    assert info.series_label == "INFORMATIONAL"
    assert info.coverage["measured_share"] == D(0)  # model content, stated
    assert info.accuracy["uncertainty"]["type"] == "interval"

    from tly.pipeline import build_settlement_print

    settlement = build_settlement_print("2026-08-24T12:00:00+00:00")
    dual = DualSeries(settlement=settlement, informational=info)
    assert dual.settlement_value == settlement.s_life_years  # untouched
    assert dual.informational.s_life_years > dual.settlement_value
