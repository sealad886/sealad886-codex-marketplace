---
name: anthropic-claude-development
description: "Use when integrating Anthropic Messages, streaming, tool use, vision, caching, or batch processing."
---

# Anthropic Claude API Development

## When to invoke

Use when integrating Anthropic Messages, streaming, tool use, vision, caching, or batch processing. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect installed anthropic SDK, configured model access, request schema, tool authority, budgets, and data-handling rules. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Confirm supported models and SDK request types from current provider documentation; define task and output limits.
2. Implement the chosen Messages/streaming/tool flow with schema validation, complete content-block handling, and bounded tool execution.
3. Test stop reasons, multiple tool calls, malformed output, rate limits, cancellation, and redacted errors with mocked responses before authorized live calls.

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
