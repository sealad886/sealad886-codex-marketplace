---
name: selenium-automation
description: "Use when implementing Selenium browser tests, resilient locators, explicit waits, page abstractions, or cross-browser checks."
---

# Selenium WebDriver tests

## When to invoke

Use when implementing Selenium browser tests, resilient locators, explicit waits, page abstractions, or cross-browser checks.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Selenium/browser/driver versions, application base URL, fixtures, waits, test isolation, and failure artifacts.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Express the user-visible behavior and stable element identity.
2. Use supported driver management and condition-based synchronization.
3. Run focused browser scenarios and collect bounded diagnostic artifacts for real failures.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run relevant browsers in the declared mode and test success/error paths; report untested browsers and retain redacted failure artifacts.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
