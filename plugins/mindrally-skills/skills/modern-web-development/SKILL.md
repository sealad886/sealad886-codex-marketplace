---
name: modern-web-development
description: "Use when building modern TypeScript web features involving React/Next.js, data clients, responsive UI, or accessible interactions."
---

# Modern Web Development

## When to invoke

Use for building modern TypeScript web features involving React/Next.js, data clients, responsive UI, or accessible interactions.

## Inputs and evidence

Inspect actual framework/router versions, rendering boundaries, existing UI/data/auth stack, deployment constraints and critical user flows. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Extend the current stack instead of adding every technology listed by the source.
2. Choose server/client boundaries from data, interactivity and secret requirements.
3. Implement validated/authorized data access and accessible responsive UI states.
4. Build and test loading/error/success paths, keyboard use and measured performance.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Framework build and user-flow tests validate authorization, hydration, UI states and accessibility; performance claims are measured.

## Must not

Do not copy another project’s branded conventions or add a competing data/styling stack. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
