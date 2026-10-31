# RSpec behavioral tests: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use describe/context/it to express behavior and conditions; avoid asserting private call sequences when a stable public result is available.

- `let` is lazy per-example memoized setup; `let!` runs through a before hook. Use eager setup only when side effects are required before the example.

- Factories and fixtures are alternatives; do not add FactoryBot or Shoulda Matchers solely to satisfy a generic example.

- The source validation matchers are supplied by Shoulda Matchers, not RSpec core; verify installed integrations before using them.

- Use verifying doubles where applicable and isolate true external service boundaries; avoid mocking so much that a broken integration still passes.

- Keep database cleanup compatible with transactions, concurrent jobs, and system/browser tests.

- Use shared examples when the same behavior contract applies to several subjects; avoid hidden broad setup in shared contexts.

- Reproduce order dependence with the reported random seed and run the failure in isolation before changing production code.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [RSpec core provides examples, shared examples, metadata, and per-example execution scopes.](https://github.com/rspec/rspec-core)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
