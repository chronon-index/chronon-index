"""B-uc3-02 / AC-3.3 / RALPH §6: snapshots are never deleted or modified.

Two history checks against git (the committed record itself):

1. Any tracked file under data/snapshots/ other than the manifests must
   never appear as Modified or Deleted in any commit.
2. Manifests are append-only ledgers: across every consecutive pair of
   committed versions, every (file, sha256) row present in the older
   version must exist unchanged in the newer one. Rows may be added; a
   changed or vanished hash is a rewrite of history and fails.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args], check=True, capture_output=True, text=True
    ).stdout


def test_snapshot_files_never_modified_or_deleted():
    out = _git("log", "--diff-filter=MD", "--name-only", "--pretty=format:", "--", "data/snapshots")
    touched = {line for line in out.splitlines() if line.strip()}
    violations = sorted(p for p in touched if not p.endswith("manifest.json"))
    assert violations == [], (
        "snapshot files were modified or deleted in history (forbidden):\n" + "\n".join(violations)
    )


def _manifest_versions(path: str) -> list[dict]:
    """All committed versions of one manifest, oldest first."""
    hashes = _git("log", "--reverse", "--pretty=format:%H", "--", path).splitlines()
    versions = []
    for h in hashes:
        raw = _git("show", f"{h}:{path}")
        versions.append(json.loads(raw))
    return versions


def test_manifests_are_append_only():
    manifest_paths = [
        line
        for line in _git("ls-files", "data/snapshots").splitlines()
        if line.endswith("manifest.json")
    ]
    assert manifest_paths, "no committed manifests found"
    problems: list[str] = []
    for path in manifest_paths:
        versions = _manifest_versions(path)
        for older, newer in zip(versions, versions[1:]):
            for name, row in older.get("files", {}).items():
                new_row = newer.get("files", {}).get(name)
                if new_row is None:
                    problems.append(f"{path}: row {name!r} deleted between versions")
                elif new_row.get("sha256") != row.get("sha256"):
                    problems.append(f"{path}: row {name!r} sha256 rewritten")
    assert problems == [], "\n".join(problems)


def test_worktree_manifests_extend_head():
    """The uncommitted working tree may only ADD manifest rows, never edit
    or drop committed ones — catches a rewrite before it is ever committed."""
    manifest_paths = [
        line
        for line in _git("ls-files", "data/snapshots").splitlines()
        if line.endswith("manifest.json")
    ]
    problems: list[str] = []
    for path in manifest_paths:
        try:
            head = json.loads(_git("show", f"HEAD:{path}"))
        except subprocess.CalledProcessError:
            continue  # staged-but-new manifest: no committed rows to protect yet
        work = json.loads((REPO / path).read_text(encoding="utf-8"))
        for name, row in head.get("files", {}).items():
            work_row = work.get("files", {}).get(name)
            if work_row is None:
                problems.append(f"{path}: worktree drops committed row {name!r}")
            elif work_row.get("sha256") != row.get("sha256"):
                problems.append(f"{path}: worktree rewrites sha256 of {name!r}")
    assert problems == [], "\n".join(problems)
