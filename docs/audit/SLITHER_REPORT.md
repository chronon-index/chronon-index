# Slither static analysis — triage record (S-10 stack)

Run: slither (pipx, solc 0.8.24) over `contracts/`, forge-std/tests/
scripts filtered. Command:
`slither . --foundry-out-directory contracts/out --filter-paths "lib/|test/|script/"`

## History

- **Initial run (11 contract findings incl. lib noise, 4 scoped):**
  - `Saeculum.oracle should be immutable` — **reviewed and REJECTED,
    then redesigned**: immutability would freeze the attestor set
    forever. Resolution: `oracle` stays mutable behind a guarded
    `setOracle` that only the CURRENT oracle can call, and the N-of-M
    contract exposes `attestHandover` — succession itself requires
    threshold attestation. (This slither hint surfaced a real design
    gap; the fix added tests.)
  - `constructor lacks zero-check on oracle_` — **FIXED**: a zero
    oracle bricks rebases forever; `ZeroAddress` revert added.
  - `setOracle lacks zero-check` — **FIXED**, same guard.

- **Current run: 2 findings, both reviewed-benign:**
  - `reentrancy-events` in `attest` / `attestHandover` (event emitted
    after the external call): the callee is `token`, which is
    `immutable`, set at deployment to our own contract, and whose
    `rebase`/`setOracle` make no external calls — no reentrancy path
    exists. Reordering would put the event before the state change it
    reports. ACCEPTED; auditor asked to confirm.

Zero unaccepted findings at commit time. Re-run required on any
contract change (the auditor re-runs independently).
