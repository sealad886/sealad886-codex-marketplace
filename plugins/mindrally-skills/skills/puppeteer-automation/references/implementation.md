# Puppeteer Browser Automation: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Current APIs and interaction

- Modern Puppeteer supports locators and createBrowserContext; old createIncognitoBrowserContext, $x and waitForTimeout recipes require version checking or replacement.
- page.waitForLoadState is a Playwright API, not a Puppeteer page API; choose Puppeteer’s documented readiness conditions.
- Headless launch option types changed; inspect installed LaunchOptions and keep the browser sandbox enabled unless an explicitly justified deployment environment requires another setup.
- Network idle is not universal app readiness; register navigation/response waits before triggering interactions.

## Resources, interception and outputs

- Use one coordinated interception policy; multiple handlers must not resolve the same request twice.
- Retry loops must release a newly created page/browser even when navigation fails; reuse resources only with isolated state.
- Blocking styles/images/fonts changes layout and content; do not use those results for faithful screenshots/PDFs without verification.
- PDF/font/image readiness and print CSS need artifact inspection; keep auth cookies/tokens and response bodies out of logs.
- Do not add stealth/bypass tooling as a default dependency; use authorized targets and respect access restrictions.

## Primary documentation

- [Primary documentation](https://pptr.dev/guides/page-interactions) — Current Puppeteer interaction documentation uses supported locator/wait interfaces tied to browser version.
- [Puppeteer context API](https://pptr.dev/api/puppeteer.browser.createbrowsercontext) — Current Browser API exposes createBrowserContext for isolated contexts.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
