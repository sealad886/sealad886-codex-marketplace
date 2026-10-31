---
name: laravel-development
description: "Use when implementing Laravel application architecture, service-container integration, migrations, jobs, or frontend bundling."
---

# Laravel Development

## When to invoke

Use for implementing Laravel application architecture, service-container integration, migrations, jobs, or frontend bundling.

## Inputs and evidence

Inspect composer/runtime versions, existing app conventions, asset build tool, database migrations, auth policies, and scheduler/queue configuration. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Extend existing routes, services and container bindings with explicit contracts.
2. Use validated requests, authorization, transactions, and deliberate event/job boundaries.
3. Integrate the configured asset pipeline and localization without assuming legacy defaults.
4. Run application, migration, queue and asset checks relevant to the change.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Relevant PHP tests, migration checks and frontend builds pass in the declared environment.

## Must not

Do not run production migrations, workers, schedules, or publication without explicit authority. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
