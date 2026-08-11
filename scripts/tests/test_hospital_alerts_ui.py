from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_HTML = ROOT / "app" / "index.html"


def app_html() -> str:
    return APP_HTML.read_text(encoding="utf-8")


def test_yellow_hospital_note_component_is_retired():
    html = app_html()

    assert ".card .hospital-note" not in html
    assert 'class="hospital-note"' not in html
    assert "community-alert-advisory" not in html
    assert "--community-advisory" not in html


def test_hospital_notes_render_as_red_official_alerts():
    html = app_html()

    assert "function renderHospitalAlerts(h, reportUrl)" in html
    assert 'class="community-alert community-alert-critical official-alert"' in html
    assert 'aria-label="Alerta oficial"' in html
    assert ">Alerta oficial</span>" in html
    assert "Orienta\\u00e7\\u00e3o da SES-RS" in html


def test_official_alert_replaces_duplicate_community_alert():
    html = app_html()
    start = html.index("function renderHospitalAlerts(h, reportUrl)")
    end = html.index("// ===== RENDER CARD =====", start)
    renderer = html[start:end]

    assert "if (officialAlert) return officialAlert;" in renderer
    assert "renderCommunityRelatos(communityNotesForHospital(h), reportUrl)" in renderer


def test_official_alert_is_full_width_before_actions():
    html = app_html()
    card_render = html[html.index("function renderCard(") : html.index("// ===== RENDER LIST =====")]

    header_end = card_render.index("'</div>' +\n            renderHospitalAlerts(h, reportUrl)")
    alert_position = card_render.index("renderHospitalAlerts(h, reportUrl)")
    actions_position = card_render.index("'<div class=\"actions\">'")

    assert header_end < alert_position < actions_position
