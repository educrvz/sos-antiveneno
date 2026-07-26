# PESA 2026-07-03 25-UF aggregate diff

Review date: 2026-07-26

This report compares local old extracted files in `/Users/educruz/Documents/SoroJá/extracted/{UF}.json` with newly downloaded Ministerio da Saude PDFs saved in `/Users/educruz/Documents/SoroJá/tmp_pesa_20260703_25uf_pdfs/` and candidate extractions in `extracted/{UF}.new.json`.

BA and SP are intentionally excluded and carried forward.

## Production confidence

Do not push refreshed hospital data to production yet. The automated PDF extraction produced complete diff files, but several states have row-count drops large enough to require manual parser/source review before promotion.

High-confidence production-safe items now:

- Internal review/report artifacts.
- Watch/check logic or operator process that carries BA/SP forward instead of treating them as removed.
- Preservation of `data/location_overrides.json` and `data/community_notes.json` as post-extraction overlays.

Not high-confidence yet: replacing public hospital rows, geocoding new rows, changing source dates/hashes, or deploying regenerated `app/hospitals.json`.

## Counts from current candidate extraction

- Candidate added CNES: 30
- Candidate removed CNES: 137
- Candidate changed CNES: 996
- Field-level changes: 1958

These counts are useful for review triage, but not production claims until parser-review states are cleared.

## State summary

| UF | Old rows | New rows | Delta | Added | Removed | Changed CNES | Field changes | Confidence | Detail report |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| AC | 17 | 16 | -1 | 0 | 1 | 1 | 1 | higher_parser_confidence | `reports/refresh_diff_AC_2026-07-26.md` |
| AL | 15 | 14 | -1 | 0 | 1 | 5 | 14 | higher_parser_confidence | `reports/refresh_diff_AL_2026-07-26.md` |
| AM | 95 | 90 | -5 | 0 | 1 | 61 | 173 | needs_manual_review | `reports/refresh_diff_AM_2026-07-26.md` |
| AP | 26 | 26 | 0 | 1 | 0 | 25 | 52 | higher_parser_confidence | `reports/refresh_diff_AP_2026-07-26.md` |
| CE | 49 | 42 | -7 | 0 | 7 | 41 | 42 | parser_review_required | `reports/refresh_diff_CE_2026-07-26.md` |
| DF | 11 | 10 | -1 | 0 | 1 | 10 | 30 | higher_parser_confidence | `reports/refresh_diff_DF_2026-07-26.md` |
| ES | 61 | 48 | -13 | 0 | 13 | 47 | 54 | parser_review_required | `reports/refresh_diff_ES_2026-07-26.md` |
| GO | 87 | 77 | -10 | 0 | 10 | 24 | 52 | parser_review_required | `reports/refresh_diff_GO_2026-07-26.md` |
| MA | 156 | 178 | 22 | 22 | 0 | 153 | 374 | parser_review_required | `reports/refresh_diff_MA_2026-07-26.md` |
| MG | 295 | 281 | -14 | 0 | 12 | 191 | 233 | parser_review_required | `reports/refresh_diff_MG_2026-07-26.md` |
| MS | 67 | 66 | -1 | 0 | 1 | 1 | 2 | higher_parser_confidence | `reports/refresh_diff_MS_2026-07-26.md` |
| MT | 105 | 73 | -32 | 0 | 30 | 30 | 46 | parser_review_required | `reports/refresh_diff_MT_2026-07-26.md` |
| PA | 172 | 162 | -10 | 0 | 8 | 62 | 215 | parser_review_required | `reports/refresh_diff_PA_2026-07-26.md` |
| PB | 14 | 14 | 0 | 0 | 0 | 14 | 17 | higher_parser_confidence | `reports/refresh_diff_PB_2026-07-26.md` |
| PE | 15 | 14 | -1 | 1 | 2 | 13 | 16 | higher_parser_confidence | `reports/refresh_diff_PE_2026-07-26.md` |
| PI | 17 | 17 | 0 | 0 | 0 | 17 | 29 | higher_parser_confidence | `reports/refresh_diff_PI_2026-07-26.md` |
| PR | 204 | 172 | -32 | 0 | 33 | 169 | 301 | parser_review_required | `reports/refresh_diff_PR_2026-07-26.md` |
| RJ | 29 | 31 | 2 | 4 | 2 | 12 | 23 | higher_parser_confidence | `reports/refresh_diff_RJ_2026-07-26.md` |
| RN | 5 | 5 | 0 | 0 | 0 | 2 | 5 | higher_parser_confidence | `reports/refresh_diff_RN_2026-07-26.md` |
| RO | 39 | 32 | -7 | 2 | 6 | 19 | 34 | parser_review_required | `reports/refresh_diff_RO_2026-07-26.md` |
| RR | 34 | 34 | 0 | 0 | 0 | 32 | 108 | higher_parser_confidence | `reports/refresh_diff_RR_2026-07-26.md` |
| RS | 65 | 65 | 0 | 0 | 0 | 54 | 103 | needs_manual_review | `reports/refresh_diff_RS_2026-07-26.md` |
| SC | 143 | 142 | -1 | 0 | 1 | 1 | 1 | higher_parser_confidence | `reports/refresh_diff_SC_2026-07-26.md` |
| SE | 17 | 14 | -3 | 0 | 3 | 5 | 8 | needs_manual_review | `reports/refresh_diff_SE_2026-07-26.md` |
| TO | 37 | 32 | -5 | 0 | 5 | 7 | 25 | parser_review_required | `reports/refresh_diff_TO_2026-07-26.md` |

