# Machine Learning: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Functional JAX training

- Pass mutable model/optimizer state explicitly and split random keys for independent operations.
- Use grad/vmap/jit on appropriate boundaries; Python control flow depending only on static values can be valid inside jit.
- Use lax.cond/scan/fori_loop for traced control flow where required; model libraries such as Flax are optional choices.

## Evaluation and resources

- Prevent data leakage and use task-appropriate metrics, subgroup/error analysis and justified numerical tolerances.
- Track warm compilation versus synchronized steady-state timing, host/device transfers, and peak memory.
- Checkpointing/sharding/rematerialization must match device capabilities and recovery needs; no automatic performance guarantee follows from JIT.

## Primary documentation

- [Primary documentation](https://docs.jax.dev/en/latest/control-flow.html) — JAX distinguishes static Python control flow from traced value-dependent control flow.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
