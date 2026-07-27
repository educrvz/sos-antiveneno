# PESA refresh — batch 9 (MS, SE, AP) — 2026-07-26

Hand-verification of the 2026-07-03 Ministry of Health PDF republish for **MS** (67 rows),
**SE** (17 rows), and **AP** (26 rows), against the current canonical `extracted/{UF}.json`
files. Per-state auto-generated diff reports are at:

- `reports/refresh_diff_MS_2026-07-26.md`
- `reports/refresh_diff_SE_2026-07-26.md`
- `reports/refresh_diff_AP_2026-07-26.md`

Candidate re-extractions (not applied — canonical files untouched):

- `extracted/MS.candidate.json`
- `extracted/SE.candidate.json`
- `extracted/AP.candidate.json`

## Method

For each state, `page.extract_tables()` output was dumped alongside raw `page.extract_text()`
for every page, and municipality/hospital names were cross-checked between the two to catch
the silent-row-drop failure mode seen in the RJ refresh. Antivenom lists were parsed by
splitting on literal commas only (no smart re-splitting), matching the canonicalization
convention already used in `extracted/{UF}.json` (e.g. AP's un-separated
"Aracnídico Escorpiônico" pairs are preserved as a single raw string, matching existing
`source_notes` annotations). A hyphen-line-wrap join fix was applied so phone numbers and
CEPs split across PDF lines (e.g. `3621-\n2719`) reassemble as `3621-2719`, not `3621- 2719`.

## Row counts

| UF | Rows before (canonical) | Rows in new PDF (candidate) | Added | Removed | Changed |
|---|---|---|---|---|---|
| MS | 67 | 67 | 0 | 0 | 0 |
| SE | 17 | 17 | 0 | 0 | 0 |
| AP | 26 | 26 | 0 | 0 | 0 |

**Result: all three states are byte-identical in content to what's already in `extracted/{UF}.json`.**
No hospital additions, no removals, and — critically for Eduardo's ask — **zero antivenom
(soro) list changes** across any of the 110 rows (67+17+26) checked. The 2026-07-03 republish
carried no substantive data changes for MS, SE, or AP.

(Note: `refresh_diff.py` reports AP's "linhas atuais/candidato" as 25, not 26 — this is a tool
artifact, not a data discrepancy. The script indexes rows by CNES, and one AP row — "Companhia
Especial de Fronteira - Clevelância do Norte" in Oiapoque — has a blank CNES in the source PDF
(preserved as `null`, consistent with the existing canonical row and its `source_notes`), so it
is excluded from the CNES-keyed diff on both sides. All 26 rows are present and matched.)

## CNES adicionados (additions)

None in any of the 3 states.

## CNES removidos (removals)

None in any of the 3 states.

## Antivenom (soro) list changes — step 5 of the task

None. No CNES in MS, SE, or AP had a changed `antivenoms_raw` list between the canonical
extraction and the new PDF.

## Notable extraction finding — SE silent row drop (same failure mode as RJ)

`pdfplumber`'s `extract_tables()` on the SE PDF silently dropped **2 of 17 rows**:

- **Page 1**: the table geometry detector returned only 7 rows, starting at "Nossa Senhora da
  Glória" — but `extract_text()` on that same page shows **Neópolis** ("Hospital de Neópolis",
  CNES 2421534) appearing *first*, before Nossa Senhora da Glória. The row was present in the
  PDF's raw text but outside the detected table box.
- **Page 2**: `extract_tables()` returned **zero tables** for the entire page, even though
  `extract_text()` shows one full row — **Simão Dias** ("Unidade de Pronto Atendimento 24H
  Pedro Valadares", CNES 2546000).

Both rows were manually parsed from raw text and cross-checked field-by-field (address, phone,
CNES, antivenom list) against the pre-existing canonical `extracted/SE.json`, where they were
already correctly present — meaning the *previous* extraction had already caught and handled
this same pdfplumber quirk. Had this check been skipped, a naive re-extraction from
`extract_tables()` alone would have wrongly reported both hospitals as "removed by MS."

MS and AP showed no such drops — table row counts matched raw-text municipality counts exactly
on every page for both.

## Overrides

`data/location_overrides.json` has no entries for MS, SE, or AP (0 overrides affected in all
three per-state reports).

## Confidence assessment

**High confidence, no action needed for any of the 3 states.** Extraction was independently
verified page-by-page (tables vs. raw text) rather than trusted from `extract_tables()` alone,
per the RJ lesson. Every field of every row (municipality, hospital name, address, phone, CNES,
antivenom list) was diffed programmatically against canonical and came back identical. The
`extracted/{UF}.json` canonical files require no changes this cycle — the July 2026 republish
did not alter MS, SE, or AP data. No commit/push/pipeline run was performed, per instructions.
