# Saeculum contract — security properties (S-10 audit brief)

For the engaged auditor: everything here is executable before you start.
Scope is deliberately tiny — 106 lines, one privileged function, no
composability, no callbacks, no upgradeability.

## The three artifacts (a divergence between any two is a finding)

1. `contracts/Saeculum.sol` — the contract.
2. `tly/token_model.py` — the NORMATIVE Python model (uint-semantics).
3. `contracts/test/Saeculum.t.sol` — the Foundry suite: fuzzed
   properties + a byte-exact parity vector against the model
   (`forge test`, 2000 fuzz runs, all green at commit time).

## Properties (proven by fuzz; please attack them)

| id | property | test |
|---|---|---|
| P-share | rebase changes no wallet's share of TOTAL_GONS | `testFuzz_ShareInvarianceUnderRebase` |
| P-path | any rebase path to the same S yields identical balances | `testFuzz_PathIndependence` |
| P-conserve | transfers never mint; Σ balances ≤ totalSupply always | `testFuzz_TransferNeverMints` |
| P-settle | epochs strictly increase; replay/reorder/non-oracle revert | `test_FirstPrintSettlesOnChain` |
| P-parity | contract == Python model on op sequences | `test_ParityWithNormativeModel` |

## Known design decisions (reviewed, intentional)

- **Multiply-then-divide balances** (`gons * supply / TOTAL_GONS`), not
  a stored gons-per-fragment: the floored-gpf form violates P-conserve
  (our own property tests caught Σ balances exceeding supply by ~26
  tokens — the known AMPL caveat). No overflow: product < 1e51 ≪ 2^256.
- **Transfers ceil the gon debit** — the sender absorbs rounding dust.
- **Oracle is a single address pre-P6** — rotates to an N-of-M attestor
  contract before launch; the rebase carries the archive `record_hash`
  so every supply change is publicly tied to the print chain.
- **No mint/burn functions exist.** Supply changes ONLY via rebase.

## Asks

Beyond the properties: reentrancy surface (none expected — no external
calls), approval race (standard ERC-20 caveat, documented), oracle-key
compromise blast radius (bounded by monotonic epochs + public hash —
a bad rebase is detectable by anyone within seconds), and anything the
fuzzer's distribution misses at supply extremes.