## Higher-confidence subset

These states have small row-count deltas in the automated extraction and are the best candidates for first manual review:

AC, AL, AP, DF, MS, PB, PE, PI, RJ, RN, RR, SC

## Parser/source review required

Review these before accepting add/remove counts as real source changes:

AM, CE, ES, GO, MA, MG, MT, PA, PR, RO, RS, SE, TO

## Geo and manual correction guard

The detailed CSV includes current published `lat`/`lng` for affected CNES when present, plus serialized `location_override` and `community_note` values. Any row with `location_override` must preserve its manual coordinates/notes unless Eduardo explicitly approves a change.

Detailed machine-review file: `reports/pesa_20260703_25uf_all_differences.csv`

Per-state detailed reports:

- `reports/refresh_diff_AC_2026-07-26.md`
- `reports/refresh_diff_AL_2026-07-26.md`
- `reports/refresh_diff_AM_2026-07-26.md`
- `reports/refresh_diff_AP_2026-07-26.md`
- `reports/refresh_diff_CE_2026-07-26.md`
- `reports/refresh_diff_DF_2026-07-26.md`
- `reports/refresh_diff_ES_2026-07-26.md`
- `reports/refresh_diff_GO_2026-07-26.md`
- `reports/refresh_diff_MA_2026-07-26.md`
- `reports/refresh_diff_MG_2026-07-26.md`
- `reports/refresh_diff_MS_2026-07-26.md`
- `reports/refresh_diff_MT_2026-07-26.md`
- `reports/refresh_diff_PA_2026-07-26.md`
- `reports/refresh_diff_PB_2026-07-26.md`
- `reports/refresh_diff_PE_2026-07-26.md`
- `reports/refresh_diff_PI_2026-07-26.md`
- `reports/refresh_diff_PR_2026-07-26.md`
- `reports/refresh_diff_RJ_2026-07-26.md`
- `reports/refresh_diff_RN_2026-07-26.md`
- `reports/refresh_diff_RO_2026-07-26.md`
- `reports/refresh_diff_RR_2026-07-26.md`
- `reports/refresh_diff_RS_2026-07-26.md`
- `reports/refresh_diff_SC_2026-07-26.md`
- `reports/refresh_diff_SE_2026-07-26.md`
- `reports/refresh_diff_TO_2026-07-26.md`

## Next gate

For each parser-review state, manually inspect the PDF extraction around removed CNES before promoting `extracted/{UF}.new.json` to canonical. After review, update source date/hash metadata and run the full geocoding/build pipeline before any Vercel production deploy.
