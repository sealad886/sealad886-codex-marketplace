---
name: testing
description: "Use when selecting or improving tests that prove a requirement, failure mode, public contract, or regression."
---

# Behavioral regression testing

## When to invoke

Use when selecting or improving tests that prove a requirement, failure mode, public contract, or regression.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect the requirement/defect, public interfaces, risk, existing test framework/fixtures, environment, and validation cost.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. State the invariant and choose the narrowest reliable test boundary.
2. Cover meaningful success, failure, and boundary cases with controlled data.
3. Run relevant tests and investigate failures before broadening checks.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run the chosen focused and relevant broader checks, record exact outcomes, and distinguish environment failure from product failure.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
