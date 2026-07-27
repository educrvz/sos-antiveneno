# PESA refresh — 2026-07-03 republish — Batch 1/2: CE, RR

Hand-verification of the Ministério da Saúde PESA PDFs republished 2026-07-03 for Ceará (CE) and Roraima (RR), against the current canonical `extracted/CE.json` and `extracted/RR.json`. Source PDFs: `tmp_pesa_20260703_25uf_pdfs/CE_20260703.pdf`, `tmp_pesa_20260703_25uf_pdfs/RR_20260703.pdf`.

**Bottom line: no data changes in either state.** Both PDFs are, byte-for-byte in content, the same dataset already captured in the canonical files. 0 additions, 0 removals, 0 field changes (including antivenom lists) in both states.

## Method

For each state: extracted every page with pdfplumber's `extract_tables()` AND `extract_text()`, and cross-checked hospital/municipality names between the two to catch the RJ-style silent table-geometry drops. Built `extracted/{UF}.candidate.json` by hand from the raw text/table cells (not from the unreliable `tmp_extract_25uf*.py` scripts), then ran `scripts/refresh_diff.py --uf {UF} --candidate ... --write`.

## CE — Ceará

- Rows before: 49. Rows after (candidate): 49.
- CNES added: 0. CNES removed: 0. CNES with field changes: 0.
- **Table-extraction drop confirmed and corrected**, same failure mode as RJ: `extract_tables()` returned only 42 of the 49 data rows. 7 rows were present in `extract_text()` but silently absent from the table geometry on 6 of the 8 pages:
  - Brejo Santo — Hospital Geral de Brejo Santo (CNES 2480646), page 1
  - Crato — Hospital e Maternidade São Francisco de Assis (CNES 2415488), page 2
  - Icó — Hospital Regional de Icó Prefeito Walfrido Monteiro Sobrinho (CNES 2611309), page 3
  - Jucás — Hospital Municipal José Facundo Filho (CNES 5077680), page 4
  - Pedra Branca — Hospital Municipal São Sebastião (CNES 2723255), page 5
  - Russas — Hospital e Casa de Saúde de Russas (CNES 2328003), page 6
  - Tauá — Hospital Regional e Maternidade Alberto Feitosa Lima (CNES 2328046), page 7

  All 7 were manually parsed from `extract_text()` and included in the candidate. All 7 already exist in the canonical `extracted/CE.json` with identical field values — meaning the 2026-07-03 PDF reproduces the same content the canonical file already has, and no "removal" false-positive occurred.
- Antivenom-list changes: none. All 49 CNES have byte-identical `antivenoms_raw` lists between canonical and the new PDF.
- Two pre-existing `source_notes` were carried forward because the underlying anomaly is still present in the new PDF: CNES 2328046 (Tauá) shows area code `(91)` instead of the expected CE code `(88)`; CNES 2333880 (Mombaça) shows a malformed 5-digit phone suffix `22726`. Both are source-PDF quirks, not extraction errors.
- Confidence: **high**. Row count matches exactly (49=49), every field cross-checked against raw PDF text.

## RR — Roraima

- Rows before: 34 (33 unique CNES — see duplicate note below). Rows after (candidate): 34 (33 unique CNES).
- CNES added: 0. CNES removed: 0. CNES with field changes: 0.
- No table-extraction drops this time: `extract_tables()` row counts matched `extract_text()` entry counts on all 3 pages (11 + 13 + 10 = 34), so nothing needed manual recovery — verified by direct comparison anyway per the task's cross-check requirement.
- **Confirmed intentional duplicate, not a data error**: CNES `2319705` (Amajari — Unidade Básica Jacir Vicente IOP) appears twice in both the source PDF and the canonical file — once as a standalone municipal entry (page 1) and again as the group header row preceding the Amajari DSEI Yanomami Polo Base / UBSI listings (page 2). This is the same pattern used for Alto Alegre (CNES 4004876 heads its own DSEI group) and Boa Vista/Pacaraima (DSEI LESTE groups). Verified this dual appearance exists identically in the new PDF text, so it is not a new anomaly.
- Sparse/blank fields (no phone, generic "Distrito Sanitário Especial Indígena YANOMAMI/LESTE" address, municipality inherited from a group header) are expected for the Polo Base / UBSI indigenous units per CLAUDE.md guidance (same pattern as AM/AP) — not treated as defects.
- Antivenom-list changes: none. All 33 unique CNES have byte-identical `antivenoms_raw` lists between canonical and the new PDF, including the non-standard raw strings already present in canonical (e.g. `Botropico-Laquético`, and the Boa Vista DSEI LESTE units' `Antibotrópico / anticrotálico / antibotrópico-crotálico / ...` phrasing, which the build-time canonicalizer routes appropriately — out of scope for this extraction step).
- 19 pre-existing `source_notes` (indigenous polo base / UBSI annotations, blank-phone notes, inherited-municipality notes, and the CNES 2319705 duplicate-entry note) were carried forward unchanged since the same conditions are confirmed present in the new PDF.
- Confidence: **high**. Row/entry counts matched exactly on every page without needing text-recovery, and every field was cross-checked against raw PDF text.

## Antivenom-list changes (Eduardo's specific ask)

**None in either state.** Zero CNES in CE or RR had a changed `antivenoms_raw` list between the current canonical data and the 2026-07-03 PDF republish.

## Low-confidence items for human review

None identified. Both states are exact content matches to canonical; the only "changes" were the intentionally-preserved `source_notes` annotations, not actual data drift.

## Files produced

- `extracted/CE.candidate.json` (49 rows, hand-verified)
- `extracted/RR.candidate.json` (34 rows, hand-verified)
- `reports/refresh_diff_CE_2026-07-26.md`
- `reports/refresh_diff_RR_2026-07-26.md`
- This file: `reports/pesa_20260703_batch12_CE_RR_summary.md`

Canonical files `extracted/CE.json` and `extracted/RR.json` were **not** modified, per instructions. No pipeline stages, geocoding, `app/hospitals.json`/`hospitals.json`, or git operations were run.
