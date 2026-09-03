#!/usr/bin/env python3
"""
TLY v0 open calculator - Total remaining human Life-Years and organic issuance.

Every input is fetched live from a public, keyless endpoint and printed with
its source URL so any third party can re-run this file and reproduce every
number. Full method in METHODOLOGY_v0.md.

Sources of record:
  [OWID] Our World in Data grapher CSVs (underlying source: UN World
         Population Prospects 2024) - world population by 5-year age group,
         crude birth rate.
         https://ourworldindata.org/grapher/population-by-five-year-age-group
         https://ourworldindata.org/grapher/crude-birth-rate
  [WHO]  WHO Global Health Observatory OData API, indicator LIFE_0000000035
         (ex - expectation of life at age x), SpatialDim=GLOBAL, both sexes -
         the global abridged life table, 2000-2021.
         https://ghoapi.azureedge.net/api/LIFE_0000000035

Method:
  S(t)   = sum over age bands of N(band) * e(band mean age)
  Mint   = births/yr * e(0)
  Spend  = N_total * 1 year  (every living person uses one year per year)
  Drift  = N_total * d(E-bar)/dt from life-table revisions (2015->2019,
           pre-COVID window, holding current population weights fixed)
  g      = (Mint - Spend + Drift) / S
  Expected deaths do NOT enter: they are already priced into e(x).
  Only EXCESS deaths versus the table burn stock (COVID scenario below).

Life-table vintage: WHO's latest global table is 2021, a COVID-depressed
anomaly year (e0=71.4). WPP 2024 puts 2023 e0 back near the 2019 level
(~73.2), so the 2019 table is used as primary and the 2021 table shown as
a lower bound.
"""
import csv, io, json, time, urllib.request
from decimal import Decimal, getcontext, ROUND_HALF_EVEN

getcontext().prec = 34
Q4 = Decimal("0.0001")
UA = {"User-Agent": "TLY-v0-open-calculator (reproducibility script)"}

OWID_AGE = "https://ourworldindata.org/grapher/population-by-five-year-age-group.csv?csvType=full"
OWID_CBR = "https://ourworldindata.org/grapher/crude-birth-rate.csv?csvType=full"
WHO = ("https://ghoapi.azureedge.net/api/LIFE_0000000035"
       "?$filter=SpatialDim%20eq%20%27GLOBAL%27%20and%20Dim1%20eq%20%27SEX_BTSX%27"
       "&$select=TimeDim,Dim2,NumericValue")

WHO_AGE = {"AGEGROUP_YEARS00-01": 0, "AGEGROUP_YEARS01-04": 1,
           "AGEGROUP_YEARS05-09": 5, "AGEGROUP_YEARS10-14": 10,
           "AGEGROUP_YEARS15-19": 15, "AGEGROUP_YEARS20-24": 20,
           "AGEGROUP_YEARS25-29": 25, "AGEGROUP_YEARS30-34": 30,
           "AGEGROUP_YEARS35-39": 35, "AGEGROUP_YEARS40-44": 40,
           "AGEGROUP_YEARS45-49": 45, "AGEGROUP_YEARS50-54": 50,
           "AGEGROUP_YEARS55-59": 55, "AGEGROUP_YEARS60-64": 60,
           "AGEGROUP_YEARS65-69": 65, "AGEGROUP_YEARS70-74": 70,
           "AGEGROUP_YEARS75-79": 75, "AGEGROUP_YEARS80-84": 80,
           "AGEGROUP_YEARS85PLUS": 85}

