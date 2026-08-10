from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent


def test_hospital_cards_support_non_ministry_source_labels():
    index = (ROOT / "app" / "index.html").read_text(encoding="utf-8")

    assert "h.source_label || 'MS'" in index
    assert "h.source_url ||" in index
    assert ">Fonte: ' + sourceLabel" in index
