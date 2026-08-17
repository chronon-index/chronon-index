# FAQ and one-pager

Status header (remove at launch): the project is pre-ratification
(loop/BACKLOG.md A-16) and pre-launch; no public prints exist yet. Every
numeric claim below is reproducible from this repo.

## One-pager

**TLY** measures humanity's total remaining time: S(t) = Σ over age, sex
and country of population × remaining life expectancy — about 362 billion
life-years on the v0 measurement (±~2%, see the error budget; the
best-estimate cohort figure is higher and published alongside, labeled).
**Mirror** is a monetary rule on that measurement: token supply M = κ·S,
so each CHRONON is a fixed fractional slice of humanity's remaining time.
Supply follows demography — glacially (+0.72%/yr organic; a COVID-scale
pandemic moves it under a tenth of a percent). Price floats; there is no
peg, no reserve, no defense. Every published figure is computed by open
code from keyless public data, hash-manifested, reproducible by anyone
(docs/REPRODUCE_FIXING.md), immutable once printed, and governed by
mechanical rules (versioned methodology, forward-only corrections,
log-only disputes). The rollout is layered: index → cash-settled
derivatives → token → (much later, behind explicit gates) per-person
issuance.

## "You are putting a price on human lives."

No — we are measuring time, and the pricing objection applies to
institutions that came long before us. Governments price life-years today,
in public, as a matter of settled policy: transport regulators publish a
Value of Statistical Life used to decide which safety rules are worth
their cost (US DOT guidance memos (verify current figure)); health systems
publish cost-per-QALY thresholds that decide which treatments are funded
(NICE (verify current threshold)). These numbers exist because the
alternative — pretending the trade-offs are not being made — produces
worse decisions in the dark. TLY prices nothing about any individual: it
measures an aggregate stock from published population statistics, with no
personal data anywhere in the pipeline. The index's own position is the
VSL/QALY position: if life-years are already being weighed, the weighing
should be open, methodical, versioned, and disputable — which is exactly
what this repository is. Opacity is worse. (Argument per RESEARCH_PROGRAM
Part V Q5; institutional specifics carry (verify) until the D9 sources are
fetched and read.)

## Questions

**Is this a stablecoin?** No. The formula governs supply only, never
price. There is no peg, hence no reserves and no reflexive defense to
attack (DECISIONS #5).

**What happens in a pandemic?** A symmetric down-rebase: every balance
shrinks by the same factor; nobody's share grows because part of humanity
died. This is machine-checked (mortality neutrality, test_e12_neutrality).
COVID-scale magnitude: −0.04% to −0.09% of supply.

**Who computes the number?** Open code in public CI; the computation IS
the publication. Anyone can re-run it byte-for-byte and compare fixing
hashes — see docs/REPRODUCE_FIXING.md. From P5, at least three
independent parties recompute every fixing.

**What if the data is wrong?** First print settles. Discovered errors go
to a public forward-only correction ledger and fold into the NEXT epoch;
history is never rewritten. Upstream revisions create new vintages beside
the old, never over them.

**What if I disagree with a fixing?** File a dispute within 48 hours —
it is logged forever, alters nothing, and delays nothing. Substantiated
disputes resolve through the correction ledger, forward.

**Is my personal data involved?** No. Individual-level data never enters
the pipeline — only published aggregates from statistical agencies. There
is nothing to leak.

**Does longevity progress dilute me?** No. Rebases are wealth-neutral:
your share of supply changes only when you transfer, and your wallet's
value is share × market cap regardless of any rebase path (machine-checked
share invariance).

**Why should I trust the methodology?** Don't trust it — check it. Every
policy is versioned; changing one without a version bump and changelog
entry fails the public build. The current methodology is a 2026
reconstruction of lost originals and says so on its face, pending
ratification.
