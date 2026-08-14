#!/usr/bin/env python3
"""Validate data/location_overrides.json before rebuilding public data."""

from __future__ import annotations

import csv
from datetime import date
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "data" / "location_overrides.json"
MASTER = ROOT / "build" / "master_geocoded_patched_v1.csv"

LAT_MIN, LAT_MAX = -34.0, 5.5
LNG_MIN, LNG_MAX = -74.5, -34.5
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ALLOWED_KEYS = {"reason", "verified_on", "lat", "lng", "address", "note", "hide"}


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
        errors.append(f"{ctx}: {field} must be a valid calendar date")
        return None


def load_publishable_cnes(master_path: Path) -> set[str]:
    with master_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {
            str(row.get("cnes", "")).strip()
            for row in reader
            if row.get("cnes") and (row.get("publish_policy") or "").strip() == "publish"
        }


def validate(
    overrides_path: Path = OVERRIDES,
    master_path: Path = MASTER,
) -> list[str]:
    errors: list[str] = []

    try:
        data = json.loads(overrides_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{overrides_path}: cannot read JSON: {exc}"]

    if not isinstance(data, dict):
        return [f"{overrides_path}: top-level value must be an object"]

    try:
        known_cnes = load_publishable_cnes(master_path)
    except Exception as exc:
        errors.append(f"{master_path}: cannot load known CNES values: {exc}")
        known_cnes = set()
    if not known_cnes:
        errors.append(f"{master_path}: no publishable CNES values found for reference checks")

    for raw_cnes, override in sorted(data.items()):
        if raw_cnes == "_official_records":
            if not isinstance(override, list):
                errors.append("_official_records must be an array")
            continue
        cnes = str(raw_cnes).strip()
        ctx = f"CNES {cnes or '?'}"
        if not cnes:
            errors.append("overrides contains a blank CNES key")
            continue
        if not cnes.isdigit():
            errors.append(f"{ctx}: CNES key must contain only digits")
        if cnes not in known_cnes:
            errors.append(
                f"{ctx}: CNES is not publishable in build/master_geocoded_patched_v1.csv"
            )
        if not isinstance(override, dict):
            errors.append(f"{ctx}: override must be an object")
            continue

        unknown = sorted(set(override) - ALLOWED_KEYS)
        if unknown:
            errors.append(f"{ctx}: unknown key(s): {', '.join(unknown)}")

        reason = override.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{ctx}: reason is required")

        parse_date(override.get("verified_on"), "verified_on", ctx, errors)

        hide = override.get("hide")
        if "hide" in override and not isinstance(hide, bool):
            errors.append(f"{ctx}: hide must be a boolean")

        has_lat = "lat" in override
        has_lng = "lng" in override
        if has_lat != has_lng:
            errors.append(f"{ctx}: lat and lng must be provided together")
        if has_lat and has_lng:
            try:
                lat = float(override.get("lat"))
                lng = float(override.get("lng"))
            except (TypeError, ValueError):
                errors.append(f"{ctx}: lat/lng must be numeric")
            else:
                if not (LAT_MIN <= lat <= LAT_MAX and LNG_MIN <= lng <= LNG_MAX):
                    errors.append(f"{ctx}: lat/lng ({lat}, {lng}) outside Brazil bbox")

        for field in ("address", "note"):
            if field in override and (
                not isinstance(override[field], str) or not override[field].strip()
            ):
                errors.append(f"{ctx}: {field} must be a non-empty string when set")

        changes_data = bool(hide is True or has_lat or "address" in override or "note" in override)
        if not changes_data:
            errors.append(f"{ctx}: override must set hide, lat/lng, address, or note")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"FAIL: {len(errors)} location override error(s)", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"OK: location overrides validated in {OVERRIDES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
