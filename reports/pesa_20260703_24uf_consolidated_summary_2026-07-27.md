# PESA 2026-07-03 refresh — 24-state consolidation (all states except RJ, BA, SP)

Date: 2026-07-27. Method: 12 parallel subagents, one per batch, each hand-verifying 1-3 states against the new MS PDFs in `tmp_pesa_20260703_25uf_pdfs/`, cross-checking `pdfplumber.extract_tables()` against raw `extract_text()` on every page (the lesson from the RJ refresh: table detection silently drops rows outside its geometry), then validating with `scripts/refresh_diff.py`. RJ was already hand-verified and shipped to production separately (see `reports/pesa_20260703_25uf_claude_validation_2026-07-26.md`).

## Headline result

**Across all 24 states (2,018 hospital rows total): zero hospitals added, zero removed, zero antivenom-availability changes.** This directly answers the antivenom comparison request — no hospital's soro coverage changed in this MS republication, anywhere, outside RJ.

| UF | Rows | Added | Removed | Antivenom changes | Other changes |
|---|---:|---:|---:|---:|---|
| AC | 17 | 0 | 0 | 0 | 1 typo fix (address casing) |
| AL | 15 | 0 | 0 | 0 | — |
| AM | 95 | 0 | 0 | 0 | — |
| AP | 26 | 0 | 0 | 0 | — |
| CE | 49 | 0 | 0 | 0 | — |
| DF | 11 | 0 | 0 | 0 | — |
| ES | 61 | 0 | 0 | 0 | — |
| GO | 87 | 0 | 0 | 0 | 2 cosmetic (apostrophe glyph; punctuation typo in antivenom string, same set) |
| MA | 156 | 0 | 0 | 0 | 1 (tool false-positive — pre-existing note text pointed at wrong row) |
| MG | 295 | 0 | 0 | 0 | **1 real: phone DDD (32)→(35) for shared-CNES row 2115786 — flagged, see below** |
| MS | 67 | 0 | 0 | 0 | — |
| MT | 105 | 0 | 0 | 0 | — |
| PA | 172 | 0 | 0 | 0 | — |
| PB | 14 | 0 | 0 | 0 | — |
| PE | 15 | 0 | 0 | 0 | — |
| PI | 17 | 0 | 0 | 0 | 17 note cleanups — PI's new PDF is text-based, OCR no longer needed (see below) |
| PR | 204 | 0 | 0 | 0 | — |
| RN | 5 | 0 | 0 | 0 | — |
| RO | 39 | 0 | 0 | 0 | — |
| RR | 34 | 0 | 0 | 0 | — |
| RS | 65 | 0 | 0 | 0 | 1 cosmetic (apostrophe glyph) |
| SC | 143 | 0 | 0 | 0 | — |
| SE | 17 | 0 | 0 | 0 | — |
| TO | 37 | 0 | 0 | 0 | — |
| **Total** | **2,018** | **0** | **0** | **0** | 22 rows touched, all cosmetic/provenance except 1 |

Numbers re-verified independently by running `scripts/refresh_diff.py --uf {UF} --candidate extracted/{UF}.candidate.json` fresh for all 24 states after the agents finished (not just trusting each agent's self-report).

## Items needing Eduardo's decision

### 1. MG — CNES 2115786 phone DDD changed, likely a Ministry data-entry error
Hospital de Pronto Socorro (Juiz de Fora) — this CNES is shared across 3 facilities (Juiz de Fora, Lavras, Poços de Caldas; documented MG quirk, see CLAUDE.md). New PDF phone: `(35) 3690-8125`, was `(32) 3690-8125`. `(35)` is Lavras/Poços de Caldas's area code, not Juiz de Fora's real DDD (`32`) — looks like the Ministry copy-pasted the wrong row's phone across the 3 shared-CNES entries. **Not auto-applied.** Recommend NOT promoting this specific field until confirmed (a wrong phone number in an emergency app is worse than a stale-but-correct one) — or confirming with the hospital directly.

### 2. RS — CNES 3626245 (HPS Canoas) still unresolved
Per your earlier error-control Sheet report, HPS Canoas may have transferred to "Hospital Nossa Senhora das Graças." The new PDF text was searched exhaustively — zero mentions of "Graças" anywhere in the RS PDF. CNES 3626245 still appears once, under "Hospital de Pronto Socorro de Canoas," unchanged. **This doesn't resolve the report — it only confirms the MS PDF hasn't caught up with whatever change was reported to you.** Still needs your separate call (keep as maintainer-verified override/note, or contact the hospital).

## Notable side-finding: PI no longer needs OCR

The PI (Piauí) PDF has historically been image-based, requiring OCR (poppler/tesseract, not installed on this machine). **The new 2026-07-03 PI PDF is text-based** — pdfplumber extracted it directly, no OCR needed. All 17 rows matched canonical exactly (content-wise); the only diffs are clearing the now-obsolete `source_notes: "V2 PDF used; PI source is image-based"` annotation. This is a genuine operational improvement worth keeping in mind for future refreshes.

## Recurring extraction-tooling finding (not a data problem)

The same `pdfplumber.extract_tables()` row-drop bug found during the RJ refresh recurred in AC (1 row), PE (1), MT (10 of 11 pages!), ES (5), TO (4), SE (2), CE (7), GO (8), AL (1), PR (22) — every dropped row was recovered by hand from raw page text and confirmed to match canonical exactly (i.e., none were real removals, all extraction artifacts). This confirms table-detection unreliability is systemic across the MS PDF format, not a one-off — any future automated refresh MUST cross-check table output against raw text per page, or use a human/agent-verified pass like this one, never trust `extract_tables()` alone.

Two states (MA, GO) also surfaced pre-existing duplicate/shared-CNES data quality issues in the *Ministry's own source data* (not introduced by this refresh) — documented in the per-state reports, unchanged, no action needed.

## Recommendation

Given zero real hospital-data changes (no additions, no removals, no antivenom changes) across all 24 states, and only 1 field-level anomaly (MG phone, flagged not applied) plus pure cosmetic fixes elsewhere:

1. **Safe to promote now:** all 24 `extracted/{UF}.candidate.json` → `extracted/{UF}.json` (cosmetic fixes + confirms current data matches the new PDFs), plus bump `data/source_dates.json` for all 24 states to `2026-07-03`.
2. **No `app/hospitals.json` / `hospitals.json` rebuild needed** — since no field that reaches the published contract actually changed (the only real diff, MG's phone, is being held for your decision, not promoted).
3. **Zero geocoding needed this round** — no new hospitals.
4. Hold MG's phone-DDD anomaly and the RS/HPS Canoas item for your explicit decision before any further action.

## Per-state detail

Full per-state and per-batch reports: `reports/pesa_20260703_batch{1..12}_*_summary.md` and `reports/refresh_diff_{UF}_2026-07-26.md` for all 24 states.
