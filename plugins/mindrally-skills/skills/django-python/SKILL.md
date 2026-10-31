---
name: django-python
description: "Use when implementing Django models, forms, views, authentication, migrations, or query performance."
---

# Django Python

## When to invoke

Use when implementing Django models, forms, views, authentication, migrations, or query performance. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Django/Python version, URL/view/model/form boundaries, database constraints, auth policy, and deployment settings. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace the requested view/domain behavior and define input, permission, and transaction contracts.
2. Implement forms/model/query behavior using existing Django features and explicit side-effect ownership.
3. Check invalid input, access/CSRF, database constraints, query counts, migration behavior, and deployment-specific settings.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
