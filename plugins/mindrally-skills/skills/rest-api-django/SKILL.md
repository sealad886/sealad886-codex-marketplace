---
name: rest-api-django
description: "Use when implementing Django REST Framework endpoints, serializers, permissions, ORM queries, or API failure handling."
---

# Django REST API boundaries

## When to invoke

Use when implementing Django REST Framework endpoints, serializers, permissions, ORM queries, or API failure handling.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Django/DRF versions, URL/view conventions, serializers, authentication classes, permission checks, schema, and query patterns.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define request/response and authorization contracts at the endpoint boundary.
2. Use existing generic views/viewsets or APIViews with explicit serializer validation and scoped querysets.
3. Verify successful, invalid, unauthorized, and cross-user cases plus query behavior.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run DRF API tests for validation, permissions, object isolation, transaction failure, and query counts where affected.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
