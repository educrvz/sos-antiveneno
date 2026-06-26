# Repository Instructions for Codex

## Project Snapshot

SoroJa is a static, mobile-first emergency reference app for finding Brazilian
antivenom hospitals. The public app lives in `app/`; the data pipeline lives in
`scripts/`; source and manual data live in `extracted/` and `data/`; generated
artifacts live in `build/`, `reports/`, `app/hospitals.json`, and
`hospitals.json`.

Keep the app static-first and offline-capable. Browser geolocation must stay on
the user's device; do not send, log, store, or add analytics around precise user
location.

## Read First

- Start with `README.md` for the project shape.
- Read `docs/PROCESS.md` only for dataset refresh, geocoding, PESA PDF,
  generated artifact, override, or community-note work.
- Read `PRIVACY.md` and `TERMS.md` before changes involving privacy, emergency
  wording, medical-risk UX, third parties, geolocation, service workers, CSP,
  forms, or public data collection. If `SECURITY.md` exists, read it for the
  same work.
- Follow more local instructions if a future subdirectory adds its own
  `AGENTS.md`.

## Token Discipline

- Use `rg` and targeted file reads before opening large files.
- Avoid loading all of `app/hospitals.json`, `hospitals.json`, `build/*`,
  `reports/*`, large CSVs, or per-state JSONs unless the task requires it.
- Prefer schemas, scripts, tests, reports summaries, and small samples over
  full generated artifacts.
- Do not duplicate `docs/PROCESS.md` in new docs; link to it and add only the
  missing operational decision.

## Data Safety

- Ministry of Health PESA data is the canonical official layer.
- `data/location_overrides.json` and `data/community_notes.json` are traceable
  layers on top of official data; do not silently fold them into source
  extracts.
- Do not manually edit generated files when a script owns them. Regenerate via
  the pipeline or the specific builder script.
- Treat unexpected row-count, CNES, UF, source-date, coordinate, or
  publish-policy changes as blockers to investigate.
- Full refreshes can call Google Maps APIs. Do not run
  `./scripts/refresh_dataset.sh` casually; use it when dataset/public artifacts
  actually need regeneration.

## App and Content Rules

- Keep the app vanilla HTML/CSS/JS unless there is a strong reason to add a
  dependency.
- Preserve the current security posture in `vercel.json`, especially CSP,
  frame restrictions, referrer policy, and geolocation permissions.
- Do not add cookies, tracking pixels, analytics, or default PII collection.
- User-facing app copy should be pt-BR. Code, internal docs, comments, commit
  messages, and PR text should be en-US unless a local file clearly uses
  another language.
- Emergency guidance must remain conservative: tell users to call SAMU 192 or
  Bombeiros 193 and confirm with the hospital/CIATox before traveling.

## Validation

- Markdown-only docs changes: `git diff --check -- <changed-files>`
- If `package.json` defines `format:check`, run `npm run format:check` for
  docs/config changes.
- Python pipeline or script changes: `python3 -m pytest scripts/tests/ -v`
- Published hospital JSON changes:
  - `python3 scripts/validate_hospitals_json.py app/hospitals.json`
  - `python3 scripts/rebuild_final_artifacts.py --check`
- Full dataset refresh or generated artifact rebuild:
  - `./scripts/refresh_dataset.sh`
  - `python3 scripts/validate_hospitals_json.py app/hospitals.json`
  - `python3 scripts/rebuild_final_artifacts.py --check`

If validation cannot be run, report the exact command and the blocker.

## Git

- Use the current branch unless the user asks for another one.
- Keep PRs narrow: one behavioral purpose, one reviewable scope.
- Use Conventional Commits when no stricter local convention exists, with a
  meaningful scope.
- Before pushing authored commits, verify the latest commit signature with
  `git log --show-signature -1`.
