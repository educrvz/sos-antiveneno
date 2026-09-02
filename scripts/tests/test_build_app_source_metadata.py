from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import build_app_hospitals_json as module  # noqa: E402


def test_state_source_metadata_uses_embedded_date_and_authority():
    row = {"source_state_file": "AL_SESAU_20260813", "source_state_abbr": "AL"}
    assert module.source_metadata(row, {"AL": "2026-07-03"}) == (
        "2026-08-13",
        "SESAU-AL",
        "https://www.saude.al.gov.br/",
    )


def test_ministry_source_metadata_uses_uf_date_without_authority():
    row = {"source_state_file": "AL.json", "source_state_abbr": "AL"}
    assert module.source_metadata(row, {"AL": "2026-07-03"}) == (
        "2026-07-03",
        None,
        None,
    )


def test_pernambuco_state_source_metadata_uses_public_authority_url():
    row = {"source_state_file": "PE_SES_20260901", "source_state_abbr": "PE"}
    assert module.source_metadata(row, {"PE": "2026-07-03"}) == (
        "2026-09-01",
        "SES-PE",
        "https://portal.saude.pe.gov.br/",
    )
