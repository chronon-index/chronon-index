"""The personal time page (S-07; RP P7-adjacent; Ben directive 2026-09-04).

Renders ``me.html``: an in-depth questionnaire that estimates ONE
person's remaining time — computed ENTIRELY CLIENT-SIDE. Nothing the
visitor enters is transmitted, stored, or logged anywhere; the page has
no network calls at all. That is what keeps the project's privacy
statement literally true ("no personal data anywhere in the pipeline")
while still offering the estimate: the pipeline never sees a person.

The math (also explained ON the page, line by line):
- Base hazard: the committed WPP 2024 World single-age qx column
  (2023), embedded in the page at build time with its sha256 lineage.
- Sex adjustment: proportional hazard (male x1.28, female x0.76 vs the
  both-sexes table — the typical published sex mortality ratio; an
  approximation, labeled as such).
- Each answer maps to a published relative-risk (hazard multiplier);
  the composite is the product, CLAMPED to [0.35, 4.0] — questionnaire
  RRs multiply badly at the extremes and honesty beats precision.
- Survival: q'(a) = min(1, m * q(a)) walked from the visitor's age;
  remaining time = trapezoid person-years; the 10th/90th percentile
  ages come from the same survival curve.

FRAMING, non-negotiable: population statistics applied to an
individual, wide uncertainty, not medical advice, not a prophecy — the
page says so above the result, not in a footnote. RP P7's
personalized-e ETHICS memo governs any deeper personalization.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

LT_FIX = "data/snapshots/2026-08-17/fixtures/wpp_lt_complete_fixture.csv.gz"

# (id, question, [(label, hazard multiplier, one-line source note)])
FACTORS = [
    (
        "smoke",
        "Smoking",
        [
            ("Never smoked", 1.0, "reference"),
            ("Former smoker (quit 5+ years)", 1.15, "quitting recovers most excess risk"),
            ("Former smoker (quit recently)", 1.35, "excess risk decays over ~10y"),
            ("Current smoker", 2.0, "Doll & Peto cohorts: ~10y expectancy loss"),
        ],
    ),
    (
        "activity",
        "Physical activity",
        [
            ("Regular vigorous exercise", 0.80, "meta-analyses: 20-30% mortality reduction"),
            ("Moderately active", 0.90, "dose-response is steep at the low end"),
            ("Mostly sedentary", 1.15, "reference-ish modern baseline"),
        ],
    ),
    (
        "bmi",
        "Body-mass index",
        [
            ("18.5-25 (normal)", 0.95, "GBD pooled cohorts"),
            ("25-30 (overweight)", 1.0, "near-flat risk in pooled data"),
            ("30-35 (obese I)", 1.25, "hazard rises non-linearly"),
            ("35+ (obese II+)", 1.6, "strong excess, cardiometabolic pathway"),
            ("Under 18.5", 1.3, "underweight carries excess risk too"),
        ],
    ),
    (
        "alcohol",
        "Alcohol",
        [
            ("None or occasional", 1.0, "reference"),
            ("Moderate (within guidelines)", 1.05, "no protective effect in modern MR studies"),
            ("Heavy", 1.5, "GBD alcohol-attributable mortality"),
        ],
    ),
    (
        "diabetes",
        "Diabetes",
        [
            ("No", 1.0, "reference"),
            ("Type 2, well controlled", 1.4, "ERFC pooled hazard ~1.8 uncontrolled"),
            ("Type 2, poorly controlled / Type 1", 1.8, "Emerging Risk Factors Collaboration"),
        ],
    ),
    (
        "bp",
        "Blood pressure",
        [
            ("Normal", 1.0, "reference"),
            ("Elevated / treated hypertension", 1.2, "treated risk sits between"),
            ("Untreated hypertension", 1.45, "Lancet pooled cohorts"),
        ],
    ),
    (
        "income",
        "Relative income / education (your country)",
        [
            ("Top third", 0.85, "Chetty et al.: rich-poor gap is years wide"),
            ("Middle third", 1.0, "reference"),
            ("Bottom third", 1.25, "socioeconomic mortality gradient"),
        ],
    ),
    (
        "family",
        "Parents' longevity",
        [
            ("Both lived / living past 80", 0.88, "heritability of lifespan is modest but real"),
            ("Mixed or unknown", 1.0, "reference"),
            ("Both died before 70 (not accidents)", 1.15, "familial cardiometabolic loading"),
        ],
    ),
    (
        "social",
        "Social connection",
        [
            ("Strong ties, partnered or close community", 0.90, "Holt-Lunstad meta-analysis"),
            ("Average", 1.0, "reference"),
            ("Isolated", 1.2, "isolation hazard comparable to light smoking"),
        ],
    ),
]

SEX_MULT = {"female": 0.76, "male": 1.28, "unspecified": 1.0}
CLAMP_LO, CLAMP_HI = 0.35, 4.0


def _qx_2023(repo_root: Path) -> tuple[list[float], str]:
    """(qx[0..100] for World 2023 from the committed fixture, its sha256)."""
    import csv
    import io

    raw = (repo_root / LT_FIX).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    text = gzip.decompress(raw).decode("utf-8")
    qx = [0.0] * 101
    for r in csv.DictReader(io.StringIO(text)):
        if r["Location"] == "World" and r["Time"] == "2023":
            age = int(r["AgeGrpStart"])
            if age <= 100:
                qx[age] = float(r["qx"])
    qx[100] = 1.0
    return qx, sha


def build_personal_page(repo_root: Path, nav: str) -> str:
    from tly.site import _SHELL  # same shell as every other page

    qx, sha = _qx_2023(repo_root)
    factors_js = json.dumps(
        [
            {"id": fid, "q": q, "opts": [{"l": lab, "m": m, "s": s} for lab, m, s in opts]}
            for fid, q, opts in FACTORS
        ]
    )
    body = f"""
