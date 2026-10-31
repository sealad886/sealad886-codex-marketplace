# Laravel: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Application behavior

- Choose PHP syntax and framework features supported by composer constraints; PHP 8.1 is not a universal requirement for current Laravel releases.
- Form Requests, policies, API Resources and Blade are tools to select according to interface needs.
- Use eager loading where measured relationship access would cause N+1 queries; bound pagination and selected data.

## Persistence and testing

- Repositories are optional abstraction boundaries, not a required layer over every Eloquent model.
- Use transactions for coupled writes and dispatch jobs at the correct commit boundary.
- Test validation, denied operations, serialization and transaction rollback; use Dusk only for browser behavior that needs it.
- Cache based on ownership and invalidation requirements; queues do not remove the need for idempotency and retry limits.

## Primary documentation

- [Primary documentation](https://laravel.com/docs/13.x/eloquent-relationships) — Eloquent supports explicit relationships and eager loading to manage related-query behavior.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
