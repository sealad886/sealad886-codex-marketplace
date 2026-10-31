---
name: ruby-rails
description: "Use when changing Rails models, controllers, migrations, jobs, caching, Hotwire views, or integration behavior."
---

# Ruby on Rails development

## When to invoke

Use when changing Rails models, controllers, migrations, jobs, caching, Hotwire views, or integration behavior.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Rails/Ruby versions, database adapter, routes, schema, job/cache adapters, assets, and test conventions.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Locate the Rails boundary that owns the requested behavior and existing conventions.
2. Implement validated/authorized requests and coherent data changes using supported framework primitives.
3. Verify migration, job, caching, and browser behavior relevant to the change.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run relevant Rails tests, migration checks in a disposable database, and changed job/view flows; state omitted production or device checks.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
