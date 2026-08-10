from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import build_app_hospitals_json as builder  # noqa: E402


def test_load_and_build_official_temporary_unit(tmp_path: Path):
    path = tmp_path / "official_temporary_units.json"
    path.write_text(
        json.dumps(
            {
                "generated_at": "2026-08-10",
                "units": [
                    {
                        "state": "RS",
                        "state_name": "Rio Grande do Sul",
                        "city": "Canoas",
                        "hospital_name": "Hospital Nossa Senhora das Graças",
                        "address": "Av. Santos Ferreira, 1864, Marechal Rondon",
                        "phones": ["(51) 2102-1000"],
                        "cnes": "2232014",
                        "antivenoms": ["Escorpiônico"],
                        "source_date": "2026-08-07",
                        "source_authority": "SES-RS",
                        "lat": -29.9271746,
                        "lng": -51.1615711,
                        "geocode_tier": 1,
                        "note": "Referência temporária; confirme antes de se deslocar.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    units = builder.load_official_temporary_units(path)
    record = builder.build_official_temporary_record(units[0], 1)

    assert record["cnes"] == "2232014"
    assert record["antivenoms"] == ["Escorpiônico"]
    assert record["source_date"] == "2026-08-07"


def test_rejects_incomplete_official_temporary_unit():
    with pytest.raises(ValueError, match="missing required field"):
        builder.build_official_temporary_record({"cnes": "2232014"}, 1)
