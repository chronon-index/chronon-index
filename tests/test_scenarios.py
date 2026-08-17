"""C-uc6-01 / AC-6.4: scenario format + test_deterministic_seeds (named)."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tly.scenarios import Scenario, run_scenario

D = Decimal
S0 = D("362412641743.4670")

BASE = Scenario(
    name="covid-replay-shape",
    seed=20260817,
    initial_s=S0,
    epochs=104,  # two years of weekly epochs
    weekly_growth=D("1.000138"),
    jitter_bp=2,
    shocks=((60, D("337000000")), (61, D("150000000"))),
)


def test_deterministic_seeds():
    """Named per AC-6.4: identical seeds → byte-identical outputs; a
    different seed diverges; the definition roundtrips through JSON."""
    a = run_scenario(BASE).render()
    b = run_scenario(BASE).render()
    assert a == b  # byte-identical

    reseeded = Scenario.from_dict({**BASE.to_dict(), "seed": 7})
    c = run_scenario(reseeded).render()
    assert c != a  # the jitter path actually depends on the seed

    roundtrip = Scenario.from_dict(BASE.to_dict())
    assert roundtrip == BASE
    assert run_scenario(roundtrip).render() == a


def test_scenario_semantics():
    result = run_scenario(BASE)
    assert len(result.m_series) == 105  # genesis + 104 epochs
    assert result.m_series[0] == S0
    assert result.shocks_applied == ((60, D("337000000")), (61, D("150000000")))
    # the shock epochs actually dent the series
    assert result.m_series[61] < result.m_series[60]


def test_no_jitter_is_pure_arithmetic():
    """jitter_bp=0: the seed is irrelevant and the series is exact
    compounding — the deterministic backbone under the stochastic skin."""
    quiet = Scenario(name="organic", seed=1, initial_s=S0, epochs=3, weekly_growth=D("1.0001"))
    quiet2 = Scenario(name="organic", seed=999, initial_s=S0, epochs=3, weekly_growth=D("1.0001"))
    r1, r2 = run_scenario(quiet), run_scenario(quiet2)
    assert r1.m_series == r2.m_series  # seed-independent without jitter
    assert r1.m_series[1] == S0 * D("1.0001")


def test_scenario_validation():
    with pytest.raises(ValueError, match="epochs must be positive"):
        Scenario(name="x", seed=1, initial_s=S0, epochs=0, weekly_growth=D("1"))
    with pytest.raises(ValueError, match="outside"):
        Scenario(
            name="x",
            seed=1,
            initial_s=S0,
            epochs=10,
            weekly_growth=D("1"),
            shocks=((10, D("1")),),
        )
