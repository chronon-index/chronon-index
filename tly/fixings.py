"""Settlement fixing records (SPEC#7 AC-7.6; DECISIONS #7/#9; C-uc7-01).

A fixing is the settlement-grade record of one epoch's value. Its schema
is provenance-complete BY CONSTRUCTION: value, epoch, methodology version,
snapshot manifest hashes, and source URLs are all mandatory — a fixing
with incomplete provenance cannot exist, not merely not-validate.

Lifecycle: DRAFT → FINAL, one way. A DRAFT may be discarded (it is not yet
a published fact); FINAL is forever — every attribute write on a FINAL
fixing raises (invariant P4; the named test is C-uc7-02). Finalization
computes the fixing hash over the canonical rendering, which is what
external recomputers compare and what the dispute log references.
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal

from tly.prints import validate_epoch

DRAFT = "DRAFT"
FINAL = "FINAL"


class FixingValidationError(ValueError):
    """The fixing record is provenance-incomplete or malformed."""


class FixingImmutabilityError(RuntimeError):
    """A FINAL fixing was asked to change (invariant P4; DECISIONS #7)."""


class Fixing:
    """One epoch's settlement fixing. Mutable only while DRAFT."""

    def __init__(
        self,
        epoch_utc: str,
        value: Decimal,
        methodology_version: str,
        snapshot_hashes: dict[str, dict[str, str]],
        source_urls: tuple[str, ...],
    ):
        validate_epoch(epoch_utc)
        if not isinstance(value, Decimal):
            raise FixingValidationError("value must be Decimal")
        if value < 0:
            raise FixingValidationError("a fixing value cannot be negative")
        if not str(methodology_version).strip():
            raise FixingValidationError("methodology_version is required")
        if not snapshot_hashes or not any(files for files in snapshot_hashes.values()):
            raise FixingValidationError("snapshot_hashes must cite at least one snapshot file")
        for snap, files in snapshot_hashes.items():
            for name, sha in files.items():
                if len(str(sha)) != 64:
                    raise FixingValidationError(f"bad sha256 for {snap}/{name}: {sha!r}")
        if not source_urls or not all(
            str(u).startswith(("https://", "http://")) for u in source_urls
        ):
            raise FixingValidationError("source_urls must be non-empty, http(s) only")

        object.__setattr__(self, "epoch_utc", epoch_utc)
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "methodology_version", methodology_version)
        object.__setattr__(self, "snapshot_hashes", snapshot_hashes)
        object.__setattr__(self, "source_urls", tuple(source_urls))
        object.__setattr__(self, "status", DRAFT)
        object.__setattr__(self, "fixing_hash", None)

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "status", DRAFT) == FINAL:
            raise FixingImmutabilityError(
                f"fixing {self.epoch_utc} is FINAL — {name!r} cannot change; "
                "corrections route to the ledger and the NEXT epoch (DEC#7)"
            )
        object.__setattr__(self, name, value)

    def render(self) -> str:
        """Canonical bytes — what the fixing hash covers."""
        return (
            json.dumps(
                {
                    "epoch_utc": self.epoch_utc,
                    "value": str(self.value),
                    "methodology_version": self.methodology_version,
                    "snapshot_hashes": self.snapshot_hashes,
                    "source_urls": list(self.source_urls),
                    "status": self.status,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

    def finalize(self) -> str:
        """DRAFT → FINAL, one way. Returns the fixing hash."""
        if self.status == FINAL:
            raise FixingImmutabilityError(f"fixing {self.epoch_utc} already FINAL")
        object.__setattr__(self, "status", FINAL)
        digest = hashlib.sha256(self.render().encode("utf-8")).hexdigest()
        object.__setattr__(self, "fixing_hash", digest)
        return digest
