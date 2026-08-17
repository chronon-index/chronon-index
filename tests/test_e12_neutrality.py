"""C-uc5-06 / AC-5.3 / RP Part IX E12 / DECISIONS #4: the two neutrality
properties, machine-checked (the METHODOLOGY §6 proofs as tests).

- Wealth neutrality: wallet value = s_i × MarketCap. A rebase changes
  supply, not shares; with market cap exogenous, d(value)/d(rebase) = 0
  and the value RATIO between any two wallets is rebase-invariant.
- Mortality neutrality: a mass-death down-rebase (the DECISIONS COVID
  calibration: 148–337M life-years ≈ 0.04–0.09% of S) leaves every share
  untouched — d(s_i)/d(deaths) = 0 — and shrinks every balance by the SAME
  factor: nobody's slice of humanity's remaining time grows because part
  of humanity died.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from tly.gons import G_TOTAL, GonsLedger, display_balances

D = Decimal
S0 = D("362412641743.4670")
COVID_BURN = D("337000000")  # upper DECISIONS band, life-years


def _populated() -> GonsLedger:
    lg = GonsLedger(S0)
    lg.transfer_gons("GENESIS", "alice", 3 * 10**29)
    lg.transfer_gons("GENESIS", "bob", 10**29 + 7)
    lg.transfer_gons("GENESIS", "carol", 12345678901234567890)
    return lg


def _values(lg: GonsLedger, market_cap: Fraction) -> dict[str, Fraction]:
    """value_i = s_i × C in EXACT rational arithmetic — no rounding can
    manufacture or hide a violation."""
    return {w: Fraction(lg.gons(w), G_TOTAL) * market_cap for w in lg.wallets()}


def test_e12_neutrality():
    """Named per SPEC AC-5.3: both properties through a realistic epoch
    sequence — organic growth, then the COVID-scale burn."""
    lg = _populated()
    cap = Fraction(76_245_800_000_000)  # exogenous market cap (any number)

    v0 = _values(lg, cap)
    lg.rebase(lg.m * D("1.000138"))  # one organic weekly epoch (+0.72%/yr / 52)
    assert _values(lg, cap) == v0  # wealth neutrality: d(value)/d(rebase)=0

    shares_before = {w: lg.share(w) for w in lg.wallets()}
    balances_before = {w: lg.balance(w) for w in lg.wallets()}
    m_before = lg.m

    burned_m = m_before - COVID_BURN  # symmetric down-rebase on mass death
    lg.rebase(burned_m)

    assert {w: lg.share(w) for w in lg.wallets()} == shares_before  # d(s)/d(deaths)=0
    assert _values(lg, cap) == v0  # value untouched by the shock itself

    factor = burned_m / m_before
    for wallet, before in balances_before.items():
        after = lg.balance(wallet)
        assert after == before * factor  # pro-rata, same factor for all
        assert after < before  # every balance shrinks; no share grows


def test_e12_value_ratio_invariant_under_any_rebase():
    lg = _populated()
    cap = Fraction(549_000_000_000_000)  # UBS-scale wealth denominator
    v = _values(lg, cap)
    ratio_ab = v["alice"] / v["bob"]
    for f in ("0.5", "3.14159", "0.0001", "42"):
        lg.rebase(lg.m * D(f))
        v2 = _values(lg, cap)
        assert v2["alice"] / v2["bob"] == ratio_ab  # exact Fraction equality


def test_e12_display_layer_shrinks_prorata_too():
    """The published (E11) balances obey the same neutrality: after the
    shock every displayed balance is <= its pre-shock value."""
    lg = _populated()
    before = display_balances(lg)
    lg.rebase(lg.m - COVID_BURN)
    after = display_balances(lg)
    assert set(after) == set(before)
    assert all(after[w] <= before[w] for w in before)
    assert sum(after.values()) < sum(before.values())
