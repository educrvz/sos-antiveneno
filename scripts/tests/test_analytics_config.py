from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLIC_PAGES = (
    ROOT / "app" / "index.html",
    ROOT / "app" / "privacy.html",
    ROOT / "app" / "terms.html",
)
GOATCOUNTER_TAG = (
    '<script data-goatcounter="https://soroja.goatcounter.com/count" '
    'async src="https://gc.zgo.at/count.js"></script>'
)


def test_public_pages_use_the_same_goatcounter_endpoint():
    for page in PUBLIC_PAGES:
        html = page.read_text(encoding="utf-8")
        assert html.count(GOATCOUNTER_TAG) == 1, page


def test_privacy_notices_disclose_goatcounter():
    for policy in (ROOT / "PRIVACY.md", ROOT / "app" / "privacy.html"):
        text = policy.read_text(encoding="utf-8")
        assert "GoatCounter" in text
        assert "localização GPS" in text
        assert "não usam cookies" in text
