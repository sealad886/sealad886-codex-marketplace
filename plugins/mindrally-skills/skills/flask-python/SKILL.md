---
name: flask-python
description: "Use when implementing Flask application factories, blueprints, validation, persistence, authentication, or request handling."
---

# Flask Python Development

## When to invoke

Use when implementing Flask application factories, blueprints, validation, persistence, authentication, or request handling. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Flask/Python/extension versions, app/request context, configuration, WSGI/ASGI deployment, auth and database ownership. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace the route contract and app factory/configuration boundaries.
2. Implement runtime validation, explicit authentication/resource authorization and safe errors with managed client/database lifetimes.
3. Use the test client and target database checks for invalid input, sessions/CSRF, failures, context teardown and production configuration.

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
