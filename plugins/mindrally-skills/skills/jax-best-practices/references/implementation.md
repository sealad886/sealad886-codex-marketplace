# JAX Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Transformations and state

- Keep transformed functions pure and pass state explicitly; use pytrees for structured parameters and state.
- Use jax.random key splitting or supported typed-key APIs; independent operations need independent keys.
- Use JAX control-flow primitives where traced values cannot drive Python branching; static arguments can cause recompilation.

## Performance and validation

- Warm up compiled functions and call block_until_ready on results before recording execution time.
- Account for host/device transfers, shape/dtype specialization, precision settings, and backend differences.
- Use rematerialization or sharding when memory/scale evidence warrants it; validate gradient and numerical behavior after changes.

## Primary documentation

- [JAX benchmarking](https://docs.jax.dev/en/latest/benchmarking.html) — JAX benchmarks separate compilation/transfer and synchronize results with block_until_ready.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
