# PESA 2026-07-03 25-UF — Independent validation of Codex pre-production review

Validation date: 2026-07-26 (Claude session, evening)
Validates: `reports/pesa_20260703_25uf_validated_add_remove.md`, `reports/pesa_20260703_25uf_aggregate_diff.md`, `reports/pesa_20260703_25uf_confirmed_field_differences.md`, and the Notion page "SoroJa PESA 2026-07-03 25-UF Pre-Production Review".

## Method

Independent of Codex's tmp extractors. For each of the 25 candidate UFs:

1. Loaded the non-blank CNES set from canonical `extracted/{UF}.json` (25 UFs, 1,758 CNES total).
2. Extracted full text from `tmp_pesa_20260703_25uf_pdfs/{UF}_20260703.pdf` with pdfplumber.
3. Removal check: every old CNES searched literally in new PDF text (plus a digit-squeezed variant to catch line wraps).
4. Addition check: every 6–7-digit token in the new PDF text not present in the old CNES set, with surrounding context captured for artifact filtering (CEP/phone fragments).
5. Field-level spot-check: old phone digit-groups and address prefixes searched in new PDF text; every mismatch inspected against the raw PDF row.

## Results — confirmations

- **Removals: 1 confirmed.** RJ CNES 6855334 (UPA Itaperuna) is the only old CNES absent from all 25 new PDFs. Matches Codex.
- **Additions in RJ confirmed:** 2287919 (Hospital Nova Santa Casa de Barra do Piraí), 2287927 (Hospital e Maternidade Maria de Nazaré), 2276186 (Hospital Nossa Senhora da Piedade), 4751140 (UPH Pedro do Rio). All present in the new RJ PDF with plausible full rows; none correspond to old blank-CNES rows (old RJ has zero blank-CNES rows).
- **Codex's false-positive filtering confirmed:** MA 998460 is a phone fragment; PE 7226001 is part of `0800-7226001`. No other new-token candidates exist in any of the 25 UFs.
- **Phone/address spot-check:** every one of the mismatch candidates inspected (DF 10464, CE 2516632, AM 2016974, AM 2016419, AM 2016923) turned out to be a PDF line-wrap artifact — the old value is still present in the new PDF. No confirmed substantive phone/address change found, consistent with Codex's finding.

## Results — correction to Codex

- **Additions are 5, not 4.** RJ CNES 2279274 (Posto de Urgência de Itaperuna, Rua Cardoso Moreira 897, (22) 3822-4657) is **not** in old `extracted/RJ.json` — Codex's note "which already existed in old data" is wrong. Old RJ has only UPA Itaperuna 6855334 for that city.
- Net reading: Itaperuna is a **facility replacement** — UPA Itaperuna (6855334, RUA E 1, Cidade Nova) out; Posto de Urgência de Itaperuna (2279274, same phone as old UPA row) in. Antivenom coverage for Itaperuna is preserved in the official source.
- Corrected RJ delta: old 29 rows → new 33 rows expected (29 − 1 + 5).

## Standing caveats (unchanged from Codex review)

- The 30/137/996 counts in `pesa_20260703_25uf_aggregate_diff.md` are tmp-parser artifacts; do not use.
- Antivenom-availability changes per row **cannot** be attributed automatically from wrapped PDF text. Field-level promotion of any state requires the canonical human-in-the-loop re-extraction (docs/PROCESS.md §3: Claude Code multimodal per state → `extracted/{UF}.new.json` → `scripts/refresh_diff.py`).
- The `extracted/*.new.json` / `*.new2.json` files from the tmp extractors are triage aids only — do NOT promote them to `extracted/{UF}.json`.
- 18–20 guard rows with community notes / manual overrides (Sheet `00__Error Reports Summary`, `data/community_notes.json`, `data/location_overrides.json`) must survive any refresh; stage 09f re-applies manual triage, and overrides apply post-extraction.
- BA and SP remain absent from the MS listing (rechecked 2026-07-26 on both listing pages) — carry forward at 2026-01-05 / 2026-05-25.

## Production classification (pending Eduardo's explicit OK — nothing pushed)

**Safe to push (branch/PR, no public-data impact):**
- Review/report artifacts (this file + Codex reports).
- Watcher/process behavior treating BA/SP as carried-forward rather than removed.

