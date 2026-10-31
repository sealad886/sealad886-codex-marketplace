# Playwright Cursor Rules: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Current APIs

- There is no general current page.waitFor API; use locator/web-first assertions, waitForURL/Response/Event or waitForFunction for a specific need.
- Use locator auto-waiting and expect conditions rather than fixed delays or broad load-state assumptions.
- Register event/response promises before the triggering action to avoid missed events.

## Maintainability and evidence

- Extract helpers only for coherent repeated behavior; avoid hiding assertions and ownership in a generic wrapper.
- Keep useful comments explaining unusual timing/invariants instead of banning inline comments universally.
- Browser projects/device descriptors supply selected browser/emulation coverage, not complete native-device qualification.
- Parallel test isolation includes servers, accounts, database state and downloaded files, beyond per-test browser contexts.

## Primary documentation

- [Primary documentation](https://playwright.dev/docs/api/class-page#page-wait-for-function) — Current Page API provides explicit wait methods rather than a generic page.waitFor.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
