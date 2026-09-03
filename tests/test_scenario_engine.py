"""Scenario engine + 1000-event catalog guards (model layer)."""

from __future__ import annotations

import json
from pathlib import Path

from tly.scenario_catalog import build_catalog
from tly.scenario_engine import Scenario, Shock, evaluate, load_inputs, project

REPO = Path(__file__).resolve().parent.parent


def _base():
    qx, pop = load_inputs()
    return qx, pop, project(qx, pop)


def test_catalog_is_exactly_1000_unique_reproducible():
    cat = build_catalog()
    assert len(cat) == 1000
    assert len({s.key for s in cat}) == 1000
    assert build_catalog()[0].key == cat[0].key  # deterministic


def test_baseline_sane_and_growing():
    qx, pop, base = _base()
    assert 360e9 < base.s[0] < 372e9  # ~0.9% above settlement level, documented
    assert abs(base.n[0] - 8_091_734_933) < 1e6
    assert base.s[-1] > base.s[0]  # WPP-medium world still grows through 2043
    assert all(-1.0 < g < 1.5 for g in base.g_pct())


def test_covid_anchor_reproduces_observed_drawdown():
    """The COVID-shaped event must land near the real ~-4% S drawdown."""
    qx, pop, base = _base()
    covid = Scenario(
        "anchor",
        "pandemic",
        "covid-shaped",
        (Shock(start=2026, duration=2, mort_mult={(60, 100): 1.25, (30, 59): 1.125}),),
    )
    o = evaluate(covid, base, qx, pop)
    assert -6.0 < o.max_drawdown_pct < -3.0


def test_mortality_shock_is_transient_fertility_is_compounding():
    """Finding 1: a one-year spike mean-reverts; a fertility shift compounds."""
    qx, pop, base = _base()
    spike = evaluate(
        Scenario("s", "t", "spike", (Shock(start=2026, duration=1, mort_mult={(0, 100): 1.5}),)),
        base,
        qx,
        pop,
    )
    fert = evaluate(
        Scenario("f", "t", "fert", (Shock(start=2026, duration=18, cbr_mult=0.7),)),
        base,
        qx,
        pop,
    )
    assert spike.ds_pct_h > spike.max_drawdown_pct / 2  # recovered most of it
    assert fert.ds_pct_h < fert.max_drawdown_pct + 0.01  # still at/near its worst


def test_breakthrough_only_moves_up():
    qx, pop, base = _base()
    o = evaluate(
        Scenario("b", "t", "seno", (Shock(start=2026, trend_mult=0.8, trend_age_lo=60),)),
        base,
        qx,
        pop,
    )
    assert o.max_drawdown_pct >= -1e-9 and o.ds_pct_h > 3.0


def test_results_json_regenerates():
    """The committed results file matches a fresh run (report is a rendering)."""
    committed = json.loads((REPO / "docs" / "reports" / "scenario_results.json").read_text())
    qx, pop, base = _base()
    cat = build_catalog()
    sample = {r["key"]: r for r in committed["results"]}
    for s in cat[::97]:  # every 97th of 1000 — 11 spot checks
        fresh = evaluate(s, base, qx, pop)
        assert abs(fresh.max_drawdown_pct - sample[s.key]["max_drawdown_pct"]) < 1e-9
        assert abs(fresh.ds_pct_h - sample[s.key]["ds_pct_h"]) < 1e-9
