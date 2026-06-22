#!/usr/bin/env python3
"""
Diff a candidate updated extraction against the current `extracted/{UF}.json`
and produce a maintainer-reviewable Markdown report.

Built for the "MS published a new PDF for state UF" workflow: after a fresh
extraction lands in `extracted/{UF}.new.json` (or any path you point at),
this tool shows:
  - CNES added (new entries to assess)
  - CNES removed (consider hide override or accept removal)
  - CNES with field changes (review each one)
  - Cross-reference against `data/location_overrides.json` so every prior
    community correction in this UF is surfaced — never silently dropped

The tool DOES NOT modify any source-of-truth file. It only reads + writes
a report at `reports/refresh_diff_{UF}_{YYYY-MM-DD}.md` (or stdout).

Usage:
    # write report to reports/refresh_diff_MG_2026-05-12.md
    python3 scripts/refresh_diff.py --uf MG --candidate extracted/MG.new.json --write

    # or to stdout
    python3 scripts/refresh_diff.py --uf MG --candidate extracted/MG.new.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = ROOT / "extracted"
OVERRIDES_PATH = ROOT / "data" / "location_overrides.json"
REPORTS_DIR = ROOT / "reports"
PUBLISHED_PATH = ROOT / "app" / "hospitals.json"

# Fields we compare row-to-row when the same CNES appears on both sides.
# `cnes`, `state` are identifiers, not change-tracked.
COMPARE_FIELDS = [
    "health_unit_name",
    "municipality",
    "address",
    "phones_raw",
    "antivenoms_raw",
    "source_notes",
]


def load_json(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _safe_rel(path: Path) -> str:
    """Render path relative to ROOT when possible, else absolute."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def index_by_cnes(rows: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in rows:
        cnes = str(r.get("cnes") or "").strip()
        if cnes:
            out[cnes] = r
    return out


def diff_rows(old: dict[str, dict], new: dict[str, dict]) -> dict:
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = []
    for cnes in sorted(set(old) & set(new)):
        diffs = []
        for f in COMPARE_FIELDS:
            o = old[cnes].get(f)
            n = new[cnes].get(f)
            if o != n:
                diffs.append((f, o, n))
        if diffs:
            changed.append((cnes, diffs))
    return {"added": added, "removed": removed, "changed": changed}


def format_value(v) -> str:
    if v is None:
        return "*(vazio)*"
    if isinstance(v, list):
        return ", ".join(str(x) for x in v) if v else "*(vazio)*"
    return str(v).replace("|", "\\|").replace("\n", " ")


def cross_reference_overrides(uf: str, old: dict, new: dict, overrides: dict,
                              published_by_cnes: dict) -> list[dict]:
    """For every override whose CNES belongs to this UF (per old extraction OR
    currently-published data), describe its current state and a recommendation.
    """
    audit = []
    for cnes, ov in overrides.items():
        # Determine if this override belongs to this UF
        in_old = cnes in old
        in_new = cnes in new
        pub_row = published_by_cnes.get(cnes)
        # The override applies to this UF if the CNES is in this state's data
        ms_state = (pub_row.get("state") if pub_row else None) or ""
        if not in_old and not in_new and ms_state != uf:
            continue

        # Build status
        kinds = []
        if ov.get("hide"):
            kinds.append("hide")
        if "lat" in ov:
            kinds.append("lat/lng")
        if "address" in ov:
            kinds.append("address")
        if "note" in ov:
            kinds.append("note")

        if in_old and not in_new:
            status = "🔴 CNES removido pelo MS — override pode ser retirado se a unidade realmente sumiu, ou convertido em `hide` com nota explicativa."
        elif not in_old and in_new:
            status = "ℹ️ CNES novo no MS — confira se o override ainda faz sentido (improvável; raríssimo override em CNES que não existia)."
        else:
            # Both sides — see if the changed fields touch what the override addresses
            changes = []
            for f in COMPARE_FIELDS:
                o = old[cnes].get(f); n = new[cnes].get(f)
                if o != n:
                    changes.append(f)
            if not changes:
                status = "✅ MS inalterado — override segue válido."
            else:
                concerns = []
                if "address" in changes and ("address" in ov or "lat" in ov):
                    concerns.append("MS mudou endereço — re-verificar lat/lng e address override")
                if "phones_raw" in changes and ov.get("note"):
                    concerns.append("MS mudou telefone — checar se nota comunitária ficou redundante/contradita")
                if "antivenoms_raw" in changes and ov.get("note"):
                    concerns.append("MS mudou lista de soros — checar se nota ficou redundante/contradita")
                if "health_unit_name" in changes and ov.get("note"):
                    concerns.append("MS mudou nome da unidade — checar se nota ainda se aplica")
                if concerns:
                    status = "🟡 REVISAR — " + "; ".join(concerns)
                else:
                    status = f"ℹ️ MS mudou ({', '.join(changes)}), mas nenhum campo do override é afetado diretamente."

        audit.append({
            "cnes": cnes,
            "kinds": kinds,
            "reason": ov.get("reason", ""),
            "status": status,
            "old_row": old.get(cnes),
            "new_row": new.get(cnes),
        })
    return audit


