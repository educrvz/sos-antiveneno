from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERCEL_CONFIG = ROOT / "vercel.json"


def load_headers() -> dict[str, str]:
    config = json.loads(VERCEL_CONFIG.read_text(encoding="utf-8"))
    header_sets = config["headers"]
    assert len(header_sets) == 1
    assert header_sets[0]["source"] == "/(.*)"
    return {item["key"]: item["value"] for item in header_sets[0]["headers"]}


def parse_csp(value: str) -> dict[str, list[str]]:
    directives: dict[str, list[str]] = {}
    for raw_directive in value.split(";"):
        raw_directive = raw_directive.strip()
        if not raw_directive:
            continue
        name, *tokens = raw_directive.split()
        directives[name] = tokens
    return directives


def test_security_headers_are_present_and_restrictive():
    headers = load_headers()

    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert headers["Strict-Transport-Security"] == (
        "max-age=63072000; includeSubDomains; preload"
    )
    assert headers["Permissions-Policy"] == (
        "geolocation=(self), camera=(), microphone=(), payment=()"
    )


def test_content_security_policy_keeps_static_app_boundaries():
    directives = parse_csp(load_headers()["Content-Security-Policy"])

    assert directives["default-src"] == ["'self'"]
    assert directives["frame-ancestors"] == ["'none'"]
    assert directives["base-uri"] == ["'self'"]
    assert directives["form-action"] == ["'self'"]


def test_content_security_policy_does_not_allow_wildcard_sources():
    directives = parse_csp(load_headers()["Content-Security-Policy"])

    for directive_name in ("connect-src", "script-src", "img-src"):
        assert all("*" not in source for source in directives[directive_name])
        assert "https:" not in directives[directive_name]


def test_inline_script_and_style_allowances_are_explicit_exceptions():
    directives = parse_csp(load_headers()["Content-Security-Policy"])

    # The app currently ships inline HTML, CSS, and JavaScript. Keep this
    # exception visible until the static shell is refactored to nonce or hash
    # based CSP.
    assert "'unsafe-inline'" in directives["style-src"]
    assert "'unsafe-inline'" in directives["script-src"]


def test_goatcounter_is_limited_to_its_script_and_collection_origins():
    directives = parse_csp(load_headers()["Content-Security-Policy"])

    assert "https://gc.zgo.at" in directives["script-src"]
    assert "https://gc.zgo.at" not in directives["connect-src"]
    assert "https://soroja.goatcounter.com/count" in directives["connect-src"]
    assert "https://soroja.goatcounter.com/count" not in directives["script-src"]
