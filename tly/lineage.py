"""Lineage verification (SPEC#4 AC-4.1; RP Part X P9; B-uc4-03).

Invariant P9: every published value traces to a manifest entry; no orphan
numbers. For a published API tree this means:

- every print cites at least one snapshot in its provenance, and every
  cited (snapshot, file, sha256) triple must EXIST in the committed
  manifests with exactly that hash — a print may not cite data the repo
  cannot produce;
- published magnitudes are non-negative where the quantity is a stock
  (S, N, Ē); burn is a signed flow and is exempt;
- the API tree itself is internally verified (index closed-world) before
  lineage is walked.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from tly.api import API_ROOT, verify_api

NON_NEGATIVE_FIELDS = ("s_life_years", "e_bar_years", "n_persons")


def check_lineage(api_out_dir: Path, snapshots_root: Path) -> list[str]:
    """All P9 violations in a published API tree (empty list = clean)."""
    verify_api(api_out_dir)  # integrity first; raises on tamper
    root = api_out_dir.joinpath(*API_ROOT)
    problems: list[str] = []

    manifests: dict[str, dict] = {}
    for d in sorted(p for p in snapshots_root.iterdir() if p.is_dir()):
        mf = d / "manifest.json"
        if mf.is_file():
            manifests[d.name] = json.loads(mf.read_text(encoding="utf-8"))["files"]

    print_files = sorted(root.glob("prints/*.json")) + [root / "latest.json"]
    for pf in print_files:
        where = pf.relative_to(root)
        data = json.loads(pf.read_text(encoding="utf-8"))

        for field in NON_NEGATIVE_FIELDS:
            if Decimal(str(data[field])) < 0:
                problems.append(f"{where}: {field} is negative")

        cited = data.get("provenance", {}).get("snapshots", {})
        if not cited:
            problems.append(f"{where}: no snapshots cited — orphan print")
            continue
        for snap_name, files in cited.items():
            manifest = manifests.get(snap_name)
            if manifest is None:
                problems.append(f"{where}: cites unknown snapshot {snap_name!r}")
                continue
            if not files:
                problems.append(f"{where}: cites snapshot {snap_name!r} with no files")
            for fname, sha in files.items():
                row = manifest.get(fname)
                if row is None:
                    problems.append(f"{where}: cites {snap_name}/{fname} absent from manifest")
                elif row.get("sha256") != sha:
                    problems.append(
                        f"{where}: cited hash for {snap_name}/{fname} does not "
                        "match the committed manifest"
                    )
    return problems
