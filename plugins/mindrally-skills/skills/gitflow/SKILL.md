---
name: gitflow
description: "Use when working in a repository that explicitly uses Gitflow feature, develop, release, or hotfix branches."
---

# Gitflow

## When to invoke

Use when working in a repository that explicitly uses Gitflow feature, develop, release, or hotfix branches. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect documented branching model, main/develop identities, status/worktrees, release base, version sources and mutation authority. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Confirm Gitflow is actually the repository policy and inspect pending/shared work before switching branches.
2. Plan or implement the authorized feature/release/hotfix path with verified source/destination refs and focused changes.
3. Verify review/CI/integration and required back-merges; tag/publish/delete only under the corresponding authority.

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
