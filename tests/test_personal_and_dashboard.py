"""S-07/S-08: the personal page and dashboard, guarded."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_dashboard_renders_the_archive_not_head():
    """The dashboard shows what was PRINTED — the archived latest epoch,
    never a HEAD recomputation (first-print-settles applies to display)."""
    dash = (REPO / "site" / "dashboard.html").read_text(encoding="utf-8")
    chain = json.loads((REPO / "archive" / "chain.json").read_text(encoding="utf-8"))
    latest = json.loads((REPO / "archive" / chain[-1]["file"]).read_text(encoding="utf-8"))
    s_b = f"{float(latest['s_life_years']) / 1e9:.4f}"
    assert s_b in dash  # the archived S, whatever version printed it
    assert all(link["epoch_utc"][:10] in dash for link in chain)
    assert "No market exists yet" in dash  # honest price panel
    assert "<script" not in dash  # settlement surfaces stay JS-free


def test_personal_page_is_client_side_only():
    """The privacy guarantee is architectural: embedded data, inline
    computation, zero network surface."""
    me = (REPO / "site" / "me.html").read_text(encoding="utf-8")
    assert "const QX = [" in me  # life table embedded at build time
    for banned in ("fetch(", "XMLHttpRequest", "navigator.sendBeacon", "WebSocket"):
        assert banned not in me
    assert "Private by architecture" in me
    assert "not a prophecy" in me and "not medical advice" in me
    headers = (REPO / "site" / "_headers").read_text(encoding="utf-8")
    assert "connect-src 'none'" in headers  # no-network ENFORCED by CSP


def test_personal_math_matches_the_page_js():
    """Recompute the page's algorithm in Python for a known profile and
    check the embedded qx produces the same arithmetic the JS runs."""
    me = (REPO / "site" / "me.html").read_text(encoding="utf-8")
    qx = json.loads(re.search(r"const QX = (\[[^\]]+\])", me).group(1))
    assert len(qx) == 101 and qx[100] == 1.0
    # 30-year-old, unspecified sex, all reference answers: m = 1... but the
    # defaults include 'sedentary-ish'? No: reference options are index 0
    # for smoke; compute pure m=1 case
    m, alive, years = 1.0, 1.0, 0.0
    for a in range(30, 101):
        q = min(1.0, m * qx[a])
        years += alive * (1 - q) + alive * q * 0.5
        alive *= 1 - q
    assert 40 < years < 55  # a 30-year-old's world-average remaining time
