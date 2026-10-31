---
name: robocorp-cursor-rules
description: "Use when implementing Robocorp Python tasks, RPA workflows, task lifecycle, logging, or controlled external automation."
---

# Robocorp Python automation

## When to invoke

Use when implementing Robocorp Python tasks, RPA workflows, task lifecycle, logging, or controlled external automation.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect robocorp-tasks/RPA Framework versions, task runner configuration, work items, credentials, and authorized external effects.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify task entrypoints and the automation’s retry/idempotency boundary.
2. Implement small Python tasks with explicit resource lifetime and validated external input.
3. Run with synthetic or approved work items and verify outputs, failures, and log redaction.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Execute a harmless representative task with synthetic work items when dependencies exist, then inspect failure handling and redacted logs.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
