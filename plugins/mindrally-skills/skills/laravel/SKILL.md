---
name: laravel
description: "Use when developing Laravel routes, Eloquent relationships, validation, Blade views, queues, or API resources."
---

# Laravel

## When to invoke

Use for developing Laravel routes, Eloquent relationships, validation, Blade views, queues, or API resources.

## Inputs and evidence

Inspect Laravel/PHP constraints, route/middleware configuration, data model, policies, frontend stack, and test environment. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Follow the existing Laravel application structure and service/container boundaries.
2. Validate requests and authorize domain operations through established policies.
3. Implement Eloquent queries/transactions, view/API transformations, and asynchronous jobs as needed.
4. Run focused feature/unit tests with database and queue failure cases.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Feature/unit tests cover requested contracts, authorization and persistence; browser tests are used only where relevant.

## Must not

Do not expose .env values or change database schema outside the requested migration scope. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
