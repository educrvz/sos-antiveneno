# PESA 2026-07-03 refresh — PR (Paraná) — hand-verification summary

- **Source PDF:** `tmp_pesa_20260703_25uf_pdfs/PR_20260703.pdf` (23 pages)
- **Canonical (before):** `extracted/PR.json` — 204 rows
- **Candidate (after):** `extracted/PR.candidate.json` — 204 rows
- **Diff report:** `reports/refresh_diff_PR_2026-07-26.md`

## Headline result

**Zero substantive changes.** After full hand-verified re-extraction, all 204
CNES match the canonical file exactly on every compared field
(`municipality`, `health_unit_name`, `address`, `phones_raw`,
`antivenoms_raw`, `source_notes`). `scripts/refresh_diff.py` confirms:

- CNES adicionados: **0**
- CNES removidos: **0**
- CNES alterados: **0**
- Antivenom-list changes: **0**

The July 3, 2026 PR PDF appears to be a re-publication of the same dataset
with no content changes for this state.

## Why this wasn't a trivial 1:1 table dump — the RJ-style traps found

`page.extract_tables()` on this PDF silently drops data exactly like it did
for RJ. Two distinct bugs were found and hand-fixed by cross-checking
`page.extract_text()` / raw word positions against every page, and
cross-referencing candidates against the canonical file:

1. **One row silently dropped at the top of every page, pages 1–22 (22
   rows total).** The row's vertical zone (y ≈ 72–123) sits just above the
   bbox `find_tables()` detects for that page's table, so `extract_tables()`
   never returns it — even though the column-divider rects are present in
   that zone. Confirmed via `page.rects` and reconstructed each dropped row
   by cropping columns directly (known x-boundaries: `15.4, 114.6, 270.5,
   433.6, 525.7, 587.2, 823.3`). One of these (CNES `2753804`, Terra Rica)
   is the RJ-style case: a **pre-existing** hospital that would have been
   wrongly reported as "removed" if the drop had gone unnoticed.

2. **Two garbled row-merges (pages 12 and 18).** A row with a *blank
   antivenoms cell* shifts column boundaries enough that `extract_tables()`
   fuses it with the following row into one unparseable cell (CNES column
   returns `None`, so both hospitals in the merge would have been silently
   dropped by a naive `if not cnes: continue` guard):
   - Page 12: **Missal** / Hospital e Maternidade Nossa Srª de Fátima (CNES
     `2575957`, blank antivenoms) merged with **Morretes** / Hospital e
     Maternidade Municipal Dr. Alcídio Bortolin (CNES `2687119`). Both
     hand-reconstructed from `page.extract_text()`.
   - Page 18: **Santo Antonio da Platina** / Hospital Regional do Norte
     Pioneiro (CNES `3316300`, blank antivenoms) merged with **Santo
     Antônio do Sudoeste** / Hospital e Maternidade Santa Izabel (CNES
     `2585057`). Both hand-reconstructed.

3. **Three genuinely blank municipality cells in the source PDF itself**
   (not a pdfplumber bug) — the first hospital of a new municipality group,
   immediately after the page-boundary drop, has no municipality text at
   all in the PDF; naive carry-forward would have wrongly inherited the
   *previous* municipality from the end of the prior page:
   - CNES `2783789` (Santa Casa de Irati) — naive carry would say "Iporã",
     correct is **Irati** (confirmed: same city name is literally embedded
     in the hospital's own name).
   - CNES `17884` (ISSAL Instituto de Saúde São Lucas) — naive carry would
     say "Paranavaí", correct is **Pato Branco**.
   - CNES `2742012` (Hospital Sagrado Coração de Jesus) — naive carry would
     say "Pranchita", correct is **Prudentópolis**.
   All three verified by word-position inspection (`page.extract_words()`)
   confirming the municipio column is empty in that exact row, and by
   cross-checking the resulting municipality against canonical.

Total row accounting: page 0 contributes 10 rows (title/header stripped);
pages 1–22 contribute 172 table rows + 22 reconstructed drops; plus the
Missal + Santo Antônio do Sudoeste rows recovered from the two garbled
merges = **204**, matching canonical exactly.

## CNES adicionados / removidos

None. (No sanity-check against raw text needed beyond the above — the
tables match 1:1 by CNES set with zero extras/missing.)

## Antivenom-list changes (`antivenoms_raw`)

None. Every one of the 204 hospitals has an identical antivenom list
before/after.

## Rows with `source_notes` (carried over unchanged from canonical)

9 rows have non-null `source_notes`, all pre-existing conditions in the
source PDF, unchanged from canonical:

| CNES | Municipality | Note |
|---|---|---|
| 2666626 | Dois Vizinhos | municipality inherited (blank in source) |
| 7117485 | Marechal Cândido Rondon | municipality inherited (blank in source) |
| 2740478 | Reserva | municipality inherited (blank in source) |
| 2575957 | Missal | antivenoms cell blank in source |
| 9502440 | Pontal do Paraná | antivenoms cell blank in source |
| 9502459 | Pontal do Paraná | antivenoms cell blank in source |
| 3316300 | Santo Antonio da Platina | antivenoms cell blank in source |
| 6657885 | São Miguel do Iguaçu | antivenoms cell blank in source |
| 2576783 | Sapopema | antivenoms cell blank in source |

## Overrides audit (`data/location_overrides.json`)

2 PR overrides found by `refresh_diff.py`, both still valid (MS data
unchanged underneath them):

- **CNES 2738252** — Hospital do Coração (Cascavel/PR): community reports
  claim demolition/deactivation; override note kept until official MS
  confirmation. MS PDF still lists it unchanged.
- **CNES 2683202** — Hospital Municipal Dr. Amadeu Puppi (Ponta Grossa/PR):
  community report claims care was decentralized to HU-UEPG/UPAs; override
  note kept until official MS confirmation. MS PDF still lists it
  unchanged.

## Confidence assessment / flags for human review

- **High confidence overall.** The extraction was independently rebuilt
  from raw PDF geometry (table cells + column-cropped text + word
  positions), not copied from canonical, and it converges to a 0-diff
  match — a strong cross-check, not a foregone conclusion.
- **Low-confidence items, flagged for a second look:**
  - The 3 "genuinely blank municipality in source" rows (Irati, Pato
    Branco, Prudentópolis anchors) are a real source-PDF oddity, not an
    extraction artifact — worth knowing if a *future* PR refresh needs the
    same manual override list, since a generic pipeline script would get
    these wrong by default.
  - The 2 garbled-merge rows (pages 12 and 18) are hand-typed from
    `page.extract_text()` reading rather than programmatic table cells —
    double-checked character-by-character against the raw text dump and
    against canonical, but flagging since this is the highest-risk manual
    step in the whole extraction.
  - `extracted/PR.json` (canonical) was **not modified** — this candidate
    file is for review only, per the task scope (PR only, batch 2).

## What was NOT touched

Per task scope: `extracted/PR.json` untouched, `app/hospitals.json` /
`hospitals.json` untouched, no geocoding run, no pipeline run, no commits,
no pushes.
