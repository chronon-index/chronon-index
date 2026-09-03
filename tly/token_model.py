"""Executable model of contracts/Saeculum.sol (S-05 pre-audit artifact).

Mirrors the Solidity reference 1:1 in integer arithmetic (uint256
semantics: floor division everywhere, no floats, no Decimal) so the
property tests here are NORMATIVE for the contract: an auditor diffs
the two side by side; any behavioral divergence is a bug in one of
them. Properties under test:

- P-share (share invariance): a rebase changes NO wallet's gons, hence
  no wallet's share of TOTAL_GONS.
- P-mortality-neutrality: rebases in any order to the same final S
  give identical balances (path independence).
- P-conservation: transfers conserve total gons exactly; balance
  conversion floors, so a transfer can never mint value.
- P-monotonic-epoch: a replayed or reordered epoch reverts (the
  contract-side first-print-settles).
"""

from __future__ import annotations

TOTAL_GONS = 10**30
DECIMALS = 9


class TokenError(AssertionError):
    pass


class SaeculumModel:
    def __init__(self, initial_supply: int, oracle: str, deployer: str):
        if initial_supply <= 0:
            raise TokenError("ZeroSupply")
        self.total_supply = initial_supply
        self.oracle = oracle
        self.last_epoch = 0
        self.last_record_hash = ""
        self.gons: dict[str, int] = {deployer: TOTAL_GONS}

    def balance_of(self, who: str) -> int:
        # multiply-then-divide (see the .sol comment): guarantees
        # sum(balances) <= total_supply; the floored-gpf form violated it
        return self.gons.get(who, 0) * self.total_supply // TOTAL_GONS

    def rebase(self, sender: str, epoch: int, new_supply: int, record_hash: str) -> None:
        if sender != self.oracle:
            raise TokenError("NotOracle")
        if epoch <= self.last_epoch:
            raise TokenError("EpochNotMonotonic")
        if new_supply <= 0:
            raise TokenError("ZeroSupply")
        self.total_supply = new_supply
        self.last_epoch = epoch
        self.last_record_hash = record_hash

    def transfer(self, sender: str, to: str, value: int) -> None:
        # ceil: the sender absorbs rounding, a transfer never mints
        gon_value = -(-value * TOTAL_GONS // self.total_supply)
        if self.gons.get(sender, 0) < gon_value:
            raise TokenError("InsufficientBalance")
        self.gons[sender] = self.gons.get(sender, 0) - gon_value
        self.gons[to] = self.gons.get(to, 0) + gon_value
