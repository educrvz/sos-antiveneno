#!/usr/bin/env python3
"""
Check for updated PESA PDFs on the Ministry of Health website.

Compares the dates we have (from `data/source_dates.json`) against the
dates currently shown on the gov.br listing for every state. Persists
the scraped website state to `data/online_dates.json` and appends any
day-over-day changes to `data/online_dates_history.jsonl`, so the git
history becomes the audit trail. Regenerates `data/dates_status.md` as
a side-by-side dashboard committed alongside.

Exit code is 0 when we're up to date with the website, non-zero when
the website is ahead — the CI workflow uses that to open an issue.

Usage:
    python3 scripts/check_updates.py

Source pages:
    Page 1: https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia
    Page 2: https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia?b_start:int=15
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DATA_DIR = os.path.join(ROOT, "data")

SOURCE_DATES = os.path.join(DATA_DIR, "source_dates.json")
SOURCE_HASHES = os.path.join(DATA_DIR, "source_hashes.json")
ONLINE_DATES = os.path.join(DATA_DIR, "online_dates.json")
ONLINE_HISTORY = os.path.join(DATA_DIR, "online_dates_history.jsonl")
STATUS_MD = os.path.join(DATA_DIR, "dates_status.md")

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
    "AC": "acre", "AL": "alagoas", "AM": "amazonas", "AP": "amapa",
    "BA": "bahia", "CE": "ceara", "DF": "distrito-federal",
    "ES": "espirito-santo", "GO": "goias", "MA": "maranhao",
    "MG": "minas-gerais", "MS": "mato-grosso-do-sul", "MT": "mato-grosso",
    "PA": "para", "PB": "paraiba", "PE": "pernambuco", "PI": "piaui",
    "PR": "parana", "RJ": "rio-de-janeiro", "RN": "rio-grande-do-norte",
    "RO": "rondonia", "RR": "roraima", "RS": "rio-grande-do-sul",
    "SC": "santa-catarina", "SE": "sergipe", "SP": "sao-paulo",
    "TO": "tocantins",
}
PDF_DOWNLOAD = (
    "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos"
    "/hospitais-de-referencia/{slug}/@@download/file"
)

STATE_CODES = {
    "Acre": "AC", "Alagoas": "AL", "Amapá": "AP", "Amazonas": "AM",
    "Bahia": "BA", "Ceará": "CE", "Distrito Federal": "DF",
    "Espírito Santo": "ES", "Goiás": "GO", "Maranhão": "MA",
    "Mato Grosso do Sul": "MS", "Mato Grosso": "MT", "Minas Gerais": "MG",
    "Pará": "PA", "Paraíba": "PB", "Paraná": "PR", "Pernambuco": "PE",
    "Piauí": "PI", "Rio de Janeiro": "RJ", "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS", "Rondônia": "RO", "Roraima": "RR",
    "Santa Catarina": "SC", "São Paulo": "SP", "Sergipe": "SE",
    "Tocantins": "TO",
}


def load_source_dates() -> dict:
    """Read what we've ingested from data/source_dates.json (UF → YYYY-MM-DD)."""
    if not os.path.exists(SOURCE_DATES):
        return {}
    with open(SOURCE_DATES, encoding="utf-8") as fh:
        return json.load(fh)


def load_source_hashes() -> dict:
    """SHA-1 of every state PDF we've ingested. Used by --hash-check to detect
    silent re-uploads where gov.br swaps PDF bytes without bumping the
    'publicado em' date.
    """
    if not os.path.exists(SOURCE_HASHES):
        return {}
    with open(SOURCE_HASHES, encoding="utf-8") as fh:
        return json.load(fh)


def fetch_live_pdf_hashes() -> dict:
    """Download each state PDF from gov.br and return UF → sha1 hex digest.
    Errors per state are logged to stderr and yield no entry (treated as
    'unknown' rather than 'changed')."""
    out = {}
    for uf, slug in STATE_SLUG.items():
        url = PDF_DOWNLOAD.format(slug=slug)
        try:
            resp = requests.get(url, timeout=60, headers={
                "User-Agent": "SoroJa-Update-Checker/1.0 (contato.soroja@gmail.com)"
            })
            resp.raise_for_status()
        except Exception as e:
            print(f"  ERROR fetching {uf} PDF: {e}", file=sys.stderr)
            continue
        out[uf] = hashlib.sha1(resp.content).hexdigest()
    return out


def load_previous_online() -> dict:
    """Load the prior online snapshot so we can diff."""
    if not os.path.exists(ONLINE_DATES):
        return {}
    with open(ONLINE_DATES, encoding="utf-8") as fh:
        return json.load(fh)


def scrape_online_dates() -> dict:
    """Scrape the gov.br pages for the publication date next to each state."""
    online = {}
    for url in PAGES:
        try:
            resp = requests.get(url, timeout=30, headers={
                "User-Agent": "SoroJa-Update-Checker/1.0 (contato.soroja@gmail.com)"
            })
            resp.raise_for_status()
        except Exception as e:
            print(f"  ERROR fetching {url}: {e}", file=sys.stderr)
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()

        # Page format: "<StateName>...publicado DD/MM/YYYY..." within ~200 chars.
        for state_name, code in STATE_CODES.items():
            pattern = re.compile(
                re.escape(state_name) + r".{1,200}?publicado\s+(\d{2}/\d{2}/\d{4})",
                re.DOTALL,
            )
            match = pattern.search(text)
            if match:
                try:
                    d = datetime.strptime(match.group(1), "%d/%m/%Y").date()
                    online[code] = d.isoformat()
                except ValueError:
                    pass

    return online


