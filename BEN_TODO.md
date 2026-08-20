# Ben's action list — everything only you can do

State as of 2026-08-18: 284 tests green, CI live, first print archived
(epoch 2026-08-17, research series). Every task an autonomous session can
execute is done; each item below needs your identity, money, signature, or
judgment. Ordered by leverage — item 1 unblocks the most.

---

## 1. A-16 — Ratify the reconstructed methodology  ⭐ highest leverage

The original SPEC.md, METHODOLOGY_v0.md and seed calculator were lost;
they were reconstructed 2026-08-16, adversarially reviewed, and every
DECISIONS.md key number was reproduced or residual-documented. Nothing
can be called official until you sign off.

**Review packet (in reading order):**
- `seed/CALC_REPORT_v0.txt` — §3 achieved-vs-target table, §7 mint-gap
  hypotheses (all refuted; −0.0026% residual stands), §8 the recovered
  drift convention: drift = [S(pop2023, WHO2019) − S(pop2023, WHO2015)]/4
  = 1.0394B exact — recovered by search, cannot be *proven* to be the
  original's definition. This is the main thing you're ratifying.
- `METHODOLOGY_v0.md` — esp. §4 (transport identity) and §8 item 7: the
  unreconciled DECISIONS tension (S₀ ≈ 330.0B vs S = 362.4126B).
- `SPEC.md` — esp. the amended AC-1.2 (golden anchor definition).
- Also decide: the error-budget module computes the cohort band as
  **381–402B** where DECISIONS prose said "~380–400B" (prose had rounded).
  Bless the computed values.

**How to ratify:** check the box on A-16 in `loop/BACKLOG.md`, note it in
`loop/JOURNAL.md`, commit. That unblocks B-uc1-13 (golden anchor commit)
and removes the "pending ratification" banners.

**Effort:** one focused evening.

---

## 2. A-17 remainder — Praevex org + public flip

Done already: private repo `HaleMarshall/tly` exists, all commits pushed,
CI green, weekly Monday print job armed. Remaining decisions:

- [x] ~~Praevex GitHub org~~ — RULED 2026-08-20: personal account is
      fine; this is a separate organisation from Praevex (the time
      project stands alone). No transfer.
- [ ] Flip visibility to **public** — required for "the CI run IS the
      official computation; anyone can watch the print being made."
      Note: everything in the repo was built to be public (no secrets by
      design), but flip only after A-16 so what goes public is ratified.
- [ ] After the flip: enable branch protection + require status checks
      (pairs with E-12 signing below).

**Effort:** 15 minutes + the judgment call.

---

## 3. B-uc2-02 — HMD account + the keyless-rule ruling

STMF weekly deaths now sit behind a login (verified: the old keyless URL
302s to /Account/Login). Registration is free, but putting credentials in
the pipeline violates your no-secrets rule (RALPH §6 / G6).

- [ ] Register at mortality.org (free) — needed for STMF *and* for the
      single-age life tables Lee-Carter needs (D-01).
- [ ] **Rule on the conflict** — options framed in the backlog:
      (a) Eurostat/CDC keyless feeds as the automated legs (Eurostat is
          already wired and live to 2026-W31), with STMF as a
          manually-refreshed snapshot you download while logged in; or
      (b) relax G6 for one read-only account via a version gate.
      Recommendation on file: (a) — it keeps the pipeline keyless and
      STMF becomes a periodic manual snapshot like any other vintage.

**Unblocks:** the STMF chain → ≥570-week backfill → the COVID-drag gate
(B-uc2-03/11/12/13), and D-01 → Lee-Carter → cohort series (C-uc6-03/04,
D-02, D-04).

**Effort:** 10 minutes to register; the ruling is one decision.

---

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
