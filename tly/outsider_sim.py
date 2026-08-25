"""Outsider simulation (C-uc7-07; SPEC#7 AC-7.5; RP Part IV P5 gate).

Mechanically follows docs/REPRODUCE_FIXING.md as an external recomputer
would, for EVERY epoch in the committed archive chain.

REPRODUCTION SEMANTICS (discovered by this job's own first run): an
archived print carries the methodology version THAT PRODUCED IT, while a
later checkout recomputes under HEAD's version — so raw byte-identity
fails the moment governance advances, even when every value is identical.
The honest contract, enforced here:

1. **Values reproduce byte-exactly** — every field EXCLUDING provenance
   (S, Ē, N, burn, coverage, accuracy) after canonical re-rendering.
2. **The archived stamp is history-consistent**, verified against
   append-only records rather than HEAD's regenerated stamp: the archived
   methodology version + policies must equal the immutable registry
   entry, and every archived (snapshot, file, sha256) citation must
   resolve into the committed manifests with a matching hash (the P9
   lineage rule — manifests GROW append-only, so the archived citation
   set is a subset of today's, never re-generated for comparison).
3. **Fixings agree.** Two independent settlements from the committed
   archive produce string-equal fixing hashes, and the chain re-verifies.

(Both refinements were forced by this job's own first runs: raw
byte-identity broke first on the version stamp when governance advanced,
then on manifest growth — each a wrong comparison, not a wrong value.)

Exit 0 only if every epoch passes all three. Any divergence names the
epoch and fails — an outsider could not reproduce us, a P5-blocking
defect.
"""

from __future__ import annotations

import json
import sys

from tly.archive import PrintArchive
from tly.fixings import settle_from_archive
from tly.methodology import VERSION_POLICY_REGISTRY
from tly.pipeline import REPO_ROOT, build_settlement_print


def _split(print_json: str) -> tuple[str, dict]:
    """(canonical values-only render, the full provenance block)."""
    data = json.loads(print_json)
    prov = data.pop("provenance", {})
    return json.dumps(data, indent=2, sort_keys=True), prov


def main() -> int:
    archive = PrintArchive(REPO_ROOT / "archive")
    chain = archive.verify()
    if not chain:
        print("no archived epochs yet — nothing to reproduce")
        return 0

    snapshots = REPO_ROOT / "data" / "snapshots"
    manifests: dict[str, dict] = {}
    for d in sorted(x for x in snapshots.iterdir() if x.is_dir()):
        mf = d / "manifest.json"
        if mf.is_file():
            manifests[d.name] = json.loads(mf.read_text(encoding="utf-8"))["files"]

    for link in chain:
        committed = (archive.root / link["file"]).read_text(encoding="utf-8")
        c_body, c_prov = _split(committed)
        # Version-keyed parameters (e.g. the one-sided error-budget band)
        # must come from the version that PRODUCED the print, never HEAD.
        recomputed = build_settlement_print(
            link["epoch_utc"], methodology_version=c_prov.get("methodology_version")
        ).render()
        r_body, _ = _split(recomputed)
        if c_body != r_body:
            print(f"DIVERGENCE at {link['epoch_utc']}: recomputed VALUES differ")
            for i, (a, b) in enumerate(zip(c_body.splitlines(), r_body.splitlines())):
                if a != b:
                    print(f"  first differing line {i}: committed={a!r} recomputed={b!r}")
                    break
            return 1

        c_version = c_prov.get("methodology_version")
        registry_entry = VERSION_POLICY_REGISTRY.get(c_version)
        if registry_entry is None:
            print(
                f"DIVERGENCE at {link['epoch_utc']}: archived version "
                f"{c_version!r} absent from the append-only registry"
            )
            return 1
        if c_prov.get("policies") != registry_entry:
            print(
                f"DIVERGENCE at {link['epoch_utc']}: archived policy strings "
                f"do not match the registry entry for {c_version}"
            )
            return 1

        cited = 0
        for snap_name, files in c_prov.get("snapshots", {}).items():
            manifest = manifests.get(snap_name)
            if manifest is None:
                print(f"DIVERGENCE at {link['epoch_utc']}: cites unknown snapshot {snap_name!r}")
                return 1
            for fname, sha in files.items():
                row = manifest.get(fname)
                if row is None or row.get("sha256") != sha:
                    print(
                        f"DIVERGENCE at {link['epoch_utc']}: citation "
                        f"{snap_name}/{fname} does not resolve in the "
                        "committed manifests"
                    )
                    return 1
                cited += 1
        print(
            f"epoch {link['epoch_utc']}: values byte-identical; stamp "
            f"registry-consistent ({c_version}); {cited} citations resolve"
        )

    head = chain[-1]["epoch_utc"]
    f1 = settle_from_archive(archive, head, snapshots)
    f2 = settle_from_archive(archive, head, snapshots)
    if f1.fixing_hash != f2.fixing_hash:
        print("DIVERGENCE: independent settlements disagree")
        return 1
    print(f"fixing {head}: hash agreement {f1.fixing_hash}")
    print("OUTSIDER SIMULATION PASSED — an external recomputer reproduces us")
    return 0


if __name__ == "__main__":
    sys.exit(main())
