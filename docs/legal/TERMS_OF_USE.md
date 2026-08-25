# Terms of Use — DRAFT for counsel review (D-15)

> STATUS: DRAFT. Not reviewed by counsel; jurisdiction and governing law
> are open (D-13: MiCA / SEC-Howey / FINMA-Cayman-UK analysis pending).
> Nothing here is in force until counsel signs off and a version is
> published at the site root.

## 1. What this project is

CHRONON/TLY is a **pre-launch research series**: a weekly, publicly
recomputable index of humanity's total remaining life-years, computed by
public CI from published official statistics. There is currently **no
token, no financial product, no settlement instrument, and no
administrator entity**. The repository, its archive, and its printed
values are research output.

## 2. License split — code vs. data vs. third-party inputs

- **Code** (`tly/`, `tests/`, workflows): [license to be fixed by
  counsel — working assumption MIT].
- **Printed values, archive chain, and derived fixtures**: free to use
  with attribution; reproduction and independent recomputation are the
  point (see `docs/REPRODUCE_FIXING.md`).
- **Third-party inputs remain under their own licenses.** In
  particular: WHO GHO and IHME materials are non-commercial and are
  used for triangulation only — they are excluded from this project's
  redistributions and deposits; the IOSCO Principles PDF is © IOSCO,
  snapshotted for governance mapping, not redistributed. Eurostat, CDC,
  ONS, WMD (MIT), and UN WPP inputs are used per their published terms,
  recorded per-source in `docs/LICENSING.md`.

## 3. No advice, no offer

Printed values are statistical estimates. Nothing published here is
investment, financial, actuarial, legal, or tax advice, nor an offer or
solicitation of any instrument, in any jurisdiction.

## 4. Accuracy and immutability semantics

Users must take the series with its stated semantics: first-print-
settles (P4) — prints are immutable once archived; errors are corrected
**forward-only** via the public correction ledger; every print carries
a computed accuracy statement and coverage share. Using a print while
ignoring its published error budget is use against its terms.

## 5. No warranty; limitation of liability

All output is provided "as is", without warranty of any kind. To the
maximum extent permitted by applicable law, the maintainers accept no
liability for losses arising from use of the series. [Counsel: standard
clauses + consumer-law carve-outs per chosen jurisdiction.]

## 6. Disputes about printed values

The dispute channel (48-hour log-only window, permanent record,
forward-only resolution — `tly/disputes.py`) is the exclusive route for
challenging a printed value. It never retroactively alters a print.

## 7. Changes

These terms will change (at minimum: entity formation, jurisdiction,
any future token event). Changes are versioned in git like everything
else in this project.
