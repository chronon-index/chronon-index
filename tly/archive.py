"""Immutable print archive (SPEC#4; DECISIONS #7/#9; invariant P4; B-uc4-08).

Append-only per-epoch records bound into a hash chain:

    record_hash(n) = sha256(prev_hash(n-1) + render(print_n))

so every print commits to the entire history before it. Editing or
removing ANY historical record breaks every later link — the chain is
verifiable by anyone from the files alone, and it is what the settlement
fixing module (SPEC#7) will anchor to (and OpenTimestamps stamps at E-02).

Mutation attempts raise ArchiveImmutabilityError: appending an epoch that
already exists, appending out of order, or asking to overwrite are all
refused. There is no delete.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tly.prints import WeeklyPrint, validate_epoch

GENESIS_HASH = "0" * 64
CHAIN_FILE = "chain.json"


class ArchiveImmutabilityError(RuntimeError):
    """An operation would mutate published history."""


class ArchiveChainError(RuntimeError):
    """The stored chain does not verify."""


def _record_hash(prev_hash: str, rendered: str) -> str:
    return hashlib.sha256((prev_hash + rendered).encode("utf-8")).hexdigest()


class PrintArchive:
    """Append-only archive rooted at a directory."""

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    @property
    def chain_path(self) -> Path:
        return self.root / CHAIN_FILE

    def _load_chain(self) -> list[dict]:
        if not self.chain_path.is_file():
            return []
        return json.loads(self.chain_path.read_text(encoding="utf-8"))

    def append(self, p: WeeklyPrint) -> str:
        """Append one print; returns its record hash."""
        chain = self._load_chain()
        epoch_dt = validate_epoch(p.epoch_utc)
        if chain:
            last = chain[-1]
            if p.epoch_utc == last["epoch_utc"] or any(
                c["epoch_utc"] == p.epoch_utc for c in chain
            ):
                raise ArchiveImmutabilityError(
                    f"epoch {p.epoch_utc} already archived — prints are FINAL"
                )
            if epoch_dt <= validate_epoch(last["epoch_utc"]):
                raise ArchiveImmutabilityError(
                    f"epoch {p.epoch_utc} not after archive head {last['epoch_utc']}"
                )
            prev_hash = last["record_hash"]
        else:
            prev_hash = GENESIS_HASH

        rendered = p.render()
        record_hash = _record_hash(prev_hash, rendered)
        record_file = self.root / f"{epoch_dt.date().isoformat()}.json"
        if record_file.exists():
            raise ArchiveImmutabilityError(f"record file exists: {record_file.name}")
        record_file.write_text(rendered, encoding="utf-8")
        chain.append(
            {
                "epoch_utc": p.epoch_utc,
                "file": record_file.name,
                "prev_hash": prev_hash,
                "record_hash": record_hash,
            }
        )
        self.chain_path.write_text(
            json.dumps(chain, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return record_hash

    def verify(self) -> list[dict]:
        """Recompute the full chain from the record files; raise on any
        break. Returns the verified chain."""
        chain = self._load_chain()
        prev_hash = GENESIS_HASH
        last_epoch = None
        for link in chain:
            rendered = (self.root / link["file"]).read_text(encoding="utf-8")
            if link["prev_hash"] != prev_hash:
                raise ArchiveChainError(f"{link['file']}: prev_hash broken")
            expected = _record_hash(prev_hash, rendered)
            if link["record_hash"] != expected:
                raise ArchiveChainError(
                    f"{link['file']}: record hash mismatch — history was edited"
                )
            epoch_dt = validate_epoch(link["epoch_utc"])
            if last_epoch is not None and epoch_dt <= last_epoch:
                raise ArchiveChainError(f"{link['file']}: epoch order broken")
            last_epoch = epoch_dt
            prev_hash = link["record_hash"]
        on_disk = {p.name for p in self.root.glob("*.json") if p.name != CHAIN_FILE}
        chained = {link["file"] for link in chain}
        if on_disk - chained:
            raise ArchiveChainError(f"unchained record files: {sorted(on_disk - chained)}")
        return chain

    @property
    def head_hash(self) -> str:
        chain = self._load_chain()
        return chain[-1]["record_hash"] if chain else GENESIS_HASH
