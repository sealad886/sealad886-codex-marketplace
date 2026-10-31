---
name: deno-typescript
description: "Use when implementing Deno TypeScript services, permissions, module resolution, KV, or native tooling."
---

# Deno TypeScript Development

## When to invoke

Use when implementing Deno TypeScript services, permissions, module resolution, KV, or native tooling. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect installed Deno version, deno.json/lockfile, imports, npm/JSR dependencies, runtime permissions, and target host. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inspect runtime and module/version constraints and define the minimum I/O permissions for the task.
2. Implement web-standard handlers and runtime validation using the current dependency/configuration workflow.
3. Run format/lint/type checks and behavior tests, then verify denied permissions, resource cleanup, and packaged behavior.

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
