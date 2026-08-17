"""Dispute log (SPEC#7 AC-7.4; DECISIONS defaults; C-uc7-04).

DECISIONS: "Dispute window on fixings: 48 h, log-only, never blocks the
next print." A dispute is a RECORD, not a lever: filing one changes no
fixing, delays no epoch, triggers no recomputation. If a dispute turns out
substantiated, the response is the correction ledger folding into the next
epoch — the dispute log is where the challenge and its disposition are
visible forever.

Mechanics: append-only JSONL keyed to the disputed fixing hash; filings
accepted only inside the 48-hour window after the fixing's epoch (the
timestamp is caller-supplied and validated — this module never reads a
clock, so behavior is deterministic and testable); late filings are
refused loudly, not silently dropped.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

from tly.prints import validate_epoch

WINDOW = timedelta(hours=48)
LOG_FILE = "disputes.jsonl"


class DisputeWindowClosed(ValueError):
    """Filed outside the 48-hour window."""


class DisputeFormatError(ValueError):
    """Malformed dispute filing."""


class DisputeLog:
    """Append-only dispute log rooted at a directory."""

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self.root / LOG_FILE

    def file_dispute(
        self,
        *,
        fixing_hash: str,
        epoch_utc: str,
        filed_utc: str,
        claimant: str,
        claim: str,
    ) -> dict:
        """Record a dispute. Returns the appended record. Alters nothing."""
        if len(fixing_hash) != 64:
            raise DisputeFormatError("fixing_hash must be a sha256 hex digest")
        if not claimant.strip() or not claim.strip():
            raise DisputeFormatError("claimant and claim are required")
        epoch = validate_epoch(epoch_utc)
        try:
            filed = datetime.fromisoformat(filed_utc)
        except ValueError as err:
            raise DisputeFormatError(f"filed_utc not ISO-8601: {filed_utc!r}") from err
        if filed.tzinfo is None:
            raise DisputeFormatError("filed_utc must be timezone-aware")
        if filed < epoch:
            raise DisputeFormatError("a dispute cannot precede its epoch")
        if filed - epoch > WINDOW:
            raise DisputeWindowClosed(
                f"window closed: {filed_utc} is more than 48h after {epoch_utc}"
            )
        record = {
            "fixing_hash": fixing_hash,
            "epoch_utc": epoch_utc,
            "filed_utc": filed_utc,
            "claimant": claimant,
            "claim": claim,
            "effect": "log-only; the fixing stands; corrections, if any, fold forward",
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")
        return record

    def disputes(self) -> list[dict]:
        if not self.path.is_file():
            return []
        return [
            json.loads(line)
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
