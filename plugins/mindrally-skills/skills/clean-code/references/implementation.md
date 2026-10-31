# Clean Code: implementation guidance

## Readability and abstraction

Keep functions cohesive rather than counting lines. A comment may explain a real
invariant, algorithm, side effect, or external constraint; needing a comment does
not automatically require splitting a function. Keep constants near their owning
concept rather than collecting all values in a global constants module. Avoid
speculative configuration or frameworks, but an interface with one implementation
can still protect an actual dependency boundary. The rule of three is a heuristic,
not permission to duplicate security or business invariants.

## Preserve semantics and scope

Refactoring can change evaluation order. The upstream canCheckout rewrite reads
a credit limit before short-circuit checks that previously prevented the read;
retain laziness when getters, nullability, side effects, or cost make it observable.
Remove obsolete code and callers within the authorized scope after reference
checks. Do not expand into unrelated cleanup. Tests should prove behavior and
regressions, not enforce preferred prose/structure or a fixed edge-case quota.
Use the simplest meaningful check for the risk, and report untested integration.
Commits and external publication still follow the user's authority.

## Primary documentation

- [Review functionality, complexity, tests and design](https://google.github.io/eng-practices/review/reviewer/looking-for.html).
- [Short-circuit evaluation semantics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Logical_AND).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
