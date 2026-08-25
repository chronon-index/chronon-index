# Privacy Statement — DRAFT for counsel review (D-15)

> STATUS: DRAFT. Not reviewed by counsel (D-13 pending). The factual
> claims below are verifiable against the repository; counsel to add
> jurisdiction-specific language (GDPR/UK-GDPR/CCPA as applicable).

## The pipeline processes no personal data

Every input to the computation is an **aggregate official statistic**:
death counts and population counts by age band, sex, week/month, and
country/region, as published by Eurostat, the US CDC/NCHS, the UK ONS,
the UN Population Division (WPP), and the World Mortality Dataset. No
input contains names, identifiers, individual records, or any attribute
of an identifiable person. This is checkable: every input file is
content-hashed in a committed manifest (`data/snapshots/*/manifest.json`)
and committed or archived in full.

This is a design rule, not an accident (RP Part XI: "no personal data
anywhere in the pipeline"). Any future source that carried
individual-level data would fail review before entering a manifest.

## The published site and API

The publication surface is **static files** (prints, archive chain,
reproduction docs). The project itself sets no cookies, runs no
analytics, and operates no accounts. [Counsel/ops note: the eventual
hosting provider (E-07, Cloudflare Pages or similar) collects standard
server logs under its own privacy policy — name the provider and link
its policy when hosting is chosen.]

## Git metadata

The public repository records standard git authorship metadata
(committer name/email) for contributors — the normal, expected
consequence of contributing to a public repository.

## Disputes and correspondence

The dispute log records what a disputant submits. Submissions become
part of a permanent public record — the dispute channel says so at the
point of submission. Do not include personal data beyond a contact
handle in a dispute.
