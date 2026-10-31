# Playwright Testing Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Locators and synchronization

- Role/label locators improve user-facing tests but do not by themselves prove full accessibility.
- Use web-first expect assertions; load state is not equivalent to application readiness and networkidle can be unsuitable for realtime apps.
- Register waitForResponse before the triggering click/request to avoid races; prefer visible end-state assertions when transport is incidental.

## Isolation and evidence

- Browser contexts isolate client state, not shared database/accounts; use owned test data and parallel-safe cleanup.
- Device descriptors emulate viewport/input/user agent and are not physical-device acceptance.
- Retries help capture evidence but must not hide flakes; inspect first meaningful trace/network/console failure with secrets redacted.
- CSS locators are acceptable where they encode a stable required contract; avoid brittle incidental DOM chains and fixed sleeps.

## Primary documentation

- [Primary documentation](https://playwright.dev/docs/locators) — Playwright locators support auto-waiting and semantic or explicit test-ID targeting.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
