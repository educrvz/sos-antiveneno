#!/usr/bin/env python3
"""Validate data/community_notes.json before it reaches the public app."""

from __future__ import annotations

from datetime import date
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMUNITY_NOTES = ROOT / "data" / "community_notes.json"
APP_HOSPITALS = ROOT / "app" / "hospitals.json"

ALLOWED_CATEGORIES = {"contact_fix", "pin_fix", "closed", "wrong_unit", "other"}
SUMMARY_MAX = 280
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_date(value: object, field: str, ctx: str, errors: list[str]) -> date | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{ctx}: {field} is required")
        return None
    if not DATE_RE.match(value):
        errors.append(f"{ctx}: {field} must be YYYY-MM-DD")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{ctx}: {field} must be YYYY-MM-DD")
        return None


def load_known_cnes(app_hospitals_path: Path) -> set[str]:
    data = json.loads(app_hospitals_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{app_hospitals_path} must be a JSON array")
    return {str(row.get("cnes", "")).strip() for row in data if row.get("cnes")}


def validate(
    community_notes_path: Path = COMMUNITY_NOTES,
    app_hospitals_path: Path = APP_HOSPITALS,
) -> list[str]:
    errors: list[str] = []

    try:
        data = json.loads(community_notes_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{community_notes_path}: cannot read JSON: {exc}"]

    if not isinstance(data, dict):
        return [f"{community_notes_path}: top-level value must be an object"]

    parse_date(data.get("generated_at"), "generated_at", str(community_notes_path), errors)

    notes = data.get("notes")
    if not isinstance(notes, dict):
        errors.append(f"{community_notes_path}: notes must be an object")
        return errors

    try:
        known_cnes = load_known_cnes(app_hospitals_path)
    except Exception as exc:
        errors.append(f"{app_hospitals_path}: cannot load known CNES values: {exc}")
        known_cnes = set()
    if not known_cnes:
        errors.append(f"{app_hospitals_path}: no CNES values found for reference checks")

    for raw_cnes, entries in sorted(notes.items()):
        cnes = str(raw_cnes).strip()
        ctx = f"CNES {cnes or '?'}"
        if not cnes:
            errors.append("notes contains a blank CNES key")
            continue
        if not cnes.isdigit():
            errors.append(f"{ctx}: CNES key must contain only digits")
        if cnes not in known_cnes:
            errors.append(f"{ctx}: CNES is not present in app/hospitals.json")
        if not isinstance(entries, list) or not entries:
            errors.append(f"{ctx}: value must be a non-empty list")
            continue

        for i, note in enumerate(entries, start=1):
            nctx = f"{ctx} note {i}"
            if not isinstance(note, dict):
                errors.append(f"{nctx}: note must be an object")
                continue

            category = note.get("category")
            if category not in ALLOWED_CATEGORIES:
                errors.append(
                    f"{nctx}: category must be one of {', '.join(sorted(ALLOWED_CATEGORIES))}"
                )

            reported_at = parse_date(note.get("reported_at"), "reported_at", nctx, errors)

            summary = note.get("public_summary")
            if not isinstance(summary, str) or not summary.strip():
                errors.append(f"{nctx}: public_summary is required")
            elif len(summary) > SUMMARY_MAX:
                errors.append(f"{nctx}: public_summary exceeds {SUMMARY_MAX} characters")

            expires_raw = note.get("expires_at")
            if expires_raw not in (None, ""):
                expires_at = parse_date(expires_raw, "expires_at", nctx, errors)
                if reported_at and expires_at and expires_at <= reported_at:
                    errors.append(f"{nctx}: expires_at must be after reported_at")

            allowed_keys = {"category", "reported_at", "public_summary", "expires_at"}
            unknown = sorted(set(note) - allowed_keys)
            if unknown:
                errors.append(f"{nctx}: unknown key(s): {', '.join(unknown)}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"FAIL: {len(errors)} community note error(s)", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"OK: community notes validated in {COMMUNITY_NOTES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
