from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import apply_official_state_corrections as module  # noqa: E402
import pytest


FIELDS = [
    "row_id", "source_state_file", "source_state_abbr", "cnes",
    "health_unit_name", "address", "lat", "lng", "place_id",
    "geocode_attempted_at", "original_lat", "original_lng", "original_place_id",
]


def row(**values):
    return {**{field: "" for field in FIELDS}, **values}


def test_replace_add_update_are_idempotent():
    rows = [
        row(row_id="AL_0001", source_state_abbr="AL", cnes="1000001", health_unit_name="Old", address="A", lat="-9.1", lng="-37.1", place_id="stale"),
        row(row_id="AL_0002", source_state_abbr="AL", cnes="3000003", health_unit_name="Galba", address="Wrong"),
    ]
    source = {"authority": "SESAU-AL", "evidence_date": "2026-08-13", "reference": "Official reply"}
    corrections = [
        {
            "id": "replace",
            "action": "replace",
            "match_cnes": "1000001",
            "base_cnes": "2000002",
            "source": source,
            "fields": {"cnes": "2000002", "health_unit_name": "Hospital", "source_state_file": "AL_SESAU_20260813", "source_state_abbr": "AL"},
        },
        {
            "id": "add",
            "action": "add",
            "base_cnes": "4000004",
            "source": source,
            "fields": {"row_id": "AL_OFFICIAL_400", "cnes": "4000004", "health_unit_name": "UPA", "source_state_file": "AL_SESAU_20260813", "source_state_abbr": "AL"},
        },
        {
            "id": "update",
            "action": "update",
            "match_cnes": "3000003",
            "base_cnes": "3000003",
            "source": source,
            "fields": {"address": "Correct", "source_state_file": "AL_SESAU_20260813", "source_state_abbr": "AL"},
        },
    ]

    updated, changed = module.apply_corrections(FIELDS, rows, corrections)
    assert changed == ["replace", "add", "update"]
    assert {row["cnes"] for row in updated} == {"2000002", "3000003", "4000004"}
    replaced = next(row for row in updated if row["cnes"] == "2000002")
    assert replaced["place_id"] == ""
    assert replaced["original_place_id"] == "stale"
    assert replaced["geocode_attempted_at"] == "2026-08-13T00:00:00Z"
    added = next(row for row in updated if row["cnes"] == "4000004")
    assert added["address"] == ""

    updated_again, changed_again = module.apply_corrections(FIELDS, updated, corrections)
    assert changed_again == []
    assert len(updated_again) == 3


def test_check_mode_detects_unapplied_correction(tmp_path: Path):
    master = tmp_path / "master.csv"
    with master.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow({"row_id": "AL_0001", "source_state_abbr": "AL", "cnes": "1000001", "health_unit_name": "Old", "address": "A"})
    corrections = tmp_path / "corrections.json"
    corrections.write_text(
        json.dumps(
            {
                "_official_records": [
                    {
                        "id": "update",
                        "action": "update",
                        "match_cnes": "1000001",
                        "base_cnes": "1000001",
                        "source": {"authority": "SESAU-AL", "evidence_date": "2026-08-13", "reference": "Official reply"},
                        "fields": {"address": "Correct", "source_state_file": "AL_SESAU_20260813", "source_state_abbr": "AL"},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    assert module.main(["--master", str(master), "--corrections", str(corrections), "--check"]) == 1
    assert module.main(["--master", str(master), "--corrections", str(corrections)]) == 0
    assert module.main(["--master", str(master), "--corrections", str(corrections), "--check"]) == 0


def test_add_requires_explicit_target_cnes():
    rows = [
        {"row_id": "AL_0001", "source_state_abbr": "AL", "cnes": "1000001", "health_unit_name": "Base", "address": "A"}
    ]
    correction = {
        "id": "unsafe-add",
        "action": "add",
        "base_cnes": "2000002",
        "source": {"authority": "SESAU-AL", "evidence_date": "2026-08-13", "reference": "Official reply"},
        "fields": {"row_id": "AL_OFFICIAL_200", "health_unit_name": "Added", "source_state_file": "AL_SESAU_20260813", "source_state_abbr": "AL"},
    }

    with pytest.raises(module.CorrectionError, match="explicit fields.cnes"):
        module.apply_corrections(FIELDS, rows, [correction])


def test_source_metadata_must_match_declared_evidence():
    fields = FIELDS
    rows = [
        {"row_id": "AL_0001", "source_state_abbr": "AL", "source_state_file": "AL.json", "cnes": "1000001", "health_unit_name": "Base", "address": "A"}
    ]
    correction = {
        "id": "mismatched-source",
        "action": "update",
        "match_cnes": "1000001",
        "base_cnes": "1000001",
        "source": {"authority": "SESAU-AL", "evidence_date": "2026-08-13", "reference": "Official reply"},
        "fields": {"source_state_abbr": "AL", "source_state_file": "AL_SESAU_20260812"},
    }

    with pytest.raises(module.CorrectionError, match="date must equal"):
        module.apply_corrections(fields, rows, [correction])


def test_rejects_invalid_calendar_date_and_cnes():
    rows = [{"row_id": "AL_0001", "source_state_abbr": "AL", "cnes": "1000001"}]
    correction = {
        "id": "invalid",
        "action": "update",
        "match_cnes": "ABC",
        "base_cnes": "ABC",
        "source": {"authority": "SESAU-AL", "evidence_date": "2026-99-99", "reference": "Official reply"},
        "fields": {"source_state_abbr": "AL", "source_state_file": "AL_SESAU_20269999"},
    }
    with pytest.raises(module.CorrectionError, match="valid ISO date"):
        module.apply_corrections(FIELDS, rows, [correction])


def test_add_upsert_clears_stale_geocode_metadata():
    rows = [row(row_id="AL_0001", source_state_abbr="AL", cnes="4000004", address="Old", place_id="stale")]
    correction = {
        "id": "add-upsert",
        "action": "add",
        "base_cnes": "4000004",
        "source": {"authority": "SESAU-AL", "evidence_date": "2026-08-13", "reference": "Official reply"},
        "fields": {"cnes": "4000004", "address": "New", "source_state_file": "AL_SESAU_20260813", "source_state_abbr": "AL"},
    }
    updated, changed = module.apply_corrections(FIELDS, rows, [correction])
    assert changed == ["add-upsert"]
    assert updated[0]["place_id"] == ""
    assert updated[0]["original_place_id"] == "stale"


def test_update_rejects_mismatched_target_cnes():
    correction = {
        "id": "bad-update",
        "action": "update",
        "match_cnes": "1000001",
        "base_cnes": "2000002",
        "source": {"authority": "SESAU-AL", "evidence_date": "2026-08-13", "reference": "Official reply"},
        "fields": {"source_state_abbr": "AL", "source_state_file": "AL_SESAU_20260813"},
    }
    with pytest.raises(module.CorrectionError, match="match_cnes to equal base_cnes"):
        module.apply_corrections(FIELDS, [row(cnes="1000001")], [correction])
