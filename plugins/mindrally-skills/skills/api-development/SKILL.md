---
name: api-development
description: "Use when designing or implementing HTTP APIs in Go net/http or NestJS TypeScript."
---

# API Development

## When to invoke

Use when designing or implementing HTTP APIs in Go net/http or NestJS TypeScript. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect the API contract, Go or NestJS version, handlers/controllers, validation, authentication, and persistence boundaries. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Identify request/response schemas, error semantics, ownership checks, and compatibility requirements for the changed endpoint.
2. Implement the selected Go handler or NestJS controller/service boundary with bounded parsing and explicit validation.
3. Verify success, malformed/oversized input, denied access, resource absence, cancellation, and documented response contracts.

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
