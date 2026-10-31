---
name: cypress
description: "Use when writing or diagnosing Cypress component or end-to-end tests, sessions, network assertions, or flaky workflows."
---

# Cypress Testing Best Practices

## When to invoke

Use when writing or diagnosing Cypress component or end-to-end tests, sessions, network assertions, or flaky workflows. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Cypress version/configuration, user behavior, selectors, state reset, network contracts, credentials, and test environment. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define a user-observable outcome and independent setup using controlled test data.
2. Queue Cypress commands with retryable assertions and synchronize on meaningful UI/network conditions.
3. Run the test alone and in its suite; inspect failures, session restoration, cleanup, and artifacts without hiding flakiness.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
