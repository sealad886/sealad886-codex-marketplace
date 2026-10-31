---
name: technical-writing
description: "Use when writing developer tutorials, API explanations, operational guides, or implementation documentation grounded in actual behavior."
---

# Technical explanations and tutorials

## When to invoke

Use when writing developer tutorials, API explanations, operational guides, or implementation documentation grounded in actual behavior.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect audience/task, source implementation, version constraints, supported commands, examples, and document publishing format.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. State the reader’s goal, prerequisites, and scope clearly.
2. Explain the verified implementation in task order with appropriately scoped examples.
3. Check facts, references, safe runnable examples, and accessibility before delivery.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run existing docs/link/render checks and safe example validation; report factual or execution uncertainty explicitly.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
