---
name: scipy-best-practices
description: "Use when implementing SciPy optimization, interpolation, integration, linear algebra, statistics, or signal processing."
---

# SciPy numerical methods

## When to invoke

Use when implementing SciPy optimization, interpolation, integration, linear algebra, statistics, or signal processing.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect SciPy/NumPy versions, mathematical model, units, array shapes, tolerances, data assumptions, and reference solutions.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Choose a numerical method matching smoothness, constraints, structure, and error budget.
2. Implement explicit bounds/tolerances and inspect solver diagnostics.
3. Compare against analytical or trusted reference cases and assess stability and sensitivity.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run reference-solution and failure cases using justified absolute/relative tolerances; report convergence and numerical limitations.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
