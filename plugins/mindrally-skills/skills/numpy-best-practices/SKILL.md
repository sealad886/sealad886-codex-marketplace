---
name: numpy-best-practices
description: "Use when implementing NumPy array operations, broadcasting, dtype control, random sampling, numerical validation, or performance tuning."
---

# NumPy Best Practices

## When to invoke

Use for implementing NumPy array operations, broadcasting, dtype control, random sampling, numerical validation, or performance tuning.

## Inputs and evidence

Inspect NumPy version, shapes/dtypes/units, aliasing ownership, numerical tolerances, memory budget and random reproducibility needs. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define shape, dtype, finite-value and mutation contracts.
2. Choose array operations and broadcasting that preserve semantics without excessive temporaries.
3. Manage copies/views, numerical error and PRNG ownership explicitly.
4. Test representative boundary arrays and measure time/peak memory before optimizing.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Numerical tests cover shape/dtype/aliasing and nonfinite behavior; performance evidence includes allocation cost.

## Must not

Do not mutate shared views or assume seeded random values are identical across all versions/platforms. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
