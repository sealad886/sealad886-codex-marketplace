---
name: bash-scripting
description: "Use when writing or debugging Bash automation, argument parsing, pipelines, cleanup, or scheduled scripts."
---

# Bash Scripting

## When to invoke

Use when writing or debugging Bash automation, argument parsing, pipelines, cleanup, or scheduled scripts. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect target shell/version, invocation environment, arguments, path ownership, exit contracts, and permissions. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Confirm Bash versus POSIX sh requirements and inspect every command substitution, expansion, and destructive boundary.
2. Implement explicit argument validation, quoted arrays/expansions, bounded resource ownership, and deliberate error propagation.
3. Run syntax/lint and safe fixtures covering missing arguments, spaces, failures, signals, and cleanup.

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
