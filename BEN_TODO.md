# Ben's action list — everything that is YOURS to do

*(Fully rewritten 2026-09-04 evening. All code for all three tiers is
finished; the index prints, signs, and verifies itself weekly. What
remains: your bookings, clicks, decisions, readings, and conversations.
Shareable page version: the "Saeculum Launch Duties" artifact.)*

## This week — the four bookings (the whole critical path; fire in parallel)

### 1. Form the Wyoming entity (FIRST — everything attaches to it) — ~$500–1k, 1–2h + EIN wait
- Pick a registered-agent service (compare Northwest Registered Agent,
  Wyoming Registered Agent; ~$50–125/yr). They file the Articles
  (state fee ~$100, same-day online). Name idea: Saeculum Foundation LLC.
- EIN immediately after: non-US owner files IRS SS-4 by fax/phone
  (1–4 weeks — the slow leg, start day one).
- Tell me when formed → I draft the operating agreement for counsel.
- Ongoing: IRS 5472 annually (~$500/yr preparer).
- Unblocks: trademark applicant, counsel client, deployer identity.

### 2. Book the reviewing attorney — ~$3–8k, 2–4 wk turnaround
- US crypto/securities attorney (flat-fee boutiques exist; ask any
  founder you know for their referral).
- Send `docs/legal/drafts/US_MEMO_PACK.md` framed as: "four drafted
  memos for REVIEW-AND-SIGNATURE, not drafting; US-only offering,
  EU/UK geo-restricted; fixed-fee quote please."
- Insist Memo C is answered (German residence + §23 EStG founder-token
  tax — the one question geo-restriction does not remove). If they
  can't do German tax, add a one-hour Steuerberater consult.
- The only genuinely reckless thing to skip. The signature is the product.

### 3. Book the USPTO trademark filer — ~$1.1–2k all-in, after the entity
- Flat-fee US trademark service ($300–1k; required — 37 CFR 2.11(a)
  makes a US attorney mandatory for foreign-domiciled applicants).
- Hand them `docs/legal/drafts/USPTO_TRADEMARK_DRAFT.md` (SAECULUM,
  classes 9/36/42, wording done). Applicant = the entity. Fees ~$750–1,050 on top.
- EUIPO deferred by your ruling (accepted risk: EU squatters until expansion).

### 4. Book the solo contract auditor — ~$3–8k, 1–2 wk engagement
- One strong solo senior auditor (Cantina/Spearbit marketplaces, or a
  well-reviewed independent). Scope is tiny: 2 contracts, ~160 lines.
- Send the repo + `docs/audit/SECURITY_PROPERTIES.md` +
  `docs/audit/SLITHER_REPORT.md` (that pair IS the brief; fuzz suite
  11/11, parity model, Slither triaged to zero unaccepted).
- Ask for: attacks on the five stated properties, oracle-compromise
  blast radius, supply-extreme edge cases.
- Mainnet is hard-gated on this in the runbook. (My own first contract
  draft had a real minting bug the property tests caught — that's why
  this line never goes to zero.)

## This week — the two clicks

### 5. Zenodo token — free, 2 min
- zenodo.org → avatar → Applications → Personal access tokens → New →
  scopes `deposit:write` + `deposit:actions`.
- Terminal (never paste the token into chat):
  `gh secret set ZENODO_TOKEN --repo chronon-index/chronon-index`
- Unblocks the quarterly DOI deposits (workflow live, currently NOOPs;
  your ORCID 0009-0004-6118-8665 already in the metadata).

### 6. Attach the domain — free, 5 min
- Cloudflare → Workers & Pages → chronon-index → Custom domains → add
  `saeculum.foundation`; add the CNAME it shows in GoDaddy DNS (or
  move nameservers to Cloudflare — cleaner).
- Tell me when it resolves → I update every committed URL, re-verify
  the API rows on the new domain, plan the repo/org rename.

## Decisions only you can rule (say yes/no/otherwise; I execute)

- **D1 Launch chain:** mainnet vs L2. Rec: **Base**; let counsel see it.
- **D2 Distribution:** how people get SAEC at launch — must be settled
  BEFORE the attorney finishes (it shapes Howey). Rec: **no public
  sale** — deploy, small entity-seeded LP, airdrop slice to
  attestors/recomputers as work compensation, disclose everything.
- **D3 Founder allocation + lock:** COI statement promises day-one
  disclosure. Rec: modest single-digit %, 2–4yr on-chain vest.
- **D4 Testnet attestor keys:** generate 3 keys you control (runbook
  shows where); real attestors replace them in February.
- **D5 Counsel timing:** your schedule said January; drafts are done
  now. Rec: **pull forward** — it's the longest external clock.
- **D6 EUIPO expansion timing:** revisit when the US registration publishes.

## January
- Counsel signature lands (if D5 stays January).
- ACLED: contact form, ask small-commercial/startup tier (attribution
  layer only — deferring again is fine). EM-DAT: free research tier;
  commercial = ask CRED.
- Trademark filing completes via the filer.

## February — the credibility milestone
- Send the drafted recomputer outreach email (repo + your
  chronon-unblock.zip) to 2–3 targets: MPIDR Rostock, a university
  demography department, DAV/SOA actuarial student chapters.
- Their weekly job is one command. When two say yes → tell me → I wire
  attestor onboarding; the N-of-M oracle set becomes real.
- While talking to them: note 1–2 possible oversight-committee names
  (IOSCO Principle 5 — only humans fill it).

## Reading list (yours alone; gates whitepaper §§1/4/6)
- Preston/Keyfitz/Wachter — the math behind e(x).
- Vaupel 2009 "Life lived and left" — gates §1.
- Blake et al. "The New Life Market" + LifeMetrics docs — gates §4
  (the perfect-math-no-demand postmortem).
- Becker 1965 — gates §6.
- IOSCO/BMR summaries — so governance conversations are yours.

## The demand conversations (worth more than any code)
2–3 informal chats: a pension fund (structurally short longevity), a
life insurer (natural opposite side), a macro-minded crypto fund. One
question, not a pitch: "If a clean, manipulation-resistant index of
humanity's remaining life-years existed, would you ever hedge or take
exposure on it — and what would it need first?"

## Standing rules — NEVER do these
- **Never create a GitHub release** on the repo (Zenodo toggle stays
  OFF; a release would deposit license-restricted WHO files under a
  permanent DOI). Deposits go through the curated workflow only.
- **Never push directly to main** (branch protection: signed + PR + checks).
- **Never delete** the deploy key, PRINT_BOT_DEPLOY_KEY, or the
  signing key (~/.ssh/tly_signing_ed25519). Rotate fine; delete never.
- **Keep `chronon-restore-A16 (1).zip` archived safely** — the
  provenance record; never secret, never lost again.

## Money, complete
| Item | Amount | When |
|---|---|---|
| Attorney review-and-sign | $3–8k | on booking |
| USPTO filing + flat-fee attorney | $1.1–2k | after entity |
| Wyoming entity | $0.5–1k | this week |
| Solo contract audit | $3–8k | pre-mainnet |
| **Total to launch** | **≈ $8–18k** | |
| Ongoing (agent + 5472 preparer + domains) | ≈ $650/yr | annual |
| Infrastructure | $0 | forever |

## What happens with zero action from you
Every Monday: pulls → print → hash chain → Bitcoin timestamp → Rekor
signature → site/API update → full historical re-verification. Monthly
digest writes itself; quarterly deposit fires once #5 is done. I verify
the first v0.7.0 print this Monday (S → 363.5117B, Ē → 44.9238).
