# Ben's action list — everything only you can do

State as of 2026-08-18: 284 tests green, CI live, first print archived
(epoch 2026-08-17, research series). Every task an autonomous session can
execute is done; each item below needs your identity, money, signature, or
judgment. Ordered by leverage — item 1 unblocks the most.

---

## 1. A-16 — ✅ CLOSED 2026-09-03

You delivered chronon-restore-A16.zip; originals restored verbatim, v0-original inputs frozen, AC-1.2 strict golden green (all 13 original values reproduce at 4dp). The reconstruction stays archived and runnable. Nothing left here.

## 2. A-19 — deploy key ✅ DONE; ONE CLICK left

Key + secret + bypass are live and END-TO-END PROVEN (the print bot pushed commit 39c475c over the key on 2026-09-03). Your one click, whenever you want strict protection: repo Settings → Rules → main-review-and-checks → Enforcement: Active. After that, main accepts only signed PR commits with passing checks (the print bot bypasses via its key). Recommendation: flip after the build loop quiets down.

## 3. B-uc2-02 — RULED (c) and BUILT. Nothing left here.

Your keyless-only ruling (docs/rulings/B-uc2-02_RULING.md) is executed:
HMD removed everywhere, no account needed ever. CDC r8kw-7aab feed live
with 8-week censoring; EU panel-edge guard live; Eurostat magec/pjan
life-table build + Lee-Carter integration queued as loop tasks
(D-01, B-uc2-19). The Lee-Carter chain is no longer human-gated.

## 4. Commercial data licenses — ACLED + EM-DAT

Both confirmed to require licenses for commercial use; both are shock-mesh
feeds (rung 5), not needed for the v1 index itself.

- [ ] ACLED commercial license (B-uc3-11) — contact via acleddata.com.
- [ ] EM-DAT commercial-use license (B-uc3-12) — CRED / UCLouvain.

**Effort/cost:** inquiry emails; pricing unknown until you ask. Can wait
until the shock mesh is actually being built.

---

## 5. Counsel + formal trademark search (D-13, D-14)

- [ ] **Trademark:** formal EUIPO + USPTO searches for CHRONON in Nice
      classes 9/36/42, likelihood-of-confusion analysis vs Cronos (CRO —
      Crypto.com, market rank 36, the live opposition risk) and the
      CHR-symbol projects. My preliminary sweep is in
      `docs/TRADEMARK_PRELIM.md`: exact "chronon" still has zero coins;
      chronon.xyz and tly.finance looked unregistered; chronon.io is on
      the Afternic aftermarket. Reserve name if blocked: SAECULUM.
- [ ] **Counsel memos:** MiCA classification (SAEC has no redemption
      claim/peg — likely "other crypto-asset"), SEC/Howey analysis,
      jurisdiction choice (FINMA Zug vs Cayman vs UK).
- [ ] After counsel exists: D-15 terms-of-use / disclaimer / privacy /
      conflict-of-interest drafts get their review.

**Budget anchor (your own plan):** counsel €10–30k at P5/P6.
**Timing:** before any settlement product or token step — not needed for
running the research index.

---

## 6. The reading program (D-12)

Two are already done for you (notes in `docs/notes/READING_NOTES.md`):
Vaupel 2009 and the IOSCO Principles — both read from primary sources,
summarized, with TLY-specific consequences.

Still yours (books + paywalled papers):
- [ ] R1: Preston/Heuveline/Guillot; Keyfitz & Caswell; Wachter
- [ ] R2: Lee-Carter 1992; CBD 2006; Renshaw-Haberman; Plat; Cairns 2009
      (its backtest protocol gates C-uc6-04); Raftery PNAS; Barbi 2018
- [ ] R3: Blake et al. "The New Life Market"; Loeys 2007; Wang 2000 —
      gate the whitepaper's LifeMetrics-postmortem section
- [ ] R4 remainder: EU BMR text; the Wheatley Review
- [ ] R6: Ampleforth docs/audits; Basis/Terra postmortems; Worldcoin PoP
- [ ] R7: Becker 1965 — gates whitepaper §6

Each finished reading: fill its entry in READING_NOTES (format is at the
top of the file). **Effort:** your plan estimates ~9–12 weeks part-time
for the full program; the whitepaper-gating subset (R3 + Becker) is ~2 weeks.

---

## 7. Hosting + infrastructure accounts

- [ ] **Zenodo** (E-05) — free; then the prepared deposit dry-run
      (`tly/zenodo.py`) goes live: one DOI per vintage.
- [ ] **Cloudflare Pages** (E-07) — free tier; domain choice ties into
      the trademark decision above. Unblocks E-08 (deploy the site + API;
      the static tree is already built and tested).
- [ ] **Object storage** (E-09) — R2 or S3, for the >60MB snapshots that
      are manifest-only in git. Unblocks E-10 (uploader).
- [ ] **Signing keys** (E-12) — sigstore/cosign + signed commits + branch
      protection on the org repo. After A-17.

**Effort:** ~an hour total for accounts; costs ≈ free tier / < €200/yr
per your plan.

---

**Update 2026-09-03:** you hold saeculum.foundation and saeculumfoundation.com (GoDaddy) — the domain half of this is done if SAECULUM is the name. Still needed: the Cloudflare (or other) hosting account for the site + R2 storage, the Zenodo account (your ORCID 0009-0004-6118-8665 is recorded and links there), and a naming ruling: is the public name SAECULUM now, or does the CHRONON trademark search (item 5) still decide?

## 8. E-14 — Recruit external recomputers  (the P5 milestone)

At least 2 independent parties who run `docs/REPRODUCE_FIXING.md` (or the
one-command Docker image — proven byte-identical cross-platform) and
publish their fixing hashes. N-of-M starts at 3-of-3 matching.

Your plan's natural candidates: a university demography group and an
actuarial society student chapter. This is the gate that makes the index
settlement-grade — and per the IOSCO mapping just completed
(`docs/IOSCO_MAPPING.md`), every remaining IOSCO gap is exactly this
entity/oversight work, not computation.

**Effort:** outreach emails once the repo is public (item 2 first).

---

## NEW (2026-09-03): G5 sign-off — the switch out of research mode

The source-of-record switch (WHO -> WPP) is fully computed and proposed:
docs/proposals/2026-09-03-G5-source-of-record.md (also on the live site).
Level change +1.0991B = +0.3033%, decomposed (table +1.1639B, resolution
-0.0648B), archived prints untouched, v0 golden untouched. Your part:
read it, and either sign off (pre-P1 shortcut) or rule that the 14-day
public window applies now that the site is live. On sign-off I execute
the one-commit v0.7.0 bump and the settlement series leaves research
mode at the next epoch.

## Suggested order

1. **A-16 ratification** (one evening — unblocks the anchor + banners)
2. **A-17 flip + org** (15 min — makes the computation genuinely public)
3. **B-uc2-02 HMD + ruling** (10 min + one decision — unblocks the
   backfill and Lee-Carter chains)
4. **Accounts batch** (Zenodo/Cloudflare/R2/keys — one hour)
5. **E-14 outreach** (after the repo is public)
6. Readings in parallel; counsel/trademark/licenses when you approach P5.

When any box above is checked, restart the loop (`./ralph.sh`) — the
backlog knows exactly which tasks each gate unblocks.
