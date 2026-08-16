"""B-uc1-11: the mint gap (−0.0026%) — hypotheses h1/h2/h3 REFUTED, residual pinned.

CALC_REPORT_v0.txt §4 proposed three explanations for achieved mint 9.6603B
vs the DECISIONS.md target 9.6606B. All three were checked against live
sources on 2026-08-17 (snapshots committed/manifested) and refuted. These
tests pin the evidence so the residual stays documented, not re-litigated:

- h1 (different births source): WPP Demographic Indicators World births
  2023 = 132,110,264 — IDENTICAL to OWID's value. The mirror is faithful.
- h2 (year convention): 2022/2024 births give 9.6870/9.6820 — further away.
- h3 (different e0 series): WHOSIS e0 2019 = 73.123374470 vs life-table ex
  73.123374469 — same quantity, last-digit rounding; changes nothing at 4dp.

Conclusion: mint = 9.6603B is the reproducible value under every surviving
convention; 9.6606B is not reproducible from any tested source pair. The
residual stands per amended AC-1.2 (reproduce-or-journal; never tune).
"""

from __future__ import annotations

import csv
import gzip
import json
from decimal import Decimal
from pathlib import Path

from tly.numeric import BILLION, Q4

REPO = Path(__file__).resolve().parent.parent
SNAP17 = REPO / "data" / "snapshots" / "2026-08-17"
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"
DEMIND_FIX = SNAP17 / "fixtures" / "wpp_demind_world_fixture.csv.gz"
WHOSIS = SNAP17 / "gho_whosis_000001_global_btsx.json"

GHO_EX_E0_2019 = Decimal("73.123374469")  # LIFE_0000000035, 2026-08-16 snapshot
OWID_BIRTHS_2023 = Decimal("132110264")  # from the 2026-08-16 snapshot
TARGET_MINT = Decimal("9.6606")  # DECISIONS.md; NOT reproduced
ACHIEVED_MINT = Decimal("9.6603")  # reproducible value


def _demind_world() -> dict[str, dict[str, Decimal]]:
    rows: dict[str, dict[str, Decimal]] = {}
    with gzip.open(DEMIND_FIX, "rt", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            rows[row["Time"]] = {
                "births_thousands": Decimal(row["Births"]),
                "lex": Decimal(row["LEx"]),
            }
    return rows


def test_h1_refuted_wpp_births_identical_to_owid():
    """The primary source and the OWID mirror agree to the person."""
    world = _demind_world()
    assert world["2023"]["births_thousands"] * 1000 == OWID_BIRTHS_2023


def test_h2_refuted_no_year_convention_matches():
    world = _demind_world()
    for year in ("2022", "2023", "2024"):
        m = (world[year]["births_thousands"] * 1000 * GHO_EX_E0_2019 / BILLION).quantize(Q4)
        assert m != TARGET_MINT, f"unexpected match for births year {year}"


def test_h3_refuted_whosis_equals_lifetable_e0_at_4dp():
    data = json.loads(WHOSIS.read_text(encoding="utf-8"), parse_float=Decimal)
    e0 = {
        int(r["TimeDim"]): r["NumericValue"]
        for r in data["value"]
        if r["SpatialDim"] == "GLOBAL" and r["Dim1"] == "SEX_BTSX"
    }[2019]
    assert e0 == Decimal("73.123374470")  # last-digit rounding of the same fact
    assert abs(e0 - GHO_EX_E0_2019) <= Decimal("1e-9")
    m = (OWID_BIRTHS_2023 * e0 / BILLION).quantize(Q4)
    assert m == ACHIEVED_MINT  # unchanged; h3 explains nothing


def test_residual_stands_documented():
    """The reproducible mint is 9.6603B; the 3,442-birth (or 0.0026 e0)
    shortfall to the DECISIONS target has no surviving explanation."""
    m = (OWID_BIRTHS_2023 * GHO_EX_E0_2019 / BILLION).quantize(Q4)
    assert m == ACHIEVED_MINT
    implied_births = (TARGET_MINT * BILLION / GHO_EX_E0_2019).quantize(Decimal("1"))
    assert implied_births - OWID_BIRTHS_2023 == Decimal("3442")
