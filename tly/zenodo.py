"""Zenodo deposit preparation (RP Part VII; E-06). Dry-run only.

Packages one vintage for a DOI deposit: the deposit directory contains the
redistributable snapshot files, a Zenodo deposition metadata payload, and
a checksums file tied to the committed manifest. NO network and NO account
— the live upload is E-05's HUMAN-gated step; this builder only prepares.

License-aware inclusion (the licensing table is LAW here, docs/LICENSING.md):
- INCLUDED: UN WPP files (CC BY 3.0 IGO — cleared), OWID files (CC BY over
  cleared upstream), WMD files (MIT), and license-evidence pages we cite.
- EXCLUDED, with the reason recorded in the deposit metadata: WHO GHO
  extracts (confirmed non-commercial clause — REDISTRIBUTING them in an
  open DOI archive is exactly what the clause restricts; the deposit
  instead carries their manifest hashes + source URLs so anyone can
  refetch and verify independently). Large in_git:false files are likewise
  manifest-only rows (hash + URL travel; bytes do not).

Every exclusion is visible in the deposition metadata — the deposit never
pretends to be more complete than the licenses allow.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# filename-prefix classification, per docs/LICENSING.md status
_EXCLUDE_PREFIXES: dict[str, str] = {
    "gho_": "WHO GHO extract — confirmed non-commercial clause "
    "(docs/LICENSING.md, VERIFIED-RESTRICTED 2026-08-17); refetch via "
    "the recorded source_url and verify against the sha256",
    "who_": "WHO site content — evidence snapshot; same restriction family",
    "hmd_": "mortality.org site content — evidence snapshot; not data",
    "vaupel_": "literature PDF under CC BY-NC 2.0 DE — non-commercial license; "
    "cite and link, never redeposit",
}


def classify(name: str) -> tuple[bool, str]:
    """(include?, reason). Inclusion reasons cite the licensing table."""
    for prefix, reason in _EXCLUDE_PREFIXES.items():
        if name.startswith(prefix):
            return False, reason
    return True, "redistributable per docs/LICENSING.md (cleared/MIT/CC BY chain)"


def build_deposit(vintage: str, out_dir: Path, repo_root: Path = REPO_ROOT) -> dict:
    """Prepare the deposit directory for one vintage; returns the
    deposition metadata that was written."""
    snap = repo_root / "data" / "snapshots" / vintage
    manifest_path = snap / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"no vintage {vintage}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    deposit = out_dir / f"tly-vintage-{vintage}"
    files_dir = deposit / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    included: dict[str, str] = {}
    excluded: dict[str, dict] = {}
    for name, row in sorted(manifest["files"].items()):
        include, reason = classify(Path(name).name)
        src = snap / name
        if row.get("in_git") is False and not src.is_file():
            excluded[name] = {
                "reason": "large file kept out of git by policy; manifest row travels",
                "sha256": row["sha256"],
                "source_url": row.get("source_url"),
            }
            continue
        if not include:
            excluded[name] = {
                "reason": reason,
                "sha256": row["sha256"],
                "source_url": row.get("source_url"),
            }
            continue
        dest = files_dir / Path(name).name
        shutil.copy2(src, dest)
        included[name] = row["sha256"]

    # the manifest itself always travels — it IS the record
    shutil.copy2(manifest_path, deposit / "manifest.json")

    deposition = {
        "metadata": {
            "title": f"TLY snapshot vintage {vintage}",
            "upload_type": "dataset",
            "description": (
                "Content-hashed upstream data snapshot for the TLY index "
                f"(vintage {vintage}). Includes only redistributable files; "
                "excluded files are listed with reasons, hashes and source "
                "URLs for independent refetch. See docs/REPRODUCE_FIXING.md "
                "in the source repository."
            ),
            "creators": [{"name": "TLY project"}],
            "license": "cc-by-4.0",
            "version": vintage,
            "keywords": ["demography", "life expectancy", "open data", "TLY"],
        },
        "included_files": included,
        "excluded_files": excluded,
    }
    (deposit / "deposition.json").write_text(
        json.dumps(deposition, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (deposit / "CHECKSUMS.sha256").write_text(
        "".join(f"{sha}  files/{Path(name).name}\n" for name, sha in sorted(included.items())),
        encoding="utf-8",
    )
    return deposition
