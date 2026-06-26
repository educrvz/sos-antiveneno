# Contributing

Thanks for helping SoroJá. This project is emergency-facing, so small,
well-scoped changes are easier to review and safer to ship.

## Before You Start

- Check existing issues, pull requests, recent commits, and maintainer branches
  before opening new work.
- Read [`docs/PROCESS.md`](docs/PROCESS.md) before changing data pipeline files
  or generated artifacts.
- Keep each pull request focused on one behavior or one documentation purpose.
- Do not include patient information, private reporter details, phone numbers
  from raw reports, screenshots with personal data, or unverified medical advice.

## Change Types

### App Changes

App code lives in [`app/index.html`](app/index.html), with service-worker
behavior in [`app/sw.js`](app/sw.js).

- Keep the app mobile-first and usable in stressful, low-connectivity contexts.
- If you change `app/index.html` or static app assets, bump `CACHE_NAME` in
  `app/sw.js` so installed PWAs pick up the update.
- Do not change emergency or medical wording casually. Prefer existing wording
  from `README.md`, `TERMS.md`, `PRIVACY.md`, or documented maintainer plans.

Suggested validation:

```bash
python3 scripts/validate_hospitals_json.py app/hospitals.json
git diff --check -- app/index.html app/sw.js
```

### Data Changes

The public app data is built from the pipeline, overrides, and community notes.
Avoid hand-editing [`app/hospitals.json`](app/hospitals.json) or
[`hospitals.json`](hospitals.json) unless the change is the expected output of a
documented rebuild.

- Verified corrections belong in [`data/location_overrides.json`](data/location_overrides.json).
- Additive public relatos belong in [`data/community_notes.json`](data/community_notes.json).
- Preserve Ministry of Health source fields unless the existing override model
  explicitly supports the correction.
- Use non-closing references for partial, exploratory, or hardening work.

Suggested validation:

```bash
python3 scripts/build_app_hospitals_json.py
python3 scripts/validate_hospitals_json.py app/hospitals.json
git diff --check -- data app/hospitals.json hospitals.json
```

### Pipeline Changes

Pipeline scripts live in [`scripts/`](scripts/) and are orchestrated by
[`scripts/refresh_dataset.sh`](scripts/refresh_dataset.sh).

- Prefer deterministic transforms over manual edits to generated files.
- Keep reports in [`reports/`](reports/) consistent with generated artifacts.
- Update [`docs/PROCESS.md`](docs/PROCESS.md) when the refresh process changes.

Suggested validation:

```bash
python3 -m pytest scripts/tests/ -v
python3 scripts/canonicalize_antivenoms.py --self-test
python3 scripts/validate_hospitals_json.py app/hospitals.json
```

### Documentation Changes

- Keep user-facing project documentation in Portuguese unless the surrounding
  file is already English.
- Keep contributor/process documentation in the language already used by that
  file.
- For documentation-only pull requests, say so in the testing section and note
  what was cross-checked.

Suggested validation:

```bash
git diff --check
```

## Commit and Pull Request Style

Recent repository history uses concise, area-prefixed titles such as:

- `app: ...`
- `data: ...`
- `pipeline: ...`
- `ci: ...`
- `docs: ...`
- `data+app: ...`

Use a similarly narrow title. If no stricter convention applies, follow
Conventional Commits with a meaningful scope.

Use GitHub closing keywords only when the pull request fully resolves the
reported issue:

- `Fixes #NNN` or `Closes #NNN` for complete fixes.
- `Refs #NNN` or `See #NNN` for partial, documentation-only, test-only,
  hardening, or design-follow-up work.

## Pull Request Body

When there is no more specific template, use:

```md
## Summary
- ...

## Context
Briefly explain the bug/root cause or documentation gap and why this approach is narrow.

## Scope
This intentionally does not change:
- ...

## Testing
- ...

Fixes #NNN
```

Use `Refs #NNN` instead of `Fixes #NNN` when the PR is partial or exploratory.

Add the validation you ran under `## Testing`. If a check cannot be run, include
the exact command and the blocker.
