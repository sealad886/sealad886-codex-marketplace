---
name: readme-best-practices
description: "Use when writing or reviewing a project README, installation instructions, quick start, examples, or repository documentation links."
---

# README accuracy and usefulness

## When to invoke

Use when writing or reviewing a project README, installation instructions, quick start, examples, or repository documentation links.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect the intended audience, supported install paths, actual CLI/API behavior, assets, license, and published version.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify what a new reader needs to decide and accomplish first.
2. Write a truthful purpose and verified minimal installation/usage path.
3. Add only useful configuration, troubleshooting, contribution, and license links; check rendering and examples.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run existing documentation/link checks, resolve local assets, and execute safe quick-start examples when practical; report examples not executed.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
