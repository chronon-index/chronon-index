"""Scenario lab: definitions and deterministic execution (SPEC#6; C-uc6-01).

Lab outputs are SIMULATIONS, never prints: every rendered result carries
the SIMULATION label (C-uc6-02), the label is not a valid print series
label, and print storage type-rejects lab objects — three independent
walls between what-if and what-is.

A scenario is DATA — a JSON-serializable definition with a pinned integer
seed — and running one is a pure function of that definition: identical
definitions produce byte-identical rendered results (RP M5 deterministic
seeds; invariant P5 applied to the lab). Stochastic components draw ONLY
from random.Random(seed); nothing reads clocks, OS entropy, or global
state.

v1 scenario shape: an initial supply, a weekly growth factor, optional
seeded growth jitter (basis points), and discrete shock events (epoch,
burn) — enough to script organic decades and pandemic weeks against the
gons engine.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from decimal import Decimal

from tly.gons import GonsLedger, genesis_ledger
from tly.guard import assert_decimal

SIMULATION_LABEL = "SIMULATION"


@dataclass(frozen=True)
class Scenario:
    name: str
    seed: int
    initial_s: Decimal
    epochs: int
    weekly_growth: Decimal  # multiplicative, e.g. 1.000138
    jitter_bp: int = 0  # +- uniform basis points on growth, seeded
    shocks: tuple[tuple[int, Decimal], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        assert_decimal(self.initial_s, "initial_s")
        assert_decimal(self.weekly_growth, "weekly_growth")
        if self.epochs <= 0:
            raise ValueError("epochs must be positive")
        for epoch, burn in self.shocks:
            assert_decimal(burn, "shock burn")
            if not 0 <= epoch < self.epochs:
                raise ValueError(f"shock epoch {epoch} outside 0..{self.epochs - 1}")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "seed": self.seed,
            "initial_s": str(self.initial_s),
            "epochs": self.epochs,
            "weekly_growth": str(self.weekly_growth),
            "jitter_bp": self.jitter_bp,
            "shocks": [[e, str(b)] for e, b in self.shocks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Scenario:
        return cls(
            name=data["name"],
            seed=int(data["seed"]),
            initial_s=Decimal(data["initial_s"]),
            epochs=int(data["epochs"]),
            weekly_growth=Decimal(data["weekly_growth"]),
            jitter_bp=int(data.get("jitter_bp", 0)),
            shocks=tuple((int(e), Decimal(b)) for e, b in data.get("shocks", [])),
        )


@dataclass(frozen=True)
class ScenarioResult:
    scenario: Scenario
    m_series: tuple[Decimal, ...]  # M after each epoch, epochs+1 points
    shocks_applied: tuple[tuple[int, Decimal], ...]

    def render(self) -> str:
        """Deterministic bytes: the P5-style output the named test diffs."""
        return (
            json.dumps(
                {
                    "series_label": SIMULATION_LABEL,
                    "scenario": self.scenario.to_dict(),
                    "m_series": [str(m) for m in self.m_series],
                    "shocks_applied": [[e, str(b)] for e, b in self.shocks_applied],
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )


def run_scenario(scenario: Scenario) -> ScenarioResult:
    """Pure function of the definition; RNG state comes only from the seed."""
    rng = random.Random(scenario.seed)
    ledger: GonsLedger = genesis_ledger(scenario.initial_s)
    shocks = dict(scenario.shocks)
    series = [ledger.m]
    applied: list[tuple[int, Decimal]] = []
    for epoch in range(scenario.epochs):
        growth = scenario.weekly_growth
        if scenario.jitter_bp:
            bp = rng.randint(-scenario.jitter_bp, scenario.jitter_bp)
            growth = growth + Decimal(bp) / Decimal(10_000)
        new_m = ledger.m * growth
        if epoch in shocks:
            new_m = new_m - shocks[epoch]
            applied.append((epoch, shocks[epoch]))
        ledger.rebase(new_m)
        series.append(ledger.m)
    return ScenarioResult(scenario=scenario, m_series=tuple(series), shocks_applied=tuple(applied))
