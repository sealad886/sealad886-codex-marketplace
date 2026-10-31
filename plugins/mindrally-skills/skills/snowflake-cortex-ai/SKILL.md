---
name: snowflake-cortex-ai
description: "Use when designing Snowflake AI SQL calls, extraction/classification, Cortex Search retrieval, or bounded model evaluation."
---

# Snowflake Cortex AI and retrieval

## When to invoke

Use when designing Snowflake AI SQL calls, extraction/classification, Cortex Search retrieval, or bounded model evaluation.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect account/region availability, exact function signatures, model access, privileges, data residency policy, evaluation data, and cost authority.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Choose a documented function and confirm its signature, return type, privileges, and regional availability.
2. Prototype on an approved small sample with explicit budgets and structured-output validation.
3. Evaluate semantic quality, error/null behavior, retrieval authorization, and measured usage before batch execution.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Validate SQL signatures and outputs on approved samples only when account access/cost authority exists; report semantic evaluation and live service checks omitted.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