<h1>Your time</h1>
<blockquote>
<p><strong>Private by architecture:</strong> everything on this page is
computed inside your browser. Nothing you enter is sent, stored, or
logged — the page makes no network requests. Close the tab and it is
gone.</p>
</blockquote>
<blockquote>
<p><strong>What this is and is not:</strong> population statistics
applied to one person. It cannot know your genome, your luck, or your
future. The honest reading of the result is a <em>central estimate with
a wide range</em> — not a prophecy, and not medical advice.</p>
</blockquote>

<form id="f" onsubmit="return false">
<p><label>Your age: <input id="age" type="number" min="0" max="100" value="30" style="width:5rem"></label>
&nbsp; <label>Sex:
<select id="sex">
<option value="unspecified">prefer not to say</option>
<option value="female">female</option>
<option value="male">male</option>
</select></label></p>
<div id="qs"></div>
<p><button id="go" style="font-size:1.1rem;padding:.4rem 1.2rem">Estimate my remaining time</button></p>
</form>

<div id="out" hidden>
<h2 id="headline"></h2>
<p id="range"></p>
<p id="share"></p>
<h2>The math, step by step</h2>
<div id="steps"></div>
</div>

<h2>How the estimate works</h2>
<p>1. The base is the <strong>UN WPP 2024 World life table</strong> (2023,
single ages) — the same committed, hash-manifested input the index
settles on (fixture sha256 <code>{sha[:16]}…</code>). It gives q(a):
the probability of dying within a year at each age a.</p>
<p>2. Your answers each carry a published <strong>relative risk</strong> —
a hazard multiplier from the epidemiology literature (source noted on
every option). They multiply into one composite m, clamped to
[{CLAMP_LO}, {CLAMP_HI}] because questionnaire risks multiply badly at
the extremes and honesty beats false precision. Sex uses the typical
published mortality ratio (male ×{SEX_MULT["male"]}, female
×{SEX_MULT["female"]}) against the both-sexes table — an approximation,
labeled as one.</p>
<p>3. Your adjusted hazard is q'(a) = min(1, m·q(a)). Walking it forward
from your age gives your survival curve; summing survivors (a death
counts half a year — the trapezoid rule) gives expected remaining
years. The 10th and 90th percentiles are read off the same curve —
that spread is the honest headline, not the single number.</p>
<p>4. Multiplying your remaining years by nothing gives your stake in
the index: S is simply this number summed over every living person on
earth. One token = one life-year of that total.</p>

<script>
const QX = {json.dumps([round(q, 6) for q in qx])};
const SEXM = {json.dumps(SEX_MULT)};
const FACTORS = {factors_js};
const CLAMP = [{CLAMP_LO}, {CLAMP_HI}];
const qs = document.getElementById("qs");
for (const f of FACTORS) {{
  const p = document.createElement("p");
  let h = "<label>" + f.q + ": <select id='" + f.id + "'>";
  for (let i = 0; i < f.opts.length; i++)
    h += "<option value='" + i + "'>" + f.opts[i].l + "</option>";
  h += "</select></label>";
  p.innerHTML = h;
  qs.appendChild(p);
}}
document.getElementById("go").onclick = () => {{
  const age = Math.max(0, Math.min(100, +document.getElementById("age").value || 0));
  const sex = document.getElementById("sex").value;
  let m = SEXM[sex];
  const steps = [["Sex adjustment (" + sex + ")", SEXM[sex], "published sex mortality ratio"]];
  for (const f of FACTORS) {{
    const o = f.opts[+document.getElementById(f.id).value];
    m *= o.m;
    if (o.m !== 1.0) steps.push([f.q + ": " + o.l, o.m, o.s]);
  }}
  const raw = m;
  m = Math.max(CLAMP[0], Math.min(CLAMP[1], m));
  let alive = 1.0, years = 0.0, p10 = null, p90 = null;
  for (let a = age; a <= 100 && alive > 1e-9; a++) {{
    const q = Math.min(1, m * QX[a]);
    years += alive * (1 - q) + alive * q * 0.5;
    const next = alive * (1 - q);
    if (p90 === null && next <= 0.9) p90 = a - age;
    if (p10 === null && next <= 0.1) p10 = a - age;
    alive = next;
  }}
  if (p10 === null) p10 = 100 - age;
  if (p90 === null) p90 = 0;
  document.getElementById("out").hidden = false;
  document.getElementById("headline").textContent =
    "Central estimate: " + years.toFixed(1) + " remaining years";
  document.getElementById("range").innerHTML =
    "<strong>The honest range:</strong> a 10% chance of fewer than <strong>" + p90 +
    "</strong> years and a 10% chance of more than <strong>" + p10 +
    "</strong> — the spread is the truth; the single number is just its middle.";
  document.getElementById("share").innerHTML =
    "That is your personal stake in the index: humanity's S is exactly this " +
    "quantity summed over all ~8.09 billion of us. One token = one life-year.";
  let sh = "<p>Composite hazard multiplier m = <strong>" + raw.toFixed(3) + "</strong>" +
    (raw !== m ? " (clamped to " + m.toFixed(2) + ")" : "") +
    ", applied as q'(a) = min(1, m·q(a)) to the WPP table from age " + age + ":</p><ul>";
  for (const [label, mult, src] of steps)
    sh += "<li>" + label + " → ×" + mult + " <em>(" + src + ")</em></li>";
  document.getElementById("steps").innerHTML = sh + "</ul>";
}};
</script>
"""
    return _SHELL.format(title="Your time — SAECULUM", nav=nav, body=body)
