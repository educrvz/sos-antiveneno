# PESA refresh 2026-07-03 — Batch 6 — AM, AC, PB

Hand-verification of the Ministério da Saúde's 2026-07-03 PESA republication against
current canonical `extracted/{UF}.json` for **AM** (95 rows), **AC** (17 rows), **PB** (14 rows).

Method: independent re-extraction with pdfplumber `extract_tables()` per page, cross-checked
against `extract_text()` per page (RJ-lesson protocol — table geometry can silently drop rows).
Candidates written to `extracted/{UF}.candidate.json`, diffed with
`scripts/refresh_diff.py --uf {UF} --candidate ... --write`. Canonical files were **not** modified.

## Headline result

All three states are essentially unchanged from the new PDFs. **Zero hospitals added, zero
removed, zero antivenom-list changes** across AM + AC + PB. One cosmetic typo fix found in AC.

| State | Rows before | Rows after | Added | Removed | Antivenom changes |
|---|---|---|---|---|---|
| AM | 95 | 95 | 0 | 0 | 0 |
| AC | 17 | 17 | 0 | 0 | 0 |
| PB | 14 | 14 | 0 | 0 | 0 |

(AM's diff report shows "Linhas atuais/candidato: 91" — that's an artifact of `refresh_diff.py`
indexing by CNES: 4 of AM's 95 rows (remote PEF/Pelotão military outposts with no CNES code)
aren't counted by the CNES-keyed diff, not a data discrepancy. Row count in the actual JSON is 95
on both sides.)

## AM (Amazonas) — 95 rows

Extracted all 10 PDF pages. Table row counts per page: 7, 10, 10, 10, 10, 10, 11, 10, 9, 8 = **95**,
matching canonical exactly. Cross-checked:
- All 91 non-null CNES codes in canonical appear verbatim in raw `extract_text()` output for every
  page — no extras, no misses (`set` diff empty both directions).
- All 13 "Polo Base" and all 10 "Pelotão" entries (the sparse indigenous/military outposts flagged
  as normal in the task brief) present in raw text matching canonical names, addresses (where present).
- Spot-checked the two split-phone rows on page 6 (Santa Isabel do Rio Negro `(97) 3441-1944/1138`
  and Santo Antônio do Içá `(97) 3461-1959/1182`, each split across two physical table rows in the
  PDF) — both reconstruct identically to canonical.
- Spot-checked page-boundary carryover rows (municipality cell empty, inherits previous row's
  municipality) at every page transition — all match canonical's municipality assignment.

**Diff result: 0 added, 0 removed, 0 changed.** No antivenom-list changes.

## AC (Acre) — 17 rows

`extract_tables()` returned only **16** rows across 2 pages (11 on page 0, 5 on page 1). Cross-checking
against `extract_text()` on page 1 surfaced the dropped row: **CNES 2001578, HUERB — Hosp. de
Urgência e Emergência de Rio Branco**, municipality Rio Branco — present in the raw text at the top
of page 1 but absent from `extract_tables()`'s detected geometry (the exact RJ-style silent-drop
failure mode). Manually parsed from raw text: address "Avenida Nações Unidas, 700 - Bosque", phone
"(68) 3223-3080", antivenoms "Botrópico, Laquético, Elapídico, Escorpiônico, Fonêutrico, Lonômico,
Loxoscélico" — all fields match canonical exactly, confirming canonical already had this row correctly
and it is **not** a new/removed hospital, just an extractor artifact I had to work around.

All other 16 rows matched canonical exactly. One address had a capitalization typo in the canonical
file relative to the actual PDF glyphs:

- **CNES 2001500, Hospital de Clínicas Raimundo Chaar (Brasiléia):** canonical address
  `BR 317, km 01, Bairro ALberto Castro s/n` → PDF actually reads `Bairro Alberto Castro s/n`
  (lowercase "l"). Cosmetic-only; recorded in the diff as one "CNES alterado" (address field).

**Diff result: 0 added, 0 removed, 1 changed (cosmetic address typo only). No antivenom-list changes.**

## PB (Paraíba) — 14 rows

`extract_tables()` returned 12 rows on page 0 + 2 on page 1 = 14, matching canonical exactly.
Cross-checked full raw text on both pages — every municipality/hospital name in the text is
accounted for in the table rows, nothing left over.

**Diff result: 0 added, 0 removed, 0 changed.** No antivenom-list changes.

## Antivenom-list ("soro") changes across all 3 states

**None.** No CNES in AM, AC, or PB had a changed `antivenoms_raw` value between the old and new PDF.

## Confidence assessment

- **AM:** High confidence. Exhaustive per-page table/text cross-check with zero discrepancies across
  all 95 rows; every CNES code independently verified present in raw text.
- **AC:** High confidence, but flagging for human awareness: the extractor did silently drop a row
  (Rio Branco/HUERB) that had to be manually recovered from raw text — this is exactly the RJ failure
  mode the task warned about. I'm confident in the recovered values (they match canonical exactly,
  including the multi-line antivenom list), but a second pair of eyes on that one row wouldn't hurt.
  The address typo fix (ALberto → Alberto) is trivial and safe to ignore or apply.
- **PB:** High confidence. Clean, unambiguous extraction with full text cross-check.

## Files produced

- `extracted/AM.candidate.json`, `extracted/AC.candidate.json`, `extracted/PB.candidate.json`
  (hand-verified candidates; canonical files untouched)
- `reports/refresh_diff_AM_2026-07-26.md`
- `reports/refresh_diff_AC_2026-07-26.md`
- `reports/refresh_diff_PB_2026-07-26.md`

No changes were promoted to `extracted/{UF}.json`, `app/hospitals.json`, or `hospitals.json`. No
geocoding, pipeline run, commit, or push was performed, per task instructions.
