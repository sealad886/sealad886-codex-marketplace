---
name: playwright
description: "Use when writing Playwright end-to-end tests, semantic locators, web-first assertions, browser projects, or trace diagnosis."
---

# Playwright Testing Best Practices

## When to invoke

Use for writing Playwright end-to-end tests, semantic locators, web-first assertions, browser projects, or trace diagnosis.

## Inputs and evidence

Inspect Playwright version/browser builds, baseURL, fixtures, test data ownership, concurrency and the user-visible requirement. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose critical behavior and isolate browser plus server-side test data.
2. Use accessible-role/label or stable test-ID locators and awaited actions.
3. Wait for observable assertions or specific events registered before the trigger.
4. Run required browser projects and inspect traces for actual failures before adding retries.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Required browser projects exercise isolated critical paths and pass without unexplained flakes; traces support failure diagnosis.

## Must not

Do not replace assertions with sleep or relabel emulated mobile coverage as physical-device testing. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