**Safe to push to production after Eduardo's OK (low risk, well-validated):**
- RJ refresh: re-extract RJ (only 31–33 rows) via canonical multimodal path, run `refresh_diff.py --uf RJ`, geocode the 5 new rows, update `data/source_dates.json` for RJ only. This is the only state with confirmed structural change.

**Needs manual review before any push (per state):**
- Field-level changes (addresses, phones, antivenom lists) for all 25 UFs — no confirmed changes found by text-matching, but only re-extraction can rule out edits. Suggested order: higher-confidence subset first (AC, AL, AP, DF, MS, PB, PE, PI, RN, RR, SC), then the noisy-parser states (AM, CE, ES, GO, MA, MG, MT, PA, PR, RO, RS, SE, TO).
- Guard-row conflict review for GO 2569701, MG 8000956, PR 2585367/2738252/2683202 (units reported closed by community but possibly still listed in the new PDFs).

## Open item from the error-control Sheet

- RS 3626245 (HPS Canoas): report of 2026-07-23 suggests service may have moved to Hospital Nossa Senhora das Graças — still `needs review`; do not publish transfer destination until verified.

## Session log

- Rechecked MS listing pages 1 and 2: 25 UFs published 03/07/2026 18h55; BA/SP absent.
- Ran independent CNES-presence validation over all 25 new PDFs (script in session scratchpad; output archived in this report).
- Inspected raw PDF rows for all phone-mismatch candidates; all were wrap artifacts.
- Verified RJ additions/removal one by one, including blank-CNES cross-check.
- No repo data files were modified. No commits, no pushes, no production deploys.
- Notion updated: main SoroJá page status consolidated; Codex pre-production review page corrected (4→5 additions) and marked validated; superseded status sections archived.

## Follow-up session (same day) — RJ refresh attempt, executed on branch `data/pesa-20260703-rj-refresh`

**Hand-verified RJ re-extraction.** Rebuilt `extracted/RJ.json` from scratch by reading pdfplumber's raw table output for all 3 pages of the new RJ PDF row-by-row (not trusting either tmp extractor — `tmp_extract_25uf.py` and the "improved" `tmp_extract_25uf_v2.py` both turned out to be unreliable; v2 produced only 11 of 33 real RJ rows for example, silently dropping most of the state). Caught a bug in pdfplumber's own table detector along the way: it silently dropped 2 rows that were present in the raw page text but not table geometry — RJ 2279274 (Posto de Urgência de Itaperuna, a genuine new addition) and RJ 2288893 (Resende, Hosp. Mun. de Emergência Henrique Sérgio Gregori, an *existing* hospital, not a new one). `scripts/refresh_diff.py --uf RJ` caught the Resende omission immediately on first run — confirms the value of running the repo's own diff tool rather than trusting any ad hoc script. Final validated RJ diff: 29 → 33 rows, 5 added, 1 removed, 2 minor address-field corrections (cosmetic dash formatting for CNES 6200702; a genuine neighborhood correction for CNES 6922597 UPA Cascatinha, "Itamarati" → "Cascatinha", sourced directly from the new PDF).

**Blocker found: Google Maps Geocoding API billing is disabled on this machine.** Running `scripts/geocode_hospitals.py` failed with `REQUEST_DENIED` / "You must enable Billing on the Google Cloud Project" for every row that needed a *fresh* geocode call (the 5 new RJ hospitals, plus incidentally 3 unrelated RJ rows whose geocode cache got busted by re-typing `extracted/RJ.json` from scratch). This is an infrastructure/account issue outside this session's authority to fix (modifying Google Cloud billing is an account-settings action) — **Eduardo needs to either re-enable billing on the linked project or rotate to a working key** before any further geocoding can run on this machine.

**Regression caught and reverted before it could be committed.** Working around the billing block by re-running the full `./scripts/refresh_dataset.sh` pipeline surfaced a much bigger problem: with live geocoding degraded, the pipeline's repair/retry stages (`repair_high_risk_geocodes.py`, `repair_muni_mismatch.py`) silently **dropped 34 previously-published hospitals across 9 states** (RJ 21, MT 4, BA 3, and one each in PA/AM/RR/MA/PE/PR) that are fine in the current production `app/hospitals.json` — none of these states were touched by the RJ refresh; they broke purely because today's degraded API access made previously-successful repair lookups fail. **This was never committed or pushed.** All pipeline-generated artifacts (`app/hospitals.json`, `hospitals.json`, `build/*.csv`) were verified byte-identical to `main` and are unchanged. The broken pipeline output was preserved via `git stash` (stash entry `pipeline-run-blocked-by-billing-2026-07-26`) rather than deleted, in case it's useful for diagnosing the repair scripts later — nothing was discarded.

