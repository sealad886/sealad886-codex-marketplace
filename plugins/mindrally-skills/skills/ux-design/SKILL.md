---
name: ux-design
description: "Use when investigating or improving user tasks, navigation, content disclosure, recovery, or usability evaluation."
---

# User experience evidence and flows

## When to invoke

Use when investigating or improving user tasks, navigation, content disclosure, recovery, or usability evaluation.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect user goals, existing flows/content, supported audience/devices, research evidence, accessibility target, and constraints.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. State the task, observed friction, and assumptions that need evidence.
2. Design the smallest coherent flow with clear content, state, and recovery.
3. Evaluate with appropriate users/tasks and accessible interaction checks; revise from evidence.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Record task-based usability observations, accessibility checks, and known research/sample limits without claiming success from design opinion alone.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
