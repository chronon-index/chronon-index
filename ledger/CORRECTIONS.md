# Correction ledger — forward-only

First print settles (DECISIONS.md #7). No historical value is ever restated.
Every deviation between vintages, and every methodology error discovered
after publication, gets an entry here and is folded into the NEXT epoch.
Entries are append-only; editing or deleting an entry is forbidden.

Format:

```
## C-NNNN | <iso-date> | <scope>
- What was wrong, with the wrong value as printed
- What is right, with evidence (source URL + hash, or derivation)
- Forward treatment: which epoch absorbs it, and how
```

---

## C-0001 | 2026-08-16 | pre-genesis (no prints affected)
- The early napkin estimate of organic issuance was g = +2.9%/yr. It omitted
  the aging spend term and misused GBD YLL.
- Corrected by open recomputation to g = +0.7197%/yr from the identity
  dS/dt = B·e(0) − N + N·dĒ/dt (mint +9.6606B, spend −8.0917B, drift
  +1.0394B). Recorded in DECISIONS.md (Key numbers).
- Forward treatment: none needed — predates all prints. Logged for lineage
  because the openness rule caught it, and that is the point of the rule.
