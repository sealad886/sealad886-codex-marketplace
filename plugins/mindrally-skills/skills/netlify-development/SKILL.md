---
name: netlify-development
description: "Use when configuring Netlify builds, Functions or Edge Functions, scheduled/background work, Blobs, Image CDN, or deploy contexts."
---

# Netlify Development Best Practices

## When to invoke

Use for configuring Netlify builds, Functions or Edge Functions, scheduled/background work, Blobs, Image CDN, or deploy contexts.

## Inputs and evidence

Inspect Netlify CLI/SDK versions, framework adapter, linked site identity, netlify.toml, deploy context, function runtime and account limits. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose standard, edge, background or scheduled execution for the actual request/lifetime contract.
2. Implement supported handler/config APIs, validation and resource authorization.
3. Configure storage/image/environment boundaries and isolate previews from production data.
4. Build and test locally; deploy only under explicit authority and verify actual platform behavior.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Local builds/functions pass relevant tests; deploy, schedule, Edge and data isolation claims require actual platform evidence.

## Must not

Do not create/link/deploy sites, change remote environment, or expose a live tunnel as a diagnostic side effect. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
