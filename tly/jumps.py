"""Jump-calibration scaffolding (SPEC#6; RP Part IX E8; RP M3; C-uc6-05).

The E8 jump component prices mortality shocks from a frequency-severity
fit over the historical calibration set: 1918 influenza, WWII, HIV, COVID.
This module is SCAFFOLDING: the event registry, the data-source pointers,
and the fitting interface — with exactly ONE calibrated entry (COVID,
whose excess-death anchor and burn band are recorded in DECISIONS.md).

The other three events carry status PENDING with (verify)-marked source
pointers and NO numbers: inventing 1918/WWII/HIV excess-death figures from
memory is forbidden (RALPH §6 — invented citations are project-ending).
The fitter REFUSES to produce parameters while any event is pending —
honest refusal is the feature; a frequency-severity fit on one point would
be numerology wearing a lab coat.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

CALIBRATED = "calibrated"
PENDING = "PENDING (verify)"


class NotCalibratedError(RuntimeError):
    """The historical set is incomplete; no parameters can be fit."""


@dataclass(frozen=True)
class JumpEvent:
    name: str
    period: str
    status: str
    excess_deaths: Decimal | None  # persons; None while PENDING
    life_years_burned_low: Decimal | None
    life_years_burned_high: Decimal | None
    sources: tuple[str, ...]  # pointers to fetch, NOT citations of read works


HISTORICAL_SHOCK_SET: tuple[JumpEvent, ...] = (
    JumpEvent(
        name="1918 influenza pandemic",
        period="1918-1920",
        status=PENDING,
        excess_deaths=None,
        life_years_burned_low=None,
        life_years_burned_high=None,
        sources=(
            "Johnson & Mueller 2002 (Bull Hist Med) mortality estimate (verify)",
            "Barro, Ursua & Weng 2020 working paper (verify)",
            "HMD historical series where national CRVS existed (verify)",
        ),
    ),
    JumpEvent(
        name="World War II",
        period="1939-1945",
        status=PENDING,
        excess_deaths=None,
        life_years_burned_low=None,
        life_years_burned_high=None,
        sources=(
            "national war-loss commissions compilations (verify)",
            "HMD country series discontinuities (verify)",
        ),
    ),
    JumpEvent(
        name="HIV/AIDS epidemic",
        period="1981-",
        status=PENDING,
        excess_deaths=None,
        life_years_burned_low=None,
        life_years_burned_high=None,
        sources=(
            "UNAIDS epidemiological estimates (verify)",
            "GBD cause-specific mortality series (verify) — NC license, triangulation only",
        ),
    ),
    JumpEvent(
        name="COVID-19 pandemic",
        period="2020-2021",
        status=CALIBRATED,
        # The one anchored entry: WHO excess-death estimate and the
        # DECISIONS.md burn band (148-337M life-years, recalibrated band
        # 120-360M is the GATE band, not the estimate band).
        excess_deaths=Decimal("14830000"),
        life_years_burned_low=Decimal("148000000"),
        life_years_burned_high=Decimal("337000000"),
        sources=(
            "WHO excess mortality estimates 2020-2021 (the 14.83M anchor; DECISIONS.md Key numbers)",
            "World Mortality Dataset (snapshotted 2026-08-17, wmd_world_mortality.csv)",
        ),
    ),
)


def pending_events() -> tuple[JumpEvent, ...]:
    return tuple(e for e in HISTORICAL_SHOCK_SET if e.status == PENDING)


def fit_frequency_severity(events: tuple[JumpEvent, ...] = HISTORICAL_SHOCK_SET):
    """E8 frequency-severity fit — REFUSES while the set is incomplete.

    When all four events are calibrated (each with excess deaths and a burn
    band from fetched primary sources), this becomes the jump parameter
    fit. Until then it raises, naming exactly what is missing — the honest
    scaffold contract."""
    missing = [e.name for e in events if e.status != CALIBRATED]
    if missing:
        raise NotCalibratedError(
            "frequency-severity fit refused — uncalibrated events: "
            + "; ".join(missing)
            + ". Fetch primary sources (see each event's pointers); never invent."
        )
    raise NotImplementedError("all events calibrated — implement the fit (C-uc6-05 successor task)")
