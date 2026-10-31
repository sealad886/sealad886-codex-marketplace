---
name: fastapi-microservices-serverless
description: "Use when deploying or adapting FastAPI services to serverless gateways, stateless scaling, or distributed workloads."
---

# FastAPI Microservices Serverless

## When to invoke

Use when deploying or adapting FastAPI services to serverless gateways, stateless scaling, or distributed workloads. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect FastAPI/Starlette/Pydantic versions, ASGI adapter/runtime, request/time limits, connection model, auth propagation, and telemetry. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define stateless request behavior and verify the provider ASGI/lifespan and background-work contract.
2. Implement bounded I/O, external state only where required, application authorization, and safe retry/idempotency behavior.
3. Test gateway paths/headers, cold starts, concurrency/pool limits, timeouts, and observability without claiming local tests prove hosted behavior.

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
