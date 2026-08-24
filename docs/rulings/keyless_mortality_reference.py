"""
keyless_mortality.py — HMD-free, credential-free mortality data layer.

Ruling B-uc2-02(c): no accounts, no secrets, no manual snapshots. Every source
below is anonymous HTTP GET. Nothing here reads an env var or a keyring.

Sources (all verified keyless 2026-08-20):
  EU weekly all-cause   Eurostat demo_r_mwk_ts        -> 2026-W32
  EU deaths by 1y age   Eurostat demo_magec           -> 2024
  EU pop by 1y age      Eurostat demo_pjan (1 Jan)    -> 2025
  US weekly all-cause   CDC SODA r8kw-7aab            -> w/e 2026-08-08
  Global life tables    UN WPP 2024 complete LT       -> 2023  (fallback only)

Dependencies: numpy, pandas (stdlib urllib for I/O — no requests, no keys).
"""

from __future__ import annotations

import gzip
import io
import json
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass

import numpy as np
import pandas as pd

_UA = {"User-Agent": "keyless-mortality/1.0 (research pipeline)"}
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
CDC_WEEKLY = "https://data.cdc.gov/resource/r8kw-7aab.json"
WPP_LT = ("https://population.un.org/wpp/assets/Excel%20Files/"
          "1_Indicator%20(Standard)/CSV_FILES/"
          "WPP2024_Life_Table_Complete_Medium_{sex}_1950-2023.csv.gz")


# ----------------------------------------------------------------- transport
def _get(url: str, params: dict | None = None, tries: int = 4, timeout: int = 120) -> bytes:
    """Anonymous GET with exponential backoff. Raises on final failure."""
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=_UA), timeout=timeout) as r:
                return r.read()
        except Exception as e:                       # noqa: BLE001 - retry anything transient
            last = e
            time.sleep(2 ** i)
    raise RuntimeError(f"GET failed after {tries} tries: {url}") from last


