---
name: google-adk
description: "Use when building Google ADK agents, typed tools, workflow orchestration, sessions/state, artifacts, memory or evaluations."
---

# Google Agent Development Kit (ADK)

## When to invoke

Use when building Google ADK agents, typed tools, workflow orchestration, sessions/state, artifacts, memory or evaluations. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect installed google-adk generation and model provider, tool authority, runner/services, session identity, eval contract and compute/data limits. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define agent responsibilities and choose supported LLM/workflow APIs with bounded iterations, cost and side effects.
2. Implement validated tools and managed state/events/artifacts with explicit user/session isolation and resource lifetimes.
3. Evaluate meaningful task/tool outcomes and failures, state persistence, cancellation and authorization before authorized deployment.

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
