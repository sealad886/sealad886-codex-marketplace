---
name: lottie
description: "Use when integrating Lottie or dotLottie web animation, playback events, loading, accessibility, or lifecycle cleanup."
---

# Lottie Animation Guidelines

## When to invoke

Use for integrating Lottie or dotLottie web animation, playback events, loading, accessibility, or lifecycle cleanup.

## Inputs and evidence

Inspect player/package versions, asset licenses, actual renderer, animation features, SSR boundaries, and target-device budgets. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Select the existing player and a supported JSON/dotLottie asset format.
2. Implement playback and load/error state through its documented props and player events.
3. Provide reduced-motion/static alternatives and lifecycle-owned listeners/observers.
4. Measure file/decode/render cost and test load failures, unmount and device performance.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Actual player builds and loads the asset; fallback, motion preference, cleanup, and device performance have direct checks.

## Must not

Do not assume SVG player APIs or asset feature support transfer between implementations. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
