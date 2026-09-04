# Ben's action list — rewritten 2026-09-05

*(Changes from the 09-04 version: recomputer outreach and demand
conversations REMOVED from the pre-launch path by your ruling — they
move to "after launch + traction." Entity naming corrected: Wyoming
prohibits "Foundation" in an LLC name (W.S. 17-29-108, flagged by the
operating-agreement draft). Every duty is now written as a runbook for
your Claude-in-Chrome agent: steps marked **[AGENT]** it can do;
**[YOU]** are the steps browser agents are barred from — creating
accounts, entering payments/credentials, final submissions.)*

Consequence of the outreach deferral, stated once: launch runs with an
oracle attestor set YOU control (3 keys). That is a centralized oracle
at launch — disclosed in the risk factors, not hidden — and
decentralization (real attestors) becomes a post-traction milestone.

---

## Duty 1 — Wyoming entity (~$500–1k · do first, everything attaches to it)

**Name ruling needed first:** NOT "Saeculum Foundation LLC" — Wyoming
bars "Foundation" for LLCs, and counsel-bait besides. Pick one:
**Saeculum Labs LLC** / **Saeculum Time LLC** / **Saeculum Index LLC**.

Runbook (registered-agent route, Northwest as the example):
1. [AGENT] Open northwestregisteredagent.com → "Start an LLC" →
   Wyoming. Fill: company name (your pick above), your name + German
   address as member. STOP at account creation.
2. [YOU] Create the account, enter payment (~$39 + $100 state fee +
   ~$125/yr agent), submit. Same-day approval is normal.
3. [AGENT] When the confirmation email lands: download the stamped
   Articles + note the filing date; report back the exact legal name
   and date.
4. [YOU] EIN — the slow leg, start same day: IRS form SS-4 by fax
   (+1-855-215-1627 from abroad) or phone (+1-267-941-1099). The agent
   can prefill the SS-4 PDF; you sign and fax (e.g. via an online fax
   service — account = [YOU]). 1–4 weeks.
5. Tell me the entity name + date → I finalize
   `docs/legal/drafts/OPERATING_AGREEMENT_DRAFT.md` (already in the
   repo — it is deliberately full of [CLASSIFICATION-SENSITIVE] marks:
   **do not sign it before the Steuerberater question in Duty 2 is
   answered; the five marked clauses decide your German tax outcome**).

## Duty 2 — attorney review (~$3–8k · the irreducible one)

Not an email campaign — one engagement, bookable via web intake forms:
1. [AGENT] Open the intake/contact pages of 2–3 flat-fee crypto-law
   shops (search "token launch legal opinion flat fee"); extract
   pricing/scope into a comparison; prefill intake forms with: US-only
   token launch, four AI-drafted memos need review-and-signature not
   drafting, fixed-fee quote requested; the launch oracle is a founder-controlled
   3-key set (disclosed) — include it explicitly in the Howey
   managerial-efforts analysis. STOP before submitting.
2. [YOU] Pick one, hit submit, take the intro call. Send them
   `docs/legal/drafts/US_MEMO_PACK.md` from the repo.
3. [YOU] On the call, insist on two things: Memo C gets a real answer
   (German-resident operator + §23 EStG founder-token tax — if they
   can't do German tax, book one hour with a German Steuerberater for
   that half), and their answer to the Duty-1 classification question
   (which LLC clauses to elect) goes to whoever finalizes the
   operating agreement.

## Duty 3 — USPTO trademark (~$1–2.1k · 2 classes · after the entity exists)

1. [AGENT] Open 2–3 flat-fee US trademark services; extract pricing;
   prefill: mark SAECULUM, **classes 9 and 42 ONLY** (§1(b)) — Class 36
   is HELD: `SAECULA WEALTH` ser. 99428273 is live-pending there with an
   unresolved SOU action (agent finding 2026-09-05; if the SOU fails,
   36 files clean later; if it registers, attorney assesses first).
   Applicant = the new entity; US attorney required (37 CFR 2.11(a));
   prefer ID-Manual wording (free-form ~$550/class vs ~$350). Attach
   `docs/legal/drafts/USPTO_TRADEMARK_DRAFT.md`. STOP before payment.
