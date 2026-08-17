"""Publish gate (SPEC#4 AC-4.6 + AC-2.4; B-uc4-05).

The ONE sanctioned way to put prints into the public API tree. Every gate
runs against the freshly built tree in a staging directory:

1. consumer-side schema on every print artifact (epoch discipline, labels,
   coverage/P7, accuracy/RP-VI-r6, provenance),
2. API integrity + closed-world index (verify_api),
3. static-only (no server runtime; AC-4.4),
4. lineage to committed manifests (P9).

Only if ALL pass is the staging tree atomically swapped into place. On any
failure the existing published tree is left byte-for-byte untouched and
PublishBlocked carries every violation — a bad print can block a publish,
but it can never half-publish or damage what is already public.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from tly.api import API_ROOT, assert_static_only, build_api, verify_api
from tly.lineage import check_lineage
from tly.prints import PrintSchemaError, WeeklyPrint, validate_print_dict
from tly.stock import LocationStock


class PublishBlocked(RuntimeError):
    """One or more gates failed; nothing was published."""

    def __init__(self, violations: list[str]):
        self.violations = violations
        super().__init__("publish blocked:\n" + "\n".join(violations))


def _gate_violations(staging: Path, snapshots_root: Path) -> list[str]:
    problems: list[str] = []
    root = staging.joinpath(*API_ROOT)
    for pf in sorted(root.glob("prints/*.json")) + [root / "latest.json"]:
        try:
            validate_print_dict(json.loads(pf.read_text(encoding="utf-8")))
        except PrintSchemaError as err:
            problems.append(f"{pf.relative_to(root)}: {err}")
    try:
        verify_api(staging)
    except ValueError as err:
        problems.append(f"api integrity: {err}")
    try:
        assert_static_only(staging)
    except ValueError as err:
        problems.append(f"static-only: {err}")
    problems.extend(check_lineage(staging, snapshots_root))
    return problems


def publish_prints(
    prints: list[WeeklyPrint],
    out_dir: Path,
    snapshots_root: Path,
    country_stocks: list[LocationStock] | None = None,
) -> Path:
    """Build → gate → atomic swap. Returns the published api root."""
    staging = out_dir.parent / (out_dir.name + ".staging")
    if staging.exists():
        shutil.rmtree(staging)
    build_api(prints, staging, country_stocks=country_stocks)

    violations = _gate_violations(staging, snapshots_root)
    if violations:
        shutil.rmtree(staging)
        raise PublishBlocked(violations)

    if out_dir.exists():
        retired = out_dir.parent / (out_dir.name + ".previous")
        if retired.exists():
            shutil.rmtree(retired)
        out_dir.rename(retired)
    staging.rename(out_dir)
    return out_dir.joinpath(*API_ROOT)
