---
name: jax-best-practices
description: "Use when implementing or profiling JAX transformations, differentiable numerical code, pytrees, randomness, or device execution."
---

# JAX Best Practices

## When to invoke

Use for JAX numerical and machine-learning code on configured devices.

## Inputs and evidence

Inspect jax/jaxlib versions, available backend/devices, array shapes/dtypes, PRNG ownership, transformation boundaries, and numerical tolerances. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Express numerical kernels as pure array functions with explicit state and random keys.
2. Apply jit, vmap, grad, or control-flow primitives to measured computation boundaries.
3. Check shapes, dtype/precision, compilation specialization, and device transfers.
4. Compare numerical results and benchmark synchronized warmed execution separately from compilation.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Numerical/gradient checks pass within justified tolerances and performance evidence separates transfer, compilation, and synchronized execution.

## Must not

Do not reuse random keys, hide Python side effects inside jit, or time asynchronous dispatch as completed computation. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
