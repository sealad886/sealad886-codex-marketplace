# Ruby implementation: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Select pattern matching, keyword arguments, endless methods, and other syntax only when supported by the declared Ruby version.

- Use classes for cohesive state/behavior and modules for namespacing or appropriate mixins; avoid broad monkey patches and unnecessary metaprogramming.

- Use blocks, procs, and lambdas deliberately; their arity and return behavior differ.

- Rescue specific expected exceptions at a boundary that can handle them; do not swallow StandardError and pretend success.

- Use ensure or block-based resource APIs for files and network clients; validate untrusted input before use.

- Use safe navigation only where nil is legitimate, rather than hiding an unexpected missing object.

- Follow the configured formatter and test framework; RSpec, factories, and single-quote style are not Ruby requirements.

- Lazy enumeration reduces materialization for suitable workloads but is not automatically faster; measure allocations and time.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Ruby classes and modules have distinct inheritance and mixin behavior.](https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
