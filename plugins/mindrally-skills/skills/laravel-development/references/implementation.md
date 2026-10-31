# Laravel Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Framework integration

- Match PHP and Laravel APIs to composer.lock and supported toolchains rather than a fixed PHP 8.1 baseline.
- Prefer framework features where useful; a Repository wrapper is optional and should clarify a necessary domain boundary.
- Use policies/gates alongside authentication and CSRF defenses; validate request data before passing it to models.

## Assets and operations

- Current Laravel applications typically use Vite; retain Laravel Mix only when the project already declares and supports it.
- Review migration effects and test locally; applied/shared migration history should remain coherent and reversible where possible.
- Queue listeners/jobs may need after-commit dispatch and idempotent handling; scheduler configuration must match the deployed process model.
- Build frontend assets, exercise changed localization, and test failure/rollback paths without triggering production jobs.

## Primary documentation

- [Primary documentation](https://laravel.com/docs/13.x/vite) — Laravel documents Vite as the current asset bundling integration.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
