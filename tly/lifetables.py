"""Keyless single-age life tables from raw Eurostat registry data (D-01;
ruling B-uc2-02(c); reference: docs/rulings/keyless_mortality_reference.py).

The graduation HMD would have done, from data HMD would have used:

- Dx from ``demo_magec`` (deaths by single year of age), UNK redistributed
  pro-rata; Ex from ``demo_pjan`` via the mid-year approximation
  Ex = (P(1 Jan t) + P(1 Jan t+1))/2 — the one place structurally coarser
  than HMD's Lexis triangles (second-order bias, material only at age 0
  and the open interval, both patched below).
- Old-age closure: weighted Kannisto logistic fitted from age 80,
  extrapolated to 110 — raw registry rates at 95+ are noise-dominated.
  The fit is closed-form weighted least squares on logits (no numpy).
- Age 0: Andreev–Kingkade a0.

MODEL LAYER: floats are the working arithmetic here (graduation and
fitting are estimation, not settlement values); anything these tables
feed into a PUBLISHED figure crosses back through the Decimal boundary
and the float quarantine. Validation: reconstructed e0/e65 vs Eurostat's
independently published demo_mlexpec (the ruling showed max |Δ| 0.0452y
on IT 2018-2024)."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path


class AgeCubeError(ValueError):
    pass


def _age_to_int(code: str, open_age_hint: int = 100) -> int | None:
    """Eurostat age code -> integer age; None for TOTAL/UNK (handled apart)."""
    if code in ("TOTAL", "UNK"):
        return None
    if code == "Y_LT1":
        return 0
    if code == "Y_OPEN":
        return open_age_hint
    if code.startswith("Y_GE"):
        return int(code[4:])
    if code.startswith("Y"):
        return int(code[1:])
    raise AgeCubeError(f"unknown age code {code!r}")


def parse_age_cube(path: Path, open_age_hint: int = 100) -> dict[str, dict[int, dict[int, float]]]:
    """JSON-stat cube with an age dimension -> {geo: {year: {age: value}}}.

    UNK (unknown-age) rows are redistributed pro-rata within their
    geo-year — dropping them would bias mx down."""
    data = json.loads(path.read_text(encoding="utf-8"))
    dims = data["id"]
    sizes = data["size"]
    for needed in ("geo", "time", "age"):
        if needed not in dims:
            raise AgeCubeError(f"cube lacks {needed}")
    idx = {d: data["dimension"][d]["category"]["index"] for d in dims}
    order = {d: sorted(idx[d], key=idx[d].get) for d in dims}
    strides: dict[str, int] = {}
    acc = 1
    for d in reversed(dims):
        strides[d] = acc
        acc *= sizes[dims.index(d)]
    for d in dims:
        if d not in ("geo", "time", "age") and sizes[dims.index(d)] != 1:
            raise AgeCubeError(f"expected singleton dimension {d}")

    out: dict[str, dict[int, dict[int, float]]] = {}
    unk: dict[tuple[str, int], float] = {}
    for flat, val in data["value"].items():
        f = int(flat)
        coords = {
            d: order[d][(f // strides[d]) % sizes[dims.index(d)]] for d in ("geo", "time", "age")
        }
        year = int(coords["time"])
        age = _age_to_int(coords["age"], open_age_hint)
        if coords["age"] == "TOTAL":
            continue
        if coords["age"] == "UNK":
            unk[(coords["geo"], year)] = unk.get((coords["geo"], year), 0.0) + float(val)
            continue
        out.setdefault(coords["geo"], {}).setdefault(year, {})[age] = out.get(
            coords["geo"], {}
        ).get(year, {}).get(age, 0.0) + float(val)
    for (geo, year), u in unk.items():
        block = out.get(geo, {}).get(year)
        if block and u:
            total = sum(block.values())
            if total > 0:
                factor = 1.0 + u / total
                for a in block:
                    block[a] *= factor
    return out


@dataclass(frozen=True)
class RawRates:
    geo: str
    year: int
    mx: dict[int, float]  # age -> Dx/Ex
    dx_weights: dict[int, float]  # deaths, as Kannisto fit weights


def raw_rates(
    magec_path: Path, pjan_path: Path, geo: str, year: int, max_age: int = 99
) -> RawRates:
    """Dx/Ex with mid-year exposures for one geo-year."""
    deaths = parse_age_cube(magec_path)[geo]
    pop = parse_age_cube(pjan_path)[geo]
    if year not in deaths or year not in pop or (year + 1) not in pop:
        raise AgeCubeError(f"{geo} {year}: need deaths[{year}], pop[{year}], pop[{year + 1}]")
    mx: dict[int, float] = {}
    wts: dict[int, float] = {}
    for a in range(0, max_age + 1):
        d = deaths[year].get(a, 0.0)
        ex = (pop[year].get(a, 0.0) + pop[year + 1].get(a, 0.0)) / 2.0
        if ex > 0:
            mx[a] = d / ex
            wts[a] = d
    return RawRates(geo=geo, year=year, mx=mx, dx_weights=wts)


def kannisto_close(
    mx: dict[int, float],
    weights: dict[int, float],
    fit_from: int = 80,
    to_age: int = 110,
) -> dict[int, float]:
    """Weighted Kannisto logistic: logit(m) = a + b·x for x >= fit_from,
    extrapolated to ``to_age``. Closed-form weighted least squares —
    sqrt(deaths) weights per the reference implementation."""
    pts = [
        (float(a), math.log(m / (1.0 - m)), math.sqrt(weights.get(a, 1.0)))
        for a, m in sorted(mx.items())
        if a >= fit_from and 0.0 < m < 1.0
    ]
    if len(pts) < 5:
        return dict(mx)
    sw = sum(w for _, _, w in pts)
    xb = sum(w * x for x, _, w in pts) / sw
    yb = sum(w * y for _, y, w in pts) / sw
    sxx = sum(w * (x - xb) ** 2 for x, _, w in pts)
    sxy = sum(w * (x - xb) * (y - yb) for x, y, w in pts)
    b = sxy / sxx
    a_ = yb - b * xb
    out = dict(mx)
    for age in range(fit_from, to_age + 1):
        z = a_ + b * age
        out[age] = math.exp(z) / (1.0 + math.exp(z))
    return out


def _a0(m0: float, sex: str = "T") -> float:
    """Andreev–Kingkade a0; sex 'T' averages the M/F rules."""

    def male(m: float) -> float:
        if m < 0.0230:
            return 0.14929 - 1.99545 * m
        if m < 0.0785:
            return 0.02832 + 3.26021 * m
        return 0.29915

    def female(m: float) -> float:
        if m < 0.0170:
            return 0.14903 - 2.05527 * m
        if m < 0.0658:
            return 0.04667 + 3.88089 * m
        return 0.31411

    if sex == "M":
        return male(m0)
    if sex == "F":
        return female(m0)
    return 0.5 * (male(m0) + female(m0))


def life_table(mx: dict[int, float], sex: str = "T") -> dict[int, dict[str, float]]:
    """Period life table from graduated single-age mx; radix 1.0; closes
    with Lx = lx/mx at the last age."""
    ages = sorted(mx)
    m = [mx[a] for a in ages]
    ax = [0.5] * len(m)
    ax[0] = _a0(m[0], sex)
    qx = [mi / (1.0 + (1.0 - axi) * mi) for mi, axi in zip(m, ax)]
    qx[-1] = 1.0
    lx = [1.0]
    for q in qx[:-1]:
        lx.append(lx[-1] * (1.0 - q))
    dx = [li * qi for li, qi in zip(lx, qx)]
    Lx = [li - (1.0 - axi) * di for li, axi, di in zip(lx, ax, dx)]
    Lx[-1] = lx[-1] / m[-1] if m[-1] > 0 else 0.0
    Tx = [0.0] * len(m)
    running = 0.0
    for i in range(len(m) - 1, -1, -1):
        running += Lx[i]
        Tx[i] = running
    return {
        a: {
            "mx": m[i],
            "qx": qx[i],
            "ax": ax[i],
            "lx": lx[i],
            "dx": dx[i],
            "Lx": Lx[i],
            "Tx": Tx[i],
            "ex": Tx[i] / lx[i],
        }
        for i, a in enumerate(ages)
    }


def build_life_table(
    magec_path: Path, pjan_path: Path, geo: str, year: int, sex: str = "T"
) -> dict[int, dict[str, float]]:
    """The full D-01 chain: raw rates -> Kannisto closure -> life table."""
    raw = raw_rates(magec_path, pjan_path, geo, year)
    graduated = kannisto_close(raw.mx, raw.dx_weights)
    return life_table(graduated, sex)
