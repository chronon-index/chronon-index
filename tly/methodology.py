"""Methodology versioning (SPEC#1 AC-1.4; RP Part I M5; RP Part XI).

Every published output is stamped with the methodology version and the
numerical policies it was computed under. Policies may change ONLY together
with a version bump recorded in docs/METHODOLOGY_CHANGELOG.md — the
VERSION_POLICY_REGISTRY below pins each version to its exact policy
strings, and test_policy_change_requires_version_bump enforces the pairing
in CI. Editing a policy without adding a new registry entry (and moving
METHODOLOGY_VERSION to it) fails the suite by construction.
"""

from __future__ import annotations

from tly.numeric import PRECISION, ROUNDING

METHODOLOGY_VERSION = "v0.6.0-reconstruction"

INTERPOLATION_POLICY = "linear-on-anchors, flat-tail"
BAND_MIDPOINT_POLICY = "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)"
DECIMAL_POLICY = f"Decimal prec {PRECISION}, {ROUNDING}"
BASELINE_POLICY = "kk-linear: per-period linear trend fit on 2015-2019 (Karlinsky-Kobak)"
P6_CLOSURE_POLICY = "exact-0: E11-scheduled weekly flows sum to the annual identity exactly"
QUANTA_POLICY = "scheduling quantum 0.000001 life-years; attribution quantum 0.001"
EXCESS_AGE_PROFILE_POLICY = (
    "excess-age-profile: 0.7 at exact age 75.5 + 0.3 at 85.5 on the epoch "
    "structure-year table (backfill burn conversion)"
)
ERROR_BUDGET_ONE_SIDED_POLICY = (
    "one-sided terms: vintage-lag +2-3%; period-vs-cohort +3-9% "
    "(E6-computed +8.06% on the committed 2010-2100 surface supersedes "
    "the +3-8% literature prose; listed never netted)"
)

# version -> the exact policy strings that version is defined by.
# Append-only: past entries are history and must never be edited.
VERSION_POLICY_REGISTRY: dict[str, dict[str, str]] = {
    "v0.1.0-reconstruction": {
        "interpolation": "linear-on-anchors, flat-tail",
        "band_midpoint": "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)",
        "decimal": "Decimal prec 34, ROUND_HALF_EVEN",
    },
    # v0.2.0: ADDS the nowcast baseline policy (B-uc2-04); prior policies
    # unchanged. See docs/METHODOLOGY_CHANGELOG.md.
    "v0.2.0-reconstruction": {
        "interpolation": "linear-on-anchors, flat-tail",
        "band_midpoint": "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)",
        "decimal": "Decimal prec 34, ROUND_HALF_EVEN",
        "baseline": "kk-linear: per-period linear trend fit on 2015-2019 (Karlinsky-Kobak)",
    },
    # v0.3.0: ADDS the P6 closure tolerance policy (B-uc2-08); prior
    # policies unchanged. See docs/METHODOLOGY_CHANGELOG.md.
    "v0.3.0-reconstruction": {
        "interpolation": "linear-on-anchors, flat-tail",
        "band_midpoint": "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)",
        "decimal": "Decimal prec 34, ROUND_HALF_EVEN",
        "baseline": "kk-linear: per-period linear trend fit on 2015-2019 (Karlinsky-Kobak)",
        "p6_closure": "exact-0: E11-scheduled weekly flows sum to the annual identity exactly",
    },
    # v0.4.0: ADDS the quanta policy (B-uc3-04) — the scheduling and
    # attribution quanta were governed constants living only in code.
    # Prior policies unchanged. See docs/METHODOLOGY_CHANGELOG.md.
    "v0.4.0-reconstruction": {
        "interpolation": "linear-on-anchors, flat-tail",
        "band_midpoint": "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)",
        "decimal": "Decimal prec 34, ROUND_HALF_EVEN",
        "baseline": "kk-linear: per-period linear trend fit on 2015-2019 (Karlinsky-Kobak)",
        "p6_closure": "exact-0: E11-scheduled weekly flows sum to the annual identity exactly",
        "quanta": "scheduling quantum 0.000001 life-years; attribution quantum 0.001",
    },
    # v0.5.0: ADDS the excess-age-profile policy (B-uc2-12/13) — the
    # burn conversion assumption for backfill excess deaths. Prior
    # policies unchanged. See docs/METHODOLOGY_CHANGELOG.md.
    "v0.5.0-reconstruction": {
        "interpolation": "linear-on-anchors, flat-tail",
        "band_midpoint": "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)",
        "decimal": "Decimal prec 34, ROUND_HALF_EVEN",
        "baseline": "kk-linear: per-period linear trend fit on 2015-2019 (Karlinsky-Kobak)",
        "p6_closure": "exact-0: E11-scheduled weekly flows sum to the annual identity exactly",
        "quanta": "scheduling quantum 0.000001 life-years; attribution quantum 0.001",
        "excess_age_profile": (
            "excess-age-profile: 0.7 at exact age 75.5 + 0.3 at 85.5 on the epoch "
            "structure-year table (backfill burn conversion)"
        ),
    },
    # v0.6.0: the registry's first parameter CHANGE (not addition) — the
    # period-vs-cohort upper moves 8 -> 9 because the E6 computation on
    # the committed surface measured +8.06%, above the literature prose
    # band (tests/test_cohort.py finding). The one-sided terms become a
    # governed, version-keyed parameter (VERSION_ONE_SIDED_TERMS below)
    # so archived prints keep reproducing under the band that made them.
    "v0.6.0-reconstruction": {
        "interpolation": "linear-on-anchors, flat-tail",
        "band_midpoint": "uniform-within-band; open-band lo+2.5 (inert beyond last anchor)",
        "decimal": "Decimal prec 34, ROUND_HALF_EVEN",
        "baseline": "kk-linear: per-period linear trend fit on 2015-2019 (Karlinsky-Kobak)",
        "p6_closure": "exact-0: E11-scheduled weekly flows sum to the annual identity exactly",
        "quanta": "scheduling quantum 0.000001 life-years; attribution quantum 0.001",
        "excess_age_profile": (
            "excess-age-profile: 0.7 at exact age 75.5 + 0.3 at 85.5 on the epoch "
            "structure-year table (backfill burn conversion)"
        ),
        "error_budget_one_sided": (
            "one-sided terms: vintage-lag +2-3%; period-vs-cohort +3-9% "
            "(E6-computed +8.06% on the committed 2010-2100 surface supersedes "
            "the +3-8% literature prose; listed never netted)"
        ),
    },
}

