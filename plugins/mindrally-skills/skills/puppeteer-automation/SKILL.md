---
name: puppeteer-automation
description: "Use when automating browser interactions, extraction, screenshots, PDFs, interception, or isolated browser sessions with Puppeteer."
---

# Puppeteer Browser Automation

## When to invoke

Use for automating browser interactions, extraction, screenshots, PDFs, interception, or isolated browser sessions with Puppeteer.

## Inputs and evidence

Inspect Puppeteer/browser versions, allowed targets/actions, context ownership, selectors, downloads/output paths and authentication sensitivity. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use supported browser/context APIs with isolation and explicit resource ownership.
2. Synchronize actions through locators or precise conditions/events before triggers.
3. Capture/extract only required data and validate screenshot/PDF completeness.
4. Close owned resources in finally and test failures, timeouts and repeated runs.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Targeted automation succeeds and failure/retry tests prove cleanup; screenshot/PDF claims include actual artifact inspection.

## Must not

Do not disable sandboxing, bypass target access controls, or reuse real user browser sessions without authority. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
