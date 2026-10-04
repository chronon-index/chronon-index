"""Dual run v2: regeneration + the findings that survived refutation."""

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
    assert fresh["baseline_sensitivity_cum_ppm"] == committed["baseline_sensitivity_cum_ppm"]
    assert fresh["panel_edge"] == committed["panel_edge"] == "2026-W27"
    assert fresh["negative_weeks"] == committed["negative_weeks"]


def test_findings_that_survived():
    r = run()
    # magnitude: every week within +-6 ppm of S under reporting-set coverage
    assert all(abs(Decimal(w["ppb_of_s"])) < 6000 for w in r["weeks"])
    # baseline dominance: defensible windows DISAGREE on sign — the point
    signs = {Decimal(v["cum_ppm"]) > 0 for v in r["baseline_sensitivity_cum_ppm"].values()}
    assert signs == {True, False}
    # reporting-set coverage is per-week and below the static 9.52%
    assert all(Decimal(w["reporting_set_coverage"]) < Decimal("9.52") for w in r["weeks"])
