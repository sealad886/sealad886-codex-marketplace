# Django REST API Development: implementation guidance

## Permission and validation boundaries

DRF authentication is separate from permission enforcement. Object permissions
are not automatically applied to every object in list querysets or to creation;
scope get_queryset and enforce create rules in the supported serializer/view hook.
Validate serializer fields and nested writes explicitly rather than trusting input
owner IDs. Use the project's authentication mechanism; SimpleJWT is optional,
and session authentication has CSRF requirements. CORS is not authorization.

## Errors and performance

Use DRF exception handling and documented status behavior rather than a universal
422 or custom response envelope. Signals are not a general exception handling
layer. Keep transactions scoped to the data invariant and defer irreversible
side effects until commit where required. Measure select_related/prefetch_related,
projections and query counts; avoid overfetching while fixing N+1. Bound pagination,
filters and uploads. Cache by authorization context and invalidate coherently.
Connection pooling depends on database/deployment and is not a generic flag.
Run backend-appropriate integration tests for constraints and transaction behavior.

## Primary documentation

- [Object permission list/create limitations](https://www.django-rest-framework.org/api-guide/permissions/).
- [DRF error handling and status semantics](https://www.django-rest-framework.org/api-guide/exceptions/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
