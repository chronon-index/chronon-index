"""C-uc6-05: jump scaffolding — honest fixtures, refusal-to-fit enforced."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tly.jumps import (
    CALIBRATED,
    HISTORICAL_SHOCK_SET,
    PENDING,
    NotCalibratedError,
    fit_frequency_severity,
    pending_events,
)

D = Decimal


def test_shock_set_shape():
    names = [e.name for e in HISTORICAL_SHOCK_SET]
    assert len(names) == 4
    assert any("1918" in n for n in names)
    assert any("War" in n for n in names)
    assert any("HIV" in n for n in names)
    assert any("COVID" in n for n in names)


def test_covid_entry_matches_decisions():
    """The single calibrated entry carries exactly the DECISIONS.md
    anchors — nothing more precise than the record supports."""
    covid = next(e for e in HISTORICAL_SHOCK_SET if "COVID" in e.name)
    assert covid.status == CALIBRATED
    assert covid.excess_deaths == D("14830000")  # WHO 14.83M
    assert covid.life_years_burned_low == D("148000000")
    assert covid.life_years_burned_high == D("337000000")


def test_pending_events_carry_no_numbers():
    """The honesty core: PENDING events have pointers, never values."""
    pend = pending_events()
    assert len(pend) == 3
    for e in pend:
        assert e.excess_deaths is None
        assert e.life_years_burned_low is None
        assert e.life_years_burned_high is None
        assert e.sources, e.name
        assert all("(verify)" in s or "DECISIONS" in s for s in e.sources), e.name


def test_fit_refuses_incomplete_set():
    """Named contract: no parameters from an incomplete set, and the error
    names every missing event."""
    with pytest.raises(NotCalibratedError) as exc:
        fit_frequency_severity()
    msg = str(exc.value)
    for name in ("1918", "World War II", "HIV"):
        assert name in msg
    assert "never invent" in msg


def test_fit_on_fully_calibrated_set_is_explicitly_unimplemented():
    """When the set IS complete, the scaffold must not silently pretend to
    fit — it raises NotImplementedError pointing at the successor task."""
    calibrated = tuple(
        e
        if e.status == CALIBRATED
        else type(e)(
            name=e.name,
            period=e.period,
            status=CALIBRATED,
            excess_deaths=D("1"),
            life_years_burned_low=D("1"),
            life_years_burned_high=D("2"),
            sources=e.sources,
        )
        for e in HISTORICAL_SHOCK_SET
    )
    with pytest.raises(NotImplementedError, match="successor task"):
        fit_frequency_severity(calibrated)


def test_pending_marker_is_verify_flavored():
    assert "(verify)" in PENDING
