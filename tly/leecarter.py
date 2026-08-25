"""Lee-Carter mortality model (C-uc6-03 / B-uc2-19; RP Part IX E7; RP M2).

Classic Lee-Carter 1992: log m(x,t) = a(x) + b(x)·k(t) + ε, fitted by the
first singular component of the centered log-rate matrix, with the
standard identification sum(b)=1, sum(k)=0, and k(t) modeled as a random
walk with drift.

The first component is computed by POWER ITERATION on CᵀC (stdlib floats,
no numpy): Lee-Carter uses only the leading singular triplet, and power
iteration converges to it at machine precision on these small matrices
(~100 ages × ~35 years). Deterministic: fixed start vector, fixed
tolerance. MODEL LAYER — floats throughout; published uses cross the
Decimal boundary.

Replication targets are FETCHED, never invented (RALPH §6): the B-uc2-02
ruling records a verified IT 1990-2024 fit (drift −2.0330, σ 2.4981,
first-component share 0.9270) produced by the reference implementation on
the same sources; the test replicates those numbers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from tly.lifetables import kannisto_close, raw_rates


@dataclass(frozen=True)
class LeeCarterFit:
    ages: tuple[int, ...]
    years: tuple[int, ...]
    ax: tuple[float, ...]
    bx: tuple[float, ...]
    kt: tuple[float, ...]
    drift: float
    sigma: float
    explained: float  # first singular component's share of variance

    def forecast_kt(self, horizon: int) -> list[float]:
        """Central random-walk-with-drift path."""
        return [self.kt[-1] + self.drift * h for h in range(1, horizon + 1)]

    def log_mx_hat(self, kt_value: float) -> list[float]:
        return [a + b * kt_value for a, b in zip(self.ax, self.bx)]


def _power_iteration_first_component(
    c: list[list[float]], tol: float = 1e-14, max_iter: int = 10_000
) -> tuple[float, list[float], list[float]]:
    """Leading singular triplet (s, u, v) of matrix C (rows×cols) via power
    iteration on CᵀC. Deterministic start: uniform vector."""
    rows, cols = len(c), len(c[0])
    v = [1.0 / math.sqrt(cols)] * cols
    s_prev = 0.0
    for _ in range(max_iter):
        # w = Cᵀ(Cv)
        cv = [sum(c[i][j] * v[j] for j in range(cols)) for i in range(rows)]
        w = [sum(c[i][j] * cv[i] for i in range(rows)) for j in range(cols)]
        norm = math.sqrt(sum(x * x for x in w))
        if norm == 0.0:
            raise ValueError("zero matrix in power iteration")
        v = [x / norm for x in w]
        s = math.sqrt(norm)  # ||Cv|| after normalization step converges to σ₁
        if abs(s - s_prev) < tol * max(1.0, s):
            break
        s_prev = s
    cv = [sum(c[i][j] * v[j] for j in range(cols)) for i in range(rows)]
    s1 = math.sqrt(sum(x * x for x in cv))
    u = [x / s1 for x in cv]
    return s1, u, v


def lee_carter(log_mx: dict[int, dict[int, float]]) -> LeeCarterFit:
    """Fit from {age: {year: log m}}; ages/years must form a full grid."""
    ages = tuple(sorted(log_mx))
    years = tuple(sorted(log_mx[ages[0]]))
    for a in ages:
        if tuple(sorted(log_mx[a])) != years:
            raise ValueError(f"ragged grid at age {a}")
    ax = [sum(log_mx[a][y] for y in years) / len(years) for a in ages]
    c = [[log_mx[a][y] - ax[i] for y in years] for i, a in enumerate(ages)]

    s1, u, v = _power_iteration_first_component(c)
    bx = list(u)
    kt = [s1 * x for x in v]
    if sum(bx) < 0:
        bx = [-x for x in bx]
        kt = [-x for x in kt]
    scale = sum(bx)
    bx = [x / scale for x in bx]
    kt = [x * scale for x in kt]
    k_mean = sum(kt) / len(kt)
    kt = [x - k_mean for x in kt]
    # re-absorb the centering shift into ax so the fit is unchanged
    ax = [a + b * k_mean for a, b in zip(ax, bx)]

    dk = [b - a for a, b in zip(kt, kt[1:])]
    drift = sum(dk) / len(dk)
    var = sum((d - drift) ** 2 for d in dk) / (len(dk) - 1)
    total_var = sum(x * x for row in c for x in row)
    return LeeCarterFit(
        ages=ages,
        years=years,
        ax=tuple(ax),
        bx=tuple(bx),
        kt=tuple(kt),
        drift=drift,
        sigma=math.sqrt(var),
        explained=(s1 * s1) / total_var,
    )


def log_mx_matrix(
    magec_path: Path,
    pjan_path: Path,
    geo: str,
    years: range,
    max_age: int = 100,
) -> dict[int, dict[int, float]]:
    """Graduated log-rate grid for one country: raw Dx/Ex per year,
    Kannisto-closed, truncated to ages 0..max_age."""
    out: dict[int, dict[int, float]] = {}
    for year in years:
        raw = raw_rates(magec_path, pjan_path, geo, year)
        graduated = kannisto_close(raw.mx, raw.dx_weights)
        for a in range(0, max_age + 1):
            m = graduated.get(a)
            if m is None or m <= 0:
                raise ValueError(f"{geo} {year}: missing/zero rate at age {a}")
            out.setdefault(a, {})[year] = math.log(m)
    return out
