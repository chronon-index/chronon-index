"""Weekly-feed vintage store (B-uc2-17; ruling B-uc2-02(c) follow-up).

Append-only: one dated pull per feed per run, stored under
``data/vintages/<feed>/<pull-date>.json`` with sha256 + provenance in a
per-feed ledger. The point is the LAG TRIANGLE: today a week's value is
whatever the source currently says; with vintages, every (week, pull-date)
pair is preserved, which is the only route to chain-ladder backfill
CORRECTION instead of censoring — and to a genuinely no-hindsight COVID
replay for future shocks (C-uc6-07's limitation note).

Store discipline mirrors the archive: a pull date can be written once;
re-pulls on the same date must be byte-identical or they raise; ledger
rows are append-only.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path


class VintageStoreError(RuntimeError):
    pass


class VintageStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _feed_dir(self, feed: str) -> Path:
        d = self.root / feed
        d.mkdir(exist_ok=True)
        return d

    def _ledger_path(self, feed: str) -> Path:
        return self._feed_dir(feed) / "ledger.jsonl"

    def store_pull(
        self,
        feed: str,
        pull_date: date,
        body: bytes,
        source_url: str,
        suffix: str = ".json",
    ) -> dict:
        """Store one pull. Idempotent for identical bytes; a DIFFERENT
        body on an existing pull date raises (vintages never mutate).
        ``suffix`` names the wire format (ONS pulls are CSV)."""
        d = self._feed_dir(feed)
        path = d / f"{pull_date.isoformat()}{suffix}"
        digest = hashlib.sha256(body).hexdigest()
        if path.exists():
            existing = hashlib.sha256(path.read_bytes()).hexdigest()
            if existing != digest:
                raise VintageStoreError(
                    f"{feed}/{pull_date}: pull already stored with different "
                    "bytes — vintages never mutate; a re-pull belongs to the "
                    "next pull date"
                )
            return {
                "feed": feed,
                "pull_date": pull_date.isoformat(),
                "sha256": digest,
                "new": False,
            }
        path.write_bytes(body)
        record = {
            "feed": feed,
            "pull_date": pull_date.isoformat(),
            "file": path.name,
            "sha256": digest,
            "bytes": len(body),
            "source_url": source_url,
        }
        with self._ledger_path(feed).open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")
        return {**record, "new": True}

    def ledger(self, feed: str) -> list[dict]:
        p = self._ledger_path(feed)
        if not p.is_file():
            return []
        return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line]

    def verify(self, feed: str) -> None:
        """Every ledger row's file exists and hash-matches; every stored
        file has a ledger row (closed world, like the archive)."""
        rows = self.ledger(feed)
        d = self._feed_dir(feed)
        ledgered = set()
        for row in rows:
            # pre-suffix ledger rows (eurostat/cdc history) lack "file"
            fname = row.get("file", f"{row['pull_date']}.json")
            path = d / fname
            if not path.is_file():
                raise VintageStoreError(f"{feed}/{row['pull_date']}: ledgered pull missing")
            if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
                raise VintageStoreError(f"{feed}/{row['pull_date']}: vintage bytes mutated")
            ledgered.add(fname)
        on_disk = {p.name for p in d.iterdir() if p.is_file() and p.name != "ledger.jsonl"}
        stray = on_disk - ledgered
        if stray:
            raise VintageStoreError(f"{feed}: unledgered vintages {sorted(stray)}")

    def lag_triangle(self, feed: str, extract_weeks) -> dict[str, dict[str, object]]:
        """{week: {pull_date: value}} across all stored vintages —
        the raw material for reporting-lag estimation. ``extract_weeks``
        maps one vintage's bytes to {week_key: value}."""
        out: dict[str, dict[str, object]] = {}
        for row in self.ledger(feed):
            fname = row.get("file", f"{row['pull_date']}.json")
            body = (self._feed_dir(feed) / fname).read_bytes()
            for week, value in extract_weeks(body).items():
                out.setdefault(week, {})[row["pull_date"]] = value
        return out
