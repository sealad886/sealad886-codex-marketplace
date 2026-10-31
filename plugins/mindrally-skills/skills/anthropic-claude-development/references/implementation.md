# Anthropic Claude API Development: implementation guidance

## Messages and tools

Use server-side credentials through the deployment's secret mechanism. The
Messages API separates the system parameter from user/assistant messages and
returns typed content blocks; do not assume `content[0]` is text. In a tool loop,
append the assistant content and return a result for every requested tool-use ID.
Validate tool names and arguments and enforce authorization outside the model.
Bound iterations, tokens, concurrency, and execution time. Treat tool results
and image/text inputs as untrusted content, not operating instructions.

## Streaming, caching, batches, and failures

Use the SDK's streaming interface and distinguish text deltas from other event
blocks and final usage/stop state. Vision requires a supported model and source
format. Prompt caching has model-specific minimums, lifetimes, and exact-prefix
requirements; it does not cache arbitrary similar queries. Batches are asynchronous:
track individual custom IDs, result/error states, retention, and cancellation.
Select models from current account availability instead of hardcoded 2025 tiers.
Use SDK retry behavior deliberately; do not retry every APIError or duplicate
costly calls blindly. Request concise conclusions or verifiable reasoning summaries
rather than private chain-of-thought. Redact keys, prompts, images, and user data
from routine logs.

## Primary documentation

- [Messages content blocks and stop reasons](https://docs.anthropic.com/en/api/messages).
- [Complete tool-use result flow](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use).
- [Prompt cache prefix requirements](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
