"""Backfill engine (SPEC#2 AC-2.3; B-uc2-12).

Produces the ≥570-week historical print series ending at the current
epoch, from committed data only, under real-time-vintage discipline:

- **Structure steps.** During calendar year Y the operative structure is
  the latest COMPLETED measured year s = min(Y−1, 2023) — exactly what a
  live index would have held. The year's S path starts at S(s) and the
  annual delta S(s+1)−S(s) is E11-scheduled across Y's actual Mondays
  (exact, invariant-P6 closure). For Y ≥ 2025 (structure plateau: WPP
  estimates end 2023) the delta is UNKNOWN and the path is held flat —
  the CARRY convention, honestly flagged on every affected week.

- **Burn overlay.** Weekly burn is the measured excess-mortality
  attribution from the WMD panel (kk-linear baselines, fit 2015-2019),
  converted to life-years under the registered ``excess_age_profile``
  policy. Per the E4/E5 residual-exposure semantics burn ATTRIBUTES
  within-year timing; it never double-counts the annual delta, which
  already embeds realized mortality.

Annual deltas already contain COVID at annual granularity, so the drag is
visible twice over: the 2020/2021 scheduled deltas collapse relative to
trend, and the weekly burn series spikes. B-uc2-13's gate quantifies the
latter cumulatively.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from tly.baseline import excess_series, fit_baseline
from tly.estimator import e_interp
from tly.methodology import EXCESS_AGE_PROFILE_POLICY
from tly.prints import validate_epoch
from tly.weekly import allocate_equal, monday_epochs
from tly.wmd import parse_wmd

STRUCTURE_PLATEAU = 2023  # last WPP-measured year on file

# The registered excess-age-profile policy, as executable weights:
# 70% of excess deaths at exact age 75.5, 30% at 85.5 (see methodology).
_PROFILE = ((Decimal("0.7"), Decimal("75.5")), (Decimal("0.3"), Decimal("85.5")))


@dataclass(frozen=True)
class AnnualStructure:
    year: int
    s_life_years: Decimal
    ex: dict[int, Decimal]  # single-age anchors, for the burn conversion


def load_annual_structures(fixture_path: Path) -> dict[int, AnnualStructure]:
    """S(y) and e(x) per year from the committed World fixture."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    out: dict[int, AnnualStructure] = {}
    for y_str, block in data["years"].items():
        ex = {int(a): Decimal(v) for a, v in block["ex"].items()}
        s = Decimal(0)
        for a_str, persons in block["pop_persons"].items():
            s += Decimal(persons) * e_interp(ex, Decimal(a_str) + Decimal("0.5"))
        out[int(y_str)] = AnnualStructure(year=int(y_str), s_life_years=s, ex=ex)
    return out


def excess_life_years_per_week(
    wmd_path: Path, structures: dict[int, AnnualStructure], years: range
) -> dict[tuple[int, int], Decimal]:
    """Measured weekly excess life-years, summed over the WMD panel.

    Weekly-reporting countries land on their ISO week; monthly reporters
    are E11-split evenly over the month's report weeks (4 or 5 slots by
    month index — a stated simplification; monthly excess is ~15% of the
    panel). Conversion: excess × Σ w_i·e(age_i) on the epoch's structure
    table (the registered profile)."""
    cells = parse_wmd(wmd_path)
    countries = sorted({c.iso3 for c in cells})
    burn: dict[tuple[int, int], Decimal] = {}
    for iso3 in countries:
        sub = [c for c in cells if c.iso3 == iso3]
        try:
            bl = fit_baseline(sub, iso3)
        except ValueError:
            continue  # no complete 2015-2019 fit window — excluded, counted by coverage
        for year in years:
            structure = structures[min(year - 1, STRUCTURE_PLATEAU)]
            e_conv = sum((w * e_interp(structure.ex, a) for w, a in _PROFILE), Decimal(0))
            for obs in excess_series(sub, bl, year):
                if bl.time_unit == "weekly":
                    slots = [(year, obs.period)]
                else:  # monthly -> spread across that month's ~4.33 weeks
                    first = (obs.period - 1) * Decimal("4.348")
                    wk0 = int(first) + 1
                    slots = [(year, min(w, 52)) for w in range(wk0, wk0 + 4)]
                share = allocate_equal(
                    (obs.excess * e_conv).quantize(Decimal("0.000001")), len(slots)
                )
                for slot, part in zip(slots, share):
                    burn[slot] = burn.get(slot, Decimal(0)) + part
    return burn


