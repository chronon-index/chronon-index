"""D-03: deterministic error budget — quadrature, one-sided listing, statement."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tly.error_budget import (
    one_sided_terms,
    SYMMETRIC_TERMS,
    build_error_budget,
    quadrature_pct,
)
from tly.guard import FloatContaminationError

D = Decimal
S_V0 = D("362412641743.467008807750")  # the golden full-precision S


def test_quadrature_is_root_sum_of_squares():
    # 1.0² + 1.5² + 0.5² = 3.5; √3.5 = 1.8708…
    assert quadrature_pct() * quadrature_pct() == D("3.5").quantize(
        (quadrature_pct() * quadrature_pct()).normalize()
    ) or abs(quadrature_pct() ** 2 - D("3.5")) < D("1e-30")
    assert str(quadrature_pct().quantize(D("0.0001"))) == "1.8708"


def test_interval_brackets_measured_s():
    budget = build_error_budget(S_V0)
    lo, hi = budget.interval
    assert lo < S_V0 < hi
    # ±1.87% of 362.41B ≈ ±6.78B
    assert (D("6.7") * 10**9) < (hi - S_V0) < (D("6.9") * 10**9)


def test_cohort_band_applies_one_sided_bounds():
    budget = build_error_budget(S_V0)
    lo, hi = budget.cohort_band
    assert lo == S_V0 * D("1.05")  # +2% +3%
    assert hi == S_V0 * D("1.12")  # +3% +9% (v0.6.0 band)


def test_archived_version_reproduces_its_own_band():
    """Version-keyed bounds: v0.5.0 prints must keep reproducing under
    the +3-8% band that made them — never HEAD's widened band."""
    budget = build_error_budget(S_V0, version="v0.5.0-reconstruction")
    lo, hi = budget.cohort_band
    assert hi == S_V0 * D("1.11")
    text = budget.statement()
    assert "381-402B" in text and "period_vs_cohort_pct +3-8%" in text


def test_statement_is_computed_not_hand_typed():
    budget = build_error_budget(S_V0)
    text = budget.statement()
    assert "362.4B" in text  # computed from S, quantized
    assert "1.9%" in text  # computed quadrature, quantized to 0.1
    assert "381-406B" in text  # COMPUTED v0.6.0 band (the A-16-blessed 381-402B is v0.5.0's)
    assert "never netted" in text
    assert "vintage_lag_pct +2-3%" in text
    assert "period_vs_cohort_pct +3-9%" in text


def test_one_sided_terms_never_enter_quadrature():
    """The structural terms are absent from the symmetric set — netting or
    quadrature-mixing them is the exact error Part VIII forbids."""
    assert set(SYMMETRIC_TERMS) & set(one_sided_terms()) == set()
    assert all(lo <= hi for lo, hi in one_sided_terms().values())
    # quadrature depends only on the symmetric terms: 3 terms, √3.5
    assert len(SYMMETRIC_TERMS) == 3


def test_input_discipline():
    with pytest.raises(FloatContaminationError):
        build_error_budget(362.4e9)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="positive"):
        build_error_budget(D("0"))
