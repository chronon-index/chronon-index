"""CI print step (SPEC#4 AC-4.2; B-uc4-04): compute the current epoch's
print and append it to the committed archive hash chain. Idempotent — an
already-archived epoch is a clean no-op, so reruns never violate P4."""

from __future__ import annotations

import sys

from tly.archive import ArchiveImmutabilityError, PrintArchive
from tly.pipeline import REPO_ROOT, build_settlement_print, current_epoch


def main() -> int:
    epoch = current_epoch()
    archive = PrintArchive(REPO_ROOT / "archive")
    try:
        record_hash = archive.append(build_settlement_print(epoch))
    except ArchiveImmutabilityError as err:
        print(f"no-op: {err}")
        return 0
    archive.verify()
    print(f"archived epoch {epoch}: {record_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
