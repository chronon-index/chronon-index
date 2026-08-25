"""CI print step (SPEC#4 AC-4.2; B-uc4-04): compute the current epoch's
print and append it to the committed archive hash chain. Idempotent — an
already-archived epoch is a clean no-op, so reruns never violate P4."""

from __future__ import annotations

import sys

from tly.archive import ArchiveImmutabilityError, PrintArchive
from tly.pipeline import REPO_ROOT, build_settlement_print, current_epoch


def _store_weekly_vintages() -> None:
    """B-uc2-17: every Monday run also stores that day's feed pulls in the
    append-only vintage store — building the lag triangle from now on.
    Fetch failure never blocks the print (the failure ladder owns that
    concern); a failed pull is simply an absent vintage for the date."""
    from datetime import datetime, timezone

    from tly.snapshot import fetch_url
    from tly.vintage_store import VintageStore

    store = VintageStore(REPO_ROOT / "data" / "vintages")
    today = datetime.now(timezone.utc).date()
    feeds = {
        "eurostat_weekly": (
            "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/"
            "data/demo_r_mwk_ts?format=JSON&sex=T&sinceTimePeriod=2024-W01"
        ),
        "cdc_weekly": (
            "https://data.cdc.gov/resource/r8kw-7aab.json?"
            "%24select=end_date,total_deaths,covid_19_deaths&"
            "%24where=%60group%60%3D%27By%20Week%27%20AND%20state%3D%27United%20States%27&"
            "%24order=end_date&%24limit=50000"
        ),
    }
    for feed, url in feeds.items():
        try:
            body = fetch_url(url)
            result = store.store_pull(feed, today, body, url)
            store.verify(feed)
            print(f"vintage {feed}/{today}: {'stored' if result['new'] else 'already stored'}")
        except Exception as err:  # noqa: BLE001 — never block the print
            print(f"vintage {feed}/{today}: pull failed ({err}) — absent vintage")


def main() -> int:
    _store_weekly_vintages()
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
