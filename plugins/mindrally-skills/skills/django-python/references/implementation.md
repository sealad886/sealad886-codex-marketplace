# Django Python: implementation guidance

## Validation and transactions

Forms/ModelForms validate their configured inputs, but model save does not
automatically call full_clean. Keep validation paths and database constraints
explicit, including bulk writes. Use transaction.atomic for coherent writes and
on_commit for effects that must follow a successful commit. Signals are not a
general decoupled error-handler or a substitute for explicit business control flow.
Choose function/class-based views according to the existing code and actual needs.

## Queries, background work, and security

Use select_related for suitable single-valued relations and prefetch_related for
appropriate collections; measure query count and fetched data. Parameterize any
necessary raw SQL. Caches require user/permission-sensitive keys and invalidation.
Celery is optional task infrastructure, not the default solution for every I/O
operation; preserve async/sync runtime constraints and retry idempotency. DRF,
Redis, Celery, WhiteNoise and a CDN are not mandatory Django dependencies. Check
CSRF, output escaping, host/HTTPS settings, secret handling, and authorization at
resource boundaries. Database migrations need reviewed data conversion and recovery.

## Primary documentation

- [full_clean is not automatically invoked by save](https://docs.djangoproject.com/en/stable/ref/models/instances/).
- [Atomic transactions and on_commit](https://docs.djangoproject.com/en/stable/topics/db/transactions/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
