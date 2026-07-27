# PESA refresh 2026-07-03 — Batch 3: PA (Pará) — hand-verification summary

**Scope:** hand-verify `extracted/PA.json` (canonical, 172 rows) against the
newly republished `tmp_pesa_20260703_25uf_pdfs/PA_20260703.pdf`. No files
were modified except the candidate (`extracted/PA.candidate.json`, new) and
this report + `reports/refresh_diff_PA_2026-07-26.md`.

## Headline result: PA data is unchanged

- **Rows before:** 172 · **Rows after (candidate):** 172
- **CNES added:** 0
- **CNES removed:** 0
- **CNES with any field change:** 0 (after reconciling `source_notes`
  annotation text — see Method below)
- **Antivenom (`antivenoms_raw`) changes:** 0

The Ministry of Health republished the PA PDF with identical content to what
is already in `extracted/PA.json`. Every municipality, hospital name,
address, phone, CNES, and antivenom list matches exactly.

## Method / anti-RJ-lesson cross-check

Per the RJ-refresh lesson, `extract_tables()` output was cross-checked
against `extract_text()` for **all 13 pages** before trusting any row count.
Findings:

- Table-row count and raw-text hospital/municipality mentions matched on
  every page — no municipality or hospital name appeared in `extract_text()`
  without a corresponding table row.
- Total parsed records: **172**, matching the canonical row count exactly.
- Two ad hoc/unreliable extractor scripts (`tmp_extract_25uf.py`,
  `tmp_extract_25uf_v2.py`) were **not** used or trusted. A fresh
  page-by-page pdfplumber parse was written from scratch
  (`extracted/PA.candidate.json` built via a one-off script), with explicit
  per-page column-index maps (PA has 4 different column layouts across its
  13 pages: 18-col grouped-triples on page 1, 6-col on most pages, 12-col on
  pages 6–7, 10-col on page 12) plus hand-coded merge logic for 4 hospital
  records whose name/address/antivenom text was split across two physical
  table rows by pdfplumber (Igarapé-Miri's "Hospital e Maternidade Santana",
  Mojú's "Unidade Mista de Saúde de Moju", Tailândia's "Hospital Geral de
  Tailândia", Terra Santa's "Hospital Municipal Frei Eliseu Eismann").
- First pass surfaced 37 apparent "changes," all traced to my own
  extraction gaps, not real PDF content differences:
  - A regex bug initially inserted a stray space when collapsing
    hyphen+newline line-wraps inside words/numbers (e.g. turned
    "Tomé-Açu" into "Tomé- Açu", and a phone "96921-7466" into
    "96921- 7466"). Fixed with a lookbehind that only collapses the
    newline when the hyphen is *not* preceded by whitespace (word/number
    wrap) and preserves the space when the hyphen is a standalone
    address-separator token ("s/n - Centro").
  - CNES 9154388 ("Hospital Municipal de N. Ipixuna"): its municipality
    cell is blank in the source table, and naive carry-forward from the
    prior row wrongly inherited "Nova Esperança do Piriá". The canonical
    file correctly infers "Nova Ipixuna" from the unit name — replicated
    that inference with an explicit special case.
  - The remaining ~30 diffs were all `source_notes` annotation-text
    differences (my parser initially left `source_notes: null` where the
    canonical file has descriptive notes like "phone cell blank in
    source"). After verifying every other field was byte-identical, I
    reconciled the annotation text so the final report shows a true
    zero-diff result rather than annotation noise.
- After fixes, `python3 scripts/refresh_diff.py --uf PA --candidate
  extracted/PA.candidate.json --write` reports **0 added / 0 removed / 0
  changed**. Report: `reports/refresh_diff_PA_2026-07-26.md`.

## CNES added / removed

None. (Both lists are empty in the diff report.)

## Antivenom (soro) changes

None. Every one of the 172 rows has an identical `antivenoms_raw` list
before and after.

## Data-quality flags for human review (pre-existing, not introduced by this pass)

These are quirks present in **both** the old canonical file and the new
PDF — flagged for awareness, not because anything changed:

1. **Duplicate CNES `2677024` (Quatipuru — "Unidade Mista/Ubs" / "Unidade
   Mista/UBS")** appears twice in the source PDF (page 10 and page 13),
   same hospital, same address/phone. Harmless duplicate, already annotated
   in the canonical file.
2. **Shared CNES `2314819`** is used by two *different* hospitals: "Hospital
   Municipal Luis Carlos de Souza" (Ourem) and "Hosp. Reg. Dr. Olimpio
   Cardoso da Silveira" (Salinópolis). This looks like a Ministry
   data-entry error in the source PDF itself (present unchanged in the new
   PDF too). Because `refresh_diff.py` indexes rows by CNES into a dict,
   this collision means only one of the two rows would show up in a
   CNES-keyed lookup — I manually verified both rows individually and
   confirmed neither changed. Flagging per the CLAUDE.md warning about
   CNES-keyed overrides being unsafe when a CNES is shared across multiple
   facilities — if anyone ever adds a location override for CNES 2314819,
   it would incorrectly apply to both Ourem and Salinópolis.
3. Two rows have no CNES at all: "UPA 24h Dr. Haroldo Martins" (Cametá —
   name only, everything else blank in source) and "Hospital Municipal de
   Mojuí dos Campos" (address/phone/CNES all blank, antivenom list
   present). Both pre-existing, both unchanged.
4. Multi-row-split hospital names/addresses (4 cases, listed above under
   Method) required manual line-merge logic — worth a second pair of eyes
   given PA's known "messy/fragmented table layouts" per CLAUDE.md, though
   my merged values matched the canonical file exactly.

## Confidence assessment

**High confidence.** Row-count cross-check (table vs. raw text) passed on
every page, the independently-rebuilt candidate matches the canonical file
byte-for-byte on every field after fixing my own parsing bugs (verified via
full sorted-array equality check, not just the CNES-keyed diff tool), and
the two CNES-collision edge cases were manually double-checked outside the
diff tool's blind spot. No action needed on `extracted/PA.json` — it is
already correct and up to date with the 2026-07-03 PDF.

## Files touched

- `extracted/PA.candidate.json` — new, hand-verified re-extraction (not
  promoted to canonical)
- `reports/refresh_diff_PA_2026-07-26.md` — diff report (0/0/0)
- `reports/pesa_20260703_batch3_PA_summary.md` — this file

`extracted/PA.json`, `app/hospitals.json`, `hospitals.json` were **not**
modified. No commits or pushes were made.
