"""AC-1.2 — the settlement golden (A-16 rulings D1/D3/D4; B-uc1-13).

The golden anchor is the RESTORED ORIGINAL ``seed/results_v0.json``
(delivered 2026-09-03 in chronon-restore-A16.zip; the reconstruction is
archived at ``ops/reconstruction/2026-08-16/``). Per D4's rewritten
AC-1.2: on the frozen ``data/snapshots/v0-original/`` input set, the v1
engine must reproduce EVERY value in the original file to 4 decimal
places — strict, satisfiable without tuning because the inputs are
pinned. "Reproduce-or-journal" applies only to live-fetch vintage runs.

Conventions of the original, honored not tuned:
- births = N x CBR/1000 (the original's cbr-derived convention; the
  reconstruction had read OWID's births count directly, which is the
  documented -0.0026% mint story, ledger C-0002),
- drift = [S(pop2023, WHO2019) - S(pop2023, WHO2015)] / 4 (D2:
  CONFIRMED original, tly_v0_calc.py lines 148-151),
- asymptote: $6 per 15 minutes -> $24/h x 8766 h/life-year.

The original calculator itself is restored verbatim in ``seed/`` as the
canonical historical artifact; it live-fetches and is not run here (P5
offline reproducibility is carried by the v1 engine + this frozen
snapshot, and by the archived reconstruction's offline test below).
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pytest

from tly.estimator import compute_stock, e_bar, total_population
from tly.loader import load_verified_snapshot
from tly.parsers import GHO_AGE_ANCHORS

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_PATH = REPO_ROOT / "seed" / "results_v0.json"
V0_SNAPSHOT = REPO_ROOT / "data" / "snapshots" / "v0-original"
Q4 = Decimal("0.0001")


def _who_table(year: int) -> dict[int, Decimal]:
    data = json.loads(
        (V0_SNAPSHOT / "gho_ex_global_btsx_2000_2010_2015.json").read_text(encoding="utf-8"),
        parse_float=Decimal,
    )
    table: dict[int, Decimal] = {}
    for r in data["value"]:
        if r["SpatialDim"] == "GLOBAL" and r["Dim1"] == "SEX_BTSX" and int(r["TimeDim"]) == year:
            v = r["NumericValue"]
            table[GHO_AGE_ANCHORS[r["Dim2"]]] = v if isinstance(v, Decimal) else Decimal(v)
    assert sorted(table) == sorted(GHO_AGE_ANCHORS.values())
    return table


@pytest.fixture(scope="module")
def recomputed():
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    snap = load_verified_snapshot(V0_SNAPSHOT)
    stock19 = compute_stock(snap.tables[2019], snap.bands, 2019)
    stock21 = compute_stock(snap.tables[2021], snap.bands, 2021)
    stock15 = compute_stock(_who_table(2015), snap.bands, 2015)
    n = total_population(snap.bands)
    e0 = snap.tables[2019][0]
    cbr = Decimal(str(golden["cbr"]))
    births = n * cbr / 1000
    mint_v = births * e0
    d_ebar = (e_bar(stock19, n) - e_bar(stock15, n)) / 4
    drift = n * d_ebar
    net = mint_v - n + drift
    asym = Decimal(24) * Decimal(8766)
    ours = {
        "S_2019_table": stock19.s_life_years,
        "S_2021_table": stock21.s_life_years,
        "pop": n,
        "e0_2019": e0,
        "births": births,
        "mint": mint_v,
        "spend": n,  # the file records spend as +N used one year each
        "drift": drift,
        "d_ebar_per_yr": d_ebar,
        "net": net,
        "g_pct": net / stock19.s_life_years * 100,
        "asymptote_usd_per_lifeyear": asym,
        "asymptote_cap_usd": asym * stock19.s_life_years,
    }
    return golden, ours


# value -> the natural unit its 4-dp comparison runs in (DECISIONS quotes
# stocks/flows in billions, births in millions, the cap in quadrillions)
UNITS = {
    "S_2019_table": Decimal(10) ** 9,
    "S_2021_table": Decimal(10) ** 9,
    "pop": Decimal(10) ** 9,
    "e0_2019": Decimal(1),
    "births": Decimal(10) ** 6,
    "mint": Decimal(10) ** 9,
    "spend": Decimal(10) ** 9,
    "drift": Decimal(10) ** 9,
    "d_ebar_per_yr": Decimal(1),
    "net": Decimal(10) ** 9,
    "g_pct": Decimal(1),
    "asymptote_usd_per_lifeyear": Decimal(1),
    "asymptote_cap_usd": Decimal(10) ** 15,
}


def test_ac_1_2_every_original_value_reproduces_at_4dp(recomputed):
    golden, ours = recomputed
    failures = []
    for key, unit in UNITS.items():
        original = (Decimal(str(golden[key])) / unit).quantize(Q4)
        recomputed_v = (ours[key] / unit).quantize(Q4)
        if original != recomputed_v:
            failures.append(f"{key}: original {original} != recomputed {recomputed_v}")
    assert not failures, "AC-1.2 STRICT failures:\n" + "\n".join(failures)


def test_golden_covers_every_numeric_field(recomputed):
    """No orphan numbers in the golden: every numeric field of the
    original file is either recomputed above or an input we pin (cbr,
    pop_year, cbr_year)."""
    golden, _ = recomputed
    numeric_fields = {k for k, v in golden.items() if isinstance(v, (int, float))}
    accounted = set(UNITS) | {"cbr", "pop_year", "cbr_year"}
    assert numeric_fields <= accounted, f"unaccounted: {numeric_fields - accounted}"


def test_archived_reconstruction_still_recomputes_byte_exact():
    """P5 regression kept from the reconstruction era: the ARCHIVED
    reconstructed calculator still reproduces its archived results file
    byte-for-byte offline (honest history stays runnable)."""
    import importlib.util

    arch = REPO_ROOT / "ops" / "reconstruction" / "2026-08-16"
    spec = importlib.util.spec_from_file_location("tly_v0_calc_recon", arch / "tly_v0_calc.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # The archived module derives REPO_ROOT from its own location, which was
    # seed/ when it lived there; running it from the archive needs only this
    # harness-side correction — the artifact itself stays byte-frozen.
    mod.REPO_ROOT = REPO_ROOT
    snapshot = mod.load_snapshot(REPO_ROOT / "data" / "snapshots" / "2026-08-16")
    rendered = mod.render_json(mod.compute(snapshot)).encode("utf-8")
    assert rendered == (arch / "results_v0.json").read_bytes()
