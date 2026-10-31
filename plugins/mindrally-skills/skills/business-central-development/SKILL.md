---
name: business-central-development
description: "Use when implementing Business Central AL tables, pages, codeunits, extensions, reports, or job queues."
---

# Microsoft Dynamics 365 Business Central Development

## When to invoke

Use when implementing Business Central AL tables, pages, codeunits, extensions, reports, or job queues. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Business Central/runtime version, app.json dependencies, object ID ranges, table schema, permissions, and transaction boundary. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Identify extension points, business invariants, data classification, and authorized schema changes.
2. Implement AL objects/events and validation with platform-correct error handling and efficient record access.
3. Compile/analyze against target symbols and test permissions, transactions, upgrades, and user-facing behavior in a sandbox.

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
