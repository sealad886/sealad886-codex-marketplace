---
name: openai-api-development
description: "Use when integrating OpenAI text, tools, structured output, embeddings, multimodal inputs, streaming, or API error handling."
---

# OpenAI API Development

## When to invoke

Use for integrating OpenAI text, tools, structured output, embeddings, multimodal inputs, streaming, or API error handling.

## Inputs and evidence

Inspect installed SDK/version, configured API endpoint, model access/capabilities, data policy, token/cost limits and current official documentation. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Select a supported endpoint and model from current task/evaluation needs.
2. Implement typed request/response, streaming and structured/tool contracts for that endpoint.
3. Validate tool arguments and authorization, handle refusals/incomplete output, and bound retries/costs.
4. Test provider-free parsing/error paths and only authorized low-cost live requests.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Tests establish request/output parsing, bounded tools/retries and error/completion handling; live API and quality evidence remain separate.

## Must not

Do not execute model-requested effects or send private content/incur charges without authority. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
