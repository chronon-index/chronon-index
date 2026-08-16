"""B-uc1-12: the recovered drift convention, pinned end to end.

drift = [S(pop2023, WHO_2019) − S(pop2023, WHO_2015)] / 4 = +1.0394B (4 dp)

— the annualized WHO-GHE vintage revision gain (2015→2019, the last two
pre-COVID vintages) at fixed 2023 structure. Recovered by exhaustive
convention search (CALC_REPORT addendum 8); flagged for A-16 ratification.
Everything here recomputes from committed snapshots only.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from tly.estimator import compute_stock
from tly.loader import load_verified_snapshot
from tly.numeric import BILLION, Q4
from tly.parsers import GHO_AGE_ANCHORS

REPO = Path(__file__).resolve().parent.parent
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"
WHO_HIST = REPO / "data" / "snapshots" / "2026-08-17" / "gho_ex_global_btsx_2000_2010_2015.json"

DRIFT_TARGET = Decimal("1.0394")
G_TARGET = Decimal("0.7197")
MINT_DECISIONS = Decimal("9.6606")  # recorded; unreproducible (addendum 7)
MINT_REPRODUCIBLE = Decimal("9.6603")
SPEND = Decimal("-8.0917")
S_2019 = Decimal("362.4126")


def _who_table(year: int) -> dict[int, Decimal]:
    data = json.loads(WHO_HIST.read_text(encoding="utf-8"), parse_float=Decimal)
    table: dict[int, Decimal] = {}
    for r in data["value"]:
        if r["SpatialDim"] == "GLOBAL" and r["Dim1"] == "SEX_BTSX" and int(r["TimeDim"]) == year:
            v = r["NumericValue"]
            table[GHO_AGE_ANCHORS[r["Dim2"]]] = v if isinstance(v, Decimal) else Decimal(v)
    assert sorted(table) == sorted(GHO_AGE_ANCHORS.values()), f"incomplete WHO {year}"
    return table


def test_drift_convention_reproduces_target():
    snap = load_verified_snapshot(SNAP16)
    s_2015 = compute_stock(_who_table(2015), snap.bands, 2015).s_life_years
    s_2019 = compute_stock(snap.tables[2019], snap.bands, 2019).s_life_years
    drift = ((s_2019 - s_2015) / 4 / BILLION).quantize(Q4)
    assert drift == DRIFT_TARGET  # 1.0394 — exact at published precision
    assert str((s_2015 / BILLION).quantize(Q4)) == "358.2550"


def test_g_chain_with_recorded_mint_reproduces_decisions():
    """(9.6606 − 8.0917 + 1.0394)/362.4126 = 0.7197 %/yr — DECISIONS g."""
    g = ((MINT_DECISIONS + SPEND + DRIFT_TARGET) / S_2019 * 100).quantize(Q4)
    assert g == G_TARGET


def test_g_chain_with_reproducible_mint_carries_residual():
    """The −0.0003B mint residual (addendum 7) propagates: g = 0.7196.
    Both values stand; the gap is the mint residual, nothing else."""
    g = ((MINT_REPRODUCIBLE + SPEND + DRIFT_TARGET) / S_2019 * 100).quantize(Q4)
    assert g == Decimal("0.7196")
    assert g != G_TARGET


def test_rejected_conventions_stay_rejected():
    """Nearest rivals from the search, pinned as non-matches so the
    recovered convention cannot be quietly swapped: WHO (2019−2010)/9 and
    (2019−2000)/19 both miss."""
    snap = load_verified_snapshot(SNAP16)
    s_2019 = compute_stock(snap.tables[2019], snap.bands, 2019).s_life_years
    for year, span, expect in ((2010, 9, "1.2569"), (2000, 19, "1.3105")):
        s_old = compute_stock(_who_table(year), snap.bands, year).s_life_years
        drift = ((s_2019 - s_old) / span / BILLION).quantize(Q4)
        assert str(drift) == expect
        assert drift != DRIFT_TARGET
