from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_HTML = ROOT / "app" / "index.html"


def app_html() -> str:
    return APP_HTML.read_text(encoding="utf-8")


def test_critical_categories_render_as_critical_alerts():
    html = app_html()

    for category in ("closed", "wrong_unit", "pin_fix"):
        assert f"categories.indexOf('{category}')" in html
    assert "severity: 'critical'" in html
    assert 'role="note" aria-label="Alerta da comunidade"' in html


def test_community_alert_precedes_directions_and_actions():
    html = app_html()
    card_render = html[html.index("function renderCard(") : html.index("// ===== RENDER LIST =====")]

    alert_position = card_render.index("renderHospitalAlerts(h, reportUrl)")
    map_position = card_render.index("mapBlockHtml +")
    actions_position = card_render.index("'<div class=\"actions\">'")

    assert alert_position < map_position < actions_position


def test_community_alert_precedes_map_popup_phone_and_directions():
    html = app_html()
    map_render = html[html.index("function renderMap()") : html.index("// ===== EVENT HANDLERS =====")]

    alert_position = map_render.index("renderHospitalAlerts(h, reportFormUrl(h))")
    phone_position = map_render.index("phonesHtml ? phonesHtml")
    directions_position = map_render.index("www.google.com/maps/dir/")

    assert alert_position < phone_position < directions_position


def test_alert_heading_uses_valid_block_structure():
    html = app_html()

    assert '<div><span class="community-alert-eyebrow">' in html
    assert '<h4 class="community-alert-title">' in html
    assert '<span><span class="community-alert-eyebrow">' not in html


def test_alert_copy_avoids_stale_report_counts_and_keeps_safety_guidance():
    html = app_html()

    assert "formatCommunitySummary" in html
    assert r"^relatos? da comunidade(?: \(\d+ relatos?\))?:\s*" in html
    assert "Antes de ir:" in html
    assert "ligue 192 ou 193" in html
    assert "n&atilde;o confirmado pelo Minist&eacute;rio da Sa&uacute;de" in html
    assert "A situa&ccedil;&atilde;o mudou? Avise o SoroJ&aacute;" in html


def test_legacy_community_notes_use_the_same_always_visible_alert():
    html = app_html()

    assert "function isLegacyCommunityNote(note)" in html
    assert "function communityNotesForHospital(h)" in html
    assert "renderHospitalAlerts(h, reportUrl)" in html
    assert "renderHospitalAlerts(h, reportFormUrl(h))" in html
    assert "if (!note || isLegacyCommunityNote(note)) return '';" in html
    assert '<details class="community-alert' not in html
    assert '<summary class="community-alert' not in html
