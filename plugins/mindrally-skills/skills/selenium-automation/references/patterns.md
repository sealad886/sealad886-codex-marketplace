# Selenium WebDriver tests: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use Selenium Manager where supported before adding webdriver-manager; browser/driver downloads depend on the environment and approved installation policy.

- Do not add --no-sandbox by default; diagnose the actual container/browser requirement before weakening isolation.

- Do not mix implicit and explicit waits; use bounded waits for the condition the action needs. Presence is not visibility or interactability.

- element_to_be_clickable checks visibility/enabled state but cannot guarantee no overlay intercepts a click; inspect the actual interaction failure.

- Choose stable IDs, labels, attributes, or scoped selectors by application semantics; no locator category is universally most reliable.

- Use page objects when they reduce duplication without hiding assertions or broad side effects. Keep tests independent and use approved synthetic accounts.

- Handle frames/windows/alerts explicitly and restore context; use a full configured base URL rather than assuming driver.get accepts relative app paths.

- Always quit the driver in teardown/finally. Retries can hide defects; preserve first failure evidence and fix synchronization/root cause.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Mixing implicit and explicit waits creates unpredictable timeout behavior.](https://www.selenium.dev/documentation/webdriver/waits/)
- [Selenium Manager provides supported automated driver management.](https://www.selenium.dev/documentation/selenium_manager/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
