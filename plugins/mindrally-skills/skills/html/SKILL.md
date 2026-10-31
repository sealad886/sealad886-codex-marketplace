---
name: html
description: "Use when writing semantic HTML documents, forms, media, interactive elements, or accessible document structure."
---

# HTML Development Guidelines

## When to invoke

Use for HTML semantics and browser markup contracts.

## Inputs and evidence

Inspect existing document structure, browser support, form submission behavior, accessible names, and framework output. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose native elements for content, navigation, and actions, with a clear heading hierarchy.
2. Implement labeled forms, valid attributes, and server-backed validation/error handling.
3. Provide useful image alternatives, media alternatives, responsive resources, and document language.
4. Validate generated HTML and exercise keyboard, focus, forms, and representative assistive technology.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Markup validation and behavioral accessibility checks demonstrate usable controls, names, document structure, and responsive media.

## Must not

Do not replace native semantics with unnecessary ARIA or confuse visual emphasis with element meaning. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
