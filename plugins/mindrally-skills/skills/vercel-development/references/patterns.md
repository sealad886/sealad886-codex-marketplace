# Vercel application runtime and delivery: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Vercel supports several frameworks/runtimes; Next.js App Router, Tailwind, and React Server Components are optional application choices.

- Select Node/Edge/Python from dependency support and platform limits; streaming is bounded by function lifetime and does not permit indefinite execution.

- API handlers and cron routes need authentication/authorization and validated inputs; wildcard CORS is not a security boundary.

- AI SDK APIs evolve: old ai/react useChat, message.content, and toDataStreamResponse examples must match the installed major and transport protocol.

- Model IDs, rates, limits, and provider availability are live configuration, not permanent hardcoded defaults.

- Use server-owned budgets and cancellation for model calls; handle typed/provider errors rather than substring-matching arbitrary error messages.

- Preview deployments depend on repository/project settings and successful builds; do not promise every PR automatically has one.

- Keep secret env values out of NEXT_PUBLIC variables and generated client artifacts; production deployment, cron changes, and external costs require authority.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Function runtimes have platform-specific capabilities and maximum lifetimes.](https://vercel.com/docs/functions/runtimes)
- [AI SDK client/server APIs and protocols change across major releases.](https://ai-sdk.dev/docs/migration-guides)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
