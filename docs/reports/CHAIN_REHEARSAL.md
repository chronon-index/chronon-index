# On-chain settlement rehearsal — real inputs, local EVM (2026-10-03)

*The first end-to-end execution of the launch stack as a single job:
deploy → attest → settle, fed by the real archive, on a local Ethereum
node (anvil, public dev accounts — no secrets touched). Sepolia differs
only by network transport; contract execution is identical bytecode.*

## What ran

1. **Deploy** via `contracts/script/Deploy.s.sol`: initial supply =
   the archived 2026-09-21 print (363511706093960100000 quanta);
   3 attestors, threshold 2. Nonce-prediction held: the token's
   constructor-pinned oracle address equals the deployed oracle
   (`oracle() = 0xe7f1…0512`).
2. **Attestation 1 of 2** (tx `0xb678…bd1a`): one `Attested` log,
   **no settlement** — `lastEpoch` still 0. A single attestor cannot
   move the supply.
3. **Attestation 2 of 2** (tx `0x4a60…28da`): three logs
   (`Attested` + `Rebase` + `Settled`). On-chain state after:
   - `lastEpoch = 1790596800` (= 2026-09-28T12:00:00Z, the real epoch)
   - `lastRecordHash = 0x9e4567a1ac56363c64976945ab8d87c3f2f5bf3ac4e9d62cd921601fe70f3285`
     — byte-equal to `archive/chain.json`'s record_hash for that epoch:
     anyone on-chain can tie the supply to the public print.
   - `totalSupply` = the attested S in quanta (equal to the prior week's
     — S is genuinely flat between structure updates; the rehearsal
     reports reality, not a staged delta).

## What this proves / what it does not

Proves: the deploy script, the circular token↔oracle wiring, the
threshold gate, idempotent-epoch finality, and the public-auditability
chain (on-chain hash == archive hash) all work as one job on real data.
Does not prove: public-network behavior (gas market, reorg handling) —
that is the Sepolia pass, which needs a faucet-funded key (a 5-minute
Ben step, card available) and real attestor keys (dashboard task D4).
