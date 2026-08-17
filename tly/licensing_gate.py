"""Licensing gate (SPEC#3 AC-3.5; RP Part VII P1 GATE; B-uc3-13).

The rule: a PUBLIC (commercial-grade) print may compute only from sources
whose licensing row is CLEARED (or CLEARED-CONSTRUCTED-ONLY when only the
provider's constructed outputs are consumed). VERIFIED-RESTRICTED sources
(WHO, IHME — confirmed non-commercial clauses) and HUMAN rows (unpurchased
licenses) block the gate. Research-mode prints may additionally use
VERIFIED-RESTRICTED sources — that is exactly the v0 posture.

HONEST CONSEQUENCE, encoded as a test: the current v0-equivalent pipeline
computes S from the WHO 2019 table, so the commercial gate CORRECTLY
BLOCKS it today. The G5 source-of-record switch to WPP tables (with its
documented ~0.5yr e0 level change) is what opens the gate — the gate makes
that migration unforgettable rather than aspirational.

The gate reads docs/LICENSING.md itself — the table is the law, and the
gate cannot drift from it because it has no other source of truth.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LICENSING = REPO_ROOT / "docs" / "LICENSING.md"

CLEARED = "CLEARED"
CLEARED_CONSTRUCTED = "CLEARED-CONSTRUCTED-ONLY"
RESTRICTED = "VERIFIED-RESTRICTED"
ROLE_LIMITED = "ROLE-LIMITED"
HUMAN = "HUMAN"
UNVERIFIED = "(verify)"

# manifest filename prefix -> licensing row name (as in the table's Source column)
PREFIX_TO_ROW: dict[str, str] = {
    "gho_": "WHO GHO / GHE",
    "who_": "WHO GHO / GHE",
    "owid_": "Our World in Data grapher",
    "wpp_": "UN WPP 2024",
    "WPP2024_": "UN WPP 2024",
    "wmd_": "World Mortality Dataset (Karlinsky & Kobak)",
    "hmd_": "HMD",
    "fixtures/": None,  # derived from already-classified parents
    "cc_": None,  # license-evidence files, not data sources
    "iosco_": None,
    "eurostat_": None,
    "cdc_": None,
    "ucdp_": None,
    "economist_": None,
    "ihme_": None,
    "vaupel_": None,  # literature evidence (CC BY-NC paper), not a data source
}


class LicensingGateError(RuntimeError):
    pass


def parse_table(path: Path = LICENSING) -> dict[str, str]:
    """{row name: status}, from the table's first and last columns."""
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("|---") or "| Source |" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        name, status_cell = cells[0], cells[-1]
        for status in (CLEARED_CONSTRUCTED, CLEARED, RESTRICTED, ROLE_LIMITED, HUMAN):
            if status_cell.startswith(status):
                rows[name] = status
                break
        else:
            rows[name] = UNVERIFIED
    if not rows:
        raise LicensingGateError("licensing table parsed to zero rows")
    return rows


def row_for_file(name: str) -> str | None:
    base = name if "/" not in name else name.split("/", 1)[0] + "/"
    for prefix, row in PREFIX_TO_ROW.items():
        if name.startswith(prefix) or base == prefix:
            return row
    raise LicensingGateError(f"no licensing classification for snapshot file {name!r}")


def check_gate(
    compute_files: list[str], *, commercial: bool, table: dict[str, str] | None = None
) -> list[str]:
    """Violations for a print computed from ``compute_files``. Empty = open.

    commercial=True is the P1 public-print gate; commercial=False is the
    research posture (VERIFIED-RESTRICTED tolerated, HUMAN still blocked).
    """
    rows = table if table is not None else parse_table()
    allowed = (
        {CLEARED, CLEARED_CONSTRUCTED}
        if commercial
        else {
            CLEARED,
            CLEARED_CONSTRUCTED,
            RESTRICTED,
        }
    )
    violations: list[str] = []
    for name in sorted(set(compute_files)):
        row = row_for_file(name)
        if row is None:
            continue
        status = rows.get(row)
        if status is None:
            violations.append(f"{name}: licensing row {row!r} missing from the table")
        elif status not in allowed:
            mode = "commercial" if commercial else "research"
            violations.append(f"{name}: source {row!r} is {status} — blocks a {mode} print")
    return violations
