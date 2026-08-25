"""C-uc6-04: the vintage backtest harness — bias measured, not asserted."""

from __future__ import annotations

from pathlib import Path

from tly.backtest import backtest

REPO = Path(__file__).resolve().parent.parent
S = REPO / "data" / "snapshots" / "2026-08-25"
MAGEC = S / "eurostat_demo_magec_it_de_se.json"
PJAN = S / "eurostat_demo_pjan_it_de_se.json"


def test_backtest_structure_and_pins():
    r = backtest(MAGEC, PJAN, "IT")
    assert r.fit_years == (1990, 2005)
    assert r.test_years == tuple(range(2006, 2025))
    assert set(r.realized_e0) == set(r.projected_e0) == set(r.test_years)
    # pinned bias figures (regression anchors from the committed snapshot)
    assert f"{r.bias:+.3f}" == "+0.405"
    assert f"{r.mae:.3f}" == "0.459"


def test_pre_covid_skill_and_covid_blindness():
    """The honest shape: over 14 pre-COVID out-of-sample years the model
    is within ~0.6y of realized e0; in 2020-21 it overshoots because a
    period model cannot foresee a shock — the reason the index carries a
    separate jump/burn channel (E8) instead of trusting the trend."""
    for geo, pre_bound in (("IT", 0.35), ("DE", 0.75), ("SE", 0.25)):
        r = backtest(MAGEC, PJAN, geo)
        pre = tuple(y for y in r.test_years if y < 2020)
        assert abs(r.bias_over(pre)) < pre_bound
    it = backtest(MAGEC, PJAN, "IT")
    assert it.bias_over((2020, 2021)) > 1.0  # COVID blindness, quantified
    assert it.projected_e0[2020] - it.realized_e0[2020] > 1.2


def test_jump_off_correction_measured_both_ways():
    """Anchoring helps where the fit's end-state is representative (IT,
    SE) and HURTS where the anchor year is atypical (DE) — measured
    honestly, not assumed beneficial."""

    def maes(geo):
        r = backtest(MAGEC, PJAN, geo)
        anch = r.mae
        unanch = sum(
            abs(r.projected_e0_unanchored[y] - r.realized_e0[y]) for y in r.test_years
        ) / len(r.test_years)
        return anch, unanch

    it_a, it_u = maes("IT")
    de_a, de_u = maes("DE")
    assert it_a < it_u  # correction helps Italy
    assert de_a > de_u  # and hurts Germany — recorded, not hidden
