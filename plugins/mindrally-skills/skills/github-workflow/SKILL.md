---
name: github-workflow
description: "Use when working on GitHub pull requests, review outcomes, issues, Actions, CODEOWNERS, or repository workflows."
---

# GitHub Workflow Best Practices

## When to invoke

Use when working on GitHub pull requests, review outcomes, issues, Actions, CODEOWNERS, or repository workflows. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect verified repository/remote, PR head/base revisions, policy/rulesets, review requests, checks/events, workflow permissions and user authority. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inspect the actual task/PR state and define scoped changes with clear behavior and verification evidence.
2. Implement authorized workflow or review repairs with least-privilege triggers, trusted artifacts and revision-bound outcomes.
3. Read all actionable feedback and checks at the actual revision; verify required gates and authorized merged/published state separately.

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
