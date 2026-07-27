# PESA refresh 2026-07-03 — Batch 8: GO, AL, PI — combined summary

Hand-verified against `tmp_pesa_20260703_25uf_pdfs/{GO,AL,PI}_20260703.pdf`, cross-checked field-by-field
against `extracted/{GO,AL,PI}.json`. Candidates written to `extracted/{GO,AL,PI}.candidate.json`.
Canonical files were **not** modified. Full diff reports:
`reports/refresh_diff_GO_2026-07-26.md`, `reports/refresh_diff_AL_2026-07-26.md`, `reports/refresh_diff_PI_2026-07-26.md`.

## Headline result

**Zero hospital additions, zero removals, zero real antivenom-availability changes across all three states.**
Every difference the diff tool initially flagged traced back to a `pdfplumber.extract_tables()` artifact in
this new batch of PDFs, not to an actual change in Ministry of Health data. Confidence: **high** for all three.

## GO — Goiás (87 rows)

- Rows before: 87. Rows after (candidate): 87. Added: 0. Removed: 0.
- **Extraction was badly behaved**: `extract_tables()` silently dropped **8 full rows** (no trace at all, not
  even an orphan fragment) and mangled several more via cross-page cell bleed. This is the RJ lesson repeating —
  the dropped rows all sit at the top of a page (right after a page break), where multi-line cells that started
  on the previous page confuse pdfplumber's table geometry detection.
- **8 rows recovered by hand from raw `extract_text()`** (verified CNES-for-CNES against canonical, all matched
  exactly): Bom Jardim de Goiás (CNES 2535238), Cavalcante (2382709), Flores de Goiás (2535327), Indiara
  (2343185), Jussara (3795292), Niquelândia (2534789), Pontalina (247774), São Miguel do Araguaia (2382431).
- **Other cell-merge bugs fixed by hand**: Catalão's CNES landed in the wrong cell (recovered: 7977123); Orizona's
  CNES got embedded inside the antivenoms text cell (recovered: 7194498); "Goianésia" and "Goiânia" (the state
  capital, home to the HDT tropical-disease referral hospital) were merged into one municipality cell — split
  back into two correct rows; Trindade / Uruaçu / Vianópolis were garbled into one unreadable row spanning three
  real facilities — split back into three correct rows using word x-position analysis. Two phone numbers also
  bled into the wrong adjacent row (Parauna's number appeared under Palmeiras de Goiás; Sítio D'Abadia's number
  appeared under Silvânia) — both corrected to the address they actually belong to per raw text and confirmed
  against canonical.
- **After all fixes, only 2 cosmetic differences remain** in the diff report, both from the source PDF's own
  typography, not data changes:
  - CNES 2343525 (Hospital de Caridade São Pedro D'alcântara, Goiás/GO): apostrophe glyph only (straight `'` in
    old data vs curly `'` in the new PDF's actual text).
  - CNES 2534967 (Hospital Regional de Formosa Dr César Saad Fayad, Formosa/GO): source PDF has a stray period
    instead of a comma after "Crotálico" — same 7 antivenom types either way, no set change.
- **CNES adicionados / removidos: none.**
- **Antivenom-list changes (real, set-level): none.**
- **Overrides:** all 3 GO overrides (CNES 2569701 note, CNES 2535556 lat/lng, CNES 2342073 note) confirmed still
  valid — MS data unchanged underneath each.

## AL — Alagoas (15 rows)

- Rows before: 15. Rows after (candidate): 15. Added: 0. Removed: 0.
- One row (Maceió, "Hospital Escola Dr. Helvio Auto - HEHA", CNES 2720035) was completely dropped by
  `extract_tables()` at the page-1 top-of-page boundary — recovered from raw text, matches canonical exactly.
- Two Maceió rows (UPA 24 horas Dr Ismar Gatto, CNES 4156730; UPA Galba Novaes, CNES 4156714) have a blank
  municipality cell in the source table (municipality is only printed once per city block) — same known quirk
  as the current canonical, `source_notes` preserved.
- **After reconciliation: zero field differences of any kind.** The final diff report shows 0 CNES changed.
- **CNES adicionados / removidos: none. Antivenom-list changes: none.**
- **Overrides:** the 1 AL override (CNES 4156714 lat/lng) confirmed still valid.

## PI — Piauí (17 rows)

- **Important finding: the new PI PDF is text-based, NOT image-based.** Per CLAUDE.md, PI has historically
  required OCR (poppler + tesseract) and the canonical data was built from a separately-OCR'd `V2_PI_*.pdf`.
  This new 2026-07-03 PI PDF extracts cleanly with plain `pdfplumber.extract_text()` / `extract_tables()` — no
  OCR tooling was needed this time, and no dropped/merged rows occurred (unlike GO/AL, `extract_tables()` behaved
  correctly on every page here).
- Rows before: 17. Rows after (candidate): 17. Added: 0. Removed: 0.
- All 17 CNES matched exactly on municipality, hospital name, address, phone, and antivenom set.
- Diff shows 17 rows "changed" but only because of:
  - `source_notes` clearing (was `"V2 PDF used; PI source is image-based"` on every row — no longer applicable
    since this refresh's source is text-based).
  - 2 cosmetic accent-typo corrections in `antivenoms_raw` (the old OCR pass had missed accents): CNES 2777770
    (Corrente) `Laquetico` → `Laquético`; CNES 4009622 (Picos) `Foneutrico, Loxoscelico, Laquetico` →
    `Fonêutrico, Loxoscélico, Laquético`.
  - 1 dash-glyph difference in `health_unit_name`: CNES 2323338 (Teresina, IDTNP) hyphen `-` → en dash `–`,
    matching the new PDF's literal text.
- **CNES adicionados / removidos: none. Antivenom-list changes (real, set-level): none** — the 2 corrections
  above are typo fixes within the same antivenom set, not availability changes.
- No overrides exist for PI.

## Antivenom-list changes (Eduardo's specific ask) — full list across all 3 states

**None.** No CNES in GO, AL, or PI had an actual change to which antivenom types are available. The only
`antivenoms_raw` diffs found were: (1) a punctuation typo fix in GO (period→comma, same 7 types), and (2) two
accent-only typo fixes in PI (same types, just missing diacritics in the old OCR'd data). Before/after values
for these two informational-only cases are in the state sections above and in the full diff reports.

## Confidence assessment for human review

- **GO:** High confidence, but recommend a maintainer skim of `reports/refresh_diff_GO_2026-07-26.md` given how
  much manual reconstruction was needed — every recovered/fixed row was cross-verified against the canonical
  file and matched exactly, but this was the most heavily-patched extraction of the three.
- **AL:** High confidence — small dataset, one dropped row cleanly recovered, ended in a perfect match.
- **PI:** High confidence, and worth flagging positively to Eduardo — PI's data source appears to have moved
  off image-based PDFs, which removes a standing OCR dependency for future refreshes of this state.

## Files touched

- `extracted/GO.candidate.json`, `extracted/AL.candidate.json`, `extracted/PI.candidate.json` (new, not promoted)
- `reports/refresh_diff_GO_2026-07-26.md`, `reports/refresh_diff_AL_2026-07-26.md`, `reports/refresh_diff_PI_2026-07-26.md`
- `reports/pesa_20260703_batch8_GO_AL_PI_summary.md` (this file)
- Canonical `extracted/{GO,AL,PI}.json` — untouched, as instructed.
