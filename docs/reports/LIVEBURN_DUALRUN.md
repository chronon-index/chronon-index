# Live-burn dual run v3 — after two refutation passes

*v1 by this session; pass 1 broke its sign claim and coverage; v2
absorbed those; pass 2 broke v2's prior-year comparison, its missing
baseline policies, and its W27 framing. v3 absorbs pass 2 in full —
every number below is produced by `tly/liveburn_dualrun.py` from
committed snapshots and pinned by tests. Refutation reports:
`~/coordinator/data/refutations/saeculum-liveburn-20261003-{2044-pass1,2059-pass2}.md`.*

## The one-paragraph version, in plain words

Turning on the weekly burn makes the index respond to how many people
actually died each week versus "expected". Everything hangs on how
"expected" is drawn. Our registered rule (a straight line through
2015–2019, stretched to 2026) says 2026 is running about 10 ppm BELOW
normal; Eurostat's own baseline and every post-pandemic rule say 2–22
ppm ABOVE. The movements are tiny either way (parts per million per
week), but the SIGN of the year flips with the choice of rule — so the
rule itself is the decision, and it must be made before the on/off
question means anything.

## The table (2026, weeks 1–27, per-week reporting-set coverage)

| expected-deaths rule | cum ppm of S | excl. edge week |
|---|---|---|
| straight line 2015–2019 (current registered policy) | −9.88 | −15.35 |
| average 2015–2019 | +19.18 | +15.47 |
| average 2016–2019 (Eurostat's own excess baseline) | +22.41 | +18.28 |
| straight line 2017–2019 | +28.45 | +29.04 |
| straight line 2016–2019 | −87.38 | −87.75 |
| straight line 2015–2018 | −26.63 | −35.83 |
| average 2023–2025 | +5.04 | +1.86 |
| straight line 2022–2025 | +23.19 | +20.04 |
| straight line 2023–2025 | −4.03 | −5.02 |
| pooled line 2015–19 + 2022–25 | −11.34 | −13.88 |
| pooled line 2015–19 + 2023–25 | −0.08 | −3.14 |

Reading it honestly: **every post-pandemic-anchored rule lands between
−4 and +23 ppm.** The −87 outlier is a four-point line through the
2017/2018 flu peaks stretched 8.5 years — it sets no floor worth
quoting. The averages ignore that expected deaths in this panel trend
upward (+3.53% over the nine stretched years, computed), so average
rules read about that much too high. Like-for-like prior years under
the current rule (same weeks 1–27): 2024 −23.05, 2025 −5.75 — the
"below normal" reading repeats every year, which is what a drawing
artefact looks like. Age-standardised expectations are impossible on
this feed (totals only).

## The June heat event, correctly framed

Against a modern baseline (average 2023–2025, identical reporters),
the spike is **W26 +15,498 then W27 +8,966** — it starts in W26 and is
larger there. Under the current 2015–19 line it appears as W26 +4,596
/ W27 +15,465 only because that line is drawn high for W26 and low for
W27 (Germany's fit carries the 2015 heat wave). Germany's W26 at
23,932 observed is a 2003-class heat event on provisional cells. The
per-country maturity rule for posting remains right — for posting
discipline, not for this event's explanation.

## What activation would mean, mechanically (unchanged from v2)

Burns post 8–13 weeks after the week they measure (reporting lag),
forward-only, never restating a published print. Weekly movements are
single-digit ppm. The panel covers 7.2–8.3% of world deaths per week,
so world-scaling multiplies panel noise 12–14×; widening the panel
with the already-built US and England+Wales adapters roughly halves
that.

## The two decisions for Ben (card wording per pass 2)

**Decision 1 — the expected-deaths rule.** Live-burn needs a rule for
"expected deaths". The registered rule (a 2015–19 straight line
stretched to 2026) says 2026 runs 10 ppm below normal; Eurostat's own
average and post-pandemic averages say 5–22 ppm above. Keeping the
line risks posting a deficit that is a drawing artefact. Switching
costs a version bump and comparability with the 2020–21 literature.

**Decision 2 — the sign rule.** Should weeks with fewer deaths than
expected add life-years back (symmetric) or count as zero (burn-only)?
Symmetric follows the arithmetic but, under the current line, would
credit about 24 ppm this year that may be a baseline artefact.
Burn-only cannot credit artefacts but only subtracts: it would post
+13.82 ppm from the positive weeks (+8.35 excluding the edge week) and
ignore every deficit week.

*(Both land on one card together with the held Sepolia item, after
pass 3.)*
