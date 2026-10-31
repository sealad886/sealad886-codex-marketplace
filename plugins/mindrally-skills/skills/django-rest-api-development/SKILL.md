---
name: django-rest-api-development
description: "Use when building Django REST Framework serializers, views, permissions, pagination, or transactional APIs."
---

# Django REST API Development

## When to invoke

Use when building Django REST Framework serializers, views, permissions, pagination, or transactional APIs. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Django/DRF versions, API schema, authentication mode, queryset visibility, serializer writes, and database invariants. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define HTTP/input/error contracts and caller/object/organization access rules at each endpoint.
2. Implement serializer validation, scoped querysets, explicit create/update ownership, and coherent transactions.
3. Test anonymous/wrong-owner/list/create access, invalid and partial input, concurrency, pagination, and query behavior.

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
