"""Print the attestation tuple for the newest archived epoch (the
testnet rebase feed's input; docs/DEPLOY_TESTNET.md). The tuple an
attestor SHOULD submit is exactly what the public archive says — an
attestor who recomputes and disagrees should submit their own numbers
and let the N-of-M stall surface the divergence."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    chain = json.loads((REPO_ROOT / "archive" / "chain.json").read_text(encoding="utf-8"))
    link = chain[-1]
    rec = json.loads((REPO_ROOT / "archive" / link["file"]).read_text(encoding="utf-8"))
    epoch_unix = int(datetime.fromisoformat(rec["epoch_utc"]).timestamp())
    supply = int(Decimal(rec["s_life_years"]) * 10**9)
    print(f"epoch:       {epoch_unix}  ({rec['epoch_utc']})")
    print(f"supply:      {supply}  (1e-9 life-years)")
    print(f"record_hash: 0x{link['record_hash']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