# ----------------------------------------------------------------- Eurostat
def eurostat(dataset: str, **filters) -> pd.DataFrame:
    """Eurostat JSON-stat 2.0 -> tidy long DataFrame (one row per cell)."""
    q = {"format": "JSON", "lang": "EN", **filters}
    d = json.loads(_get(EUROSTAT + dataset, q))
    dim_ids, sizes = d["id"], d["size"]
    labels = []
    for k in dim_ids:
        idx = d["dimension"][k]["category"]["index"]
        labels.append(sorted(idx, key=idx.get) if isinstance(idx, dict) else list(idx))
    # JSON-stat stores a sparse dict keyed by the row-major flat index
    strides = np.cumprod([1] + sizes[::-1][:-1])[::-1]
    rows = []
    for flat, val in d["value"].items():
        f = int(flat)
        rows.append([labels[i][(f // strides[i]) % sizes[i]] for i in range(len(sizes))] + [val])
    return pd.DataFrame(rows, columns=list(dim_ids) + ["value"])


def _age_to_int(code: str, open_age_hint: int = 100) -> float:
    """Eurostat age code -> integer age. Y_OPEN/Y_GE* map to their start age."""
    if code in ("TOTAL", "UNK"):
        return np.nan
    if code == "Y_LT1":
        return 0.0
    if code == "Y_OPEN":
        return float(open_age_hint)
    if code.startswith("Y_GE"):
        return float(code[4:])
    if code.startswith("Y"):
        return float(code[1:])
    return np.nan


def _pivot_by_age(df: pd.DataFrame, open_age_hint: int) -> pd.DataFrame:
    """Long Eurostat frame -> (age x year) matrix, UNK redistributed pro-rata."""
    df = df.copy()
    df["a"] = df["age"].map(lambda c: _age_to_int(c, open_age_hint))
    unk = df[df["age"] == "UNK"].set_index("time")["value"] if (df["age"] == "UNK").any() else None
    df = df[df["a"].notna()]
    m = df.pivot_table(index="a", columns="time", values="value", aggfunc="sum").sort_index()
    if unk is not None:                              # spread unknown-age deaths proportionally
        for t in m.columns:
            u = float(unk.get(t, 0.0) or 0.0)
            if u:
                m[t] = m[t] * (1.0 + u / m[t].sum())
    m.columns = [int(c) for c in m.columns]
    return m.sort_index(axis=1)


@dataclass
class DxEx:
    """Raw Lexis-square deaths and mid-year exposures, ages 0..open_age."""
    Dx: pd.DataFrame        # age x year
    Ex: pd.DataFrame        # age x year
    open_age: int
    geo: str
    sex: str

    @property
    def mx(self) -> pd.DataFrame:
        return self.Dx / self.Ex.replace(0.0, np.nan)


def deaths_exposures_eu(geo: str, sex: str = "T", open_age: int = 99) -> DxEx:
    """
    Build HMD-equivalent Dx/Ex from raw Eurostat registry data.

    Ex uses the mid-year approximation Ex = (P(1 Jan t) + P(1 Jan t+1)) / 2.
    HMD instead uses Lexis triangles + monthly births; Eurostat does not publish
    triangles, so this is the one place we are structurally coarser than HMD.
    Bias is second-order (cohort-size curvature), typically <0.5% of exposure
    outside age 0 and the open interval.
    """
    d = eurostat("demo_magec", geo=geo, sex=sex)
    p = eurostat("demo_pjan", geo=geo, sex=sex)
    D = _pivot_by_age(d, open_age + 1)
    P = _pivot_by_age(p, open_age + 1)

    ages = [a for a in range(0, open_age + 1)]
    D = D.reindex(ages).fillna(0.0)
    P = P.reindex(ages)
    years = [y for y in D.columns if y in P.columns and (y + 1) in P.columns]
    D = D[years]
    E = pd.DataFrame({y: (P[y].values + P[y + 1].values) / 2.0 for y in years}, index=ages)
    return DxEx(Dx=D, Ex=E, open_age=open_age, geo=geo, sex=sex)


# ------------------------------------------------------- old-age graduation
def kannisto_close(mx: pd.Series, fit_from: int = 80, to_age: int = 110,
                   weights: pd.Series | None = None) -> pd.Series:
    """
    Kannisto logistic closure: logit(mu_x) = a + b*x for x >= fit_from,
    extrapolated to `to_age`. This is what HMD does above ~80; without it,
    raw Eurostat rates at 95+ are noise-dominated and Lee-Carter b_x blows up.
    """
    s = mx.dropna()
    s = s[(s.index >= fit_from) & (s > 0) & (s < 1)]
    if len(s) < 5:
        return mx.reindex(range(int(mx.index.min()), to_age + 1))
    y = np.log(s.values / (1.0 - s.values))
    w = np.ones_like(y) if weights is None else np.sqrt(weights.reindex(s.index).fillna(1.0).values)
    b, a = np.polyfit(s.index.values.astype(float), y, 1, w=w)
    out = mx.reindex(range(int(mx.index.min()), to_age + 1)).astype(float)
    hi = np.arange(fit_from, to_age + 1, dtype=float)
    z = a + b * hi
    out.loc[hi.astype(int)] = np.exp(z) / (1.0 + np.exp(z))
    return out


# ------------------------------------------------------------- life table
def _a0(m0: float, sex: str = "T") -> float:
    """Andreev-Kingkade a0. Sex 'T' averages the M/F rules."""
    def _m(m):   # male
        return 0.14929 - 1.99545 * m if m < 0.0230 else (0.02832 + 3.26021 * m if m < 0.0785 else 0.29915)
    def _f(m):
        return 0.14903 - 2.05527 * m if m < 0.0170 else (0.04667 + 3.88089 * m if m < 0.0658 else 0.31411)
    return {"M": _m, "F": _f}.get(sex, lambda m: 0.5 * (_m(m) + _f(m)))(m0)


def life_table(mx: pd.Series, sex: str = "T") -> pd.DataFrame:
    """Period life table from single-age mx. Closes with 1/m at the last age."""
    ages = np.asarray(mx.index, dtype=int)
    m = np.asarray(mx.values, dtype=float)
    ax = np.full_like(m, 0.5)
    ax[0] = _a0(m[0], sex)
    qx = m / (1.0 + (1.0 - ax) * m)
    qx[-1] = 1.0
    px = 1.0 - qx
    lx = np.empty_like(m); lx[0] = 1.0
    lx[1:] = np.cumprod(px[:-1])
    dx = lx * qx
    Lx = lx - (1.0 - ax) * dx
    Lx[-1] = lx[-1] / m[-1] if m[-1] > 0 else 0.0
    Tx = np.cumsum(Lx[::-1])[::-1]
    return pd.DataFrame({"mx": m, "qx": qx, "ax": ax, "lx": lx, "dx": dx,
                         "Lx": Lx, "Tx": Tx, "ex": Tx / lx}, index=ages)


# ------------------------------------------------------------- Lee-Carter
@dataclass
class LeeCarter:
    ages: np.ndarray
    years: np.ndarray
    ax: np.ndarray
    bx: np.ndarray
    kt: np.ndarray
    drift: float
    sigma: float
    explained: float          # share of variance in the first SVD component

    def forecast(self, h: int, sims: int = 0, seed: int = 0):
        """Central RW-with-drift path; optionally `sims` simulated k_t paths."""
        k = self.kt[-1] + self.drift * np.arange(1, h + 1)
        if not sims:
            return k
        rng = np.random.default_rng(seed)
        shocks = rng.normal(0.0, self.sigma, size=(sims, h)).cumsum(axis=1)
        return k[None, :] + shocks

    def mx_hat(self, kt: np.ndarray) -> np.ndarray:
        """log mx = ax + bx * kt  ->  (age x horizon) rate matrix."""
        return np.exp(self.ax[:, None] + self.bx[:, None] * np.atleast_1d(kt)[None, :])


def lee_carter(log_mx: pd.DataFrame) -> LeeCarter:
    """Classic SVD Lee-Carter with sum(bx)=1, sum(kt)=0 identification."""
    M = log_mx.to_numpy(dtype=float)
    ax = np.nanmean(M, axis=1)
    C = M - ax[:, None]
    C = np.where(np.isfinite(C), C, 0.0)
    U, S, Vt = np.linalg.svd(C, full_matrices=False)
    bx, kt = U[:, 0], S[0] * Vt[0]
    if bx.sum() < 0:
        bx, kt = -bx, -kt
    scale = bx.sum()
    bx, kt = bx / scale, kt * scale
    kt = kt - kt.mean()
    dk = np.diff(kt)
    return LeeCarter(ages=np.asarray(log_mx.index), years=np.asarray(log_mx.columns),
                     ax=ax, bx=bx, kt=kt, drift=float(dk.mean()), sigma=float(dk.std(ddof=1)),
                     explained=float(S[0] ** 2 / (S ** 2).sum()))


# --------------------------------------------------------------- weekly EU
def eu_weekly_edge(min_geos: int = 20, sex: str = "T", lookback: int = 12) -> str:
    """
    Last ISO week for which at least `min_geos` countries have reported.
    The EU weekly panel has a badly ragged edge: on 2026-08-20 only FI had
    printed W32, while 26 geos had W27. Aggregating at the nominal max week
    silently prints a fake 80% drop in EU deaths -- always cut here.
    """
    df = eurostat("demo_r_mwk_ts", sex=sex)
    cnt = df[df["time"].str.contains("-W")].groupby("time")["geo"].nunique().sort_index()
    ok = cnt[cnt >= min_geos]
    return ok.index[-1] if len(ok) else cnt.index[-1]


def weekly_deaths_eu(geo: str, sex: str = "T") -> pd.Series:
    """Eurostat demo_r_mwk_ts weekly all-cause counts, indexed by ISO week."""
    df = eurostat("demo_r_mwk_ts", geo=geo, sex=sex)
    s = df.set_index("time")["value"].sort_index()
    return s[[t for t in s.index if "-W" in t and not t.endswith("W99")]]


# --------------------------------------------------------------- weekly US
def weekly_deaths_us(state: str = "United States", censor_weeks: int = 8) -> pd.DataFrame:
    """
    CDC SODA r8kw-7aab weekly all-cause. This is the ONLY still-updating keyless
    US weekly all-cause feed: muzy-jte6, y5bj-9g5w, u6jv-9ijr and xkkf-xrst were
    all frozen on 2025-04-21. Cost: no age breakdown.

    `censor_weeks` drops the immature tail (NCHS backfills for ~8 weeks; the most
    recent week typically prints ~50% of its final value).
    """
    params = {
        "$select": "end_date,total_deaths,covid_19_deaths,percent_of_expected_deaths",
        "$where": f"`group`='By Week' AND state='{state}'",
        "$order": "end_date",
        "$limit": "50000",
    }
    df = pd.DataFrame(json.loads(_get(CDC_WEEKLY, params)))
    df["end_date"] = pd.to_datetime(df["end_date"])
    for c in ("total_deaths", "covid_19_deaths", "percent_of_expected_deaths"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.sort_values("end_date").set_index("end_date")
    df["mature"] = np.arange(len(df))[::-1] >= censor_weeks
    return df


# ------------------------------------------------------------- WPP fallback
def wpp_life_table(iso3: str, sex: str = "Both", year_from: int = 1950) -> pd.DataFrame:
    """
    UN WPP 2024 complete (single-age) life table for non-Eurostat geographies.
    ~200MB gzip, so cache the download. NOTE: WPP mx are model-smoothed UN
    estimates, not raw registry counts -- fitting Lee-Carter to them is fitting
    a model to a model. Use only where no raw national feed exists.
    """
    raw = _get(WPP_LT.format(sex=sex), timeout=600)
    chunks = pd.read_csv(io.BytesIO(gzip.decompress(raw)), low_memory=False, chunksize=500_000)
    keep = []
    for ch in chunks:
        sub = ch[(ch["ISO3_code"] == iso3) & (ch["Time"] >= year_from)]
        if len(sub):
            keep.append(sub[["Time", "AgeGrpStart", "mx", "qx", "lx", "ex"]])
    return pd.concat(keep).rename(columns={"Time": "year", "AgeGrpStart": "age"})


# ------------------------------------------------------------------- usage
if __name__ == "__main__":
    # Italy: raw Eurostat -> graduated mx -> life table -> Lee-Carter, zero credentials.
    de = deaths_exposures_eu("IT", sex="T")
    mx = de.mx
    grad = pd.DataFrame({y: kannisto_close(mx[y], 80, 110, weights=de.Dx[y]) for y in mx.columns})
    lt = life_table(grad[grad.columns[-1]].ffill(), sex="T")
    print(f"IT {grad.columns[-1]}  e0 = {lt.loc[0, 'ex']:.4f}   e65 = {lt.loc[65, 'ex']:.4f}")

    fit = lee_carter(np.log(grad.loc[0:100, [c for c in grad.columns if c >= 1990]]))
    print(f"Lee-Carter  drift = {fit.drift:.4f}  sigma = {fit.sigma:.4f}  "
          f"var explained = {fit.explained:.4f}")

    us = weekly_deaths_us()
    m = us[us["mature"]]
    print(f"US weekly all-cause, last mature week {m.index[-1]:%Y-%m-%d}: "
          f"{int(m['total_deaths'].iloc[-1]):,}")
    print(f"EU IT weekly last: {weekly_deaths_eu('IT').index[-1]}  "
          f"| EU panel edge (>=20 geos): {eu_weekly_edge()}")
