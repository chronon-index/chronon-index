# Testnet deployment runbook (pre-audit, testnet ONLY)

Deploys the Saeculum token + N-of-M oracle to Sepolia. Mainnet is
GATED on: audit closed, counsel sign-off, attestor set real (E-14).

## One-time

1. A funded Sepolia key (faucet ETH suffices). NEVER a key holding
   real value; NEVER committed — exported in the shell only.
2. An RPC URL (any public Sepolia endpoint).

## Deploy

```bash
export SAEC_INITIAL_SUPPLY=$(python3 - <<'PY'
import json, pathlib
chain = json.loads(pathlib.Path("archive/chain.json").read_text())
rec = json.loads(pathlib.Path("archive", chain[-1]["file"]).read_text())
from decimal import Decimal
print(int(Decimal(rec["s_life_years"]) * 10**9))  # 1e-9 LY quanta
PY
)
export SAEC_ATTESTORS=0x...,0x...,0x...   # 3 test keys you control
export SAEC_THRESHOLD=2
forge script contracts/script/Deploy.s.sol \
  --rpc-url "$SEPOLIA_RPC" --private-key "$DEPLOY_KEY" --broadcast
```

The initial supply is the LAST ARCHIVED PRINT — the chain starts where
the paper record stands, and the first on-chain rebase is the next
epoch's attested print.

## Weekly rebase feed (testnet rehearsal of the real flow)

Each attestor key runs, after Monday's print lands:
```bash
python -m tly.attest_feed   # prints (epoch, supply, record_hash) from the archive
cast send $ORACLE "attest(uint64,uint256,bytes32)" <epoch> <supply> <hash> \
  --rpc-url "$SEPOLIA_RPC" --private-key "$ATTESTOR_KEY"
```
Two agreeing attestations settle the epoch; watch the `Settled` event.
