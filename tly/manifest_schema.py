"""Manifest schema validation (SPEC#3 AC-3.3; B-uc3-01).

Both directions, per snapshot directory:

- DISK → MANIFEST: every file on disk (manifest.json excluded) must have a
  manifest row. An unmanifested file is an unaccounted input — the build
  fails (invariant P9: no orphan numbers means no orphan inputs).
- MANIFEST → FIELDS: every row needs sha256 + bytes, plus provenance —
  either fetched (source_url + retrieved_utc) or derived (derived_from +
  derived_from_sha256 + derivation). Present files must hash-match their
  row; rows marked in_git:false may be absent from disk (large-file
  policy) but never malformed.

Run by the test suite, therefore by CI on every push.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tly.snapshot import MANIFEST_FILE


class ManifestSchemaError(ValueError):
    """A snapshot directory violates the manifest schema."""


def validate_snapshot_dir(snapshot_dir: Path) -> list[str]:
    """Validate one snapshot directory; returns the list of violations
    (empty = valid). Raising is the caller's choice so CI output can show
    ALL problems at once instead of the first."""
    problems: list[str] = []
    manifest_path = snapshot_dir / MANIFEST_FILE
    if not manifest_path.is_file():
        return [f"{snapshot_dir.name}: missing {MANIFEST_FILE}"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows: dict = manifest.get("files", {})

    on_disk = {
        str(p.relative_to(snapshot_dir))
        for p in snapshot_dir.rglob("*")
        if p.is_file() and p.name != MANIFEST_FILE
    }

    for name in sorted(on_disk - set(rows)):
        problems.append(f"{snapshot_dir.name}/{name}: file on disk has NO manifest row")

    for name, row in sorted(rows.items()):
        where = f"{snapshot_dir.name}/{name}"
        if not isinstance(row, dict):
            problems.append(f"{where}: row is not an object")
            continue
        for field in ("sha256", "bytes"):
            if field not in row:
                problems.append(f"{where}: missing {field}")
        fetched = "source_url" in row
        derived = "derived_from" in row
        if fetched:
            if "retrieved_utc" not in row:
                problems.append(f"{where}: fetched row missing retrieved_utc")
        elif derived:
            for field in ("derived_from_sha256", "derivation"):
                if field not in row:
                    problems.append(f"{where}: derived row missing {field}")
            parent = row.get("derived_from")
            if parent not in rows:
                problems.append(f"{where}: derived_from {parent!r} has no manifest row")
            elif rows[parent].get("sha256") != row.get("derived_from_sha256"):
                problems.append(f"{where}: derived_from_sha256 does not match parent row")
        else:
            problems.append(f"{where}: row has neither source_url nor derived_from")

        path = snapshot_dir / name
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if "sha256" in row and digest != row["sha256"]:
                problems.append(f"{where}: disk sha256 mismatch")
            if "bytes" in row and path.stat().st_size != row["bytes"]:
                problems.append(f"{where}: disk size mismatch")
        elif row.get("in_git") is not False:
            problems.append(f"{where}: missing from disk but not marked in_git:false")
    return problems


def validate_all_snapshots(snapshots_root: Path) -> list[str]:
    problems: list[str] = []
    for d in sorted(p for p in snapshots_root.iterdir() if p.is_dir()):
        problems.extend(validate_snapshot_dir(d))
    return problems
