# Ruby on Rails development: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Rails 8 provides Solid Queue/Cache/Cable, Propshaft, Kamal tooling, and an authentication generator; use the project’s configured adapters rather than replacing them automatically.

- Neither PostgreSQL nor Redis/Sidekiq is mandatory for Rails. Database choice and production migration behavior depend on the existing deployment.

- Generators are useful when available, but inspect generated diffs and avoid overwriting existing files. bin/dev exists only in projects that configure it.

- Strong parameters constrain writable attributes but do not replace record-level authorization. Devise authenticates; Pundit authorizes; neither supplies the other automatically.

- Choose eager loading from observed association access and query counts. Index changes need query evidence and an appropriate migration plan.

- Use ActiveJob with the configured backend; retries require idempotency and transaction-aware enqueueing.

- Hotwire, Tailwind, ViewComponent, Vite, RSpec, and FactoryBot are optional project choices, not universal requirements.

- Keep business logic in cohesive existing boundaries; neither fat models nor service objects should be imposed by slogan.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Rails 8 introduces Solid defaults, Propshaft, Kamal changes, and authentication generation.](https://guides.rubyonrails.org/8_0_release_notes.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
