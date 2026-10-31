---
name: htmx
description: "Use when building server-rendered interactions with htmx requests, swaps, history, validation, or progressive enhancement."
---

# HTMX Development

## When to invoke

Use for htmx-backed HTML interactions and server response behavior.

## Inputs and evidence

Inspect installed htmx version/extensions, server fragments, request methods, CSRF policy, swap targets, and error response configuration. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define the server response contract and stable swap target for each interaction.
2. Use request, trigger, target, and swap attributes with accessible native controls.
3. Configure validation/error rendering explicitly and preserve server authorization and CSRF protection.
4. Test successful swaps, errors, focus, history restoration, and concurrent request behavior.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Browser/server checks confirm expected swaps and explicit error handling, secure mutations, keyboard behavior, and navigable history.

## Must not

Do not assume hx-swap alone makes HTTP error responses render or treat hx-confirm as authorization. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
