# US regulatory memo pack — DRAFT FOR COUNSEL REVIEW (S-09)

> STATUS: AI-drafted 2026-09-04 for attorney review-and-signature. Not
> legal advice; nothing here is in force until a licensed attorney has
> reviewed, corrected, and signed. Regulatory facts reflect knowledge
> through early 2026 and are flagged (verify) — the reviewer updates
> them. **Scoping ruling (Ben, 2026-09-04): US-only offering; EU/UK/
> other jurisdictions geo-restricted at launch** — this pack therefore
> contains no MiCA analysis (see Memo C for the one EU question that
> survives geo-restriction).

---

## Memo A — Howey analysis of the SAECULUM token

**Question:** is SAEC an "investment contract" under *SEC v. W.J. Howey
Co.*, 328 U.S. 293 (1946)?

**Facts counsel can verify mechanically:** supply algorithmically
mirrors a published demographic index (S = humanity's remaining
life-years) computed by public CI from UN/national-statistics data;
weekly rebases carry the archive record hash; no staking, no yield, no
dividends, no buybacks; the computation, code, and governance are
public and independently recomputable; holder share of supply is
invariant by construction.

**Factor 1 — investment of money:** likely satisfied on any sale for
value. Concede.

**Factor 2 — common enterprise:** horizontal commonality arguably
present (all holders' fortunes move with one index). Concede arguendo.

**Factor 3 — expectation of profits:** contestable. The asset's value
proposition is *denomination in time* (a unit-of-account/store-of-value
claim), not profit. Supply growth (~+0.4–0.8%/yr) dilutes no one
(share invariance) and enriches no one; there is no cash flow. Analogy:
closer to a commodity or collectible index exposure than to equity.
Counterpoint counsel must weigh: any tradable asset invites price-
appreciation expectation; marketing discipline (below) is load-bearing.

**Factor 4 — from the efforts of others:** the strongest defense
factor. Post-launch, the number that drives supply is produced by the
UN Population Division and national statistical agencies, not by the
promoter; the pipeline is deterministic, open-source, and
independently recomputed (outsider-sim weekly; external recomputers at
P5). The founder cannot improve the index by effort — the manipulation
paper (docs/reports/MANIPULATION_ECONOMICS.md) quantifies that even
data fabrication moves it by parts-per-million. Compare the SEC
framework's "Active Participant" analysis (2019 Digital Asset
Framework (verify current status)): the essential managerial efforts
here are those of *statistical agencies*, which no reasonable buyer
relies on as a profit-seeking enterprise.

**Draft conclusion for review:** a credible position exists that SAEC
is not a security under Howey, resting on factors 3–4; the position is
strongest if (a) no yield/staking is ever offered, (b) marketing never
promises appreciation, (c) launch follows full decentralization of the
oracle (N-of-M attestors), and (d) the founder's holdings are
disclosed and vesting-locked. Counsel to opine on residual risk and on
whether a no-action posture, Reg D/Reg S structuring, or a CFTC-side
classification (Memo B) is the sound path.

---

## Memo B — the 2025-26 US statutory landscape

(All items (verify) — this moved fast and my knowledge ends early 2026.)

- **GENIUS Act (2025, enacted):** stablecoin regime. SAEC is NOT a
  stablecoin (no fiat peg, no redemption promise) — confirm the
  definitional carve-out language does not accidentally capture
  index-pegged rebasing assets.
- **CLARITY Act (House-passed 2025; Senate status (verify)):** would
  route "digital commodities" to CFTC jurisdiction with a
  decentralization pathway. SAEC's profile (functional network,
  no issuer control over the index, open computation) appears to fit
  the digital-commodity lane; counsel to map the certification/
  disclosure requirements if enacted.
- **SEC posture:** enforcement retreat + Project Crypto rulemaking
  (verify current state). The relevant question is whether a
  registration-exempt public distribution (fair launch, no ICO) is
  now viable, and what disclosure package makes it defensible.

---

## Memo C — the operator-residence question (the one EU issue that
survives geo-restriction)

Ben is a German resident operating the index from Germany. Even with a
US-only token offering: (a) does operating/publishing the INDEX from
Germany trigger any BaFin/EU regime (benchmark regulation applies to
EU-supervised-entity USE of a benchmark, not to publication as such —
(verify BMR scope for non-EU-used benchmarks)); (b) does German law
attribute the US entity's activity to the German-resident founder
(reverse-solicitation and marketing rules); (c) personal tax treatment
of founder tokens under German law (§23 EStG one-year rule vs business
income — this one has real money attached). **This memo is why
"US-only" does not reduce counsel scope to zero.**

---

## Memo D — entity and structure recommendation (for confirmation)

Wyoming LLC (or DUNA if genuine member-governance is wanted) as the
launch entity: ~$100–500 filing + registered agent; foreign-owned
single-member LLC needs an EIN and annual IRS 5472 (~$500/yr
preparer). The entity holds the IP, operates the site, publishes the
index, and (post-audit) deploys the contract. Escalation path: if
CLARITY-style registration materializes, a purpose-built entity
succeeds it (the P5 administrator-entity plan). Counsel to confirm
Wyoming vs Delaware and the Germany-US treaty/PE implications of a
German-resident managing member.

---

## Geo-restriction implementation (so the US-only claim is true)

Terms of use restricted to US persons; IP-based geoblocking of the
token app for EU/UK; no marketing directed at the EU; attestation at
any sale interface. The INDEX (the website/data) stays world-readable
— it is publication, not an offering. Counsel to confirm this split.
