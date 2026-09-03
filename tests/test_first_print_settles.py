"""C-uc7-03 / AC-7.2 / DEC#7: the fixing equals the first published print,
always; a later "better" value never replaces it."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.archive import ArchiveImmutabilityError, PrintArchive
from tly.fixings import FINAL, FixingValidationError, settle_from_archive
from tly.pipeline import build_settlement_print

REPO = Path(__file__).resolve().parent.parent
SNAPSHOTS = REPO / "data" / "snapshots"
EPOCH = "2026-08-17T12:00:00+00:00"

D = Decimal


def test_first_print_settles(tmp_path):
    """The real pipeline print is archived; the fixing MUST equal it —
    and a 'better' recomputation cannot enter the archive to change that."""
    archive = PrintArchive(tmp_path)
    first = build_settlement_print(EPOCH)
    archive.append(first)

    fixing = settle_from_archive(archive, EPOCH, SNAPSHOTS)
    assert fixing.status == FINAL
    assert fixing.value == first.s_life_years  # the fixing IS the first print
    assert fixing.methodology_version == first.provenance["methodology_version"]

    # a later "better" value cannot enter the archive for this epoch
    with pytest.raises(ArchiveImmutabilityError):
        archive.append(build_settlement_print(EPOCH))

    # settling again is byte-identical — no path to a different fixing
    again = settle_from_archive(archive, EPOCH, SNAPSHOTS)
    assert again.fixing_hash == fixing.fixing_hash
    assert again.render() == fixing.render()


def test_fixing_source_urls_are_real_manifest_urls(tmp_path):
    """URLs in the fixing resolve from the committed manifests — actual
    upstream endpoints, not placeholders."""
    archive = PrintArchive(tmp_path)
    archive.append(build_settlement_print(EPOCH))
    fixing = settle_from_archive(archive, EPOCH, SNAPSHOTS)
    assert fixing.source_urls  # non-empty
    assert all(u.startswith("https://") for u in fixing.source_urls)
    joined = " ".join(fixing.source_urls)
    # v0.7.0 consumed-files citation: WPP (source of record) + WMD
    assert "population.un.org" in joined
    assert "world_mortality" in joined
    # the demoted WHO source must NOT be cited by a v0.7.0 settlement
    assert "ghoapi.azureedge.net" not in joined


def test_fixing_cannot_precede_its_print(tmp_path):
    archive = PrintArchive(tmp_path)
    with pytest.raises(FixingValidationError, match="cannot .*precede|no archived print"):
        settle_from_archive(archive, EPOCH, SNAPSHOTS)
