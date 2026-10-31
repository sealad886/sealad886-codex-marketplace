---
name: anime-js
description: "Use when building or diagnosing Anime.js timelines, SVG motion, interactive animations, or framework integration."
---

# Anime.js Animation Guidelines

## When to invoke

Use when building or diagnosing Anime.js timelines, SVG motion, interactive animations, or framework integration. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect installed Anime.js major version, animation targets, lifecycle owner, accessibility needs, and performance evidence. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Choose the installed major version API and identify the motion state and timeline ownership.
2. Implement only required animation primitives and clean up effects, listeners, and inline changes with the component lifecycle.
3. Check reduced motion, interruption/restart, unmount, SVG behavior, and performance on the target device.

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
