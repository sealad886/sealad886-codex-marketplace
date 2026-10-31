---
name: bitbucket-workflow
description: "Use when working on Bitbucket pull requests, Pipelines, merge checks, or Jira-linked development."
---

# Bitbucket Workflow Best Practices

## When to invoke

Use when working on Bitbucket pull requests, Pipelines, merge checks, or Jira-linked development. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Bitbucket Cloud versus Data Center, plan/features, branch policy, pipeline YAML, PR revision, and integration permissions. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inspect established branch/review rules and keep the PR focused with reproducible verification evidence.
2. Implement and validate version-correct pipeline steps, artifacts, services, caches, and protected deployment boundaries.
3. Read back actual builds/reviews/merge conditions and distinguish pending checks from completed outcomes.

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
