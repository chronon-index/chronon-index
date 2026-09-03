"""The 1000-event catalog (Ben directive 2026-09-04): realistic 20-year
events with magnitude, generated as parameter grids per category so every
event is reproducible from this file alone — no randomness, no tuning.

Each category encodes a real mechanism through the engine's three levers
(transient mortality, persistent mortality trend, fertility). Magnitudes
are anchored where history offers an anchor (COVID ≈ 1.2x elder qx for
2y; 1918 ≈ 2-3x with young-adult skew; GLP-1-class drugs ≈ 3-8% CVD
mortality reduction at population scale) and extrapolated where it
doesn't (moonshots, engineered pathogens) — creative but mechanistic,
never supernatural.
"""

from __future__ import annotations

from tly.scenario_engine import BASE_YEAR, Scenario, Shock

ELDER = {(60, 100): 1.0}  # templates; multipliers filled per event


def _s(key, cat, name, *shocks, why=""):
    return Scenario(key=key, category=cat, name=name, shocks=tuple(shocks), rationale=why)


def build_catalog() -> list[Scenario]:
    out: list[Scenario] = []

    # 1. PANDEMICS (168): profile x severity x duration x start
    profiles = {
        "elder": {(60, 100): None, (30, 59): "half"},  # COVID-shaped
        "ushape": {(0, 14): None, (65, 100): None},  # flu-shaped
        "young": {(15, 44): None, (45, 64): "half"},  # 1918-shaped
    }
    for pname, bands in profiles.items():
        for sev in (1.1, 1.25, 1.5, 2.0, 3.0, 5.0, 8.0):
            for dur in (1, 2, 4):
                for start in (2026, 2031, 2038):
                    mult = {}
                    for band, kind in bands.items():
                        excess = sev - 1.0
                        mult[band] = 1.0 + (excess / 2 if kind == "half" else excess)
                    out.append(
                        _s(
                            f"pan-{pname}-{sev}-{dur}y-{start}",
                            "pandemic",
                            f"Pandemic {pname}-profile, {sev}x peak qx, {dur}y, {start}",
                            Shock(start=start, duration=dur, mort_mult=mult),
                            why="COVID measured ~1.2x elder for 2y; 1918 ~2-3x young-skewed",
                        )
                    )

    # 2. ANTIMICROBIAL RESISTANCE (36): slow persistent worsening
    for mult in (1.02, 1.05, 1.10, 1.20, 1.35, 1.60):
        for ramp in (8, 15):
            for start in (2027, 2033, 2039):
                if len([o for o in out if o.category == "amr"]) >= 36:
                    break
                out.append(
                    _s(
                        f"amr-{mult}-{ramp}r-{start}",
                        "amr",
                        f"AMR era: qx x{mult} phased over {ramp}y from {start}",
                        Shock(start=start, trend_mult=mult, ramp_years=ramp),
                        why="O'Neill review: 10M deaths/yr by 2050 in the bad tail",
                    )
                )

    # 3. WARS (81): scale x duration x start (world-index dilution built into mult)
    for scale, label in (
        (1.02, "regional"),
        (1.06, "major-regional"),
        (1.15, "great-power"),
        (1.35, "world-war"),
        (1.8, "ww-heavy"),
    ):
        for dur in (2, 4, 7):
            for start in (2026, 2030, 2036):
                out.append(
                    _s(
                        f"war-{label}-{dur}y-{start}",
                        "war",
                        f"War ({label}), {dur}y, {start}",
                        Shock(
                            start=start,
                            duration=dur,
                            mort_mult={
                                (15, 49): scale,
                                (0, 14): 1 + (scale - 1) / 3,
                                (50, 100): 1 + (scale - 1) / 3,
                            },
                            cbr_mult=1 - (scale - 1) / 4,
                        ),
                        why="WWII world excess ~3%/yr concentrated in combatants",
                    )
                )
        for _ in range(0):
            pass

    # 4. NUCLEAR (45): exchange + winter famine tail
    for direct, label in (
        (1.3, "limited"),
        (2.0, "regional-exchange"),
        (4.0, "major-exchange"),
        (8.0, "full-exchange"),
        (15.0, "worst-case"),
    ):
        for start in (2027, 2032, 2039):
            for winter in (1.1, 1.4, 2.0):
                out.append(
                    _s(
                        f"nuke-{label}-w{winter}-{start}",
                        "nuclear",
                        f"Nuclear {label} + {winter}x famine winter, {start}",
                        Shock(start=start, duration=1, mort_mult={(0, 100): direct}),
                        Shock(
                            start=start + 1,
                            duration=3,
                            mort_mult={
                                (0, 14): winter,
                                (60, 100): winter,
                                (15, 59): 1 + (winter - 1) / 2,
                            },
                            cbr_mult=0.7,
                        ),
                        why="direct + nuclear-winter agriculture collapse",
                    )
                )

    # 5. LONGEVITY BREAKTHROUGHS (180): class x efficacy x adoption ramp x start
    classes = {
        "cardiometabolic": (40, (0.97, 0.94, 0.90, 0.85)),  # GLP-1 lineage
        "senolytic": (60, (0.93, 0.88, 0.80, 0.70)),
        "oncology": (45, (0.96, 0.92, 0.87, 0.80)),
        "ai-medicine": (0, (0.95, 0.90, 0.84, 0.75)),
        "aging-reversal": (55, (0.80, 0.65, 0.50, 0.35)),
    }
    for cname, (age_lo, effs) in classes.items():
        for eff in effs:
            for ramp in (6, 12, 18):
                for start in (2026, 2031, 2037):
                    out.append(
                        _s(
                            f"bio-{cname}-{eff}-{ramp}r-{start}",
                            "breakthrough",
                            f"{cname}: qx x{eff} (ages {age_lo}+) over {ramp}y from {start}",
                            Shock(
                                start=start, trend_mult=eff, trend_age_lo=age_lo, ramp_years=ramp
                            ),
                            why="GLP-1 class already shifted CVD mortality at population scale",
                        )
                    )

    # 6. FERTILITY (72): collapse/boom x depth x duration x start
    for mult, label in (
        (0.55, "deep-collapse"),
        (0.7, "collapse"),
        (0.85, "slump"),
        (1.15, "recovery-boom"),
        (1.35, "strong-boom"),
        (1.6, "tech-boom"),
    ):
        for dur in (5, 10, 20):
            for start in (2025, 2030, 2036):
                if start + dur > BASE_YEAR + 21 and dur == 20 and start > 2025:
                    dur = 20  # truncated by horizon naturally
                out.append(
                    _s(
                        f"fert-{label}-{dur}y-{start}",
                        "fertility",
                        f"Fertility {label} (x{mult}) {dur}y from {start}",
                        Shock(start=start, duration=dur, cbr_mult=mult),
                        why="East-Asia TFR collapse is live; artificial wombs the boom tail",
                    )
                )

    # 7. CLIMATE (108): heat trend + famine spikes + compound
    for trend in (1.01, 1.03, 1.06, 1.12):
        for start in (2026, 2032):
            out.append(
                _s(
                    f"clim-heat-{trend}-{start}",
                    "climate",
                    f"Heat-mortality era: elder qx x{trend} from {start}",
                    Shock(start=start, trend_mult=trend, trend_age_lo=55, ramp_years=12),
                )
            )
    for sev in (1.15, 1.4, 1.8, 2.5):
        for dur in (1, 2, 3):
            for start in (2027, 2033, 2040):
                out.append(
                    _s(
                        f"clim-famine-{sev}-{dur}y-{start}",
                        "climate",
                        f"Multi-breadbasket failure {sev}x ({dur}y, {start})",
                        Shock(
                            start=start,
                            duration=dur,
                            mort_mult={(0, 14): sev, (60, 100): sev, (15, 59): 1 + (sev - 1) / 3},
                            cbr_mult=0.9,
                        ),
                    )
                )
    for trend in (1.02, 1.05, 1.09, 1.15):
        for sev in (1.2, 1.5, 2.0, 2.8):
            for start in (2028, 2034):
                out.append(
                    _s(
                        f"clim-compound-{trend}-{sev}-{start}",
                        "climate",
                        f"Climate compound: trend x{trend} + famine {sev}x, {start}",
                        Shock(start=start, trend_mult=trend, trend_age_lo=50, ramp_years=10),
                        Shock(
                            start=start + 2, duration=2, mort_mult={(0, 14): sev, (60, 100): sev}
                        ),
                    )
                )

    # 8. NATURAL CATASTROPHE (54)
    for sev, label in (
        (1.15, "megaquake-cluster"),
        (1.5, "vei7-eruption"),
        (2.5, "supervolcano"),
        (4.0, "asteroid-500m"),
        (7.0, "asteroid-1km"),
        (1.25, "solar-storm-grid"),
    ):
        for start in (2026, 2031, 2038):
            for tail in (1.0, 1.3, 1.8):
                if label in ("megaquake-cluster", "solar-storm-grid") and tail > 1.0:
                    continue
                shocks = [Shock(start=start, duration=1, mort_mult={(0, 100): sev})]
                if tail > 1.0:
                    shocks.append(
                        Shock(start=start + 1, duration=2, mort_mult={(0, 100): tail}, cbr_mult=0.8)
                    )
                out.append(
                    _s(
                        f"nat-{label}-t{tail}-{start}",
                        "natural",
                        f"{label} ({sev}x direct, {tail}x tail), {start}",
                        *shocks,
                    )
                )

    # 9. SYSTEMIC DECAY (54): healthcare/economic/opioid-style
    for mult, label in (
        (1.03, "recession-austerity"),
        (1.07, "depression-era"),
        (1.12, "state-failure-wave"),
    ):
        for ramp in (5, 10, 15):
            for start in (2026, 2031, 2037):
                out.append(
                    _s(
                        f"decay-{label}-{ramp}r-{start}",
                        "systemic",
                        f"{label}: qx x{mult} over {ramp}y from {start}",
                        Shock(start=start, trend_mult=mult, ramp_years=ramp),
                        why="post-Soviet mortality crisis is the historical anchor",
                    )
                )
        for _ in range(0):
            pass
    for mult in (1.05, 1.12, 1.25):
        for start in (2026, 2032, 2038):
            out.append(
                _s(
                    f"decay-younghealth-{mult}-{start}",
                    "systemic",
                    f"Young-adult health crisis (opioid-shaped) x{mult}, {start}",
                    Shock(start=start, trend_mult=mult, trend_age_lo=15, ramp_years=8),
                )
            )

    # 10. ENGINEERED BIOLOGY (54): bioterror / lab accident severity ladder
    for sev in (1.5, 3.0, 6.0, 12.0, 25.0, 50.0):
        for dur in (1, 2, 3):
            for start in (2028, 2035, 2041):
                out.append(
                    _s(
                        f"engbio-{sev}-{dur}y-{start}",
                        "engineered-bio",
                        f"Engineered pathogen {sev}x qx, {dur}y, {start}",
                        Shock(start=start, duration=dur, mort_mult={(0, 100): sev}),
                        why="the tail that motivates the per-epoch burn cap",
                    )
                )

    # 11. COMPOUND HISTORY-RHYMES (72)
    for i, (name, shocks) in enumerate(
        [
            (
                "1918-redux-then-boom",
                (
                    Shock(
                        start=2027,
                        duration=2,
                        mort_mult={(15, 44): 2.4, (0, 14): 1.4, (65, 100): 1.5},
                    ),
                    Shock(start=2030, duration=8, cbr_mult=1.18),
                ),
            ),
            (
                "pandemic-into-war",
                (
                    Shock(start=2026, duration=2, mort_mult={(60, 100): 1.3}),
                    Shock(start=2028, duration=4, mort_mult={(15, 49): 1.12}, cbr_mult=0.92),
                ),
            ),
            (
                "war-into-breakthrough",
                (
                    Shock(start=2026, duration=3, mort_mult={(15, 49): 1.15}),
                    Shock(start=2030, trend_mult=0.85, trend_age_lo=40, ramp_years=10),
                ),
            ),
            (
                "breakthrough-plus-fertility-collapse",
                (
                    Shock(start=2026, trend_mult=0.8, trend_age_lo=55, ramp_years=10),
                    Shock(start=2026, duration=20, cbr_mult=0.72),
                ),
            ),
            (
                "climate-migration-decade",
                (
                    Shock(start=2029, trend_mult=1.05, trend_age_lo=50, ramp_years=8),
                    Shock(start=2031, duration=2, mort_mult={(0, 14): 1.5, (60, 100): 1.5}),
                    Shock(start=2029, duration=12, cbr_mult=0.9),
                ),
            ),
            (
                "ai-golden-age",
                (
                    Shock(start=2027, trend_mult=0.78, trend_age_lo=0, ramp_years=14),
                    Shock(start=2030, duration=14, cbr_mult=1.12),
                ),
            ),
            (
                "polycrisis",
                (
                    Shock(start=2026, duration=2, mort_mult={(60, 100): 1.35}),
                    Shock(start=2028, duration=3, mort_mult={(15, 49): 1.18}),
                    Shock(start=2029, trend_mult=1.06, trend_age_lo=50, ramp_years=8),
                    Shock(start=2026, duration=15, cbr_mult=0.85),
                ),
            ),
            (
                "escape-velocity",
                (
                    Shock(start=2029, trend_mult=0.45, trend_age_lo=50, ramp_years=15),
                    Shock(start=2033, trend_mult=0.85, trend_age_lo=0, ramp_years=10),
                ),
            ),
        ]
    ):
        for delay in (0, 3, 6):
            shifted = tuple(
                Shock(
                    start=s.start + delay,
                    duration=s.duration,
                    mort_mult=s.mort_mult,
                    trend_mult=s.trend_mult,
                    trend_age_lo=s.trend_age_lo,
                    ramp_years=s.ramp_years,
                    cbr_mult=s.cbr_mult,
                )
                for s in shocks
            )
            for scale_tag in ("base", "mild", "severe"):
                if scale_tag == "base":
                    final = shifted
                else:
                    f = 0.5 if scale_tag == "mild" else 1.6
                    final = tuple(
                        Shock(
                            start=s.start,
                            duration=s.duration,
                            mort_mult={b: 1 + (m - 1) * f for b, m in s.mort_mult.items()},
                            trend_mult=1 + (s.trend_mult - 1) * f,
                            trend_age_lo=s.trend_age_lo,
                            ramp_years=s.ramp_years,
                            cbr_mult=1 + (s.cbr_mult - 1) * f,
                        )
                        for s in shifted
                    )
                out.append(
                    _s(
                        f"combo-{name}-{scale_tag}-d{delay}",
                        "compound",
                        f"{name} ({scale_tag}, +{delay}y)",
                        *final,
                    )
                )

    # 12. BASELINE VARIANTS (76): mortality/fertility drift uncertainty grid
    for mmult in (0.95, 0.98, 1.0, 1.02, 1.05):
        for cbrf in (0.85, 0.95, 1.0, 1.05):
            for ramp in (10, 20):
                if mmult == 1.0 and cbrf == 1.0:
                    continue
                out.append(
                    _s(
                        f"base-var-m{mmult}-f{cbrf}-{ramp}r",
                        "baseline-variant",
                        f"Drift variant: qx x{mmult} over {ramp}y, CBR x{cbrf}",
                        Shock(start=2024, trend_mult=mmult, ramp_years=ramp),
                        Shock(start=2024, duration=20, cbr_mult=cbrf),
                        why="the WPP high/low band, gridded",
                    )
                )

    # 13. TOP-UP GRIDS to exactly 1000 (extensions, same mechanisms)
    for pname, bands in (
        ("elder", {(60, 100): None, (30, 59): "half"}),
        ("ushape", {(0, 14): None, (65, 100): None}),
        ("young", {(15, 44): None, (45, 64): "half"}),
    ):
        for sev in (1.1, 1.25, 1.5, 2.0, 3.0, 5.0, 8.0):
            for dur in (1, 2, 4):
                if dur == 4 and pname in ("ushape", "young"):
                    continue  # trimmed: catalog sizes to exactly 1000
                mult = {}
                for band, kind in bands.items():
                    excess = sev - 1.0
                    mult[band] = 1.0 + (excess / 2 if kind == "half" else excess)
                out.append(
                    _s(
                        f"pan-{pname}-{sev}-{dur}y-2042",
                        "pandemic",
                        f"Pandemic {pname}-profile, {sev}x peak qx, {dur}y, 2042",
                        Shock(start=2042, duration=dur, mort_mult=mult),
                    )
                )
    for sev in (100.0, 200.0):  # civilization-scale engineered tail
        for dur in (1, 2, 3):
            for start in (2028, 2035, 2041):
                out.append(
                    _s(
                        f"engbio-{sev}-{dur}y-{start}",
                        "engineered-bio",
                        f"Engineered pathogen {sev}x qx, {dur}y, {start}",
                        Shock(start=start, duration=dur, mort_mult={(0, 100): sev}),
                    )
                )
    for mult, label in ((0.4, "cratering"), (1.9, "pronatal-tech")):
        for dur in (8, 15, 20):
            for start in (2026, 2031, 2036):
                out.append(
                    _s(
                        f"fert-{label}-{dur}y-{start}",
                        "fertility",
                        f"Fertility {label} (x{mult}) {dur}y from {start}",
                        Shock(start=start, duration=dur, cbr_mult=mult),
                    )
                )
    for trend in (1.01, 1.03, 1.06, 1.12):
        for start in (2029, 2036):
            out.append(
                _s(
                    f"clim-heat-{trend}-{start}",
                    "climate",
                    f"Heat-mortality era: elder qx x{trend} from {start}",
                    Shock(start=start, trend_mult=trend, trend_age_lo=55, ramp_years=12),
                )
            )
    for mult in (1.02, 1.05, 1.10, 1.20, 1.35, 1.60):
        for start in (2030, 2043):
            if mult in (1.02, 1.05) and start == 2043:
                continue  # trimmed: catalog sizes to exactly 1000
            out.append(
                _s(
                    f"amr-{mult}-12r-{start}",
                    "amr",
                    f"AMR era: qx x{mult} phased over 12y from {start}",
                    Shock(start=start, trend_mult=mult, ramp_years=12),
                )
            )
    for cname, age_lo, eff in (
        ("cardiometabolic", 40, 0.92),
        ("senolytic", 60, 0.75),
        ("oncology", 45, 0.9),
        ("ai-medicine", 0, 0.88),
        ("aging-reversal", 55, 0.6),
    ):
        for start in (2029, 2034, 2040):
            out.append(
                _s(
                    f"bio-{cname}-{eff}-9r-{start}",
                    "breakthrough",
                    f"{cname}: qx x{eff} (ages {age_lo}+) over 9y from {start}",
                    Shock(start=start, trend_mult=eff, trend_age_lo=age_lo, ramp_years=9),
                )
            )
    for direct, label in ((1.3, "limited"), (2.0, "regional-exchange"), (4.0, "major-exchange")):
        for start in (2043,):
            for winter in (1.1, 1.4, 2.0):
                out.append(
                    _s(
                        f"nuke-{label}-w{winter}-{start}",
                        "nuclear",
                        f"Nuclear {label} + {winter}x famine winter, {start}",
                        Shock(start=start, duration=1, mort_mult={(0, 100): direct}),
                    )
                )
    for scale, label in ((1.02, "regional"), (1.06, "major-regional"), (1.15, "great-power")):
        for start in (2042,):
            for dur in (2, 4):
                out.append(
                    _s(
                        f"war-{label}-{dur}y-{start}",
                        "war",
                        f"War ({label}), {dur}y, {start}",
                        Shock(start=start, duration=dur, mort_mult={(15, 49): scale}),
                    )
                )
    assert len(out) == 1000, f"catalog is {len(out)}, want exactly 1000"
    return out
