---
name: autogen-development
description: "Use when building AutoGen AgentChat agents, tools, teams, state persistence, or controlled code execution."
---

# AutoGen Multi-Agent Development

## When to invoke

Use when building AutoGen AgentChat agents, tools, teams, state persistence, or controlled code execution. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect installed autogen packages and API generation, model client, tool schemas, team termination, execution permissions, and cost limits. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Choose the installed AgentChat/Core API and define agent responsibilities, tool trust boundaries, and bounded termination.
2. Implement asynchronous agents and teams with supported executors, explicit state save/load, and owned resource lifetimes.
3. Check tool validation, multiple handoffs, cancellation, termination, state restore, model-client cleanup, and executor failures.

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
