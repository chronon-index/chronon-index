# Becoming a SAECULUM attestor (post-launch program)

*Written 2026-09-09, activated when the outreach phase begins
(post-launch + traction, per the 2026-09-05 ruling). Until then the
oracle runs on a disclosed founder-controlled key set.*

An attestor independently recomputes each weekly print and attests the
result on-chain. Agreement of N attestors IS the settlement; your
divergence STALLS it — that power and that duty are the whole job.

## Weekly (one command + one transaction)

1. `git pull` the public repo; run the reproduction
   (`docs/REPRODUCE_FIXING.md`) — it recomputes every archived epoch
   from committed artifacts and diffs byte-for-byte.
2. Run `python -m tly.attest_feed` — it prints the (epoch, supply,
   record_hash) tuple your recomputation supports.
3. Submit `attest(epoch, supply, recordHash)` to the oracle contract
   from your registered key (a `cast send` one-liner; gas is cents on
   the launch L2).

If YOUR recomputation disagrees with the archive: attest what YOU
computed. A stalled epoch is the system working — the divergence gets
investigated in public, and you can replace your attestation until
threshold is reached (self-correction is a contract feature).

## What you attest to (and what you don't)

You attest that the published number follows from the recorded inputs
by the published method. You do NOT attest that upstream data is true
(sources revise; the vintage archive exists for that), and you carry
no liability for the index's value — see the reproduction doc §8.

## Onboarding

One key registration in the oracle's attestor set (a governed
handover-attested change), your entry in the public attestor registry,
and credit in the project documentation. Independence requirements: no
compensation tied to index level; your infrastructure, not ours.
