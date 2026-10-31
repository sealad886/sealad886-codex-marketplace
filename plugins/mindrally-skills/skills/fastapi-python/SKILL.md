---
name: fastapi-python
description: "Use when implementing FastAPI endpoints, dependencies, Pydantic models, lifespan, or async data access."
---

# FastAPI Python

## When to invoke

Use when implementing FastAPI endpoints, dependencies, Pydantic models, lifespan, or async data access. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect FastAPI/Pydantic version, API schema, dependency lifetimes, auth policy, database clients, and request limits. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define route input/output/error and resource authorization contracts.
2. Implement validated models and dependencies with correct sync/async resource lifecycle and safe serialization.
3. Test validation, response shape, denied access, cancellation/errors, lifespan cleanup, and actual client/database behavior.

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