def emit_markdown(uf: str, candidate_path: Path, old: dict, new: dict,
                  diff: dict, audit: list[dict]) -> str:
    today = date.today().isoformat()
    L: list[str] = []
    L.append(f"# Refresh diff — {uf} — {today}")
    L.append("")
    L.append(f"- **Candidato:** `{_safe_rel(candidate_path)}`")
    L.append(f"- **Atual:** `extracted/{uf}.json`")
    L.append(f"- **Linhas atuais:** {len(old)}")
    L.append(f"- **Linhas no candidato:** {len(new)}")
    L.append(f"- **CNES adicionados:** {len(diff['added'])}")
    L.append(f"- **CNES removidos:** {len(diff['removed'])}")
    L.append(f"- **CNES alterados:** {len(diff['changed'])}")
    L.append(f"- **Overrides desta UF afetados:** {len(audit)}")
    L.append("")
    L.append("> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.")
    L.append("")

    # --- Added ---
    L.append("## CNES adicionados")
    L.append("")
    if not diff["added"]:
        L.append("Nenhum.")
    else:
        L.append("| CNES | Município | Nome | Endereço | Soros |")
        L.append("|---|---|---|---|---|")
        for cnes in diff["added"]:
            r = new[cnes]
            L.append(f"| {cnes} | {format_value(r.get('municipality'))} | {format_value(r.get('health_unit_name'))} | {format_value(r.get('address'))} | {format_value(r.get('antivenoms_raw'))} |")
    L.append("")

    # --- Removed ---
    L.append("## CNES removidos")
    L.append("")
    if not diff["removed"]:
        L.append("Nenhum.")
    else:
        L.append("| CNES | Município | Nome | Endereço | Soros |")
        L.append("|---|---|---|---|---|")
        for cnes in diff["removed"]:
            r = old[cnes]
            L.append(f"| {cnes} | {format_value(r.get('municipality'))} | {format_value(r.get('health_unit_name'))} | {format_value(r.get('address'))} | {format_value(r.get('antivenoms_raw'))} |")
    L.append("")

    # --- Changed ---
    L.append("## CNES alterados")
    L.append("")
    if not diff["changed"]:
        L.append("Nenhum.")
    else:
        for cnes, changes in diff["changed"]:
            r = new[cnes]
            L.append(f"### {cnes} — {format_value(r.get('health_unit_name'))} ({format_value(r.get('municipality'))})")
            L.append("")
            L.append("| Campo | Antes | Depois |")
            L.append("|---|---|---|")
            for f, o, n in changes:
                L.append(f"| `{f}` | {format_value(o)} | {format_value(n)} |")
            L.append("")

    # --- Override audit ---
    L.append("## Auditoria de overrides")
    L.append("")
    L.append("Para cada override desta UF, comparação com o MS atualizado.")
    L.append("Decida manualmente se cada um continua válido antes de promover o candidato.")
    L.append("")
    if not audit:
        L.append("Nenhum override aplicável a esta UF.")
    else:
        for a in audit:
            L.append(f"### CNES {a['cnes']} — tipos: {', '.join(a['kinds']) or '(vazio)'}")
            L.append("")
            L.append(f"**Status:** {a['status']}")
            L.append("")
            if a["reason"]:
                L.append(f"**Reason gravado:** {a['reason']}")
                L.append("")

    L.append("---")
    L.append("")
    L.append("Próximos passos sugeridos:")
    L.append("")
    L.append("1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.")
    L.append("2. Aplicar ajustes manuais no candidato se necessário.")
    L.append(f"3. Substituir: `cp {_safe_rel(candidate_path)} extracted/{uf}.json`")
    L.append(f"4. Atualizar `data/source_dates.json` com a nova data do MS.")
    L.append("5. Rodar `./scripts/refresh_dataset.sh`.")
    L.append("6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).")
    L.append("7. Commit + push.")
    L.append("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Diff a candidate extraction against the canonical one.")
    ap.add_argument("--uf", required=True, help="State code, e.g. MG")
    ap.add_argument("--candidate", required=True, type=Path,
                    help="Path to candidate extracted JSON, e.g. extracted/MG.new.json")
    ap.add_argument("--write", action="store_true",
                    help="Write report to reports/refresh_diff_{UF}_{date}.md instead of stdout")
    args = ap.parse_args()

    uf = args.uf.strip().upper()
    canonical_path = EXTRACTED_DIR / f"{uf}.json"
    if not canonical_path.exists():
        print(f"ERROR: {canonical_path} not found.", file=sys.stderr)
        return 2
    if not args.candidate.exists():
        print(f"ERROR: candidate {args.candidate} not found.", file=sys.stderr)
        return 2

    old_rows = load_json(canonical_path)
    new_rows = load_json(args.candidate)
    old = index_by_cnes(old_rows)
    new = index_by_cnes(new_rows)
    diff = diff_rows(old, new)

    overrides = load_json(OVERRIDES_PATH) if OVERRIDES_PATH.exists() else {}
    published = load_json(PUBLISHED_PATH) if PUBLISHED_PATH.exists() else []
    pub_by_cnes = {str(r.get("cnes") or ""): r for r in published if r.get("cnes")}
    audit = cross_reference_overrides(uf, old, new, overrides, pub_by_cnes)

    md = emit_markdown(uf, args.candidate, old, new, diff, audit)

    if args.write:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        out = REPORTS_DIR / f"refresh_diff_{uf}_{date.today().isoformat()}.md"
        out.write_text(md, encoding="utf-8")
        print(f"Wrote {out}")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
