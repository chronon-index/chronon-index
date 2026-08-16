"""Snapshot-first data acquisition (RALPH_LOOP §6; RP Parts VI-VII; SPEC#3).

Fetch sources over the network ONCE into data/snapshots/<date>/ with a
manifest recording, per file: source URL, retrieval timestamp (UTC), sha256,
and byte count. All computation then runs offline from the snapshot;
:func:`verify_manifest` proves a snapshot is intact before any compute
(AC-1.5 offline-only rule).

Network etiquette (verified the hard way — see loop/LEARNINGS.md): send a
User-Agent, keep requests few and large, back off exponentially with jitter,
and never touch the World Bank API (WAF-blocked this project 2026-08-16).
"""

from __future__ import annotations

import hashlib
import json
import random
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_FILE = "manifest.json"

USER_AGENT = (
    "tly-research/0.1 (benjaminpauls.stocks@gmail.com; "
    "open reproducible index research; github: pending)"
)

NETWORK_POLICY = (
    "User-Agent sent; few-and-large requests; exponential backoff with "
    "jitter; World Bank API not used (WAF-blocked 2026-08-16)."
)


class SnapshotIntegrityError(Exception):
    """A snapshot file is missing or does not match its manifest hash."""


def fetch_url(url: str, attempts: int = 4, sleep: Callable[[float], None] = time.sleep) -> bytes:
    """GET with User-Agent and exponential backoff + jitter. Raises after N attempts."""
    last_err: Exception | None = None
    for attempt in range(attempts):
        if attempt:
            sleep((2**attempt) + random.uniform(0.0, 1.5))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, OSError) as err:
            last_err = err
            print(f"  attempt {attempt + 1}/{attempts} failed: {err}", file=sys.stderr)
    raise RuntimeError(f"fetch failed after {attempts} attempts: {url}") from last_err


def fetch_snapshot(
    snapshot_dir: Path,
    sources: Mapping[str, str],
    fetcher: Callable[[str], bytes] = fetch_url,
    note: str | None = None,
) -> dict:
    """Fetch every source into ``snapshot_dir`` and write the manifest.

    ``fetcher`` is injectable so the manifest logic is testable offline.
    Returns the manifest dict (also written as manifest.json).
    """
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict = {
        "snapshot_date": snapshot_dir.name,
        "network_policy": NETWORK_POLICY,
        "files": {},
    }
    if note:
        manifest["note"] = note
    for name, url in sources.items():
        body = fetcher(url)
        (snapshot_dir / name).write_bytes(body)
        manifest["files"][name] = {
            "source_url": url,
            "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "sha256": hashlib.sha256(body).hexdigest(),
            "bytes": len(body),
        }
    (snapshot_dir / MANIFEST_FILE).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def verify_manifest(snapshot_dir: Path, *, require_all: bool = True) -> dict:
    """Recompute every file hash against the manifest; raise on any mismatch.

    Returns the verified manifest. This is the offline integrity gate: a
    compute path must call this before reading snapshot files (AC-1.5), so
    a truncated or edited snapshot can never silently produce a number.

    ``require_all=False`` permits ABSENCE of files the manifest itself
    declares uncommitted (``in_git: false`` — large snapshots kept out of
    git by policy, RP Part VII); their recorded hashes remain the citable
    record. A present file must always match its hash, and files without
    the in_git:false marker must always exist.
    """
    manifest_path = snapshot_dir / MANIFEST_FILE
    if not manifest_path.is_file():
        raise SnapshotIntegrityError(f"missing manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for name, meta in manifest["files"].items():
        path = snapshot_dir / name
        if not path.is_file():
            if not require_all and meta.get("in_git") is False:
                continue
            raise SnapshotIntegrityError(f"missing snapshot file: {path}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != meta["sha256"]:
            raise SnapshotIntegrityError(
                f"hash mismatch for {name}: manifest {meta['sha256']}, actual {digest}"
            )
    return manifest
