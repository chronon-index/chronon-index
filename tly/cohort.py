"""Cohort expectancy and cohort-S (D-04; RP Part IX E6; SPEC#2 AC-2.5).

E6: e_cohort(a, t) = expected remaining years for a person aged a in year
t, surviving DIAGONALLY through the mortality surface — q(a, t),
q(a+1, t+1), … — rather than down a single period column. Because future
diagonals cross PROJECTED mortality (WPP medium variant), cohort values
are MODEL CONTENT: they feed the INFORMATIONAL series only and can never
touch settlement (enforced structurally in prints/fixings).

Surface: World qx per single age, 2010–2023 measured + 2024–2100
projected (committed fixture with dual provenance). Conventions, stated:
- Trapezoid person-years: a survivor of the interval contributes 1 year,
  a decedent ½ (uniform within interval) — the discrete E6 integral.
- Beyond age 100 (the surface's open age) the diagonal closes with the
  period table of its final calendar year (Kannisto-free: WPP's own
  closed tables end at 100+ with qx=1).
- Beyond calendar 2100 the surface holds the 2100 period column
  (affects only cohorts younger than ~25 in 2025; stated, not hidden).

The deterministic error budget's one-sided "period-vs-cohort +3–8%" term
is VALIDATED here: computed cohort-S must land inside that band above
measured-period S.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING

from tly import numeric  # noqa: F401
from tly.guard import assert_no_floats

if TYPE_CHECKING:
    from tly.prints import WeeklyPrint

MAX_AGE = 100
LAST_YEAR = 2100
HALF = Decimal("0.5")
ONE = Decimal(1)


def load_qx_surface(path: Path) -> dict[int, dict[int, Decimal]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["quantity"] == "qx"
    return {
        int(y): {int(a): Decimal(v) for a, v in block.items()} for y, block in data["years"].items()
    }


def cohort_e(surface: dict[int, dict[int, Decimal]], age: int, year: int) -> Decimal:
    """E6 by diagonal survival with trapezoid person-years."""
    assert_no_floats(surface, "surface")
    if year not in surface:
        raise ValueError(f"surface lacks year {year}")
    e = Decimal(0)
    alive = ONE
    a, t = age, year
    while a <= MAX_AGE and alive > 0:
        q = surface[min(t, LAST_YEAR)][a]
        e += alive * (ONE - q) + alive * q * HALF  # survivors 1y, deaths ½y
        alive *= ONE - q
        a += 1
        t += 1
    return e


def cohort_s(
    surface: dict[int, dict[int, Decimal]],
    pop_by_age: dict[int, Decimal],
    year: int,
) -> Decimal:
    """Cohort-S = Σ N(a) · e_cohort(a, year) — the INFORMATIONAL stock."""
    assert_no_floats(pop_by_age, "pop_by_age")
    total = Decimal(0)
    for age, persons in pop_by_age.items():
        total += persons * cohort_e(surface, min(age, MAX_AGE), year)
    return total


def informational_print(
    surface: dict[int, dict[int, Decimal]],
    pop_by_age: dict[int, Decimal],
    year: int,
    epoch_utc: str,
    snapshot_dirs: list[Path],
) -> "WeeklyPrint":
    """The INFORMATIONAL cohort print for the dual series (D-04): cohort-S
    with the symmetric measurement interval, labeled model content."""
    from tly.error_budget import build_error_budget
    from tly.prints import WeeklyPrint
    from tly.stock import stamp

    s = cohort_s(surface, pop_by_age, year)
    n = sum(pop_by_age.values(), Decimal(0))
    budget = build_error_budget(s)
    lo, hi = budget.interval
    return WeeklyPrint(
        epoch_utc=epoch_utc,
        series_label="INFORMATIONAL",
        s_life_years=s,
        e_bar_years=s / n,
        n_persons=n,
        burn_life_years=Decimal(0),
        coverage={
            "measured_share": Decimal(0),
            "note": (
                "cohort series: every diagonal crosses PROJECTED mortality "
                "(WPP medium) — model content by construction; measured_share "
                "0 states that honestly"
            ),
        },
        accuracy={
            "statement": (
                f"Best-estimate cohort stock (E6 over the 2010-2100 qx "
                f"surface, structure year {year}): projected-mortality "
                "model content — informs, never settles. Symmetric "
                "measurement interval only; projection-model uncertainty "
                "is NOT quantified until the P3 stochastic machinery."
            ),
            "uncertainty": {"type": "interval", "lower": str(lo), "upper": str(hi)},
            "produced_by": "tly.cohort.informational_print",
        },
        provenance=stamp(snapshot_dirs),
    )
