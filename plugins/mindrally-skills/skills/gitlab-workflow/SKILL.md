---
name: gitlab-workflow
description: "Use when working on GitLab merge requests, pipelines, environments, security jobs, issues, or repository gates."
---

# GitLab Workflow Best Practices

## When to invoke

Use when working on GitLab merge requests, pipelines, environments, security jobs, issues, or repository gates. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect GitLab offering/version/tier, MR head/base, CI includes/expanded jobs, runner scopes, variables, protected environments and task authority. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inspect MR policy and pipeline sources/revisions before changing jobs or review state.
2. Implement focused provider-correct CI/rules/artifacts with isolated dependencies, least privilege and protected deployments.
3. Validate expanded configuration and actual pipelines/reviews, then verify authorized integration and cleanup from readback.

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
