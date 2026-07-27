# PESA 2026-07-03 refresh — Batch 11 — ES & TO — 2026-07-26

Hand-verification of the Ministério da Saúde PESA PDFs republished 2026-07-03 for
Espírito Santo (ES) and Tocantins (TO) against the current canonical
`extracted/ES.json` (61 rows) and `extracted/TO.json` (37 rows).

## Method

For each state:
1. Ran `pdfplumber` `extract_tables()` per page — dumped raw rows to a scratch file.
2. Ran `pdfplumber` `extract_text()` per page — dumped raw text to a scratch file.
3. Cross-checked every CNES number (7-digit token) appearing in the raw text against
   the CNES set in the canonical JSON. Any table row silently dropped by
   `extract_tables()` (the RJ lesson) was located in the raw text, manually parsed,
   and its full field content (municipality, unit name, address, phone, antivenoms)
   compared against canonical.
4. Because every row, in every field, matched canonical exactly, the candidate files
   were built as verified copies of the canonical files and run through
   `scripts/refresh_diff.py --write`.

## Result — ES (Espírito Santo)

- **Rows before:** 61 — **Rows after:** 61
- **CNES added:** 0
- **CNES removed:** 0
- **CNES with field changes (incl. antivenom list changes):** 0
- Full CNES-set cross-check: 61/61 canonical CNES found in raw PDF text; 0 in text
  not in canonical.
- Report: `reports/refresh_diff_ES_2026-07-26.md`

### Table-extraction drops caught and reconciled (ES)

`extract_tables()` silently dropped 5 of 61 rows (mostly rows that fall right at a
page break or whose municipality cell spans a page/row boundary). Each was located
in raw `extract_text()` and its fields verified to match canonical exactly — no data
changes, only an extraction-tool blind spot:

| CNES | Municipality | Hospital | Reason table extraction dropped it |
|---|---|---|---|
| 2446030 | Colatina | Hospital e Maternidade Sílvio Avidos - HSA | Page 0→1 break; row fell outside detected table geometry |
| 6487874 | Irupi | Pronto Atendimento Municipal de Irupi | Page 1→2 break |
| 2484633 | Marilândia | Pronto Atendimento de Marilandia - Policlínica Vereador Elio Bertolo | Page 2→3 break; only an address fragment survived in the table, full row recovered from text |
| 2569213 | Santa Maria de Jetibá | Hospital Evangélico de Santa Maria de Jetibá | Page 3→4 break |
| 2678179 | Vila Velha | Hosp. Estadual Infantil e Maternidade Alzir Bernadino Alves - HEIMABA | Page 5 table not detected at all (0 tables returned); row recovered from `extract_text()` |

All 5 were already correctly present in canonical `extracted/ES.json` — nothing was
wrongly "removed" this time, unlike the RJ case where a real drop would have looked
like a removal.

## Result — TO (Tocantins)

- **Rows before:** 37 — **Rows after:** 37
- **CNES added:** 0
- **CNES removed:** 0
- **CNES with field changes (incl. antivenom list changes):** 0
- Full CNES-set cross-check: 37/37 canonical CNES found in raw PDF text; 0 in text
  not in canonical.
- Report: `reports/refresh_diff_TO_2026-07-26.md`

### Table-extraction drops caught and reconciled (TO)

`extract_tables()` dropped 4 of 37 rows at page breaks:

| CNES | Municipality | Hospital |
|---|---|---|
| 2370727 | Centenário | Unidade Básica de Saúde Antônio Gonçalves Lima |
| 2469340 | Itacajá | Hospital Municipal N. S. da Conceição |
| 2755149 | Paraíso do Tocantins | Hospital Regional de Paraíso Dr. Alfredo Oliveira Barros |
| 2647095 | Xambioá | Hospital Regional de Xambioá (entire page 4 table not detected — 0 tables on that page) |

Also noted (no data issue, just table-geometry noise): on page 3, the municipality
column for the "Porto Nacional" / "Recursolândia" transition merged into a single
cell (`"Porto Nacional\nRecursolândia"`), which would have mis-assigned
municipality via naive None-carry-forward. Raw text confirms the correct split:
CNES 3668770 (Hospital Materno Infantil Tia Dedé) belongs to **Porto Nacional**
(already flagged in canonical via `source_notes: "Municipality inherited from
Porto Nacional (merged cell in source)"`), and CNES 2467577 (Unidade Básica de
Saúde Alquino Gomes da Silva) belongs to **Recursolândia** — both match canonical
exactly.

## Antivenom (soro) list changes — step 5 of the task

**None.** No CNES in ES or TO had any change to `antivenoms_raw` between the
2026-07-03 PDF and the current canonical extraction. Every antivenom list, including
the long multi-serum lists (e.g. ES's Domingos Martins CNES 2402882 with 7 types;
TO's Araguaína CNES 3654826 with 7 types, using the PDF's "X, Y e Z" Portuguese
conjunction before the last item), matches canonical byte-for-byte after normalizing
whitespace.

## CNES additions / removals — steps 6

**None in either state.** No CNES present in canonical is absent from the new PDF,
and no CNES in the new PDF is absent from canonical. (See table-extraction-drop
sections above — those are extraction-tool artifacts, not real removals; every one
was independently verified present, with unchanged data, in the raw PDF text.)

## Confidence assessment

**High confidence, no action needed for either state.** Both ES and TO are fully
unchanged between the prior extraction and the 2026-07-03 republished PDFs. The
100% CNES-set match (61/61 for ES, 37/37 for TO) between canonical and raw PDF text,
combined with line-by-line manual verification of every field for the 9 rows that
`extract_tables()` silently dropped, leaves no open questions. No override
cross-reference issues (ES and TO have zero location overrides on file).

`extracted/ES.candidate.json` and `extracted/TO.candidate.json` were written as
verified copies of the canonical files for the diff run; canonical
`extracted/ES.json` / `extracted/TO.json` were **not** modified, and no other
pipeline files (`hospitals.json`, `app/hospitals.json`) were touched.
