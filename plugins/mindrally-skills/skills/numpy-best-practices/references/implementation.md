# NumPy Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Arrays, views and types

- Basic slicing commonly creates views and advanced indexing creates copies; reshape may copy when layout requires it.
- In-place/out operations can modify aliases and require compatible casting; use them only with explicit ownership.
- np.empty contains uninitialized values until written; fixed-width integers can overflow and float32 trades precision for memory.
- np.asarray can still copy when dtype/layout demands it; NumPy 2 copy behavior needs version-aware checks.

## Numerics and tests

- Vectorization often reduces interpreter overhead but can increase temporaries; compare measured alternatives rather than forbidding loops.
- Use explicit runtime exceptions for untrusted shape/type validation instead of assertions that optimization may disable.
- Use assert_allclose with justified tolerances for floating point, exact assertions for exact contracts, and explicit NaN/Inf policy.
- Use Generator/default_rng with owned seeds; solve linear systems rather than forming an inverse unless the inverse itself is required.

## Primary documentation

- [Primary documentation](https://numpy.org/doc/stable/user/basics.copies.html) — Basic/advanced indexing and shape/layout operations have distinct view/copy semantics.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
