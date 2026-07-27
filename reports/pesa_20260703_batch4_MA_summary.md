# PESA 2026-07-03 refresh — Batch 4 — MA (Maranhão) — hand-verification summary

**Source PDF:** `tmp_pesa_20260703_25uf_pdfs/MA_20260703.pdf` (14 pages)
**Canonical (untouched):** `extracted/MA.json`
**Candidate (new, hand-verified):** `extracted/MA.candidate.json`
**Diff report:** `reports/refresh_diff_MA_2026-07-26.md`

## Row counts

| | Rows | Unique CNES |
|---|---|---|
| Before (`extracted/MA.json`) | 156 | 154 (2 CNES appear twice — see "Known duplicates" below) |
| After (`extracted/MA.candidate.json`) | 156 | 154 |

**CNES added: 0**
**CNES removed: 0**
**Field changes (`CNES alterados`): 1 — and it is not a real MS data change (see below)**
**Antivenom-list (`antivenoms_raw`) changes: 0**

## Method (anti-RJ-lesson cross-check)

Given the documented risk that `pdfplumber.extract_tables()` can silently drop rows, this extraction did **not** rely on `extract_tables()` at all. Instead:

1. Extracted `page.extract_words()` for every page and derived column boundaries (x0 ranges) from the page-1 header row (`MUNICÍPIO`/`UNIDADE DE SAÚDE`/`ENDEREÇO`/`TELEFONES`/`CNES`/`ATENDIMENTOS DISPONÍVEIS`), then verified those boundaries held on continuation pages (no header row) by sampling word x0 clusters on page 2.
2. Grouped words into visual rows by `top` position, assigned each word to a logical column by x0, then partitioned rows into hospital blocks using the **CNES token** (7-digit number) as the block terminator — this correctly handles blocks that span 2, 3, or 4 physical lines (municipality/hospital-name/address wraps).
3. Cross-validated independently with a dumb full-text regex scan (`\b\d{7}\b` over every page's `extract_text()`) — found exactly 156 CNES-like tokens (154 unique), identical set to the word/column-based extraction and identical to `extracted/MA.json`'s CNES set. Two independent extraction methods agree perfectly — no evidence of dropped or hidden rows.
4. For the small number of blocks with a blank municipality cell (shared/merged municipality cell spanning 2 hospitals in the source PDF), inherited the municipality from the next block, matching the exact same resolution already baked into the canonical file for these cases (verified by name: CAXIAS ×2, COLINAS, IMPERATRIZ, NOVA COLINAS, SÃO LUIS, TIMON).
5. Ran `scripts/refresh_diff.py --uf MA --candidate extracted/MA.candidate.json --write` and read the generated report.

## Result: MA data is essentially unchanged from the last extraction

Every one of the 156 rows matches `extracted/MA.json` on `municipality`, `health_unit_name`, `address`, `phones_raw`, and `antivenoms_raw` — field for field, including the exact abbreviation case (`SAEsc` vs `SAESC`), the exact slash- vs comma-separated antivenom notation, and known source quirks like the "SÃO PREDRO DOS CRENTES" (likely typo for SÃO PEDRO) municipality spelling.

### The one flagged "CNES alterados" row is a note-wording difference, not a data change

**CNES 2645424 — Centro de Saúde Candida Silva Rego (NOVA COLINAS)**

| Field | `extracted/MA.json` | `extracted/MA.candidate.json` |
|---|---|---|
| `source_notes` | "phone shown as 'Sem contato'; municipality inherited (blank in source)" | "phone shown as 'Sem contato' in source" |

I independently checked the raw word positions for this row: the token "NOVA COLINAS" (x0=26, top=317) sits directly in this hospital's own physical text row (same row as "Candida Silva Rego ... 2645424"), not blank. The canonical file's note appears to describe the *previous* row (CNES 2655837, "Unidade Mista Casa de Saude Nossa Senhora Santana") which genuinely has a blank municipality cell in the source and inherits "NOVA COLINAS" from this row — and indeed `extracted/MA.json`'s row for 2655837 carries no explanatory note despite also being a blank/inherited case. Net effect: the **value** for both rows (`NOVA COLINAS`) is identical in old and new; only this one row's explanatory annotation text differs. Not a real MS content change — left as informational-only, no action needed. If preferred, the note could simply be reworded to match, but the underlying data is correct either way.

## Antivenom-list (`antivenoms_raw`) changes — Eduardo's specific ask

**None.** Zero hospitals had a changed `antivenoms_raw` list between the old and new PDF. Abbreviation-variant counts across all 156 rows are identical old vs. new: `SABC`×156, `SABL`×156, `SAB`×156, `SAC`×156, `SAAr`×156, `SAE`×149, `SAEsc`×148, `SAESC`×8, `SALon`×5.

## CNES added — none

## CNES removed — none

## Known duplicates in source (preserved, unchanged)

Both pre-existing duplicate CNES in `extracted/MA.json` are present identically in the new PDF:

- **CNES 2451573** — "Hospital Jorge Oliveira" (ARARI) appears twice on page 1 of the source PDF with slightly different address/phone formatting (one row has phone `(98) 3453 1120`, the other has "Sem contato"). Documented in canonical with a `source_notes` explaining the duplicate.
- **CNES 2462095** — shared between two genuinely different hospitals/municipalities: "Hospital e Maternidade Nayla Gonçalo" (BACABEIRA) and "Hospital Municipal Elda Rieiro Fonseca" (HUMBERTO DE CAMPOS). Likely a genuine MS data-entry error (same CNES code reused), preserved as-is since it's a straight transcription of the source, not something this extraction should "fix."

## Override cross-reference

`scripts/refresh_diff.py` found exactly one `location_overrides.json` entry belonging to MA: **CNES 6483089** (Hosp. Macrorregional de Urgência e Emergência de Presidente Dutra / SOCORRÃO — a community-reported phone-number correction from 2026-04-29). Status: **MS unchanged — override remains valid.** Verified this record's full row (4-line wrapped block in the source PDF) matches the canonical file exactly on every field.

## Confidence assessment / flags for human review

- **High confidence overall.** Two independent extraction methods (word/column-position-based block parsing, and a naive full-text CNES regex scan) converged on the same 156 rows / 154 unique CNES, matching `extracted/MA.json` exactly on every substantive field.
- **Low-risk item:** the CNES 2645424 note-wording mismatch described above — cosmetic only, does not affect published data if this candidate is ever promoted.
- **Worth a human glance:** the two pre-existing duplicate-CNES situations (2451573, 2462095) are unchanged carry-overs from the prior extraction, not new — flagging only because duplicate CNES values are inherently a bit fragile for any future CNES-keyed tooling (per the CLAUDE.md warning about not CNES-keying overrides when a CNES is shared across facilities). No action taken; just noting they're still present in the 2026-07-03 PDF.
- No messy table layout, ambiguous line-wrap, or genuinely new/removed hospital was found for MA in this refresh. Nothing else flagged.

## Files touched

- **Created:** `extracted/MA.candidate.json` (156 rows, hand-verified)
- **Created:** `reports/refresh_diff_MA_2026-07-26.md`
- **Created:** this file, `reports/pesa_20260703_batch4_MA_summary.md`
- **Not touched:** `extracted/MA.json`, `app/hospitals.json`, `hospitals.json`, `data/location_overrides.json`, or any pipeline/geocoding step. No commits made.