def write_online_dates(online: dict) -> None:
    """Persist current website state. Sorted keys → stable diff."""
    payload = {uf: online[uf] for uf in sorted(online)}
    with open(ONLINE_DATES, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def append_history(prev: dict, curr: dict, detected_at: date) -> int:
    """Append one row per state whose date changed. Returns number of changes.

    On the very first run, `prev` is empty — we treat that as establishing
    the baseline rather than logging 27 phantom "null → date" transitions.
    """
    if not prev:
        return 0
    changes = []
    all_ufs = set(prev) | set(curr)
    for uf in sorted(all_ufs):
        before = prev.get(uf)
        after = curr.get(uf)
        if before == after:
            continue
        changes.append({
            "detected_at": detected_at.isoformat(),
            "uf": uf,
            "from": before,
            "to": after,
        })
    if changes:
        with open(ONLINE_HISTORY, "a", encoding="utf-8") as fh:
            for c in changes:
                fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    return len(changes)


def write_status_dashboard(local: dict, online: dict) -> None:
    """Side-by-side dashboard committed to the repo. No timestamps inside —
    git history is the timeline.
    """
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
    counts = {"match": 0, "ms_newer": 0, "we_newer": 0, "missing_local": 0, "missing_online": 0}
    for state_name, uf in sorted(STATE_CODES.items(), key=lambda kv: kv[1]):
        ours = local.get(uf)
        theirs = online.get(uf)
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
        rows.append(f"| {uf} | {state_name} | {ours or '—'} | {theirs or '—'} | {status} |")

    lines.extend(rows)
    lines.extend([
        "",
        f"**Resumo:** {counts['match']} em dia · {counts['ms_newer']} site mais novo · "
        f"{counts['we_newer']} nosso mais novo · {counts['missing_local']} faltam aqui · "
        f"{counts['missing_online']} faltam no site",
        "",
    ])
    with open(STATUS_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def print_human_report(local: dict, online: dict) -> int:
    """Stdout for CI logs + humans. Returns count of states where MS is ahead."""
    print("=" * 60)
    print("  SoroJá — Verificador de Atualizações PESA")
    print("=" * 60)
    print()
    print(f"Estados na nossa base: {len(local)}/27")
    print(f"Estados encontrados no site MS: {len(online)}/27")
    print()

    updates_needed = []
    we_ahead = []
    for uf in sorted(STATE_CODES.values()):
        ours = local.get(uf)
        theirs = online.get(uf)
        if not ours or not theirs:
            continue
        if theirs > ours:
            updates_needed.append((uf, ours, theirs))
        elif ours > theirs:
            we_ahead.append((uf, ours, theirs))

    if updates_needed:
        print("🔴 ATUALIZAÇÕES DISPONÍVEIS:")
        print("-" * 50)
        for uf, ours, theirs in updates_needed:
            print(f"  {uf}: nossa {ours} → site {theirs} ← NOVO!")
        print()
    else:
        print("✅ Nenhuma atualização disponível.")
        print()

    if we_ahead:
        print("ℹ️  Estados onde nossa data é posterior à do site (investigar):")
        for uf, ours, theirs in we_ahead:
            print(f"  {uf}: nossa {ours} > site {theirs}")
        print()

    print(f"Fonte: {SOURCE_URL}")
    return len(updates_needed)


def check_hashes() -> int:
    """Download every PDF and SHA-compare against data/source_hashes.json.
    Returns the count of states whose binary differs from what we ingested.
    """
    stored = load_source_hashes()
    if not stored:
        print("WARN: data/source_hashes.json is missing; skipping hash check.", file=sys.stderr)
        return 0
    print("Verificando SHA dos PDFs ao vivo (pode demorar)…")
    live = fetch_live_pdf_hashes()
    drift = []
    for uf in sorted(STATE_SLUG):
        s = stored.get(uf)
        l = live.get(uf)
        if not s or not l:
            continue
        if s != l:
            drift.append((uf, s, l))

    print()
    print(f"PDFs verificados: {len(live)}/27")
    if drift:
        print("🔴 DRIFT BINÁRIO DETECTADO:")
        print("-" * 50)
        for uf, s, l in drift:
            print(f"  {uf}: local sha {s[:10]} ≠ site sha {l[:10]} — possível reupload silencioso pelo MS")
    else:
        print("✅ Todos os PDFs do site são idênticos aos que ingerimos.")
    print()
    return len(drift)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1] if __doc__ else None)
    ap.add_argument(
        "--hash-check", action="store_true",
        help="Also download every PDF and SHA-compare against data/source_hashes.json "
             "to catch silent re-uploads. Cheap (~25MB), but slower than the date check.",
    )
    args = ap.parse_args()

    os.makedirs(DATA_DIR, exist_ok=True)
    local = load_source_dates()
    prev_online = load_previous_online()
    online = scrape_online_dates()
    if not online:
        print("ERROR: failed to scrape any online dates.", file=sys.stderr)
        return 2

    write_online_dates(online)
    n_changes = append_history(prev_online, online, date.today())
    write_status_dashboard(local, online)

    updates_needed = print_human_report(local, online)
    if n_changes:
        print(f"\n📝 {n_changes} mudança(s) no site detectada(s) e gravada(s) em data/online_dates_history.jsonl")

    drift_count = 0
    if args.hash_check:
        print()
        drift_count = check_hashes()

    # Exit non-zero if EITHER the website is ahead OR a binary drift was detected.
    return 0 if (updates_needed == 0 and drift_count == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