2. [YOU] Pay and submit with your pick. They handle the office actions.

## Duty 4 — contract audit (~$3–8k · gates mainnet)

1. [AGENT] Open cantina.xyz and spearbit.com (and 1–2 well-reviewed
   solo auditors' sites); extract engagement models + indicative
   pricing for a ~160-line 2-contract scope; prefill request forms:
   repo link, `docs/audit/SECURITY_PROPERTIES.md` +
   `docs/audit/SLITHER_REPORT.md` as the brief, asks = attack the five
   properties, oracle-compromise blast radius, supply extremes. STOP
   before submitting.
2. [YOU] Pick, submit, sign the engagement. Findings come to me; I fix
   and re-run everything.

## Duty 5 — Zenodo token (free · 2 min · entirely [YOU])

Credential creation — agents are barred, and rightly:
1. zenodo.org → avatar → Applications → Personal access tokens → New →
   scopes `deposit:write` + `deposit:actions`.
2. Terminal: `gh secret set ZENODO_TOKEN --repo chronon-index/chronon-index`
   → paste at the prompt (never into chat). Quarterly DOI deposits arm
   themselves; your ORCID 0009-0004-6118-8665 is already in the metadata.

## Duty 6 — attach the domain (free · 5 min)

1. [AGENT] Cloudflare dash → Workers & Pages → chronon-index → Custom
   domains → Add → `saeculum.foundation` → read out the CNAME target
   it displays. STOP (DNS change = settings change).
2. [YOU] Approve; [AGENT with your ok] add that CNAME in GoDaddy DNS
   for saeculum.foundation.
3. Tell me when it resolves → I update every committed URL, re-verify
   the API rows on the new domain, plan the repo/org rename.

## Decisions still open (one-word answers move them)

- **D-name:** Labs / Time / Index LLC (see Duty 1).
- **D1 chain:** rec **Base**; counsel sees it before final.
- **D2 distribution:** must precede the attorney's signature. Rec: no
  public sale — deploy, small entity-seeded LP, disclose everything.
  (Attestor airdrop leg is deferred with the outreach ruling.)
- **D3 founder allocation + on-chain vest:** rec single-digit %, 2–4yr.
- **D4 testnet keys:** 3 keys you generate; runbook shows where.
- **D5 counsel timing:** rec pull forward from January (longest clock).

## January (unchanged)
- Counsel signature lands (if D5 stays January) · ACLED + EM-DAT
  license contacts (attribution layer only; deferring again is fine) ·
  trademark filing completes · EUIPO expansion decision.

## Moved to AFTER launch + traction (your ruling, 2026-09-05)
- Recomputer outreach (E-14) — with it, the real attestor set, the
  "independently verified" claim, and the stochastic methodology bump.
- Oversight-committee name-gathering.
- Demand conversations (pension funds / insurers).

## Reading list (unchanged; gates whitepaper §§1/4/6)
Preston/Keyfitz/Wachter · Vaupel 2009 · Blake et al. + LifeMetrics
docs · Becker 1965 · IOSCO/BMR summaries.

## Standing rules — NEVER
- No GitHub releases on the repo (Zenodo toggle stays OFF — a release
  would deposit license-restricted WHO files under a permanent DOI).
- No direct pushes to main (signed + PR + checks).
- Never delete the deploy key, PRINT_BOT_DEPLOY_KEY, or
  ~/.ssh/tly_signing_ed25519. Rotate fine; delete never.
- Keep `chronon-restore-A16 (1).zip` archived safely, forever.

## Money (unchanged)
Attorney $3–8k · USPTO $1.1–2k · entity $0.5–1k · audit $3–8k →
**≈ $8–18k to launch**; ~$650/yr ongoing; infrastructure $0.

## Zero-action baseline
Mondays: pull → print → chain → Bitcoin stamp → Rekor signature → site/
API → full historical re-verification. Monthly digest; quarterly DOI
once Duty 5 is done. I verify Monday's first v0.7.0 print
(S → 363.5117B, Ē → 44.9238).
