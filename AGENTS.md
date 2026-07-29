# crawler-workbench Working Agreement

## Mission

This repository is a Python workbench for reliable web data collection. Each scenario
must produce both working code and evidence that the collection approach can be
operated and maintained.

The goal is not to collect the most data. The goal is to make sound collection
decisions and document their trade-offs.

## Repository Map

- `apps/requests/`: static HTML and public API collection.
- `apps/selenium/`: browser automation and failure-handling practice.
- `apps/playwright/`: browser automation and network-response analysis.
- `apps/pipeline/`: validation, storage, scheduling, and operations.

Keep an exercise inside its matching directory. Shared utilities may be added
later under `apps/common/` only after at least two exercises genuinely need
them.

## Language and Runtime

- Implement every exercise in Python. This includes browser automation:
  use the official Python bindings for Selenium and Playwright.
- JavaScript or TypeScript is not an implementation target for this repository.
  Read page JavaScript only when needed to understand rendering, API requests,
  or browser behavior.
- Use one Python version consistently after the first exercise introduces a
  runtime configuration. Record it in the project documentation.

## Collection Policy

1. Use public APIs, pages intended for public access, or local fixtures for
   practice. Prefer local fixtures whenever they can demonstrate the same
   technique.
2. Check the target's terms of use and `robots.txt` before collecting. Record
   the result in the exercise `README.md` or `notes.md`.
3. Do not bypass login, CAPTCHA, paywalls, access controls, or anti-bot
   protections. Do not use proxy or User-Agent rotation to evade a site's
   policy.
4. Do not collect, store, commit, or share unnecessary personal data, secrets,
   cookies, credentials, or session tokens.
5. Set explicit timeouts and a conservative request rate. Retry only temporary
   failures, with backoff and a bounded retry count.
6. Stop or slow collection on `429`, persistent `403`, or clear signs that the
   target does not permit automated access. Document the decision.

## Standard Scenario Shape

Each completed scenario should contain the following where applicable:

- `README.md`: purpose, source type, run command, and collection-policy note.
- `main.py` or another clearly named entry point.
- `requirements.txt` or documented dependency installation command when it has
  non-standard dependencies.
- `tests/` for parsing, validation, or transformation logic that can be tested
  without the live target.
- `sample_output/`: small, sanitized output or fixture. Never commit raw
  personal data or secrets.
- `notes.md`: failed attempts, source-change risks, and operational decisions.

Do not make a live website the only way to test parsing logic. Preserve a small
sanitized HTML or JSON fixture when possible.

## Implementation Rules

1. Separate fetching, parsing, validation, and persistence. Avoid putting the
   whole pipeline in one browser callback or one large function.
2. Prefer the least complex collection method that works:
   public API -> direct HTTP request -> browser automation.
3. For browser automation, use stable locators and explicit wait conditions.
   Do not depend on fixed `sleep` calls except for an intentionally documented
   experiment.
4. Treat page HTML, API payloads, and database rows as untrusted input. Validate
   required fields, types, ranges, duplicates, and missing values before saving.
5. Make repeated runs safe. Define an idempotency key or duplicate policy before
   writing to a database or file.
6. Log enough context to diagnose a failed run: source, request or job ID,
   status, retry count, elapsed time, record counts, and failure reason. Never
   log secrets or full personal-data payloads.
7. Keep configuration in environment variables or an ignored local config file.
   Commit an `.env.example` only when configuration is introduced.

## Scenario Workflow

Use this order for every scenario:

1. Define the collection contract: target fields, source, update frequency,
   success criteria, and policy constraints.
2. Inspect the source manually: DOM shape, API/XHR requests, pagination,
   loading behavior, and likely change points.
3. Choose and document the collection method with a short reason.
4. Implement the smallest end-to-end path: fetch -> parse -> validate -> save.
5. Add failure handling: timeout, bounded retry/backoff, empty-result handling,
   schema-change detection, and duplicate behavior.
6. Verify with fixtures and one controlled live run when permitted.
7. Write `notes.md` with what failed, what changed, and how the job would be
   monitored in production.
8. Finish with an implementation recap: record the design, key trade-offs, and
   remaining operational risks.

## Completion Criteria

A scenario is complete only when all of the following are true:

- It runs from a documented command.
- Its output has passed the defined validation checks.
- Re-running it does not create unintended duplicates.
- Expected failure paths have been exercised or reasoned about with tests.
- No secrets, cookies, personal data, or large raw artifacts are committed.
- The README and notes describe the design and operational decisions without
  requiring the reader to reverse-engineer the code.

## Change Hygiene

- Keep commits scoped to a single scenario or infrastructure concern.
- Do not modify or delete another scenario to make the current one pass.
- Run the smallest relevant checks before declaring work complete.
- Update this file when a repeated decision becomes a project-wide rule.
