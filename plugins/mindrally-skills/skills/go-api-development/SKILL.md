---
name: go-api-development
description: "Use when implementing Go net/http handlers, ServeMux routing, JSON APIs, middleware or request tests."
---

# Go API Development with Standard Library

## When to invoke

Use when implementing Go net/http handlers, ServeMux routing, JSON APIs, middleware or request tests. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect go.mod/toolchain, public handler/service contracts, callers, shared state, downstream resources, auth and deployment constraints. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace the request/domain/resource path and define errors, ownership, cancellation and authorization invariants.
2. Implement supported routing/data APIs with bounded parsing, contextual I/O, explicit synchronization and coherent side effects.
3. Run focused tests and appropriate race/integration checks; verify timeout, shutdown, invalid input and denied-resource behavior.

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
