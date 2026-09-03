"""S-05: normative property tests for the Saeculum reference contract
(mirrored by tly/token_model.py; an auditor diffs model vs .sol)."""

from __future__ import annotations

import pytest

from tly.token_model import TOTAL_GONS, SaeculumModel, TokenError

S0 = 362_412_641_743 * 10**9  # ~S in 1e-9 life-year quanta
S1 = 363_511_706_093 * 10**9  # the v0.7.0 level


def _fresh():
    m = SaeculumModel(S0, oracle="oracle", deployer="genesis")
    m.transfer("genesis", "alice", 1_000_000 * 10**9)
    m.transfer("genesis", "bob", 250_000 * 10**9)
    return m


def test_p_share_invariance_under_rebase():
    """THE property: a rebase moves no one's gons — every share of
    humanity's remaining time is untouched; only balances rescale."""
    m = _fresh()
    gons_before = dict(m.gons)
    shares_before = {w: g / TOTAL_GONS for w, g in m.gons.items()}
    m.rebase("oracle", 1, S1, "hash1")
    assert m.gons == gons_before
    assert {w: g / TOTAL_GONS for w, g in m.gons.items()} == shares_before
    # balances scaled UP with S (more time -> more tokens, same share)
    assert m.balance_of("alice") > 1_000_000 * 10**9 * 999 // 1000


def test_p_mortality_neutrality_path_independence():
    """Rebase 5 times vs once to the same final S: identical balances."""
    a, b = _fresh(), _fresh()
    for i, s in enumerate((S0 - 10**15, S0 + 3 * 10**15, S1 - 10**14, S1 + 10**13, S1)):
        a.rebase("oracle", i + 1, s, f"h{i}")
    b.rebase("oracle", 1, S1, "h")
    for w in ("genesis", "alice", "bob"):
        assert a.balance_of(w) == b.balance_of(w)


def test_p_conservation_and_floor_never_mints():
    m = _fresh()
    total_before = sum(m.gons.values())
    for i in range(50):
        m.transfer("alice", "bob", 7 + i * 13)
    assert sum(m.gons.values()) == total_before == TOTAL_GONS
    # sum of balances never exceeds supply (floors can only lose dust)
    assert sum(m.balance_of(w) for w in m.gons) <= m.total_supply


def test_p_monotonic_epoch_first_print_settles():
    m = _fresh()
    m.rebase("oracle", 10, S1, "h")
    with pytest.raises(TokenError, match="EpochNotMonotonic"):
        m.rebase("oracle", 10, S0, "replay")
    with pytest.raises(TokenError, match="EpochNotMonotonic"):
        m.rebase("oracle", 9, S0, "reorder")
    with pytest.raises(TokenError, match="NotOracle"):
        m.rebase("mallory", 11, S0 // 2, "attack")


def test_model_mirrors_contract_source():
    """The .sol and the model must state the same constants and revert
    conditions — the cheap structural half of the audit diff."""
    from pathlib import Path

    sol = (Path(__file__).resolve().parent.parent / "contracts" / "Saeculum.sol").read_text()
    assert "10 ** 30" in sol and TOTAL_GONS == 10**30
    assert "decimals = 9" in sol
    for err in ("NotOracle", "EpochNotMonotonic", "ZeroSupply"):
        assert err in sol
    assert "epoch <= lastEpoch" in sol  # first-print-settles on-chain
    assert "_gons[who] * totalSupply) / TOTAL_GONS" in sol  # mul-then-div form