**Attempted workaround:** tried public Nominatim (OpenStreetMap) for the 5 new RJ addresses since it needs no billing. Got a precise hit for only 1 of 5 (UPH Pedro do Rio, and even that was area-level, not rooftop). Not precise enough to publish coordinates for a safety-critical antivenom locator — did not use it.

**Current branch state (`data/pesa-20260703-rj-refresh`, not merged, not pushed):**
- `extracted/RJ.json` — hand-verified, 33 rows, ready for review. **Not yet geocoded** — the 5 new rows have no lat/lng and cannot be published until geocoding works again.
- `data/source_dates.json`, `data/source_hashes.json` — RJ bumped to 2026-07-03 / new PDF hash.
- `Docs Estado/RJ_20260703.pdf` — new source PDF added.
- `reports/refresh_diff_RJ_2026-07-26.md` — regenerated from the corrected candidate, matches this report.
- `app/hospitals.json`, `hospitals.json`, `build/*` — untouched, identical to `main`.

**Resolved without API geocoding.** Eduardo confirmed the 5 addresses were correct and asked to skip the API and provide coordinates manually. Looked each of the 5 up individually on Google Maps (address text cross-checked against the PESA PDF for every one), captured verified lat/lng, and hand-patched `app/hospitals.json` + `hospitals.json` directly — bypassing the broken Google Geocoding API entirely rather than waiting on the billing fix:

| CNES | Unidade | Coordinates |
|---|---|---|
| 2276186 | Hospital Nossa Senhora da Piedade | -22.1639849, -43.2942472 |
| 2279274 | Posto de Urgência de Itaperuna | -21.203276, -41.892226 |
| 2287919 | Hospital Nova Santa Casa de Barra do Piraí | -22.4700253, -43.8225565 |
| 2287927 | Hospital e Maternidade Maria de Nazaré | -22.4613711, -43.8260489 |
| 4751140 | UPH Pedro do Rio | -22.3318535, -43.1315447 |

Built the 5 new records with `scripts/phone_utils.expand_phones` and `scripts/canonicalize_antivenoms.canonicalize_list` (the same library functions `build_app_hospitals_json.py` uses) so the schema matches exactly — not a hand-typed shortcut. `geocode_tier: 1` (manually verified, equivalent to ROOFTOP). Removed CNES 6855334, applied the 2 address corrections. Confirmed via `scripts/validate_hospitals_json.py` (2,276 records, OK) and a CNES-level diff against `main`: **added {2276186, 2279274, 2287919, 2287927, 4751140}, removed {6855334}, changed {6200702, 6922597} — nothing else touched.** Verified live in a local preview (`python3 -m http.server` on `app/`): searched "Itaperuna", the new Posto de Urgência de Itaperuna card renders correctly with the right address, phone, antivenom icons, and "Atualizado 03/07/2026 — Fonte: MS".

The Google Cloud billing blocker documented above is still real and still blocks the *automated* pipeline (`scripts/geocode_hospitals.py` / `refresh_dataset.sh`) for any future full refresh — but is no longer blocking this specific RJ change, which is now complete and ready for Eduardo's go/no-go on PR #37.

**Remaining 24 UFs: not attempted this session.** Given the RJ case just demonstrated that automated table extraction can silently drop rows even in a small, clean 3-page PDF, and that a blind full-text strict-match field check produces too many false positives on larger/messier states (line-wrap reading-order issues), promoting any of the other 24 states' data safely requires the same hand-verification approach used for RJ here — realistically hours of dedicated work per larger state (MG 295 rows, PR 204, PA 172, AM 95). Not attempted in this pass to avoid rushing state-by-state verification for a safety-critical dataset. The `refresh_diff_{UF}_2026-07-26.md` reports for all 25 states are committed for reference; none of the other 24 `extracted/{UF}.json` files were modified.