# Version-keyed one-sided error-budget terms (percent bounds as strings;
# tly.error_budget converts to Decimal). Append-only like the policy
# registry: reproduction of an archived print selects ITS version's band.
_PRE_V6_ONE_SIDED = {
    "vintage_lag_pct": ("2", "3"),
    "period_vs_cohort_pct": ("3", "8"),
}
VERSION_ONE_SIDED_TERMS: dict[str, dict[str, tuple[str, str]]] = {
    "v0.1.0-reconstruction": _PRE_V6_ONE_SIDED,
    "v0.2.0-reconstruction": _PRE_V6_ONE_SIDED,
    "v0.3.0-reconstruction": _PRE_V6_ONE_SIDED,
    "v0.4.0-reconstruction": _PRE_V6_ONE_SIDED,
    "v0.5.0-reconstruction": _PRE_V6_ONE_SIDED,
    "v0.6.0-reconstruction": {
        "vintage_lag_pct": ("2", "3"),
        "period_vs_cohort_pct": ("3", "9"),
    },
}


def one_sided_terms_for(version: str) -> dict[str, tuple[str, str]]:
    """The one-sided error-budget bounds GOVERNED by ``version`` — raises
    on unknown versions rather than guessing a band."""
    try:
        return VERSION_ONE_SIDED_TERMS[version]
    except KeyError:
        raise KeyError(f"no one-sided terms registered for {version!r}") from None


def current_policies() -> dict[str, str]:
    """The live policy strings, as the code actually computes them."""
    return {
        "interpolation": INTERPOLATION_POLICY,
        "band_midpoint": BAND_MIDPOINT_POLICY,
        "decimal": DECIMAL_POLICY,
        "baseline": BASELINE_POLICY,
        "p6_closure": P6_CLOSURE_POLICY,
        "quanta": QUANTA_POLICY,
        "excess_age_profile": EXCESS_AGE_PROFILE_POLICY,
        "error_budget_one_sided": ERROR_BUDGET_ONE_SIDED_POLICY,
    }


def output_metadata() -> dict[str, object]:
    """Stamp block for every published artifact (AC-1.4)."""
    return {
        "methodology_version": METHODOLOGY_VERSION,
        "policies": current_policies(),
    }
