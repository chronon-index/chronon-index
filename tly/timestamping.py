"""OpenTimestamps workflow (RP Part VII; SPEC#4 AC-4.3; E-02).

Bitcoin-anchored timestamping of print/archive hashes via the external
`ots` client (opentimestamps-client). This module owns the WORKFLOW —
what gets stamped, where proofs live, what state each proof is in — and
shells out to the real client for the cryptography. It never fakes a
proof: when no client is installed, targets are tracked as UNSTAMPED and
the status says so (the CI gate at B-uc4-06 turns that into a publish
blocker once the client is provisioned).

Layout, beside the archive: for each stamped target
    stamps/<name>.hash   the 64-hex digest that was stamped (one line)
    stamps/<name>.ots    the proof, once the client produced it

States: UNSTAMPED (no .ots), STAMPED (proof exists; may still be pending
Bitcoin attestation — upgrading is the client's job), plus a hash-match
check between the .hash file and the live target (a stale stamp is
surfaced, never hidden).
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

UNSTAMPED = "UNSTAMPED"
STAMPED = "STAMPED"
STALE = "STALE"  # .hash no longer matches the live target hash


class TimestampError(RuntimeError):
    pass


def ots_client() -> str | None:
    """Path to the external `ots` client, or None (honest absence)."""
    return shutil.which("ots")


@dataclass(frozen=True)
class StampStatus:
    name: str
    state: str
    digest: str | None
    proof_path: Path | None


class StampStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _hash_path(self, name: str) -> Path:
        return self.root / f"{name}.hash"

    def _ots_path(self, name: str) -> Path:
        return self.root / f"{name}.ots"

    def record_target(self, name: str, digest: str) -> Path:
        """Write the digest to be stamped. Refuses to silently change an
        already-recorded digest (stamped history is history)."""
        if len(digest) != 64:
            raise TimestampError("digest must be sha256 hex")
        path = self._hash_path(name)
        if path.exists() and path.read_text(encoding="utf-8").strip() != digest:
            raise TimestampError(
                f"{name}: digest already recorded and differs — a new epoch "
                "needs a new name, never an overwrite"
            )
        path.write_text(digest + "\n", encoding="utf-8")
        return path

    def stamp(self, name: str) -> StampStatus:
        """Invoke the real client on the recorded hash file. Raises if no
        client is installed — callers decide whether that blocks (CI) or
        merely records UNSTAMPED (local dev)."""
        client = ots_client()
        if client is None:
            raise TimestampError(
                "no `ots` client installed — install opentimestamps-client; "
                "the target remains UNSTAMPED (never faked)"
            )
        hash_path = self._hash_path(name)
        if not hash_path.is_file():
            raise TimestampError(f"{name}: no recorded target to stamp")
        subprocess.run(
            [client, "stamp", str(hash_path)],
            check=True,
            capture_output=True,
            timeout=120,
        )
        produced = hash_path.with_suffix(".hash.ots")
        if produced.is_file():  # client names proofs <file>.ots
            produced.replace(self._ots_path(name))
        if not self._ots_path(name).is_file():
            raise TimestampError(f"{name}: client ran but produced no proof")
        return self.status(name)

    def status(self, name: str, live_digest: str | None = None) -> StampStatus:
        hash_path = self._hash_path(name)
        if not hash_path.is_file():
            return StampStatus(name=name, state=UNSTAMPED, digest=None, proof_path=None)
        digest = hash_path.read_text(encoding="utf-8").strip()
        if live_digest is not None and live_digest != digest:
            return StampStatus(name=name, state=STALE, digest=digest, proof_path=None)
        ots = self._ots_path(name)
        if ots.is_file():
            return StampStatus(name=name, state=STAMPED, digest=digest, proof_path=ots)
        return StampStatus(name=name, state=UNSTAMPED, digest=digest, proof_path=None)
