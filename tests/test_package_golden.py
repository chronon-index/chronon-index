"""A-13 PACKAGE golden test (RALPH_LOOP §5 Phase A; SPEC AC-1.2).

The tly package (parsers + estimator), run over the committed 2026-08-16
snapshot, must reproduce seed/results_v0.json to 4 decimal places — and,
where the golden file records full-precision Decimals, byte-exactly. This
is the ground-truth anchor every refactor must keep green.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from tly.estimator import compute_stock, e_bar, e_interp, mint, total_population
from tly.numeric import BILLION, Q4
from tly.parsers import parse_births, parse_gho_life_tables, parse_population_bands

REPO = Path(__file__).resolve().parent.parent
SNAPSHOT = REPO / "data" / "snapshots" / "2026-08-16"
GOLDEN = json.loads((REPO / "seed" / "results_v0.json").read_text(encoding="utf-8"))
A = GOLDEN["achieved"]


def _package_results():
    tables = parse_gho_life_tables(SNAPSHOT, (2019, 2021))
    bands = parse_population_bands(SNAPSHOT, 2023)
    births = parse_births(SNAPSHOT, 2023)
    return tables, bands, births


def test_package_reproduces_golden_at_4dp():
    tables, bands, births = _package_results()
    s2019 = compute_stock(tables[2019], bands, 2019)
    s2021 = compute_stock(tables[2021], bands, 2021)
    n = total_population(bands)

    assert str(s2019.s_billions_4dp) == A["S_2019_billions"]  # 362.4126
    assert str(s2021.s_billions_4dp) == A["S_2021_billions"]  # 348.1905
    assert str((n / BILLION).quantize(Q4)) == A["N_billions"]  # 8.0917
    assert str(e_bar(s2019, n).quantize(Q4)) == A["E_bar_years"]  # 44.7880
    assert str((-n / BILLION).quantize(Q4)) == A["spend_minus_N_billions"]
    m = mint(births, tables[2019][0])
    assert str((m / BILLION).quantize(Q4)) == A["mint_B_times_e0_billions"]  # 9.6603


def test_package_matches_golden_full_precision():
    """Stronger than 4 dp: full prec-34 strings must match the golden file."""
    tables, bands, births = _package_results()
    s2019 = compute_stock(tables[2019], bands, 2019)
    s2021 = compute_stock(tables[2021], bands, 2021)
    n = total_population(bands)

    assert str(s2019.s_life_years) == A["S_2019_life_years"]
    assert str(s2021.s_life_years) == A["S_2021_life_years"]
    assert str(n) == A["N_persons"]
    assert str(e_bar(s2019, n)) == A["E_bar_years_full"]
    assert str(mint(births, tables[2019][0])) == A["mint_B_times_e0_life_years"]


def test_package_band_terms_match_golden_detail():
    """Per-band decomposition equals the golden band_detail, both years."""
    tables, bands, _ = _package_results()
    for year in (2019, 2021):
        stock = compute_stock(tables[year], bands, year)
        golden_rows = GOLDEN["band_detail"][str(year)]
        assert len(stock.band_terms) == len(golden_rows)
        for bt, row in zip(stock.band_terms, golden_rows):
            assert [bt.label, str(bt.midpoint), str(bt.count), str(bt.e_mid), str(bt.term)] == row


def test_e_interp_properties():
    table = {0: Decimal("70"), 1: Decimal("69.5"), 5: Decimal("66"), 85: Decimal("6")}
    assert e_interp(table, Decimal("0")) == Decimal("70")  # exact anchor
    assert e_interp(table, Decimal("0.5")) == Decimal("69.75")  # linear between
    assert e_interp(table, Decimal("3")) == Decimal("67.75")  # 1..5 segment
    assert e_interp(table, Decimal("85")) == Decimal("6")  # last anchor
    assert e_interp(table, Decimal("102.5")) == Decimal("6")  # flat tail
    try:
        e_interp(table, Decimal("-1"))
        raise AssertionError("expected ValueError below first anchor")
    except ValueError:
        pass
