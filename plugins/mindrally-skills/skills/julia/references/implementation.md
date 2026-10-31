# Julia Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Dispatch and data representation

- Write methods generic enough for the required inputs; argument annotations primarily select dispatch and do not inherently improve performance.
- Use concrete fields and function barriers to help inference; distinguish abstract interfaces from concrete stored values.
- Use immutable structs or mutable state according to ownership needs; StaticArrays are an optional dependency for suitable small fixed-size data.

## Performance, display, and tests

- Avoid untyped global state in hot paths; inspect allocations and inference with project-supported tooling.
- Benchmark warmed functions and account for interpolation/setup; use views when aliasing and lifetime are acceptable.
- Implement show(io, value) for a deliberate textual representation; dump is a structural debugging facility.
- Use Test testsets and expected-error/numerical cases; document public APIs and unusual behavior rather than mandating docstrings on every private function.

## Primary documentation

- [Julia performance tips](https://docs.julialang.org/en/v1/manual/performance-tips/) — Performance depends on type stability and function boundaries; annotations are not inherently speedups.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
