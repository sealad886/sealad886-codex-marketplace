---
name: pixi-js
description: "Use when building PixiJS scenes, assets, tickers, pointer interaction, texture caching, or mobile rendering performance."
---

# Pixi.js Game Development

## When to invoke

Use for building PixiJS scenes, assets, tickers, pointer interaction, texture caching, or mobile rendering performance.

## Inputs and evidence

Inspect PixiJS major version, renderer/backend capabilities, scene/texture ownership, asset pipeline, ticker semantics and target devices. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Initialize the supported Application/renderer and load assets with explicit ownership.
2. Implement scenes and input using current display/event APIs.
3. Optimize only measured draw, CPU, memory or battery bottlenecks.
4. Test resize, interaction, backgrounding, asset failure and teardown on targets.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Target rendering/input and cleanup tests pass; claimed frame/memory/battery improvements have device measurements.

## Must not

Do not destroy shared textures or claim fastest rendering from backend selection alone. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
