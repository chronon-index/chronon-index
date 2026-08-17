"""B-uc4-03 / AC-4.1 / invariant P9: no orphan numbers.

The named test publishes a REAL pipeline print into a temp API tree and
walks every figure back to the repo's committed manifests. Then each
violation class is provoked: broken citation, unknown snapshot, orphan
print, negative stock.
"""

from __future__ import annotations

import json
from pathlib import Path

from tly.api import API_ROOT, build_api
from tly.lineage import check_lineage
from tly.pipeline import build_settlement_print

REPO = Path(__file__).resolve().parent.parent
SNAPSHOTS = REPO / "data" / "snapshots"
EPOCH = "2026-08-17T12:00:00+00:00"


def _publish(tmp_path: Path):
    build_api([build_settlement_print(EPOCH)], tmp_path)
    return tmp_path.joinpath(*API_ROOT)


def _rewrite(root: Path, rel: str, mutate) -> None:
    """Mutate one artifact AND refresh its index hash (so lineage, not the
    integrity layer, is what catches the problem)."""
    import hashlib

    path = root / rel
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data)
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    index_path = root / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["artifacts"][rel] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n")


def test_p9_lineage(tmp_path):
    """Named per RP Part X: the real published print resolves every cited
    snapshot file to the committed manifests; zero violations."""
    _publish(tmp_path)
    assert check_lineage(tmp_path, SNAPSHOTS) == []


def test_p9_detects_hash_citation_mismatch(tmp_path):
    root = _publish(tmp_path)

    def corrupt(data):
        snaps = data["provenance"]["snapshots"]
        name = sorted(snaps)[0]
        fname = sorted(snaps[name])[0]
        snaps[name][fname] = "0" * 64

    _rewrite(root, "latest.json", corrupt)
    problems = check_lineage(tmp_path, SNAPSHOTS)
    assert any("does not match the committed manifest" in p for p in problems)


def test_p9_detects_unknown_snapshot_and_orphan(tmp_path):
    root = _publish(tmp_path)
    _rewrite(
        root,
        "latest.json",
        lambda d: d["provenance"].__setitem__("snapshots", {"2099-01-01": {"x": "0" * 64}}),
    )
    problems = check_lineage(tmp_path, SNAPSHOTS)
    assert any("unknown snapshot" in p for p in problems)

    root2 = _publish(tmp_path / "b")
    _rewrite(
        root2,
        "latest.json",
        lambda d: d["provenance"].__setitem__("snapshots", {}),
    )
    problems2 = check_lineage(tmp_path / "b", SNAPSHOTS)
    assert any("orphan print" in p for p in problems2)


def test_p9_detects_negative_stock(tmp_path):
    root = _publish(tmp_path)
    _rewrite(root, "latest.json", lambda d: d.__setitem__("n_persons", "-1"))
    problems = check_lineage(tmp_path, SNAPSHOTS)
    assert any("n_persons is negative" in p for p in problems)
