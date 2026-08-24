# Ben's action list — everything only you can do

State as of 2026-08-18: 284 tests green, CI live, first print archived
(epoch 2026-08-17, research series). Every task an autonomous session can
execute is done; each item below needs your identity, money, signature, or
judgment. Ordered by leverage — item 1 unblocks the most.

---

## 1. A-16 — one file left: deliver chronon-index-READY.zip  ⭐

Your D1–D7 rulings (docs/rulings/A16_DECISIONS.md) are EXECUTED as of
2026-08-24: reconstructions archived to ops/reconstruction/, drift
convention confirmed against the original source (D2), the mint residual
explained and ledgered as C-0002 (D3), SPEC AC-1.2 rewritten (D4), D5/D6
doc corrections applied, D7 commendation journaled.

**The only thing left:** `chronon-index-READY.zip` is not on this machine
(searched disk, iCloud, the org, and both scaffold zips — only the
pre-merge scaffolds exist here). Drop it in `~/Downloads` and the next
session executes the restore: originals → live tree, D3b v0-original
snapshot freeze, golden swap to full precision, A-16 box checked.

## 2. A-17 — DONE. Successor: A-19 deploy key (10 minutes)

Done 2026-08-20: repo transferred to the **chronon-index** org, renamed, and
flipped **public**. Canonical remote is now
`github.com/chronon-index/chronon-index`; the old `HaleMarshall/tly` URL
redirects. Ruleset `main-integrity` is ACTIVE on main — no force pushes, no
deletions. Local clones keep working via the redirect, but retarget them:

    git remote set-url origin git@github.com:chronon-index/chronon-index.git

**What is left (A-19).** The second ruleset, `main-review-and-checks`
(signed commits + PR + required `test` check), is created but **disabled**,
because turning it on right now would break the weekly print: GitHub gives
rulesets no GitHub-Actions bypass actor, so the print bot's push to `main`
would be rejected. A write-enabled **deploy key** is the one bypass actor
that works for a bot without handing humans a bypass:

    ssh-keygen -t ed25519 -C "tly-print-bot" -f /tmp/print_bot -N ""

1. `cat /tmp/print_bot.pub` -> Settings -> Deploy keys -> Add deploy key,
   **tick "Allow write access"**.
2. `cat /tmp/print_bot` -> Settings -> Secrets and variables -> Actions ->
   New repository secret named `PRINT_BOT_DEPLOY_KEY`.
3. Settings -> Rulesets -> `main-review-and-checks` -> Bypass list ->
   Add bypass -> **Deploy keys**; set Enforcement to **Active**; save.
4. Actions -> weekly-print -> Run workflow. Confirm the archive commit lands.
5. `shred -u /tmp/print_bot /tmp/print_bot.pub`

`print.yml` is already wired for step 2 and falls back to `GITHUB_TOKEN`
if the secret is absent, so nothing breaks between now and then.

**Note on the no-secrets principle.** G6/RALPH#6 is about *data sources*
being keyless — no API keys in the fetch path. A repo-scoped deploy key is
CI infrastructure, not a data credential, and it is strictly narrower than
the `GITHUB_TOKEN` the job already holds. If you would rather hold the line
absolutely, the alternative is to stop pushing prints to `main` and land
them on a `prints` branch instead — cleaner cryptographically, but it
splits the archive hash chain, which contradicts B-uc4-08.

---

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
