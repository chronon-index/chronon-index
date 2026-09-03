"""Zenodo deposit automation (S-03; E-05 successor; RP Part VII).

Quarterly, CI deposits a CURATED archive set to Zenodo and gets a DOI —
one citable, CERN-preserved record per quarter. Never the repo zip:
the GitHub auto-archive toggle stays OFF because a release would
deposit committed WHO GHO files, and LICENSING excludes WHO/IHME (and
NC/all-rights-reserved literature: vaupel_*, iosco_*) from deposits.

Curation rule, executable: a file enters the deposit iff its top-level
tree is in DEPOSIT_TREES and no EXCLUDED_PREFIX matches its name. The
suite pins that the exclusion actually bites on the real repo.

Credentials: ZENODO_TOKEN is CI infrastructure (an Actions secret,
like the deploy key) — NOT a data-source credential; G6 keyless applies
to the data pipeline, which remains keyless. Without the secret the
job reports NOOP and exits 0 (the deploy-key pattern). The metadata
carries Ben's ORCID for attribution.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tarfile
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ZENODO_API = "https://zenodo.org/api"
ORCID = "0009-0004-6118-8665"

DEPOSIT_TREES = ("archive", "stamps", "ledger", "seed")
DEPOSIT_FILES = (
    "README.md",
    "METHODOLOGY_v0.md",
    "docs/METHODOLOGY_CHANGELOG.md",
    "docs/REPRODUCE_FIXING.md",
    "docs/LICENSING.md",
)
# license-excluded name prefixes (LICENSING.md rules): never deposited
EXCLUDED_PREFIXES = ("who_", "gho_", "ihme_", "vaupel_", "iosco_")


def deposit_members(repo_root: Path = REPO_ROOT) -> list[Path]:
    """The curated file list — deterministic, license-clean."""
    out: list[Path] = []
    for tree in DEPOSIT_TREES:
        root = repo_root / tree
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*")):
            if p.is_file() and not p.name.startswith(EXCLUDED_PREFIXES):
                out.append(p)
    for f in DEPOSIT_FILES:
        p = repo_root / f
        if p.is_file():
            out.append(p)
    return out


def build_tarball(out_path: Path, repo_root: Path = REPO_ROOT) -> str:
    """Deterministic tar.gz of the curated set; returns its sha256.

    Plain ``tarfile.open(w:gz)`` is NOT deterministic: the gzip header
    embeds the output filename and current time (found by the
    determinism test). Tar to memory, then gzip with mtime=0 and an
    empty embedded name."""
    import gzip
    import io

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for p in deposit_members(repo_root):
            info = tar.gettarinfo(p, arcname=str(p.relative_to(repo_root)))
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            with p.open("rb") as f:
                tar.addfile(info, f)
    with open(out_path, "wb") as raw:
        with gzip.GzipFile(filename="", mtime=0, fileobj=raw, mode="wb", compresslevel=9) as gz:
            gz.write(buf.getvalue())
    return hashlib.sha256(out_path.read_bytes()).hexdigest()


def _metadata(quarter: str, sha256: str) -> dict:
    return {
        "metadata": {
            "title": f"SAECULUM / TLY index — archive deposit {quarter}",
            "upload_type": "dataset",
            "description": (
                "Quarterly deposit of the SAECULUM index's public record: the "
                "immutable print archive (hash chain), OpenTimestamps proofs, "
                "correction ledger, the v0 golden anchor, and reproduction "
                "documentation. Every value recomputes from public artifacts; "
                f"tarball sha256 {sha256}. License-restricted inputs (WHO GHO, "
                "IHME, NC literature) are excluded per the published licensing "
                "table. Live series: https://chronon-index.pages.dev"
            ),
            "creators": [{"name": "Pauls, Benjamin", "orcid": ORCID}],
            "license": "cc-by-4.0",
            "keywords": [
                "demography",
                "life expectancy",
                "index",
                "mortality",
                "reproducible research",
                "SAECULUM",
                "TLY",
            ],
        }
    }


def run(quarter: str | None = None) -> int:
    token = os.environ.get("ZENODO_TOKEN", "")
    quarter = quarter or f"{time.gmtime().tm_year}-Q{(time.gmtime().tm_mon - 1) // 3 + 1}"
    tarball = REPO_ROOT / f"saeculum-deposit-{quarter}.tar.gz"
    sha = build_tarball(tarball)
    size = tarball.stat().st_size
    print(
        f"curated deposit {quarter}: {len(deposit_members())} files, "
        f"{size / 1e6:.1f} MB, sha256 {sha[:16]}…"
    )
    if not token:
        tarball.unlink()
        print(
            "NOOP: ZENODO_TOKEN not set — deposit skipped (deploy-key pattern; "
            "set the Actions secret to arm)"
        )
        return 0

    import urllib.request

    def api(method: str, url: str, data: bytes | None = None, ctype: str = "application/json"):
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", ctype)
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode() or "{}")

    dep = api(
        "POST", f"{ZENODO_API}/deposit/depositions", json.dumps(_metadata(quarter, sha)).encode()
    )
    bucket = dep["links"]["bucket"]
    api("PUT", f"{bucket}/{tarball.name}", tarball.read_bytes(), "application/octet-stream")
    pub = api("POST", dep["links"]["publish"])
    tarball.unlink()
    print(f"DEPOSITED: DOI {pub.get('doi', '?')} ({pub['links'].get('record_html', '')})")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else None))
