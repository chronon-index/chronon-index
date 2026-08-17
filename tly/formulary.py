"""The formulary (RP Part IX; SPEC#0 G8; D-05): E1–E12 as a tested module.

Each equation is a registry entry carrying its statement and its HOME — the
module that implements it (None where implementation is legitimately
pending, with the pending phase named). The cross-reference test asserts
every claimed home imports and mentions its equation number in its source,
so the formulary cannot drift from the code that embodies it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Equation:
    number: str
    statement: str
    home: str | None  # importable module path, or None
    pending: str | None = None  # phase note when home is None


FORMULARY: tuple[Equation, ...] = (
    Equation("E1", "S(t) = Σ over (a,c) of N(a,c,t)·e(a,c,t)", "tly.stock"),
    Equation(
        "E2",
        "v0 estimator: S = Σ bands N_band·e(mid(band)); uniform-within-band mid; "
        "piecewise-linear e on anchors, flat tail",
        "tly.estimator",
    ),
    Equation(
        "E3",
        "Transport: ∂N/∂t + ∂N/∂a = −μN; ∂e/∂a = μe − 1",
        None,
        "derivation lives in METHODOLOGY_v0.md §4; code embodiment via E4/E5",
    ),
    Equation("E4", "Identity: dS/dt = B·e(0) − N + N·dĒ/dt − Σ(excess·e(a))", "tly.decomposition"),
    Equation("E5", "Discrete accounting of E4 with within-year factors", "tly.decomposition"),
    Equation(
        "E6",
        "Cohort expectancy over the projected mortality surface",
        None,
        "P2 phase (Lee-Carter, C-uc6-03/04; needs D-01 HMD data)",
    ),
    Equation("E7", "Lee-Carter: ln m(x,t) = α(x) + β(x)κ(t) + ε", None, "P2 phase (C-uc6-03)"),
    Equation("E8", "Stochastic index with jump component (1918/WWII/HIV/COVID)", "tly.jumps"),
    Equation("E9", "Error propagation: Var(S) = Σ e²Var(N) + N²Var(e) + cov", "tly.error_budget"),
    Equation("E10", "Gons rebase: balance = gons/F; F-only rebases; shares invariant", "tly.gons"),
    Equation("E11", "Largest-remainder allocation; Σ parts == total exactly", "tly.burn"),
    Equation(
        "E12", "Neutrality: value = s·MarketCap; d(value)/d(rebase)=0; d(s)/d(deaths)=0", "tly.gons"
    ),
)


def implemented() -> tuple[Equation, ...]:
    return tuple(e for e in FORMULARY if e.home is not None)


def pending() -> tuple[Equation, ...]:
    return tuple(e for e in FORMULARY if e.home is None)
