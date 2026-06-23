from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import validate_community_notes as validator  # noqa: E402


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def write_hospitals(path: Path, cnes_values: list[str]) -> None:
    write_json(path, [{"cnes": cnes, "hospital_name": f"H {cnes}"} for cnes in cnes_values])


def test_valid_notes_pass(tmp_path: Path):
    notes = tmp_path / "community_notes.json"
    hospitals = tmp_path / "hospitals.json"
    write_hospitals(hospitals, ["123"])
    write_json(
        notes,
        {
            "generated_at": "2026-06-22",
            "notes": {
                "123": [
                    {
                        "category": "contact_fix",
                        "reported_at": "2026-06-21",
                        "public_summary": "Relato da comunidade: telefone atualizado.",
                    }
                ]
            },
        },
    )

    assert validator.validate(notes, hospitals) == []


def test_rejects_unknown_cnes_and_category(tmp_path: Path):
    notes = tmp_path / "community_notes.json"
    hospitals = tmp_path / "hospitals.json"
    write_hospitals(hospitals, ["123"])
    write_json(
        notes,
        {
            "generated_at": "2026-06-22",
            "notes": {
                "999": [
                    {
                        "category": "source_contribution",
                        "reported_at": "2026-06-21",
                        "public_summary": "Relato da comunidade: texto.",
                    }
                ]
            },
        },
    )

    errors = validator.validate(notes, hospitals)

    assert "CNES 999: CNES is not present in app/hospitals.json" in errors
    assert any("category must be one of" in error for error in errors)


def test_rejects_empty_reference_cnes_set(tmp_path: Path):
    notes = tmp_path / "community_notes.json"
    hospitals = tmp_path / "hospitals.json"
    write_hospitals(hospitals, [])
    write_json(
        notes,
        {
            "generated_at": "2026-06-22",
            "notes": {
                "123": [
                    {
                        "category": "contact_fix",
                        "reported_at": "2026-06-21",
                        "public_summary": "Relato da comunidade: telefone atualizado.",
                    }
                ]
            },
        },
    )

    errors = validator.validate(notes, hospitals)

    assert any("no CNES values found for reference checks" in error for error in errors)
    assert "CNES 123: CNES is not present in app/hospitals.json" in errors


def test_rejects_bad_dates_and_expiry_order(tmp_path: Path):
    notes = tmp_path / "community_notes.json"
    hospitals = tmp_path / "hospitals.json"
    write_hospitals(hospitals, ["123"])
    write_json(
        notes,
        {
            "generated_at": "not-a-date",
            "notes": {
                "123": [
                    {
                        "category": "closed",
                        "reported_at": "2026-06-21",
                        "expires_at": "2026-06-21",
                        "public_summary": "Relato da comunidade: local pode estar fechado.",
                    }
                ]
            },
        },
    )

    errors = validator.validate(notes, hospitals)

    assert any("generated_at must be YYYY-MM-DD" in error for error in errors)
    assert "CNES 123 note 1: expires_at must be after reported_at" in errors


def test_rejects_non_calendar_iso_date_forms(tmp_path: Path):
    notes = tmp_path / "community_notes.json"
    hospitals = tmp_path / "hospitals.json"
    write_hospitals(hospitals, ["123"])
    write_json(
        notes,
        {
            "generated_at": "2026-W26-1",
            "notes": {
                "123": [
                    {
                        "category": "closed",
                        "reported_at": "20260621",
                        "public_summary": "Relato da comunidade: local pode estar fechado.",
                    }
                ]
            },
        },
    )

    errors = validator.validate(notes, hospitals)

    assert any("generated_at must be YYYY-MM-DD" in error for error in errors)
    assert "CNES 123 note 1: reported_at must be YYYY-MM-DD" in errors


def test_rejects_long_summary_and_unknown_keys(tmp_path: Path):
    notes = tmp_path / "community_notes.json"
    hospitals = tmp_path / "hospitals.json"
    write_hospitals(hospitals, ["123"])
    write_json(
        notes,
        {
            "generated_at": "2026-06-22",
            "notes": {
                "123": [
                    {
                        "category": "other",
                        "reported_at": "2026-06-21",
                        "public_summary": "x" * (validator.SUMMARY_MAX + 1),
                        "raw_report": "must not publish raw text",
                    }
                ]
            },
        },
    )

    errors = validator.validate(notes, hospitals)

    assert f"CNES 123 note 1: public_summary exceeds {validator.SUMMARY_MAX} characters" in errors
    assert "CNES 123 note 1: unknown key(s): raw_report" in errors
