from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMUNITY_NOTES = ROOT / "data" / "community_notes.json"
HOSPITALS = ROOT / "app" / "hospitals.json"


def test_rio_paranaiba_note_is_dated_and_conservative():
    notes = json.loads(COMMUNITY_NOTES.read_text(encoding="utf-8"))["notes"]
    note = notes["2184680"][0]

    assert note["category"] == "other"
    assert note["reported_at"] == "2026-10-16"
    assert "não atende acidentes com animais peçonhentos" in note["public_summary"]
    assert "não confirmada oficialmente" in note["public_summary"]
    assert "(34) 3855-1228" in note["public_summary"]


def test_rio_paranaiba_generated_record_keeps_official_fields_and_adds_note():
    hospitals = json.loads(HOSPITALS.read_text(encoding="utf-8"))
    hospital = next(h for h in hospitals if h.get("cnes") == "2184680")

    assert hospital["hospital_name"] == (
        "Hospital Municipal Dona Maria Conceição Frantino Valério"
    )
    assert hospital["address"] == "Av. Trajano José Da Silva, 98"
    assert hospital["phones"] == ["(34) 3855-1228"]
    assert hospital["antivenoms"] == ["Escorpiônico"]
    assert hospital["community_notes"] == [
        {
            "category": "other",
            "reported_at": "2026-10-16",
            "public_summary": (
                "Em contato telefônico, foi informado que esta unidade não atende "
                "acidentes com animais peçonhentos. Informação ainda não confirmada "
                "oficialmente. Ligue e confirme o atendimento antes de se deslocar: "
                "(34) 3855-1228."
            ),
        }
    ]
