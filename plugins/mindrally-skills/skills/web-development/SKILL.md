---
name: web-development
description: "Use when implementing HTML/CSS, Bootstrap, Django templates/forms, or HTMX-enhanced web interactions."
---

# Server-rendered web features

## When to invoke

Use when implementing HTML/CSS, Bootstrap, Django templates/forms, or HTMX-enhanced web interactions.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect existing framework versions, template/view/form ownership, auth/CSRF setup, response fragments, and browser support.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define the server-rendered behavior and optional client enhancement.
2. Implement semantic accessible templates with validated/authorized server handlers.
3. Verify normal navigation, enhanced requests, errors, and responsive rendering.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run view/form tests and browser checks for full/fragment requests, CSRF rejection, unauthorized objects, keyboard use, and responsive layout.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
