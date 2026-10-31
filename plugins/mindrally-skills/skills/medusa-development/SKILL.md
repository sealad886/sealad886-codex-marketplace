---
name: medusa-development
description: "Use when extending Medusa v2 modules, data models, workflows, routes, subscribers, jobs, or admin interfaces."
---

# Medusa Development

## When to invoke

Use for extending Medusa v2 modules, data models, workflows, routes, subscribers, jobs, or admin interfaces.

## Inputs and evidence

Inspect Medusa/framework versions, module services/links, workflow conventions, authentication/ownership, persistence invariants and admin SDK setup. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Model the domain and invariants using supported module/data-model APIs.
2. Compose multi-step mutations with workflow steps, compensation and explicit concurrency behavior.
3. Expose validated authorized routes or subscribers and select Query for appropriate cross-module reads.
4. Test workflow success, retries, compensation, ownership and concurrent mutations.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Module/workflow tests establish invariants under retries, denial, failure compensation and concurrency.

## Must not

Do not assume compensation makes arbitrary commerce side effects atomic or reversible. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
