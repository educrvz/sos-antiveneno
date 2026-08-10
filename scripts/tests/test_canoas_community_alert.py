from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMUNITY_NOTES = ROOT / "data" / "community_notes.json"
HOSPITALS = ROOT / "app" / "hospitals.json"


def test_canoas_hps_keeps_structured_community_alert():
    notes = json.loads(COMMUNITY_NOTES.read_text(encoding="utf-8"))["notes"]
    canoas_notes = notes["3626245"]

    assert canoas_notes == [
        {
            "category": "closed",
            "reported_at": "2026-04-23",
            "public_summary": (
                "Relato da comunidade (2 relatos): confirmação de que o HPS "
                "continua fechado."
            ),
        }
    ]


def test_canoas_hps_generated_card_contains_new_alert_data():
    hospitals = json.loads(HOSPITALS.read_text(encoding="utf-8"))
    canoas = next(h for h in hospitals if h.get("cnes") == "3626245")

    assert canoas["community_notes"][0]["category"] == "closed"
    assert "2 relatos" in canoas["community_notes"][0]["public_summary"]
    assert canoas["note"].startswith("Informação oficial da SES-RS")
