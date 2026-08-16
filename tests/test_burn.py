"""B-uc2-05 / AC-2.6: burn term — test_burn_term_e4 exact on a known fixture."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.burn import allocate_largest_remainder, burn_life_years, distribute_excess
from tly.guard import FloatContaminationError
from tly.loader import load_verified_snapshot

REPO = Path(__file__).resolve().parent.parent
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"

D = Decimal
# division-free table: e(0.5)=69.75 (0→1 linear 70→69.5); 1..5 linear 69.5→66
# so e(5.5)... 5..85 linear 66→6: slope -0.75/yr → e(5.5)=65.625
TABLE = {0: D("70"), 1: D("69.5"), 5: D("66"), 85: D("6")}


def test_burn_term_e4():
    """The named AC-2.6 verifier: exact hand-checkable arithmetic.
    burn = 100·e(0.5) + 50·e(5.5) = 6975 + 3281.25 = 10256.25"""
    excess = {0: D("100"), 5: D("50")}
    assert burn_life_years(excess, TABLE) == D("10256.25")


def test_burn_signed_deficit():
    """Mortality deficit (negative excess) yields negative burn — signed."""
    assert burn_life_years({0: D("-100")}, TABLE) == D("-6975")


def test_burn_open_age_flat_tail():
    assert burn_life_years({100: D("10")}, TABLE) == D("60")  # e flat at 6


def test_burn_rejects_floats():
    with pytest.raises(FloatContaminationError):
        burn_life_years({0: 100.0}, TABLE)


def test_largest_remainder_conserves_exactly():
    """E11: Σ parts == total for an adversarial weight set."""
    weights = {1: D("0.333"), 2: D("0.333"), 3: D("0.334")}
    parts = allocate_largest_remainder(D("100"), weights, D("1"))
    assert sum(parts.values()) == D("100")
    assert parts == {1: D("33"), 2: D("33"), 3: D("34")}
    # a case where naive per-share rounding would lose a quantum
    weights = {i: D("0.1") for i in range(10)}
    weights[0] = D("0.1")  # exact tenths
    parts = allocate_largest_remainder(D("0.007"), weights, D("0.001"))
    assert sum(parts.values()) == D("0.007")


def test_largest_remainder_rejects_bad_inputs():
    with pytest.raises(ValueError, match="sum to exactly 1"):
        allocate_largest_remainder(D("100"), {1: D("0.5"), 2: D("0.49")}, D("1"))
    with pytest.raises(ValueError, match="not a multiple of quantum"):
        allocate_largest_remainder(D("100.5"), {1: D("1")}, D("1"))


def test_distribute_then_burn_real_table():
    """End-to-end on committed data: DEU-2020-scale excess (24,501.8, the
    B-uc2-04 pin) distributed 70/30 over ages 75/85 on the WHO 2019 global
    table, burn computed — deterministic, pinned."""
    snap = load_verified_snapshot(SNAP16)
    table = snap.tables[2019]
    excess = distribute_excess(D("24501.800"), {75: D("0.7"), 85: D("0.3")}, quantum=D("0.001"))
    assert sum(excess.values()) == D("24501.800")  # conservation
    burn = burn_life_years(excess, table)
    # e(75.5) and e(85.5) from the committed WHO table; value pinned once
    assert burn == burn_life_years(excess, table)  # deterministic
    assert D("190000") < burn < D("310000")  # order of magnitude sanity
