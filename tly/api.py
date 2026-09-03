"""Static JSON API builder (SPEC#4 AC-4.4; RP Part VII; B-uc4-02).

The API is deliberately static: committed JSON files only, servable from
any dumb host — the attack surface is the repo and the data, never a
server. Layout under ``<out>/api/v1/``:

- ``latest.json``            — the newest epoch's print
- ``prints/<date>.json``     — one file per epoch (date = epoch's date part)
- ``countries.json``         — per-country S/Ē/N breakdown (optional)
- ``index.json``             — every artifact with its sha256 (the API
  self-describes its own integrity; an external recomputer can verify a
  mirror byte for byte)

All rendering is deterministic (sorted keys, Decimal-as-string): building
twice from the same prints yields byte-identical trees (invariant P5).
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path

from tly.prints import WeeklyPrint, validate_epoch, validate_print_dict
from tly.stock import LocationStock

API_ROOT = ("api", "v1")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _countries_doc(stocks: list[LocationStock]) -> str:
    doc = {
        s.location: {
            "iso3": s.iso3,
            "year": s.year,
            "sex": s.sex,
            "s_life_years": str(s.s_life_years),
            "e_bar_years": str(s.e_bar),
            "n_persons": str(s.n_persons),
        }
        for s in stocks
    }
    return json.dumps(doc, indent=2, sort_keys=True) + "\n"


def build_api(
    prints: list[WeeklyPrint],
    out_dir: Path,
    country_stocks: list[LocationStock] | None = None,
) -> dict[str, str]:
    """Build the static tree; returns {relative_path: sha256} (= index)."""
    if not prints:
        raise ValueError("cannot build an API from zero prints")
    epochs = [p.epoch_utc for p in prints]
    if len(set(epochs)) != len(epochs):
        raise ValueError("duplicate epochs in print list")
    ordered = sorted(prints, key=lambda p: p.epoch_utc)

    root = out_dir.joinpath(*API_ROOT)
    artifacts: dict[str, str] = {}

    def emit(rel: str, text: str) -> None:
        _write(root / rel, text)
        artifacts[rel] = hashlib.sha256(text.encode("utf-8")).hexdigest()

    for p in ordered:
        date = validate_epoch(p.epoch_utc).date().isoformat()
        emit(f"prints/{date}.json", p.render())
    emit("latest.json", ordered[-1].render())
    if country_stocks is not None:
        emit("countries.json", _countries_doc(country_stocks))

    index = {
        "epochs": [p.epoch_utc for p in ordered],
        "latest_epoch": ordered[-1].epoch_utc,
        "artifacts": artifacts,
    }
    _write(root / "index.json", json.dumps(index, indent=2, sort_keys=True) + "\n")
    return artifacts


def verify_api(out_dir: Path) -> None:
    """Consumer-side integrity check: every artifact matches index.json,
    and nothing exists in the tree that the index does not describe."""
    root = out_dir.joinpath(*API_ROOT)
    index = json.loads((root / "index.json").read_text(encoding="utf-8"))
    for rel, sha in index["artifacts"].items():
        body = (root / rel).read_bytes()
        actual = hashlib.sha256(body).hexdigest()
        if actual != sha:
            raise ValueError(f"api artifact {rel}: sha256 mismatch")
    on_disk = {str(p.relative_to(root)) for p in root.rglob("*.json") if p.name != "index.json"}
    undescribed = on_disk - set(index["artifacts"])
    if undescribed:
        raise ValueError(f"api artifacts not in index: {sorted(undescribed)}")


def assert_static_only(out_dir: Path) -> None:
    """AC-4.4: no server runtime in the build output — JSON files only,
    every one of them parseable, nothing executable."""
    root = out_dir.joinpath(*API_ROOT)
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if p.suffix != ".json":
            raise ValueError(f"non-JSON artifact in static API: {p}")
        json.loads(p.read_text(encoding="utf-8"))  # must parse
        if p.stat().st_mode & 0o111:
            raise ValueError(f"executable bit set on API artifact: {p}")


def load_latest_s(out_dir: Path) -> Decimal:
    """Convenience for consumers/tests: the settlement S from latest.json."""
    root = out_dir.joinpath(*API_ROOT)
    data = json.loads((root / "latest.json").read_text(encoding="utf-8"))
    return Decimal(data["s_life_years"])


def build_api_from_archive(archive_root: Path, out_dir: Path) -> dict[str, str]:
    """Build the static tree from the COMMITTED archive — every print is
    emitted byte-verbatim from its archived record (first-print-settles:
    the API serves what was printed, never a recomputation). Returns the
    index mapping like :func:`build_api`."""
    chain = json.loads((archive_root / "chain.json").read_text(encoding="utf-8"))
    if not chain:
        raise ValueError("cannot build an API from an empty archive")
    root = out_dir.joinpath(*API_ROOT)
    artifacts: dict[str, str] = {}

    def emit(rel: str, text: str) -> None:
        _write(root / rel, text)
        artifacts[rel] = hashlib.sha256(text.encode("utf-8")).hexdigest()

    latest_text = None
    epochs = []
    for link in chain:
        text = (archive_root / link["file"]).read_text(encoding="utf-8")
        validate_print_dict(json.loads(text))
        date = validate_epoch(link["epoch_utc"]).date().isoformat()
        emit(f"prints/{date}.json", text)
        epochs.append(link["epoch_utc"])
        latest_text = text
    emit("latest.json", latest_text)
    index = {"epochs": epochs, "latest_epoch": epochs[-1], "artifacts": artifacts}
    _write(root / "index.json", json.dumps(index, indent=2, sort_keys=True) + "\n")
    return artifacts
