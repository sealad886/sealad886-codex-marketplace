---
name: playwright-cursor-rules
description: "Use when maintaining Playwright tests with stable locators, conditional waits, fixtures, parallel isolation, or browser coverage."
---

# Playwright Cursor Rules

## When to invoke

Use for maintaining Playwright tests with stable locators, conditional waits, fixtures, parallel isolation, or browser coverage.

## Inputs and evidence

Inspect installed Playwright Test APIs, configuration, fixture/test data ownership, browser matrix and failing trace where relevant. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Name the required behavior and choose a stable observable assertion.
2. Use fixtures and selectors based on accessible semantics or intentional test contracts.
3. Synchronize through awaited assertions/events and isolate mutable state across workers.
4. Run focused then relevant browser coverage and disposition flaky failures from evidence.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Stable-condition tests pass under the required parallel/browser configuration with owned state and actionable failure artifacts.

## Must not

Do not use retries or broad waits to conceal unresolved race conditions. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