def fetch_bytes(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(1.5 * (i + 1))

def band_mean_age(label):
    """Mean exact age of a population band, uniform-within-band assumption."""
    if label.startswith("100"):
        return 101.0
    lo, hi = label.replace(" years", "").split("-")
    return (int(lo) + int(hi) + 1) / 2.0   # e.g. 0-4 -> 2.5, 80-84 -> 82.5

def e_at(age, table):
    """Piecewise-linear interpolation of ex on exact-age anchors; flat >= 85."""
    xs = sorted(table)
    if age >= xs[-1]:
        return table[xs[-1]]
    for lo, hi in zip(xs, xs[1:]):
        if lo <= age <= hi:
            w = (age - lo) / (hi - lo)
            return table[lo] * (1 - w) + table[hi] * w
    return table[xs[0]]

def main():
    print("=" * 76)
    print("TLY v0 - Total remaining human Life-Years (all inputs fetched live)")
    print("=" * 76)

    # ---- population by age band [OWID <- UN WPP 2024] ------------------------
    rows = list(csv.DictReader(io.StringIO(fetch_bytes(OWID_AGE).decode())))
    world = [r for r in rows if r["Entity"] == "World"]
    latest_pop_year = max(int(r["Year"]) for r in world)
    wrow = next(r for r in world if int(r["Year"]) == latest_pop_year)
    bands = {k: float(v) for k, v in wrow.items()
             if k not in ("Entity", "Code", "Year") and v}
    pop = sum(bands.values())
    print(f"\n[OWID/WPP2024] World population by 5y band, {latest_pop_year}: "
          f"total {pop:,.0f}")
    print(f"  {OWID_AGE}")

    # ---- global life tables [WHO GHO] ----------------------------------------
    who = json.loads(fetch_bytes(WHO).decode())["value"]
    tables = {}
    for r in who:
        tables.setdefault(int(r["TimeDim"]), {})[WHO_AGE[r["Dim2"]]] = float(r["NumericValue"])
    t19, t21 = tables[2019], tables[2021]
    print(f"\n[WHO GHO] Global abridged life table, both sexes")
    print(f"  2019: e(0)={t19[0]:.4f}  e(30)={t19[30]:.4f}  e(65)={t19[65]:.4f}  e(85+)={t19[85]:.4f}")
    print(f"  2021: e(0)={t21[0]:.4f}  (COVID-depressed; shown as lower bound)")
    print(f"  {WHO}")

    # ---- the stock ------------------------------------------------------------
    def stock(table):
        S = Decimal(0)
        detail = []
        for label, n in bands.items():
            m = band_mean_age(label)
            e = e_at(m, table)
            ly = Decimal(n) * Decimal(e)
            S += ly
            detail.append((label, n, m, e, float(ly)))
        return S.quantize(Q4, rounding=ROUND_HALF_EVEN), detail

    S19, detail = stock(t19)
    S21, _ = stock(t21)
    print(f"\n{'band':>12} {'population':>16} {'mean age':>9} {'e(mean)':>9} {'life-years':>18}")
    for label, n, m, e, ly in detail:
        print(f"{label:>12} {n:>16,.0f} {m:>9.1f} {e:>9.3f} {ly:>18,.0f}")
    print(f"\n  S (2019 table, PRIMARY) = {float(S19):,.0f}  = {float(S19)/1e9:.4f}B life-years")
    print(f"  S (2021 table, lower bound) = {float(S21)/1e9:.4f}B life-years")
    print(f"  E-bar (avg remaining years per living person) = {float(S19/Decimal(pop)):.4f}")
    print(f"  Note: flat e for 90+ bands overstates their e by ~1-2y; those bands")
    print(f"  are {sum(n for l,n,_,_,_ in [(d[0],d[1],0,0,0) for d in detail] if l.startswith(('90','95','100')))/pop*100:.3f}% of population -> bias on S < +0.05%.")

    # ---- organic issuance ------------------------------------------------------
    cbr_rows = list(csv.DictReader(io.StringIO(fetch_bytes(OWID_CBR).decode())))
    wcbr = [r for r in cbr_rows if r["Entity"] == "World" and r.get("Birth rate")]
    cbr_year = max(int(r["Year"]) for r in wcbr)
    cbr = float(next(r for r in wcbr if int(r["Year"]) == cbr_year)["Birth rate"])
    births = cbr / 1000.0 * pop
    mint = Decimal(births) * Decimal(t19[0])
    spend = Decimal(pop)

    def ebar_for(table):
        return sum(n * e_at(band_mean_age(l), table) for l, n in bands.items()) / pop
    d_ebar = (ebar_for(tables[2019]) - ebar_for(tables[2015])) / 4.0
    drift = Decimal(pop) * Decimal(d_ebar)
    net = mint - spend + drift
    g = net / S19

    print(f"\nOrganic issuance decomposition (per year):")
    print(f"  Mint   = births x e(0) = {births:,.0f} x {t19[0]:.4f} = +{float(mint)/1e9:.4f}B")
    print(f"           [OWID/WPP crude birth rate {cbr:.3f}/1000, {cbr_year}]")
    print(f"  Spend  = every living person uses 1 year        = -{float(spend)/1e9:.4f}B")
    print(f"  Drift  = N x d(E-bar)/dt = {pop:,.0f} x {d_ebar:+.4f} = {float(drift)/1e9:+.4f}B")
    print(f"           [WHO tables 2015 -> 2019, current weights held fixed]")
    print(f"  Net    = {float(net)/1e9:+.4f}B per year")
    print(f"  g      = {float(g)*100:+.4f}% per year")
    print(f"  Expected deaths do not appear - they are already inside e(x).")
    print(f"  Only EXCESS deaths versus the table burn stock.")

    # ---- COVID-scale shock ------------------------------------------------------
    # WHO: 14.83M excess deaths associated with COVID-19 across 2020-2021.
    # https://www.who.int/news/item/05-05-2022-14.9-million-excess-deaths-were-associated-with-the-covid-19-pandemic-in-2020-and-2021
    excess = 14.83e6
    print(f"\nCOVID-scale shock (WHO excess deaths 2020-21 = {excess/1e6:.2f}M):")
    for ed, label in ((10.0, "our-table, older skew"), (12.0, "our-table, central"),
                      (15.0, "our-table, younger skew"), (22.7, "WHO YLL-paper implied")):
        burn = Decimal(excess) * Decimal(ed)
        print(f"  mean e at death = {ed:>5.1f} -> burn {float(burn)/1e6:>7.1f}M life-years"
              f" = {float(burn/S19)*100:.4f}% of S   ({label})")

    # ---- vision-consistent asymptote ---------------------------------------------
    usd_hr = Decimal("6.00") / (Decimal(15) / Decimal(60))
    usd_yr = usd_hr * Decimal("8766")
    cap = usd_yr * S19
    # Global personal wealth: UBS GWR base USD 454.4T end-2022, grown by the
    # published rates +4.2% (2023), +4.6% (2024), +10.8% (2025) -> ~USD 549T.
    # https://www.ubs.com/global/en/media/display-page-ndp/en-20260630-gwr-2026.html
    wealth = Decimal("454.4e12") * Decimal("1.042") * Decimal("1.046") * Decimal("1.108")
    print(f"\nVision-consistent asymptote (burger = 15 minutes):")
    print(f"  $6.00 / 15 min -> ${float(usd_hr):.4f}/h -> ${float(usd_yr):,.2f} per life-year")
    print(f"  implied cap = ${float(cap)/1e15:,.4f} quadrillion "
          f"= {float(cap/wealth):.1f}x global personal wealth (~$549T, UBS GWR chain)")

    json.dump({"S_2019_table": float(S19), "S_2021_table": float(S21),
               "pop": pop, "pop_year": latest_pop_year, "e0_2019": t19[0],
               "births": births, "cbr": cbr, "cbr_year": cbr_year,
               "mint": float(mint), "spend": float(spend), "drift": float(drift),
               "d_ebar_per_yr": d_ebar, "net": float(net), "g_pct": float(g)*100,
               "asymptote_usd_per_lifeyear": float(usd_yr),
               "asymptote_cap_usd": float(cap)},
              open("results_v0.json", "w"), indent=2)
    print(f"\nresults_v0.json written. Re-run this file anywhere to reproduce.")

if __name__ == "__main__":
    main()
