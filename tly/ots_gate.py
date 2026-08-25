"""OpenTimestamps publish gate (B-uc4-06; SPEC#4 AC-4.3; RP Part VII).

Bridges E-02's StampStore workflow to the archive chain and CI:

``stamp``  — for every link in the committed chain, record
             ``stamps/<epoch-stem>.hash`` = the link's record_hash and
             invoke the real client for any missing proof. Backfill is
             honest: a proof made later attests "this hash existed by
             stamp time", never the print time — the chain itself dates
             the print.
``verify`` — the publish blocker: every archived epoch must have a
             recorded digest EQUAL to its chain record_hash and a .ots
             proof on disk. Any gap names the epoch and exits nonzero.

NOT asserted here: Bitcoin attestation depth. A fresh proof is pending
until a calendar aggregates it into a Bitcoin block; upgrading and
chain-verifying proofs is the client's job against a Bitcoin source of
truth (documented in REPRODUCE_FIXING). The AC gates existence + hash
match before publish, and that is exactly what ``verify`` enforces.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from tly.timestamping import STAMPED, StampStore

REPO_ROOT = Path(__file__).resolve().parent.parent


def chain_targets(archive_root: Path) -> dict[str, str]:
    """{epoch-stem: record_hash} for every committed chain link."""
    chain = json.loads((archive_root / "chain.json").read_text(encoding="utf-8"))
    return {Path(link["file"]).stem: link["record_hash"] for link in chain}


def gate(archive_root: Path, stamps_root: Path) -> list[str]:
    """Every archived epoch stamped-and-matching. [] means publishable."""
    problems: list[str] = []
    store = StampStore(stamps_root)
    for name, record_hash in chain_targets(archive_root).items():
        status = store.status(name, live_digest=record_hash)
        if status.digest is None:
            problems.append(f"{name}: no recorded stamp target for record_hash {record_hash}")
        elif status.digest != record_hash:
            problems.append(
                f"{name}: recorded digest {status.digest} != chain record_hash {record_hash}"
            )
        elif status.state != STAMPED:
            problems.append(f"{name}: target recorded but no .ots proof exists")
    return problems


def stamp_missing(archive_root: Path, stamps_root: Path) -> list[str]:
    """Record + stamp every unproven chain link; returns names stamped."""
    store = StampStore(stamps_root)
    stamped: list[str] = []
    for name, record_hash in chain_targets(archive_root).items():
        store.record_target(name, record_hash)
        if store.status(name).state != STAMPED:
            store.stamp(name)
            stamped.append(name)
    return stamped


def main(argv: list[str]) -> int:
    mode = argv[0] if argv else "verify"
    archive_root = REPO_ROOT / "archive"
    stamps_root = REPO_ROOT / "stamps"
    if mode == "stamp":
        stamped = stamp_missing(archive_root, stamps_root)
        print(f"stamped {len(stamped)} epoch(s): {', '.join(stamped) or 'none needed'}")
        return 0
    problems = gate(archive_root, stamps_root)
    for p in problems:
        print(f"OTS GATE: {p}")
    if problems:
        print("OTS GATE FAILED — publish blocked (SPEC#4 AC-4.3)")
        return 1
    n = len(chain_targets(archive_root))
    print(f"OTS gate passed: {n} archived epoch(s) stamped and matching")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
