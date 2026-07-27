# PESA 2026-07-03 refresh — Batch 7: MT, PE, DF

Hand-verification of the Ministério da Saúde PDFs republished 2026-07-03 against the current canonical
`extracted/{UF}.json` files, following the RJ-refresh methodology (cross-check `extract_tables()` output
against `extract_text()` on every page — pdfplumber silently drops rows whose geometry it can't detect).

**Bottom line: no data changes in any of the 3 states.** Row counts, hospital names, addresses, phones,
CNES codes, and antivenom lists are byte-identical to the currently published canonical files. This is a
confirm-and-close batch, not a promote-new-data batch.

---

## DF — Distrito Federal

- Source: `tmp_pesa_20260703_25uf_pdfs/DF_20260703.pdf` (2 pages)
- Rows before: 11 | Rows after: 11
- CNES added: 0 | CNES removed: 0 | CNES field changes: 0
- Antivenom-list changes: **none**

**Extraction notes:** `extract_tables()` on both pages captured all 11 rows correctly this time (unlike
MT/PE below) — no dropped rows detected. Cross-checked every municipality name and CNES appearing in
`extract_text()` against the table rows; all 11 accounted for. All addresses, phones, and antivenom lists
match the canonical file exactly, including the pre-existing `source_notes` on CNES 2645157 (Paranoá,
"antivenom list wraps across pages 1-2"), which was preserved.

**Confidence: high.** Straightforward extraction, full text/table agreement, zero discrepancies.

---

## PE — Pernambuco

- Source: `tmp_pesa_20260703_25uf_pdfs/PE_20260703.pdf` (2 pages)
- Rows before: 15 | Rows after: 15
- CNES added: 0 | CNES removed: 0 | CNES field changes: 0
- Antivenom-list changes: **none**

**Extraction notes — RJ-style dropped row confirmed:** page 2's `extract_tables()` output was missing the
first data row — **Petrolina / Hospital Universitário de Petrolina (HU-UNIVASF), CNES 6042414** — which is
clearly present in `extract_text()` for that page ("Hospital Universitário de ... Petrolina (HU-UNIVASF) ...
6501/6526 6042414 ..."). Manually parsed that row from the raw text (municipality Petrolina, address
"Avenida José de Sá Maniçoba, s/n - Centro", phone "(87) 2101-6501/6526", antivenoms Botrópico/Crotálico/
Elapídico/Escorpiônico/Fonêutrico/Loxoscélico) and it matches the canonical entry for that CNES exactly —
this row was already correctly captured in the current canonical file, so nothing changes; this only
confirms extract_tables() would have wrongly dropped it if trusted blindly.

**Confidence: high.** All 15 CNES, including the one requiring manual text-parsing, match canonical exactly.

---

## MT — Mato Grosso (largest batch, 105 rows, 11 pages)

- Source: `tmp_pesa_20260703_25uf_pdfs/MT_20260703.pdf` (11 pages)
- Rows before: 105 | Rows after: 105
- CNES added: 0 | CNES removed: 0 | CNES field changes: 0
- Antivenom-list changes: **none**

**Extraction notes — systematic dropped-row pattern:** `extract_tables()` dropped the **first data row of
every page except page 0** (10 of 11 pages affected — a consistent pattern, likely because the first
in-flow row of each page starts mid-way through a wrapped multi-line cell whose top edge pdfplumber
misjudges). All 10 were manually parsed from `extract_text()` and cross-checked field-by-field against the
canonical file:

| Page | Dropped municipality | Hospital | CNES |
|---|---|---|---|
| 1 | Araguaiana | Unidade de Pronto Atendimento | 7257155 |
| 2 | Cáceres (2nd facility) | Hospital Regional | 2534460 |
| 3 | Colíder | Hospital Regional | 2392410 |
| 4 | Guarantã do Norte | Hospital Municipal Nossa Senhora do Rosário | 2392046 |
| 5 | Juscimeira | Hospital Municipal Johannes Berthold Henning | 2396092 |
| 6 | Nova Maringá | Unidade Pronto Atendimento | 5146437 |
| 7 | Paranaita | Hospital Municipal Alipio Candido da Silva | 2471604 |
| 8 | Reserva do Cabaçal | PSF Adalto Ribeiro | 2393913 |
| 9 | Salto do Céu | Hospital Municipal | 2394189 |
| 10 | Sorriso | Hospital Regional | 2795655 |

All 10 reconstructed rows match the canonical file's existing entries exactly (municipality, unit name,
address, phone, CNES, antivenom list) — confirming the current canonical MT.json already has these correct
(they were presumably manually recovered in a past extraction pass), and the new PDF changed nothing about
them.

For the 95 rows extract_tables() *did* capture, a full positional diff against canonical initially surfaced
9 false-positive differences — all whitespace/quote-character artifacts from naive `\n`→space joining across
wrapped cells (e.g. `s/n-Alvorado` vs `s/n- Alvorado`, curly vs straight quote in `"São Lucas"`), not content
changes. Normalized to canonical's formatting; zero real diffs remain.

**One self-caught extraction bug:** my first candidate build set `source_notes: null` uniformly instead of
preserving the two existing maintainer annotations in canonical MT.json:
- CNES 2472791 (Hospital Municipal Cristo Rei, Ribeirão Cascalheira): `"source typo 'Escopiônico' preserved"`
- CNES 3028925 (Unidade de Pronto Atendimento, Rondonópolis): `"same CNES as Hospital da Criança Wilma Bohac Francisco"`

Both notes describe genuine source-data quirks still present in the new PDF (the "Escopiônico" typo is
literally in the new PDF's antivenom text for that row, and the duplicate CNES 3028925 across two
Rondonópolis facilities is also still present). Restored both notes in the candidate before running the
diff tool; `refresh_diff.py` then reported zero CNES-level changes, confirming the fix.

Note the diff tool's CNES-indexed counts show "103" lines (not 105) for both old and new — this is because
CNES 3028925 and 9204970 are each shared by two different facilities in the source data (Rondonópolis has 4
facilities but 3 unique CNES; campo Novo do Parecis/Barra do Bugres share CNES 9204970), which collapses in a
CNES-keyed dict. This is a pre-existing characteristic of the source data, not a discrepancy introduced by
this refresh — the row-level (positional) comparison, which correctly preserves all 105 rows, showed zero
differences.

**Confidence: high**, with one caveat worth a human glance: the CNES 9204970 duplicate (Barra do Bugres AND
campo Novo do Parecis both listed under that CNES with different addresses/phones) looks like it could be a
genuine Ministry-side data-entry error rather than an intentional shared-facility CNES — this predates this
refresh (it's identical in the current canonical file) so it's flagged here for awareness, not as a new
issue to fix.

---

## Overrides cross-reference

`data/location_overrides.json` was checked by `refresh_diff.py`'s built-in override-audit step for all 3
states — **0 overrides apply to MT, PE, or DF.** No override-validity concerns to review.

---

## Files touched

- `extracted/DF.candidate.json`, `extracted/PE.candidate.json`, `extracted/MT.candidate.json` — new
  hand-verified candidates (not promoted to canonical)
- `reports/refresh_diff_DF_2026-07-26.md`, `reports/refresh_diff_PE_2026-07-26.md`,
  `reports/refresh_diff_MT_2026-07-26.md` — generated by `scripts/refresh_diff.py`
- `reports/pesa_20260703_batch7_MT_PE_DF_summary.md` — this file

**Canonical files (`extracted/DF.json`, `extracted/PE.json`, `extracted/MT.json`) were NOT modified.**
No commit/push performed, no pipeline run, no geocoding attempted, per task instructions.