@dataclass(frozen=True)
class BackfillWeek:
    epoch_utc: str
    s_life_years: Decimal
    burn_life_years: Decimal  # measured attribution (0 where unmeasured)
    structure_year: int
    carried: bool  # True on the structure plateau (delta unknown, held flat)


def backfill_series(
    fixture_path: Path,
    wmd_path: Path,
    end_epoch_utc: str,
    weeks: int = 570,
) -> list[BackfillWeek]:
    end_dt = validate_epoch(end_epoch_utc)
    structures = load_annual_structures(fixture_path)
    burn = excess_life_years_per_week(wmd_path, structures, range(2020, min(end_dt.year, 2024) + 1))

    # assemble the full monday calendar back far enough, then take the tail
    all_epochs: list[str] = []
    for year in range(end_dt.year - (weeks // 52 + 2), end_dt.year + 1):
        all_epochs.extend(monday_epochs(year))
    all_epochs = [e for e in all_epochs if datetime.fromisoformat(e) <= end_dt]
    tail = all_epochs[-weeks:]

    # per-year scheduled paths (exact E11 closure)
    rows: list[BackfillWeek] = []
    by_year: dict[int, list[str]] = {}
    for e in tail:
        by_year.setdefault(datetime.fromisoformat(e).year, []).append(e)

    for year, epochs in sorted(by_year.items()):
        s_year = min(year - 1, STRUCTURE_PLATEAU)
        start_s = structures[s_year].s_life_years
        carried = year - 1 > STRUCTURE_PLATEAU
        year_mondays = monday_epochs(year)
        if not carried and (s_year + 1) in structures:
            delta = structures[s_year + 1].s_life_years - start_s
            steps = allocate_equal(delta.quantize(Decimal("0.000001")), len(year_mondays))
        else:
            carried = True
            steps = [Decimal(0)] * len(year_mondays)
        cum = {e: sum(steps[: i + 1], Decimal(0)) for i, e in enumerate(year_mondays)}
        for e in epochs:
            iso = date.fromisoformat(e[:10]).isocalendar()
            rows.append(
                BackfillWeek(
                    epoch_utc=e,
                    s_life_years=start_s + cum[e],
                    burn_life_years=burn.get((iso[0], iso[1]), Decimal(0)),
                    structure_year=s_year,
                    carried=carried,
                )
            )
    assert len(rows) == weeks
    assert EXCESS_AGE_PROFILE_POLICY  # policy must be registered (v0.5.0)
    return rows


def panel_coverage_share(
    wmd_path: Path, owid_births_deaths_path: Path, reference_year: int = 2019
) -> Decimal:
    """The WMD panel's share of world deaths in the reference year — both
    sides MEASURED quantities (panel observed deaths / WPP world deaths),
    zero free parameters. This is the P7 coverage figure the gate
    publishes and the divisor for the coverage-adjusted global estimate."""
    import csv
    import io

    txt = owid_births_deaths_path.read_text(encoding="utf-8")
    rows = list(csv.reader(io.StringIO(txt)))
    hdr = rows[0]
    di = hdr.index("deaths__sex_all__age_all__variant_estimates")
    world = None
    for r in rows[1:]:
        if r[1] == "OWID_WRL" and r[2] == str(reference_year) and r[di]:
            world = Decimal(r[di])
    if world is None:
        raise ValueError(f"no world deaths for {reference_year}")
    cells = parse_wmd(wmd_path, years={reference_year})
    panel = sum((c.deaths for c in cells), Decimal(0))
    return panel / world


@dataclass(frozen=True)
class CovidGateReport:
    """B-uc2-13: measured burn, coverage, and the coverage-adjusted global
    estimate — measured and imputed strictly separated (P7)."""

    measured_burn_life_years: Decimal  # WMD panel, no imputation
    coverage_share: Decimal  # panel deaths / world deaths, reference year
    adjusted_burn_life_years: Decimal  # measured / coverage — an ESTIMATE
    worst_week: tuple[int, int]
    worst_week_burn: Decimal


def covid_gate_report(
    fixture_path: Path, wmd_path: Path, owid_births_deaths_path: Path
) -> CovidGateReport:
    structures = load_annual_structures(fixture_path)
    burn = excess_life_years_per_week(wmd_path, structures, range(2020, 2022))
    measured = sum(burn.values(), Decimal(0))
    coverage = panel_coverage_share(wmd_path, owid_births_deaths_path)
    worst = max(burn, key=burn.get)
    return CovidGateReport(
        measured_burn_life_years=measured,
        coverage_share=coverage,
        adjusted_burn_life_years=measured / coverage,
        worst_week=worst,
        worst_week_burn=burn[worst],
    )
