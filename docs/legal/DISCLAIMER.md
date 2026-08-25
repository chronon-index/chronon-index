# Disclaimer — DRAFT for counsel review (D-15)

> STATUS: DRAFT. Not reviewed by counsel (D-13 pending). Wording below
> is the project's honest self-description for counsel to harden.

**Research series.** Every value published by this project is a
research-mode statistical estimate produced by public CI from published
official statistics. No token exists. No value printed here settles any
obligation. The commercial licensing gate (`tly/licensing_gate.py`)
structurally blocks commercial-use paths pending the source-of-record
switch and ratification (A-16/G5).

**Not advice.** Nothing here is investment, financial, actuarial,
medical, legal, or tax advice. The maintainers are not licensed
advisors. Do not make financial decisions based on this series.

**Estimates, with published error.** Every print carries a computed
accuracy statement: a symmetric measurement interval (quadrature over
stated terms) and one-sided structural terms, listed and never netted
(`tly/error_budget.py`). The cohort series is model content
(projected mortality) and is labeled INFORMATIONAL — it can never touch
settlement. The COVID replay (`docs/reports/COVID_REPLAY.md`)
quantifies real-time error honestly: at a shock's edge an estimate can
be wrong in sign. Users who ignore the published uncertainty are
misusing the series.

**Immutability, not infallibility.** Prints are immutable once archived
(first-print-settles). Discovered errors are recorded and corrected
forward-only in the public ledger (`ledger/CORRECTIONS.md`); the
archived past is never rewritten. An archived value being immutable
does not mean it was right.

**Demographic aggregates only.** The index measures populations, never
individuals. No value here says anything about any person's life
expectancy or any individual's mortality.

**Third-party data.** Input data comes from official statistical
agencies under their own terms; errors in upstream sources propagate to
prints and are handled by the vintage/correction machinery, not hidden.
