#!/usr/bin/env python3
"""Apply authoritative state-level corrections to the final geocoded master.

The Ministry of Health PDFs remain the canonical base. This stage applies a
small, auditable layer of later or more precise official state evidence after
the generated pipeline and committed manual-triage decisions. It supports:

* ``update``: replace fields on an existing CNES row;
* ``replace``: correct a row whose CNES or identity is wrong; and
* ``add``: add an official state reference unit missing from the Ministry row.

The operation is idempotent. ``--check`` fails when the master would change.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MASTER = ROOT / "build" / "master_geocoded_patched_v1.csv"
DEFAULT_CORRECTIONS = ROOT / "data" / "location_overrides.json"
ALLOWED_ACTIONS = {"add", "replace", "update"}
STATE_SOURCE_RE = re.compile(
    r"^(?P<uf>[A-Z]{2})_(?P<authority>[A-Z0-9-]+)_(?P<date>\d{8})$",
    re.IGNORECASE,
)


class CorrectionError(ValueError):
    """Raised when a correction is ambiguous or malformed."""


def read_master(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


def read_corrections(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    corrections = data.get("_official_records") if isinstance(data, dict) else None
    if not isinstance(corrections, list):
        raise CorrectionError("location overrides must include an _official_records array")
    return corrections


def _matches(rows: list[dict[str, str]], cnes: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get("cnes", "").strip() == cnes]


def _validate_correction(correction: dict, fieldnames: list[str]) -> None:
    cid = correction.get("id") or "<missing id>"
    action = correction.get("action")
    fields = correction.get("fields")
    source = correction.get("source")
    if not isinstance(cid, str) or not cid.strip():
        raise CorrectionError("every correction needs a non-empty id")
    if action not in ALLOWED_ACTIONS:
        raise CorrectionError(f"{cid}: action must be one of {sorted(ALLOWED_ACTIONS)}")
    if not isinstance(fields, dict) or not fields:
        raise CorrectionError(f"{cid}: fields must be a non-empty object")
    unknown_fields = sorted(set(fields) - set(fieldnames))
    if unknown_fields:
        raise CorrectionError(f"{cid}: unknown master fields: {', '.join(unknown_fields)}")
    if not isinstance(source, dict) or not all(source.get(k) for k in ("authority", "evidence_date", "reference")):
        raise CorrectionError(f"{cid}: source must include authority, evidence_date, and reference")
    try:
        evidence_date = date.fromisoformat(str(source["evidence_date"]))
    except ValueError as exc:
        raise CorrectionError(f"{cid}: source.evidence_date must be a valid ISO date") from exc
    source_file = str(fields.get("source_state_file") or "")
    source_match = STATE_SOURCE_RE.match(source_file)
    source_uf = str(fields.get("source_state_abbr") or "").upper()
    if not source_match or not source_uf:
        raise CorrectionError(
            f"{cid}: fields must include source_state_abbr and a dated source_state_file"
        )
    encoded_uf = source_match.group("uf").upper()
    encoded_authority = f"{source_match.group('authority').upper()}-{encoded_uf}"
    raw_date = source_match.group("date")
    encoded_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
    if encoded_uf != source_uf:
        raise CorrectionError(f"{cid}: source_state_file UF must equal source_state_abbr")
    if encoded_authority != str(source["authority"]).upper():
        raise CorrectionError(f"{cid}: source_state_file authority must equal source.authority")
    if encoded_date != evidence_date.isoformat():
        raise CorrectionError(f"{cid}: source_state_file date must equal source.evidence_date")
    if action in {"replace", "update"} and not correction.get("match_cnes"):
        raise CorrectionError(f"{cid}: {action} requires match_cnes")
    if not correction.get("base_cnes"):
        raise CorrectionError(f"{cid}: base_cnes is required")
    for key in ("base_cnes", "match_cnes"):
        value = correction.get(key)
        if value is not None and not re.fullmatch(r"\d{7}", str(value)):
            raise CorrectionError(f"{cid}: {key} must contain exactly 7 digits")
    if action == "update" and str(correction["match_cnes"]) != str(correction["base_cnes"]):
        raise CorrectionError(f"{cid}: update requires match_cnes to equal base_cnes")
    if action in {"add", "replace"} and "cnes" not in fields:
        raise CorrectionError(f"{cid}: {action} requires an explicit fields.cnes")
    if str(fields.get("cnes", correction.get("base_cnes"))) != str(correction["base_cnes"]):
        raise CorrectionError(f"{cid}: fields.cnes must equal base_cnes")


def _apply_fields(row: dict[str, str], fields: dict) -> bool:
    changed = False
    for key, value in fields.items():
        normalized = "" if value is None else str(value)
        if row.get(key, "") != normalized:
            row[key] = normalized
            changed = True
    return changed


def _archive_geocode(row: dict[str, str]) -> bool:
    changed = False
    for field in ("formatted_address", "lat", "lng", "place_id", "partial_match", "location_type"):
        archive = f"original_{field}"
        if archive in row and not row.get(archive) and row.get(field):
            row[archive] = row[field]
            changed = True
    return changed


def _derive_fields(row: dict[str, str], action: str, evidence_date: str) -> bool:
    """Keep pipeline-derived columns consistent with authoritative base facts."""
    derived = {
        "state_clean": row.get("state", ""),
        "municipality_clean": row.get("municipality", ""),
        "health_unit_name_clean": row.get("health_unit_name", ""),
        "address_clean": row.get("address", ""),
        "phones_clean": row.get("phones_raw", ""),
        "antivenoms_joined": ", ".join(
            part.strip() for part in row.get("antivenoms_raw", "").split("|") if part.strip()
        ),
        "geocode_query": ", ".join(
            part for part in (
                row.get("health_unit_name", ""),
                row.get("address", ""),
                "Brasil",
            ) if part
        ),
        "normalization_notes": f"official state {action}",
        "needs_review_pre_geocode": "false",
        "geocode_status": "OK",
        "result_types": "official_cnes",
        "partial_match": "false",
        "place_id": "",
        "geocode_attempted_at": f"{evidence_date}T00:00:00Z",
    }
    return _apply_fields(row, {key: value for key, value in derived.items() if key in row})


def apply_corrections(
    fieldnames: list[str], rows: list[dict[str, str]], corrections: list[dict]
) -> tuple[list[dict[str, str]], list[str]]:
    changed_ids: list[str] = []
    seen_ids: set[str] = set()

    for correction in corrections:
        _validate_correction(correction, fieldnames)
        cid = correction["id"]
        if cid in seen_ids:
            raise CorrectionError(f"duplicate correction id: {cid}")
        seen_ids.add(cid)

        action = correction["action"]
        target_cnes = str(correction["base_cnes"])
        fields = correction["fields"]
        target_matches = _matches(rows, target_cnes)
        if len(target_matches) > 1:
            raise CorrectionError(f"{cid}: target CNES {target_cnes} is duplicated")

        if action == "add":
            if target_matches:
                is_created_row = bool(fields.get("row_id")) and (
                    target_matches[0].get("row_id") == str(fields["row_id"])
                )
                changed = False if is_created_row else _archive_geocode(target_matches[0])
                changed = _apply_fields(target_matches[0], fields) or changed
                changed = _derive_fields(
                    target_matches[0], action, correction["source"]["evidence_date"]
                ) or changed
            else:
                new_row = {name: "" for name in fieldnames}
                _apply_fields(new_row, fields)
                _derive_fields(new_row, action, correction["source"]["evidence_date"])
                rows.append(new_row)
                changed = True
        else:
            match_cnes = str(correction["match_cnes"])
            source_matches = _matches(rows, match_cnes)
            if action == "replace" and match_cnes != target_cnes:
                if source_matches and target_matches:
                    raise CorrectionError(
                        f"{cid}: both source CNES {match_cnes} and target CNES {target_cnes} exist"
                    )
                candidates = source_matches or target_matches
            else:
                candidates = source_matches
            if len(candidates) != 1:
                raise CorrectionError(
                    f"{cid}: expected exactly one row for CNES {match_cnes} or {target_cnes}"
                )
            changed = _archive_geocode(candidates[0])
            changed = _apply_fields(candidates[0], fields) or changed
            changed = _derive_fields(
                candidates[0], action, correction["source"]["evidence_date"]
            ) or changed

        if changed:
            changed_ids.append(cid)

    row_ids = [row.get("row_id", "") for row in rows]
    if len(row_ids) != len(set(row_ids)):
        raise CorrectionError("official corrections produced duplicate row_id values")
    for correction in corrections:
        target_cnes = str(correction["base_cnes"])
        if len(_matches(rows, target_cnes)) != 1:
            raise CorrectionError(
                f"{correction['id']}: target CNES {target_cnes} must match exactly one row after apply"
            )
    return rows, changed_ids


def write_master(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as fh:
            tmp_path = Path(fh.name)
            writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="raise")
            writer.writeheader()
            writer.writerows(rows)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_path, path)
    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", type=Path, default=DEFAULT_MASTER)
    parser.add_argument("--corrections", type=Path, default=DEFAULT_CORRECTIONS)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    try:
        fieldnames, rows = read_master(args.master)
        corrections = read_corrections(args.corrections)
        rows, changed_ids = apply_corrections(fieldnames, rows, corrections)
    except (OSError, json.JSONDecodeError, CorrectionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if changed_ids:
            print(
                "ERROR: official state corrections are not applied: " + ", ".join(changed_ids),
                file=sys.stderr,
            )
            return 1
        print(f"Official state corrections current ({len(corrections)} checked).")
        return 0

    if changed_ids:
        write_master(args.master, fieldnames, rows)
    print(f"Applied {len(changed_ids)} official state correction(s): " + (", ".join(changed_ids) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
