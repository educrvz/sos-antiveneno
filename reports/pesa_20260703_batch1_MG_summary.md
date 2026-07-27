# PESA 2026-07-03 refresh — MG hand-verification summary

**Source PDF:** `tmp_pesa_20260703_25uf_pdfs/MG_20260703.pdf` (21 pages)
**Canonical (before):** `extracted/MG.json` — 295 rows, 292 unique CNES
**Candidate (after):** `extracted/MG.candidate.json` — 295 rows, 292 unique CNES
**Diff report:** `reports/refresh_diff_MG_2026-07-26.md`

## Method

- Extracted `page.extract_tables()` **and** `page.extract_text()` for all 21 pages independently.
- Cross-checked every page's table row count against a regex scan of the raw text for CNES-shaped tokens (5–8 digit numbers). All apparent mismatches (4 pages showed extra "candidates") turned out to be phone numbers printed without internal punctuation (e.g. `34067585`), not dropped rows — verified by grepping each page's raw text. **No rows were silently dropped by `extract_tables()` for MG** (unlike the RJ refresh).
- Page 1 carries the state title + header row (18 padded columns); pages 2–21 are continuation pages with a clean 6-column layout (município, unidade, endereço, telefones, CNES, soros). 6 rows across the PDF have a blank município cell (mid-page-break continuation of the previous hospital's município) — each was manually resolved against its preceding row and cross-checked against canonical `MG.json` (all 6 matched canonical's existing municipality assignment exactly).
- Wrote a text-cleaning rule set (line-wrap collapse, and a hyphen-attached-to-word/number join rule that removes the wrap point without inserting a space — e.g. `Guarda-\nMór` → `Guarda-Mór`, `3522-\n4214` → `3522-4214`) and validated it against canonical field values for all 295 rows before trusting it.
- Final QA: did a **strict positional row-by-row comparison** (not just CNES-keyed, since MG has duplicate CNES across facilities) between all 295 canonical rows and all 295 candidate rows, field by field.

## Row counts

| | Rows | Unique CNES |
|---|---|---|
| Before (`MG.json`) | 295 | 292 |
| After (`MG.candidate.json`) | 295 | 292 |

## CNES added

None.

## CNES removed

None.

## Antivenom list (`antivenoms_raw`) changes

**None.** Verified for all 295 rows (both via the diff tool's CNES-keyed comparison and an independent strict positional comparison). No hospital's antivenom coverage changed in the new MG PDF.

## Other field changes

Exactly **one** real change in the entire 295-row dataset:

- **CNES `2115786` — Hospital de Pronto Socorro (Juiz de Fora)**
  `phones_raw`: `(32) 3690-8125` → `(35) 3690-8125`

**Important caveat — the automated diff tool missed this.** `scripts/refresh_diff.py` indexes rows by CNES (`out[cnes] = r`), and MG has two CNES values shared across multiple distinct facilities (documented in `CLAUDE.md`: "CNES 2115786 is shared across 3 MG units"). CNES `2115786` appears 3 times (Juiz de Fora, Lavras, Poços de Caldas); the tool's dict-based index keeps only the *last* occurrence (Poços de Caldas), which is unchanged — so the tool silently reported 0 changes for this CNES even though row 1 of 3 (Juiz de Fora) changed. I caught it only via manual positional (index-aligned) comparison. This is the same class of blind spot flagged in the RJ post-mortem, now confirmed to reproduce whenever the automated diff is used on a UF with duplicate CNES rows.

I manually verified the change against the raw PDF: page 11 raw text and table both independently show `(35) 3690-8125` for the Juiz de Fora / Hospital de Pronto Socorro row — this is not an extraction artifact, it's genuinely what the new PDF prints.

**Confidence flag:** `(35)` is not a Juiz de Fora area code (Juiz de Fora is DDD 32; DDD 35 belongs to the south/southwest MG region, e.g. Poços de Caldas/Lavras — the same region as the other two facilities sharing this CNES). This looks like a likely Ministry-side data-entry error (possibly copy-paste bleed between the three rows that share this CNES), not a real phone number change. Recommend a human confirm before promoting — either keep the new (possibly wrong) MS value for fidelity to the source, or flag/override it the way `data/location_overrides.json` already handles other known-bad MG source fields (e.g. the Passos address-swap overrides for CNES 2775999/4042751).

## `source_notes` — 2 rows, non-substantive

Two rows had a `source_notes` field in canonical documenting the same "blank município, inherited from previous row" pattern I independently rediscovered during extraction (CNES `7417659` Ipatinga UPA, and CNES `6875343` Teófilo Otoni "Upa"). I carried these existing notes forward into the candidate unchanged after confirming the same PDF layout quirk is still present in the new PDF — not a scored diff, just preserving accurate metadata.

## Overrides audit (`data/location_overrides.json`)

6 MG overrides cross-referenced against the candidate — all 6 report "✅ MS inalterado — override segue válido" (the fields each override touches are unchanged in the new PDF):

- CNES 8000956 — Policlínica Pronto Atendimento (Conselheiro Lafaiete) — `note` override
- CNES 2219564 — Hospital Universitário Clemente de Faria (Montes Claros) — `note` override
- CNES 2134071 — Hospital Imaculada Conceição (Conceição do Mato Dentro) — `note` override
- CNES 7802951 — UPA Adolpho Pereira Resende (Carmo do Paranaíba) — `lat/lng` override
- CNES 2775999 — Santa Casa Misericórdia (Passos) — `lat/lng, note` override (address-swap fix)
- CNES 4042751 — Unidade Pronto Atendimento (Passos) — `lat/lng, note` override (address-swap fix)

No overrides need re-verification as a result of this refresh.

## Confidence assessment / items for human review

1. **Low confidence — needs a human decision:** CNES 2115786 (Juiz de Fora) phone DDD change 32→35 (see above). Likely MS data-entry error given the duplicate-CNES sharing pattern, but faithfully extracted from the new PDF as published.
2. **Duplicate CNES across facilities (pre-existing, not new):** `2115786` (Juiz de Fora / Lavras / Poços de Caldas) and `6875343` (Teófilo Otoni ×2, "Central de Rede de Frio" and "Upa") — both already flagged in `CLAUDE.md` as a known MS data quality issue for MG. Nothing new to do here beyond the point above; just don't CNES-key any future override touching `2115786` or `6875343` (per the existing repo warning).
3. **High confidence — everything else.** All 295 rows independently re-extracted, cross-checked page-by-page against raw text (no dropped rows), and a strict positional field-by-field comparison against canonical found only the single change above. No ambiguous line-wraps, no messy table geometry, no OCR involved (MG is a normal digital-text PDF, not the PI-style scanned case).

## Files touched (candidate only, canonical untouched per instructions)

- Created: `extracted/MG.candidate.json`
- Created: `reports/refresh_diff_MG_2026-07-26.md`
- Created: `reports/pesa_20260703_batch1_MG_summary.md` (this file)
- **Not modified:** `extracted/MG.json`, `app/hospitals.json`, `hospitals.json`, `data/location_overrides.json`
