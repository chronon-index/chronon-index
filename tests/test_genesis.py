"""C-uc5-07 / AC-5.6: genesis M = κ·S (κ=1), hours/minutes display, Decimal only."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tly.gons import (
    HOURS_PER_YEAR,
    KAPPA,
    GonsError,
    genesis_ledger,
    tokens_to_hours_minutes,
)
from tly.guard import FloatContaminationError
from tly.pipeline import build_settlement_print

D = Decimal


def test_genesis_m_equals_s_exactly():
    """κ = 1: the money supply IS the real measured stock — proven against
    the live pipeline's S, full precision, no quantization anywhere."""
    p = build_settlement_print("2026-08-17T12:00:00+00:00")
    lg = genesis_ledger(p.s_life_years)
    assert KAPPA == 1
    assert lg.m == p.s_life_years  # exact, prec-34 string-equal
    assert str(lg.m) == str(p.s_life_years)


def test_hours_display_convention():
    assert HOURS_PER_YEAR == D(8766)  # 365.25 days x 24 h (DECISIONS default)
    assert tokens_to_hours_minutes(D(1)) == (8766, 0)  # one token = one year
    assert tokens_to_hours_minutes(D("0.5")) == (4383, 0)
    assert tokens_to_hours_minutes(D("0.0001")) == (0, 52)  # floors the minute
    assert tokens_to_hours_minutes(D(0)) == (0, 0)


def test_display_floors_never_overstates():
    """One minute of remaining time is 1/(8766*60) tokens; a hair less
    must display as zero minutes, never rounded up."""
    one_minute = D(1) / (HOURS_PER_YEAR * 60)
    just_under = one_minute * D("0.999")
    assert tokens_to_hours_minutes(one_minute) == (0, 1)
    assert tokens_to_hours_minutes(just_under) == (0, 0)


def test_decimal_end_to_end():
    with pytest.raises(FloatContaminationError):
        genesis_ledger(362412641743.4670)  # type: ignore[arg-type]
    with pytest.raises(FloatContaminationError):
        tokens_to_hours_minutes(1.0)  # type: ignore[arg-type]
    with pytest.raises(GonsError, match="negative time"):
        tokens_to_hours_minutes(D("-1"))
