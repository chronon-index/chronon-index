"""Weekly print object (SPEC#2; DECISIONS defaults; B-uc2-06).

A print is the atomic published artifact: measured-period S with the
SETTLEMENT label (DECISIONS: settle on measurement, inform with the model —
cohort-S prints carry INFORMATIONAL from P2), stamped with its epoch
(Mondays 12:00 UTC exactly), coverage honesty block (invariant P7), burn,
and full provenance (methodology version + policies + snapshot hashes).

Prints are immutable once constructed (frozen dataclass; invariant P4 —
first print settles, corrections forward-only via the ledger). The JSON
rendering is deterministic: Decimal-as-string, sorted keys, so identical
inputs are byte-identical (invariant P5).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

SERIES_LABELS = ("SETTLEMENT", "INFORMATIONAL")
PRINT_SCHEMA_VERSION = "print-v1"

REQUIRED_FIELDS = (
    "schema_version",
    "epoch_utc",
    "series_label",
    "s_life_years",
    "e_bar_years",
    "n_persons",
    "burn_life_years",
    "coverage",
    "provenance",
)


class PrintSchemaError(ValueError):
    """The print dict violates the published schema."""


def validate_epoch(epoch_utc: str) -> datetime:
    """Epochs are Mondays 12:00:00 UTC exactly (DECISIONS default)."""
    try:
        dt = datetime.fromisoformat(epoch_utc)
    except ValueError as err:
        raise PrintSchemaError(f"epoch_utc not ISO-8601: {epoch_utc!r}") from err
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(None):
        raise PrintSchemaError(f"epoch_utc must be explicit UTC: {epoch_utc!r}")
    if dt.weekday() != 0 or (dt.hour, dt.minute, dt.second, dt.microsecond) != (12, 0, 0, 0):
        raise PrintSchemaError(f"epoch must be Monday 12:00:00 UTC exactly, got {epoch_utc!r}")
    return dt


@dataclass(frozen=True)
class WeeklyPrint:
    """One epoch's published figures. Frozen: a constructed print is FINAL."""

    epoch_utc: str
    series_label: str
    s_life_years: Decimal
    e_bar_years: Decimal
    n_persons: Decimal
    burn_life_years: Decimal
    coverage: dict  # P7 block: {"measured_share": "...", "by_country": {...}}
    provenance: dict  # stamp(): methodology_version, policies, snapshots
    schema_version: str = field(default=PRINT_SCHEMA_VERSION)

    def __post_init__(self) -> None:
        validate_epoch(self.epoch_utc)
        if self.series_label not in SERIES_LABELS:
            raise PrintSchemaError(f"series_label must be one of {SERIES_LABELS}")
        for name in ("s_life_years", "e_bar_years", "n_persons", "burn_life_years"):
            if not isinstance(getattr(self, name), Decimal):
                raise PrintSchemaError(f"{name} must be Decimal")

    def to_json_dict(self) -> dict:
        def encode(obj):
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, dict):
                return {k: encode(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [encode(v) for v in obj]
            return obj

        return {
            "schema_version": self.schema_version,
            "epoch_utc": self.epoch_utc,
            "series_label": self.series_label,
            "s_life_years": str(self.s_life_years),
            "e_bar_years": str(self.e_bar_years),
            "n_persons": str(self.n_persons),
            "burn_life_years": str(self.burn_life_years),
            "coverage": encode(self.coverage),
            "provenance": encode(self.provenance),
        }

    def render(self) -> str:
        """Deterministic bytes (P5): sorted keys, no float ever serialized."""
        return json.dumps(self.to_json_dict(), indent=2, sort_keys=True) + "\n"


def validate_print_dict(data: dict) -> None:
    """Schema gate for consumers/recomputers. P7: coverage is REQUIRED and
    must carry measured_share — a print may not omit its own honesty."""
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise PrintSchemaError(f"missing required fields: {missing}")
    if data["schema_version"] != PRINT_SCHEMA_VERSION:
        raise PrintSchemaError(f"unknown schema_version {data['schema_version']!r}")
    validate_epoch(data["epoch_utc"])
    if data["series_label"] not in SERIES_LABELS:
        raise PrintSchemaError(f"series_label must be one of {SERIES_LABELS}")
    cov = data["coverage"]
    if not isinstance(cov, dict) or "measured_share" not in cov:
        raise PrintSchemaError("coverage.measured_share is required (invariant P7)")
    prov = data["provenance"]
    if not isinstance(prov, dict) or "methodology_version" not in prov or "snapshots" not in prov:
        raise PrintSchemaError("provenance must carry methodology_version and snapshots")


@dataclass(frozen=True)
class DualSeries:
    """One epoch's dual publication (DECISIONS: settle on measurement,
    inform with the model).

    ``settlement`` is the measured-period S print — REQUIRED, and the ONLY
    place a settlement value can come from. ``informational`` is the
    cohort-model print — optional (absent before P2 delivers cohort values,
    D-04) and structurally incapable of affecting settlement: the
    settlement_value accessor reads the SETTLEMENT print alone, and both
    prints are frozen.
    """

    settlement: WeeklyPrint
    informational: WeeklyPrint | None = None

    def __post_init__(self) -> None:
        if self.settlement.series_label != "SETTLEMENT":
            raise PrintSchemaError("settlement slot requires a SETTLEMENT-labeled print")
        if self.informational is not None:
            if self.informational.series_label != "INFORMATIONAL":
                raise PrintSchemaError("informational slot requires an INFORMATIONAL-labeled print")
            if self.informational.epoch_utc != self.settlement.epoch_utc:
                raise PrintSchemaError(
                    "dual series must share one epoch: "
                    f"{self.settlement.epoch_utc} vs {self.informational.epoch_utc}"
                )

    @property
    def settlement_value(self) -> Decimal:
        """THE value derivatives settle on. Reads the SETTLEMENT print only —
        there is no code path from the cohort model to this number."""
        return self.settlement.s_life_years

    def to_json_dict(self) -> dict:
        out = {"settlement": self.settlement.to_json_dict()}
        out["informational"] = self.informational.to_json_dict() if self.informational else None
        return out

    def render(self) -> str:
        return json.dumps(self.to_json_dict(), indent=2, sort_keys=True) + "\n"
