---
name: ci-cd-best-practices
description: "Use when implementing or diagnosing build/test pipelines, artifact promotion, deployment gates, or rollback procedures."
---

# CI/CD Best Practices

## When to invoke

Use when implementing or diagnosing build/test pipelines, artifact promotion, deployment gates, or rollback procedures. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect CI provider/version, triggers, tested revision, runner permissions, artifacts/cache boundaries, existing gates, and deployment authority. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Map triggers and revision identity to build, verification, artifact promotion, and required approvals.
2. Implement deterministic installs and isolated jobs with minimal permissions, trustworthy artifacts, bounded execution, and explicit dependencies.
3. Validate provider syntax and actual runs; diagnose first meaningful failures and verify authorized rollout/recovery behavior.

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
