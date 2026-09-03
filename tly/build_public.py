"""Build the committed publication surface (E-08; RP Part VII/XI).

``site/`` at the repo root IS the deployed artifact: rendered governance
pages (tly.site), the static JSON API emitted byte-verbatim from the
committed archive (tly.api.build_api_from_archive), and the Cloudflare
``_headers`` file. Building is deterministic — CI rebuilds after every
print and the suite asserts the committed tree matches a fresh build, so
the site can never drift from the artifacts it claims to render.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from tly.api import build_api_from_archive
from tly.site import REPO_ROOT, build_site, not_found_page

HEADERS = """\
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; img-src 'self'

/api/*
  Access-Control-Allow-Origin: *
  Cache-Control: public, max-age=300
"""


def build_public(repo_root: Path = REPO_ROOT) -> Path:
    out = repo_root / "site"
    if out.exists():
        shutil.rmtree(out)  # full rebuild: no stale files can survive
    build_site(repo_root, repo_root)  # writes <repo_root>/site/*.html
    build_api_from_archive(repo_root / "archive", out)
    (out / "404.html").write_text(not_found_page(), encoding="utf-8")
    (out / "_headers").write_text(HEADERS, encoding="utf-8")
    return out


if __name__ == "__main__":
    out = build_public()
    n = sum(1 for p in out.rglob("*") if p.is_file())
    print(f"site built: {n} files under {out}")
    sys.exit(0)
