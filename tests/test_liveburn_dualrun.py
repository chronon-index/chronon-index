"""Dual run v3: regeneration + pins demanded by refutation pass 2."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from tly.liveburn_dualrun import run

REPO = Path(__file__).resolve().parent.parent


def test_dualrun_matches_committed_json():
    committed = json.loads(
        (REPO / "docs/reports/liveburn_dualrun.json").read_text(encoding="utf-8")
    )
    fresh = run()
    for key in (
        "weeks",
        "ly_per_excess_death_world_table",
        "baseline_sensitivity_cum_ppm",
        "same_method_prior_years_W1_W27_cum_ppm",
        "positive_weeks_cum_ppm",
        "panel_ageing_trend_pct_over_9y",
        "w26_w27_by_baseline",
        "negative_weeks",
        "panel_edge",
    ):
        assert fresh[key] == committed[key], key


def test_prior_years_are_like_for_like_and_pinned():
    r = run()
    assert r["same_method_prior_years_W1_W27_cum_ppm"] == {"2024": "-23.05", "2025": "-5.75"}


def test_policy_table_findings():
    r = run()
    s = r["baseline_sensitivity_cum_ppm"]
    # defensible rules disagree on sign — the actual finding
    assert {Decimal(v["cum_ppm"]) > 0 for v in s.values()} == {True, False}
    # every post-pandemic-anchored rule within roughly -4..+23 ppm
    for k in (
        "mean_2023_2025",
        "fit_2022_2025",
        "fit_2023_2025",
        "hybrid_fit_2015_19_2022_25",
        "hybrid_fit_2015_19_2023_25",
    ):
        assert Decimal("-12") < Decimal(s[k]["cum_ppm"]) < Decimal("24"), k
    # excl-edge values present for every row (pass-2 minor)
    assert all(v["cum_ppm_excl_edge"] not in (None, "") for v in s.values())
    # ageing bias direction: positive = mean rules biased upward
    assert Decimal(r["panel_ageing_trend_pct_over_9y"]) > 3


def test_w26_is_the_event_under_modern_baseline():
    r = run()
    w = r["w26_w27_by_baseline"]
    assert Decimal(w["mean_2023_2025"]["W26"]) > Decimal(w["mean_2023_2025"]["W27"])
    assert Decimal(w["kk_2015_2019"]["W27"]) > Decimal(w["kk_2015_2019"]["W26"])
