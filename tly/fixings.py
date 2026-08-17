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


def settle_from_archive(archive, epoch_utc: str, snapshots_root) -> Fixing:
    """The ONE way to produce a settlement fixing (SPEC#7 AC-7.2; DEC#7):
    read the epoch's print from the archive and finalize a fixing carrying
    that print's value, its cited snapshot hashes, and the REAL source
    URLs looked up from the committed manifests those hashes point into.

    First-print-settles holds by composition: the archive accepts exactly
    one print per epoch (re-appends raise), and this function reads only
    the archive — so the fixing can never see a later "better" value, and
    settling the same epoch twice yields byte-identical fixings.
    """
    import json as _json
    from pathlib import Path as _Path

    chain = archive.verify()
    link = next((c for c in chain if c["epoch_utc"] == epoch_utc), None)
    if link is None:
        raise FixingValidationError(
            f"no archived print for epoch {epoch_utc} — a fixing cannot precede its print"
        )
    record = _json.loads((archive.root / link["file"]).read_text(encoding="utf-8"))
    if record.get("series_label") != "SETTLEMENT":
        raise FixingValidationError(
            f"epoch {epoch_utc} archived a {record.get('series_label')!r} print — "
            "the cohort/INFORMATIONAL series can never be a settlement input "
            "(SPEC#7 AC-7.4; DECISIONS dual-series rule)"
        )
    prov = record["provenance"]

    urls: list[str] = []
    root = _Path(snapshots_root)
    for snap, files in sorted(prov["snapshots"].items()):
        manifest_path = root / snap / "manifest.json"
        if not manifest_path.is_file():
            raise FixingValidationError(f"cited snapshot {snap} has no manifest")
        rows = _json.loads(manifest_path.read_text(encoding="utf-8"))["files"]
        for name in sorted(files):
            row = rows.get(name)
            if row is None:
                raise FixingValidationError(f"cited file {snap}/{name} not in manifest")
            url = row.get("source_url")
            if url:
                urls.append(url)
            elif row.get("derived_from"):
                parent = rows.get(row["derived_from"], {})
                if parent.get("source_url"):
                    urls.append(parent["source_url"])
    if not urls:
        raise FixingValidationError("no source URLs resolvable from cited manifests")

    fixing = Fixing(
        epoch_utc=epoch_utc,
        value=Decimal(record["s_life_years"]),
        methodology_version=prov["methodology_version"],
        snapshot_hashes=prov["snapshots"],
        source_urls=tuple(dict.fromkeys(urls)),  # dedupe, keep order
    )
    fixing.finalize()
    return fixing
