# Security Policy

## Supported Scope

The supported security scope is the current production site and the code,
data pipeline, and GitHub Actions workflows on the default branch of this
repository.

Historical deployments, forks, local development builds, and downstream
copies are outside the maintained security scope.

## Before You Report

SoroJa is a static, client-side web app that publishes public hospital
reference data in `app/hospitals.json`. The app uses browser geolocation only
on the user's device to calculate distance to hospitals; the user's location
should not be sent to this project, stored by this project, or shared by this
project for analytics or advertising. See the privacy policy in
[`app/privacy.html`](app/privacy.html).

Please use the normal data-correction channels, not the security process, for:

- Wrong pins, outdated phone numbers, closed hospitals, missing hospitals, or
  other corrections to the public hospital dataset.
- Questions about Ministry of Health source PDFs or data refresh timing.
- General bugs that do not affect confidentiality, integrity, availability, or
  user privacy.

Those issues can be reported with the app's "Reportar erro" action, by opening
a public GitHub issue, or by emailing `contato.soroja@gmail.com`.

## What To Report Privately

Please report security vulnerabilities privately when they could affect users,
maintainers, the published dataset, or the deployment pipeline. Examples
include:

- Cross-site scripting or HTML/script injection through published hospital data,
  community reports, overrides, or generated pages.
- A bug that sends, stores, exposes, or logs precise user location without clear
  user action and consent.
- Service worker, cache, or PWA behavior that could serve attacker-controlled or
  stale unsafe content.
- Exposed secrets, API keys, tokens, or credentials.
- GitHub Actions, data-pipeline, or repository-permission flaws that could let
  an attacker alter `hospitals.json` or the production site.
- Dependency, CDN, or third-party integration issues that create a concrete
  vulnerability in this project.

## Reporting a Vulnerability

If GitHub private vulnerability reporting is enabled for this repository, use
GitHub's "Report a vulnerability" flow.

Otherwise, email `contato.soroja@gmail.com` with a private report. Please
include:

- A short description of the vulnerability and impact.
- Steps to reproduce, including URLs, affected files, payloads, or proof of
  concept where safe to share.
- Browser, device, and deployment details, if relevant.
- Whether the issue is already public or known to be exploitable.

Please do not open a public issue for a vulnerability until the maintainer has
had a chance to triage and prepare a fix.

## Response Expectations

You should receive an initial response within a few days. Confirmed
vulnerabilities will be prioritized based on impact, exploitability, and risk to
users or the integrity of the hospital dataset.

When a fix is available, the maintainer may publish a GitHub security advisory,
release notes, or a public issue/PR summary as appropriate.
