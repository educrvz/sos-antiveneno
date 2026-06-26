from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import validate_location_overrides as validator  # noqa: E402


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def write_master(path: Path, cnes_values: list[str], publish_policy: str = "publish") -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["row_id", "cnes", "publish_policy"])
        writer.writeheader()
        for i, cnes in enumerate(cnes_values, start=1):
            writer.writerow(
                {"row_id": f"SP_{i:04d}", "cnes": cnes, "publish_policy": publish_policy}
            )


def test_valid_coordinate_override_passes(tmp_path: Path):
    overrides = tmp_path / "location_overrides.json"
    master = tmp_path / "master.csv"
    write_master(master, ["123"])
    write_json(
        overrides,
        {
            "123": {
                "reason": "Pin verified manually.",
                "verified_on": "2026-06-22",
                "lat": -23.55,
                "lng": -46.63,
            }
        },
    )

    assert validator.validate(overrides, master) == []


def test_valid_hide_override_passes(tmp_path: Path):
    overrides = tmp_path / "location_overrides.json"
    master = tmp_path / "master.csv"
    write_master(master, ["123"])
    write_json(
        overrides,
        {
            "123": {
                "reason": "Source row is unsafe to publish.",
                "verified_on": "2026-06-22",
                "hide": True,
            }
        },
    )

    assert validator.validate(overrides, master) == []


def test_rejects_unknown_cnes_and_unknown_keys(tmp_path: Path):
    overrides = tmp_path / "location_overrides.json"
    master = tmp_path / "master.csv"
    write_master(master, ["123"])
    write_json(
        overrides,
        {
            "999": {
                "reason": "Pin verified manually.",
                "verified_on": "2026-06-22",
                "lat": -23.55,
                "lng": -46.63,
                "raw_report": "do not publish",
            }
        },
    )

    errors = validator.validate(overrides, master)

    assert "CNES 999: CNES is not publishable in build/master_geocoded_patched_v1.csv" in errors
    assert "CNES 999: unknown key(s): raw_report" in errors


def test_rejects_non_publishable_cnes(tmp_path: Path):
    overrides = tmp_path / "location_overrides.json"
    master = tmp_path / "master.csv"
    write_master(master, ["123"], publish_policy="hide_muni_mismatch")
    write_json(
        overrides,
        {
            "123": {
                "reason": "Pin verified manually.",
                "verified_on": "2026-06-22",
                "lat": -23.55,
                "lng": -46.63,
            }
        },
    )

    errors = validator.validate(overrides, master)

    assert any("no publishable CNES values found for reference checks" in error for error in errors)
    assert "CNES 123: CNES is not publishable in build/master_geocoded_patched_v1.csv" in errors


def test_rejects_partial_or_out_of_range_coordinates(tmp_path: Path):
    overrides = tmp_path / "location_overrides.json"
    master = tmp_path / "master.csv"
    write_master(master, ["123", "456"])
    write_json(
        overrides,
        {
            "123": {
                "reason": "Missing lng.",
                "verified_on": "2026-06-22",
                "lat": -23.55,
            },
            "456": {
                "reason": "Outside Brazil.",
                "verified_on": "2026-06-22",
                "lat": 40.0,
                "lng": -46.63,
            },
        },
    )

    errors = validator.validate(overrides, master)

    assert "CNES 123: lat and lng must be provided together" in errors
    assert "CNES 456: lat/lng (40.0, -46.63) outside Brazil bbox" in errors


def test_rejects_bad_metadata_and_no_action(tmp_path: Path):
    overrides = tmp_path / "location_overrides.json"
    master = tmp_path / "master.csv"
    write_master(master, ["123"])
    write_json(
        overrides,
        {
            "123": {
                "reason": "",
                "verified_on": "2026-W26-1",
                "hide": "true",
            }
        },
    )

    errors = validator.validate(overrides, master)

    assert "CNES 123: reason is required" in errors
    assert "CNES 123: verified_on must be YYYY-MM-DD" in errors
    assert "CNES 123: hide must be a boolean" in errors
    assert "CNES 123: override must set hide, lat/lng, address, or note" in errors


def test_rejects_empty_reference_cnes_set(tmp_path: Path):
    overrides = tmp_path / "location_overrides.json"
    master = tmp_path / "master.csv"
    write_master(master, [])
    write_json(
        overrides,
        {
            "123": {
                "reason": "Pin verified manually.",
                "verified_on": "2026-06-22",
                "lat": -23.55,
                "lng": -46.63,
            }
        },
    )

    errors = validator.validate(overrides, master)

    assert any("no publishable CNES values found for reference checks" in error for error in errors)
    assert "CNES 123: CNES is not publishable in build/master_geocoded_patched_v1.csv" in errors
