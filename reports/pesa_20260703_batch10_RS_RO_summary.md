# PESA 2026-07-03 refresh — Batch 10 — RS + RO

Hand-verified re-extraction of `RS_20260703.pdf` and `RO_20260703.pdf` against
the canonical `extracted/RS.json` / `extracted/RO.json`. Methodology: pdfplumber
`extract_text()` per page, manually transcribed record-by-record, cross-checked
against `extract_tables()` output per the RJ lesson (any hospital/municipality
name present in raw text but missing from `extract_tables()` rows was manually
recovered and included). Canonical files were **not** modified. Candidates
written to `extracted/RS.candidate.json` and `extracted/RO.candidate.json`.
Diffs run via `scripts/refresh_diff.py`; reports at
`reports/refresh_diff_RS_2026-07-26.md` and `reports/refresh_diff_RO_2026-07-26.md`.

## RS — Rio Grande do Sul

- Rows: 65 (before) → 65 (after)
- CNES added: 0
- CNES removed: 0
- CNES with field changes: 1 (cosmetic only)
- Antivenom-list changes: **0**

`extract_tables()` fragmented every multi-line record into several table "rows"
(one logical hospital = 2-3 fragmented rows) but did not drop any record —
cross-checked page-by-page text against table row counts: 10+11+12+11+13+8 = 65,
matching canonical exactly.

**Only diff found:** CNES 2252023, "Hospital de Caridade Sant'Ana" (Bom Retiro
do Sul) — the new PDF renders the apostrophe as a curly/typographic quote
(U+2019 `'`) instead of the straight quote (U+0027 `'`) used in the canonical
JSON. Confirmed via direct codepoint inspection of the extracted text — this is
a genuine character-level difference in the new PDF glyph, not a pdfplumber
artifact. No address/phone/CNES/antivenom change. **Low confidence this is a
real content change** — recommend treating as cosmetic and either accepting the
candidate's spelling or normalizing apostrophes at canonicalization time; not
a soro/antivenom issue either way.

### RS / CNES 3626245 — "HPS Canoas" open item (explicitly requested check)

Searched the full RS PDF text for "Graças" / "Graça" — **zero occurrences**.
CNES 3626245 appears exactly once in the new PDF, still under municipality
**Canoas**, hospital name **"Hospital de Pronto Socorro de Canoas"** (= HPS
Canoas), same address ("Rua Caçapava, 100, Mathias Velho"), same phone
"(51) 3415 4500", same antivenom list (Botrópico, Escorpiônico, Loxoscélico,
Fonêutrico) — identical to the current canonical record. **The new MS PDF
gives no indication of a transfer to "Hospital Nossa Senhora das Graças."**
This does not resolve the open Sheet item — it only reports what the
2026-07-03 PDF actually contains; the possible transfer may still be real
and simply not yet reflected in MS's own data.

## RO — Rondônia

- Rows: 39 (before) → 39 (after)
- CNES added: 0
- CNES removed: 0
- CNES with field changes: 0
- Antivenom-list changes: **0**

`extract_tables()` silently dropped **3 of 39 records** in this PDF (same
failure mode as RJ) — none visible in the table output but present in
`extract_text()`:
- **Chupinguaia** — U M José Ivaldo De Souza (CNES 2806711), page 2
- **Mirante Da Serra** — Hospital Municipal De Miante Da Serra SAMUEL MARQUES (CNES 2808625), page 3
- **Theobroma** — Hospital Municipal José Almerindo do rosario (CNES 4003357), page 4

All three were manually recovered from raw text and, field-by-field
(municipality, hospital name, address, phone, CNES, antivenom list), match the
canonical `extracted/RO.json` entries **exactly** — no changes. This also
double-confirms the canonical file itself was correctly hand-extracted
previously, so the diff tool correctly reports zero changes for these rows
once they're included in the candidate.

Every one of the remaining 36 records was also compared field-by-field
against canonical (addresses, multi-line phone joins, CNES, and the messy
comma/semicolon-mixed `antivenoms_raw` splits, e.g. Cerejeiras, Corumbiara,
Colorado Do Oeste) — all identical, including preserved source typos
("Rotálico", "Lonômoico", "Antiaracmidico") and known blank-cell quirks
(Alto Alegre Dos Parecis / Nova União / Vale Do Anari null CNES; Cujubim's
phone fragment "69"; Rio Crespo's CEP-like CNES "36613-9464").

**Note (pre-existing, not a refresh finding):** the diff tool's report header
says "Linhas atuais: 35 / Linhas no candidato: 35" instead of 39 — this is
because `scripts/refresh_diff.py` indexes rows by CNES in a dict, and CNES
**2798484 is shared by two different hospitals** in RO — "Hospital de Pequeno
Porte Osvaldo Cruz" (Alto Paraíso) and "Hospital Regional Adamastor Teixeira
De Oliveira" (Vilhena) — so one collapses in the index. This duplicate CNES
already exists in the current canonical file (unchanged by this refresh) and
is the same class of issue flagged for MG in `CLAUDE.md` ("do not CNES-key
overrides when a CNES is shared across multiple facilities"). Flagging for
awareness only — no action taken.

## Antivenom (soro) change list (step 5)

**None.** Zero `antivenoms_raw` changes in either RS (65 rows) or RO (39
rows).

## Confidence assessment

- **RS: high confidence, ready to promote.** Full 65/65 match; the only diff
  is a single non-substantive apostrophe glyph.
- **RO: high confidence, ready to promote.** Full 39/39 match after manually
  recovering 3 table-extraction-dropped rows, all of which matched canonical
  exactly on recovery.
- **CNES 3626245 (HPS Canoas):** no change in the new PDF; the open
  Sheet item about a possible transfer to "Hospital Nossa Senhora das Graças"
  remains unresolved by this source — needs a decision from Eduardo, not an
  extraction fix.
- No low-confidence extraction items requiring further manual review beyond
  what's noted above.
