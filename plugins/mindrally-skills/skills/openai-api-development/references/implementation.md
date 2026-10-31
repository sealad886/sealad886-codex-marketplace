# OpenAI API Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## API and SDK evolution

- Responses is the documented recommendation for new projects; Chat Completions remains supported and uses different tool/input/output shapes.
- Do not build new work around retired/deprecated Assistants recipes; use current migration documentation for existing integrations.
- Model names, pricing, token limits, sampling parameters and multimodal capabilities change; do not recommend the source’s fixed GPT-3.5/o1/4o list.
- Current Python SDK error names and output helpers depend on the installed version; InvalidRequestError is an older SDK API.

## Tools, privacy and reliability

- Tool calls are untrusted requests: allowlist functions, validate schemas and arguments, enforce authorization and bound recursive rounds.
- Streaming text alone does not prove successful completion; inspect terminal status, errors and incomplete/refusal outcomes.
- Embeddings need per-input token and aggregate batch limits, model/dimension identity and privacy-aware caches; larger is not universally most accurate.
- Account for SDK retries before adding application retries; retry appropriate transient failures with jitter/deadlines, not every APIError.
- Keep keys server-side in approved local/secret storage and never print them; SDK installation or a model list does not prove inference quality.

## Primary documentation

- [Primary documentation](https://developers.openai.com/api/docs/guides/migrate-to-responses) — Responses is recommended for new projects while Chat Completions remains supported with different interfaces.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
