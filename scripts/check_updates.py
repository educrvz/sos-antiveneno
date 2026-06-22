#!/usr/bin/env python3
"""
Check for updated PESA PDFs on the Ministry of Health website.

Compares the dates we have (from `data/source_dates.json`, with local PDF
filenames as a fallback) against the dates currently shown on the gov.br
listing for every state. Persists the scraped website state to
`data/online_dates.json` and appends any day-over-day changes to
`data/online_dates_history.jsonl`, so the git history becomes the audit
trail. Regenerates `data/dates_status.md` as a side-by-side dashboard
committed alongside.

Exit code is 0 when we're up to date with the website, non-zero when the
website is ahead, our committed baseline is incomplete, or the HTML parser
can no longer find one or more states. The optional `--hash-check` also
fails when the live PDF bytes differ from `data/source_hashes.json`.

Usage:
    python3 scripts/check_updates.py
    python3 scripts/check_updates.py --hash-check

Source pages:
    Page 1: https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia
    Page 2: https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia?b_start:int=15
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup

    HAS_WEB = True
except ImportError:
    HAS_WEB = False

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PDF_DIR = ROOT / "Docs Estado"
SOURCE_DATES = DATA_DIR / "source_dates.json"
SOURCE_HASHES = DATA_DIR / "source_hashes.json"
ONLINE_DATES = DATA_DIR / "online_dates.json"
ONLINE_HISTORY = DATA_DIR / "online_dates_history.jsonl"
STATUS_MD = DATA_DIR / "dates_status.md"

PAGES = [
    "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia",
    "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia?b_start:int=15",
]

SOURCE_URL = (
    "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos"
    "/hospitais-de-referencia"
)

# Slug per state for the @@download URL (lowercase, dash-separated, no accents).
STATE_SLUG = {
    "AC": "acre",
    "AL": "alagoas",
    "AM": "amazonas",
    "AP": "amapa",
    "BA": "bahia",
    "CE": "ceara",
    "DF": "distrito-federal",
    "ES": "espirito-santo",
    "GO": "goias",
    "MA": "maranhao",
    "MG": "minas-gerais",
    "MS": "mato-grosso-do-sul",
    "MT": "mato-grosso",
    "PA": "para",
    "PB": "paraiba",
    "PE": "pernambuco",
    "PI": "piaui",
    "PR": "parana",
    "RJ": "rio-de-janeiro",
    "RN": "rio-grande-do-norte",
    "RO": "rondonia",
    "RR": "roraima",
    "RS": "rio-grande-do-sul",
    "SC": "santa-catarina",
    "SE": "sergipe",
    "SP": "sao-paulo",
    "TO": "tocantins",
}
PDF_DOWNLOAD = (
    "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos"
    "/hospitais-de-referencia/{slug}/@@download/file"
)

STATE_CODES = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Distrito Federal": "DF",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso do Sul": "MS",
    "Mato Grosso": "MT",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO",
}
CODE_TO_STATE = {code: state for state, code in STATE_CODES.items()}


def _parse_iso_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _serialize_dates(values: dict[str, date]) -> dict[str, str]:
    return {code: values[code].isoformat() for code in sorted(values)}


def load_source_dates(source_dates_path: Path = SOURCE_DATES) -> dict[str, date]:
    """Read the committed UF → YYYY-MM-DD baseline."""
    if not source_dates_path.exists():
        return {}
    try:
        data = json.loads(source_dates_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"  ERROR reading {source_dates_path}: {exc}", file=sys.stderr)
        return {}
    if not isinstance(data, dict):
        print(f"  ERROR: {source_dates_path} must be a JSON object", file=sys.stderr)
        return {}

    out: dict[str, date] = {}
    for code, value in data.items():
        normalized_code = str(code).upper()
        if normalized_code not in CODE_TO_STATE:
            continue
        parsed = _parse_iso_date(str(value))
        if parsed is None:
            print(
                f"  WARN: ignoring invalid source date for {normalized_code}: {value!r}",
                file=sys.stderr,
            )
            continue
        out[normalized_code] = parsed
    return out


def load_source_hashes(source_hashes_path: Path = SOURCE_HASHES) -> dict[str, str]:
    """Read the committed UF → SHA-1 baseline used by --hash-check."""
    if not source_hashes_path.exists():
        return {}
    try:
        data = json.loads(source_hashes_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"  ERROR reading {source_hashes_path}: {exc}", file=sys.stderr)
        return {}
    if not isinstance(data, dict):
        print(f"  ERROR: {source_hashes_path} must be a JSON object", file=sys.stderr)
        return {}

    out: dict[str, str] = {}
    for code, value in data.items():
        normalized_code = str(code).upper()
        if normalized_code not in STATE_SLUG:
            continue
        digest = str(value).strip().lower()
        if digest:
            out[normalized_code] = digest
    return out


def _scan_pdf_dates(pdf_dir: Path = PDF_DIR) -> dict[str, date]:
    """Read dates from local PDF filenames ({UF}_{YYYYMMDD}.pdf)."""
    local: dict[str, date] = {}
    if not pdf_dir.exists():
        return local

    for path in pdf_dir.iterdir():
        name = path.name
        if not name.endswith(".pdf"):
            continue
        parts = name.removesuffix(".pdf").split("_")
        state_code = None
        date_str = None
        for part in parts:
            if len(part) == 2 and part.isalpha() and part.isupper() and part in CODE_TO_STATE:
                state_code = part
            if len(part) == 8 and part.isdigit():
                date_str = part
        if state_code and date_str:
            try:
                local[state_code] = datetime.strptime(date_str, "%Y%m%d").date()
            except ValueError:
                pass
    return local


def get_local_dates(
    source_dates_path: Path = SOURCE_DATES,
    pdf_dir: Path = PDF_DIR,
) -> dict[str, date]:
    """Return the baseline dates used for comparison.

    CI checkouts do not contain `Docs Estado/` because PDFs are ignored by git,
    so the committed `data/source_dates.json` is the primary source. Local PDF
    filenames remain a fallback and can temporarily advance or fill gaps while a
    maintainer prepares the committed metadata update.
    """
    local = load_source_dates(source_dates_path)
    pdf_dates = _scan_pdf_dates(pdf_dir)
    for code, pdf_date in pdf_dates.items():
        if code not in local or pdf_date > local[code]:
            local[code] = pdf_date
    return local


def load_previous_online(online_dates_path: Path = ONLINE_DATES) -> dict[str, date]:
    """Load the last persisted online snapshot so we can diff transitions."""
    if not online_dates_path.exists():
        return {}
    try:
        data = json.loads(online_dates_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"  ERROR reading {online_dates_path}: {exc}", file=sys.stderr)
        return {}
    if not isinstance(data, dict):
        print(f"  ERROR: {online_dates_path} must be a JSON object", file=sys.stderr)
        return {}

    out: dict[str, date] = {}
    for code, value in data.items():
        normalized_code = str(code).upper()
        if normalized_code not in CODE_TO_STATE:
            continue
        parsed = _parse_iso_date(str(value))
        if parsed:
            out[normalized_code] = parsed
    return out


def parse_online_dates_from_html(text: str) -> dict[str, date]:
    """Parse gov.br page text for per-state PDF publication dates."""
    online: dict[str, date] = {}
    for state_name, code in STATE_CODES.items():
        pattern = re.compile(
            re.escape(state_name) + r".{1,200}?publicado\s+(\d{2}/\d{2}/\d{4})",
            re.DOTALL,
        )
        match = pattern.search(text)
        if not match:
            continue
        try:
            online[code] = datetime.strptime(match.group(1), "%d/%m/%Y").date()
        except ValueError:
            pass
    return online


def scrape_online_dates() -> dict[str, date]:
    """Scrape the gov.br pages for the publication date next to each state."""
    if not HAS_WEB:
        print(
            "  ERROR: requests and beautifulsoup4 are required to scrape gov.br.",
            file=sys.stderr,
        )
        return {}

    online: dict[str, date] = {}
    for url in PAGES:
        try:
            resp = requests.get(
                url,
                timeout=30,
                headers={
                    "User-Agent": "SoroJa-Update-Checker/1.0 (contato.soroja@gmail.com)"
                },
            )
            resp.raise_for_status()
        except Exception as exc:
            print(f"  ERROR fetching {url}: {exc}", file=sys.stderr)
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()
        online.update(parse_online_dates_from_html(text))

    return online


def write_online_dates(
    online: dict[str, date],
    online_dates_path: Path = ONLINE_DATES,
) -> None:
    """Persist the current website state with stable key ordering."""
    online_dates_path.write_text(
        json.dumps(_serialize_dates(online), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def append_history(
    prev: dict[str, date],
    curr: dict[str, date],
    detected_at: date,
    history_path: Path = ONLINE_HISTORY,
) -> int:
    """Append one JSONL row per state whose online date changed."""
    if not prev:
        return 0

    changes = []
    all_ufs = set(prev) | set(curr)
    for uf in sorted(all_ufs):
        before = prev.get(uf)
        after = curr.get(uf)
        if before == after:
            continue
        changes.append(
            {
                "detected_at": detected_at.isoformat(),
                "uf": uf,
                "from": before.isoformat() if before else None,
                "to": after.isoformat() if after else None,
            }
        )

    if changes:
        with history_path.open("a", encoding="utf-8") as fh:
            for change in changes:
                fh.write(json.dumps(change, ensure_ascii=False) + "\n")
    return len(changes)


def analyze_dates(local: dict[str, date], online: dict[str, date]):
    updates_needed = []
    up_to_date = []
    we_ahead = []
    missing_local = []
    missing_online = []

    for code in sorted(CODE_TO_STATE):
        online_date = online.get(code)
        local_date = local.get(code)
        state_name = CODE_TO_STATE[code]

        if not online_date:
            missing_online.append((code, state_name))
            continue

        if not local_date:
            missing_local.append((code, state_name, online_date))
            continue

        if online_date > local_date:
            updates_needed.append((code, state_name, local_date, online_date))
        elif local_date > online_date:
            we_ahead.append((code, state_name, local_date, online_date))
            up_to_date.append((code, state_name, local_date))
        else:
            up_to_date.append((code, state_name, local_date))

    return updates_needed, up_to_date, we_ahead, missing_local, missing_online


def compare_dates(local: dict[str, date], online: dict[str, date]):
    """Compatibility helper used by unit tests and callers."""
    updates_needed, up_to_date, _we_ahead, missing_local, missing_online = analyze_dates(
        local,
        online,
    )
    return updates_needed, up_to_date, missing_local, missing_online


def write_status_dashboard(
    local: dict[str, date],
    online: dict[str, date],
    status_path: Path = STATUS_MD,
) -> None:
    """Write a side-by-side markdown dashboard committed by CI."""
    lines = [
        "# Estado dos dados PESA",
        "",
        "Comparação entre o que está publicado no SoroJá (`source_dates.json`)",
        f"e a [página oficial do Ministério da Saúde]({SOURCE_URL}).",
        "Atualizado automaticamente por `scripts/check_updates.py` (CI diária).",
        "",
        "| UF | Estado | Nossa data | Site MS | Status |",
        "|----|--------|-----------|---------|--------|",
    ]
    rows = []
    counts = {
        "match": 0,
        "ms_newer": 0,
        "we_newer": 0,
        "missing_local": 0,
        "missing_online": 0,
    }

    for code in sorted(CODE_TO_STATE):
        state_name = CODE_TO_STATE[code]
        ours = local.get(code)
        theirs = online.get(code)
        if ours and theirs:
            if ours == theirs:
                status, key = "✅ em dia", "match"
            elif theirs > ours:
                status, key = "🔴 site mais novo", "ms_newer"
            else:
                status, key = "ℹ️ site mais antigo", "we_newer"
        elif theirs and not ours:
            status, key = "⚠️ ausente nos nossos", "missing_local"
        elif ours and not theirs:
            status, key = "⚠️ ausente no site", "missing_online"
        else:
            status, key = "❓ desconhecido", "missing_local"
        counts[key] += 1
        rows.append(
            f"| {code} | {state_name} | {ours.isoformat() if ours else '—'} | "
            f"{theirs.isoformat() if theirs else '—'} | {status} |"
        )

    lines.extend(rows)
    lines.extend(
        [
            "",
            f"**Resumo:** {counts['match']} em dia · {counts['ms_newer']} site mais novo · "
            f"{counts['we_newer']} nosso mais novo · {counts['missing_local']} faltam aqui · "
            f"{counts['missing_online']} faltam no site",
            "",
        ]
    )
    status_path.write_text("\n".join(lines), encoding="utf-8")


def print_human_report(local: dict[str, date], online: dict[str, date]) -> int:
    """Stdout for CI logs + humans. Returns the count of actionable mismatches."""
    updates_needed, up_to_date, we_ahead, missing_local, missing_online = analyze_dates(
        local,
        online,
    )

    print("=" * 60)
    print("  SoroJá — Verificador de Atualizações PESA")
    print("=" * 60)
    print()
    print(f"Datas locais encontradas: {len(local)}/27")
    if SOURCE_DATES.exists():
        print(f"Base local: {SOURCE_DATES.relative_to(ROOT)} (+ PDFs locais se existirem)")
    else:
        print(f"Base local: PDFs em {PDF_DIR}")
    print(f"Estados encontrados no site MS: {len(online)}/27")
    print()

    if updates_needed:
        print("🔴 ATUALIZAÇÕES DISPONÍVEIS:")
        print("-" * 50)
        for code, name, local_date, online_date in updates_needed:
            print(f"  {code} ({name})")
            print(f"     Local:  {local_date.strftime('%d/%m/%Y')}")
            print(f"     Online: {online_date.strftime('%d/%m/%Y')} ← NOVO!")
            print("     Baixar: acesse gov.br e baixe o PDF atualizado")
            print()
    else:
        print("✅ Nenhuma atualização disponível.")
        print()

    if missing_local:
        print("⚠️  DATAS LOCAIS NÃO ENCONTRADAS:")
        for code, name, online_date in missing_local:
            print(f"  {code} ({name}) — online: {online_date.strftime('%d/%m/%Y')}")
        print("  Atualize data/source_dates.json ou baixe o PDF correspondente em Docs Estado/.")
        print()

    if missing_online:
        print("⚠️  ESTADOS NÃO ENCONTRADOS ONLINE:")
        for code, name in missing_online:
            print(f"  {code} ({name})")
        print("  A página do gov.br pode ter mudado de formato; confira o parser.")
        print()

    if we_ahead:
        print("ℹ️  ESTADOS ONDE NOSSA DATA É MAIS NOVA QUE A DO SITE:")
        for code, name, local_date, online_date in we_ahead:
            print(
                f"  {code} ({name}) — local {local_date.strftime('%d/%m/%Y')} > "
                f"site {online_date.strftime('%d/%m/%Y')}"
            )
        print()

    print(f"✅ {len(up_to_date)} estados em dia ou adiantados localmente")
    print()
    print(f"Fonte: {SOURCE_URL}")
    print()

    if updates_needed or missing_local:
        print("PRÓXIMOS PASSOS:")
        print("  1. Baixe os PDFs atualizados do gov.br")
        print(f"  2. Salve como {{UF}}_{{YYYYMMDD}}.pdf em {PDF_DIR}")
        print("  3. Re-extraia o(s) estado(s) afetado(s) para extracted/{UF}.json")
        print("  4. Atualize data/source_dates.json e data/source_hashes.json")
        print("  5. Execute: ./scripts/refresh_dataset.sh")
        print("  6. Valide, revise o diff e abra PR")

    return len(updates_needed) + len(missing_local) + len(missing_online)


def fetch_live_pdf_hashes() -> dict[str, str]:
    """Download each state PDF from gov.br and return UF → SHA-1 digest."""
    if not HAS_WEB:
        print(
            "ERROR: requests and beautifulsoup4 are required for --hash-check.",
            file=sys.stderr,
        )
        return {}

    out: dict[str, str] = {}
    for uf, slug in STATE_SLUG.items():
        url = PDF_DOWNLOAD.format(slug=slug)
        try:
            resp = requests.get(
                url,
                timeout=60,
                headers={
                    "User-Agent": "SoroJa-Update-Checker/1.0 (contato.soroja@gmail.com)"
                },
            )
            resp.raise_for_status()
        except Exception as exc:
            print(f"  ERROR fetching {uf} PDF: {exc}", file=sys.stderr)
            continue
        out[uf] = hashlib.sha1(resp.content).hexdigest()
    return out


def check_hashes() -> int:
    """Compare live PDF SHA-1 values against data/source_hashes.json."""
    stored = load_source_hashes()
    if not stored:
        print("WARN: data/source_hashes.json is missing; skipping hash check.", file=sys.stderr)
        return 0

    print("Verificando SHA dos PDFs ao vivo (pode demorar)…")
    live = fetch_live_pdf_hashes()
    drift = []
    for uf in sorted(STATE_SLUG):
        stored_hash = stored.get(uf)
        live_hash = live.get(uf)
        if not stored_hash or not live_hash:
            continue
        if stored_hash != live_hash:
            drift.append((uf, stored_hash, live_hash))

    print()
    print(f"PDFs verificados: {len(live)}/27")
    if drift:
        print("🔴 DRIFT BINÁRIO DETECTADO:")
        print("-" * 50)
        for uf, stored_hash, live_hash in drift:
            print(
                f"  {uf}: local sha {stored_hash[:10]} ≠ site sha {live_hash[:10]} — "
                "possível reupload silencioso pelo MS"
            )
    else:
        print("✅ Todos os PDFs do site são idênticos aos que ingerimos.")
    print()
    return len(drift)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check for updated PESA PDFs on the Ministry of Health website."
    )
    parser.add_argument(
        "--hash-check",
        action="store_true",
        help=(
            "Also download every PDF and SHA-compare against "
            "data/source_hashes.json to catch silent re-uploads."
        ),
    )
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)

    local = get_local_dates()
    prev_online = load_previous_online()
    online = scrape_online_dates()
    if not online:
        print("ERROR: failed to scrape any online dates.", file=sys.stderr)
        return 2

    write_online_dates(online)
    change_count = append_history(prev_online, online, date.today())
    write_status_dashboard(local, online)

    mismatch_count = print_human_report(local, online)
    if change_count:
        print(
            f"📝 {change_count} mudança(s) no site detectada(s) e gravada(s) em "
            "data/online_dates_history.jsonl"
        )

    drift_count = 0
    if args.hash_check:
        print()
        drift_count = check_hashes()

    return 0 if mismatch_count == 0 and drift_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
