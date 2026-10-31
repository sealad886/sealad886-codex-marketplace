---
name: git-workflow
description: "Use when planning or performing authorized Git branching, selective commits, synchronization, conflict handling, or integration."
---

# Git Workflow Best Practices

## When to invoke

Use when planning or performing authorized Git branching, selective commits, synchronization, conflict handling, or integration. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect repo/common Git dir, status/index/untracked changes, worktrees, remotes/upstreams, current operations, hooks/signing and user authority. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inventory all existing work and verify branch/remote identities before choosing any mutation.
2. Apply the authorized coherent operation while preserving unrelated bytes/staging and repository policy.
3. Read back commits/refs/status and validation evidence; verify actual integration before any authorized cleanup.

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
