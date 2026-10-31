# Angular: implementation guidance

## Components and reactive templates

Modern Angular components are standalone by default (from v19); older projects
may require explicit metadata or NgModules. Preserve the project structure rather
than importing mandatory suffixes from an older style guide. Use signals for local
reactive values and computed derivations; use RxJS where asynchronous streams need
its operators. Use `async` or lifecycle-safe subscription handling. `inject()` is
available in injection contexts; do not call it arbitrarily outside those contexts.

## Rendering, performance, and security

Use built-in template control flow and stable `@for` tracking in versions that
support it; do not prescribe deprecated `*ngFor` for new code. Use deferred views
and image optimization when they improve the measured path. Pure pipes still have
costs; signals do not automatically eliminate all rendering work. Let Angular
sanitize supported bindings, and avoid bypass-security trust APIs for untrusted
values. Validate at server boundaries as well as forms. Check component behavior
and service contracts with the project's actual test runner; no fixed coverage
percentage proves correctness. Preserve formatter and model-type conventions.

## Primary documentation

- [Standalone component defaults and imports](https://angular.dev/guide/components).
- [Built-in control flow and track expressions](https://angular.dev/guide/templates/control-flow).
- [Sanitization and security trust boundaries](https://angular.dev/best-practices/security).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
