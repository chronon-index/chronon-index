"""Item 3: the dual run regenerates from committed artifacts."""

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
    assert fresh["cumulative_ppm_of_s"] == committed["cumulative_ppm_of_s"]
    assert fresh["panel_edge"] == committed["panel_edge"] == "2026-W27"
    assert fresh["coverage_share"] == committed["coverage_share"]
    assert len(fresh["weeks"]) == len(committed["weeks"])


def test_findings_hold():
    r = run()
    # magnitude: every week within +-5 ppm of S
    assert all(abs(Decimal(w["ppb_of_s"])) < 5000 for w in r["weeks"])
    # the sign finding: 2026 cumulative is NEGATIVE (below-baseline mortality)
    assert Decimal(r["cumulative_ppm_of_s"]) < 0
    # amplification factor stated honestly
    assert Decimal(r["noise_amplification"]) > 10
