# Kotlin Development Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Types and data

- Kotlin uses Any, not JavaScript any; use inference for clear local values and explicit API types where needed.
- val prevents reassignment, not mutation of a referenced object. Read-only collection interfaces do not prove deep immutability.
- Use data classes for value semantics when appropriate; domain invariants still need deliberate construction/validation.

## Functions and concurrency

- Follow repository style rather than fixed instruction counts, no-blank-line rules, or invented arrow-function requirements.
- Use suspend functions and structured coroutine scopes for asynchronous ownership; suspension is not guaranteed non-blocking if the body calls blocking APIs.
- Choose dispatchers for the workload and avoid swallowing CancellationException in broad catches.
- Test public behavior and meaningful boundaries rather than mandating one test for every public function.

## Primary documentation

- [Primary documentation](https://kotlinlang.org/docs/coroutines-basics.html) — Kotlin coroutines suspend computations and run on managed threads with structured lifetimes.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
