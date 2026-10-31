---
name: gsap
description: "Use when building GSAP timelines, ScrollTrigger behavior, SVG animation, or lifecycle-safe React animation."
---

# GSAP Animation Guidelines

## When to invoke

Use when the project already uses GSAP or explicitly selects it for animation.

## Inputs and evidence

Inspect GSAP/plugin versions, target elements, framework lifecycle, reduced-motion requirements, and measured rendering bottlenecks. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose tweens or a timeline with explicit start/end states and interruption behavior.
2. Scope selectors and register only required plugins; connect animation ownership to component lifecycle.
3. Implement responsive and reduced-motion variants, with cleanup for delayed handlers.
4. Measure on target devices and verify resizing, replay, unmount, and interrupted transitions.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Animations have correct end states and cleanup, respect reduced motion, and pass target-device performance and keyboard/focus checks.

## Must not

Do not assume force3D guarantees GPU acceleration or enable global ticker changes without measured need. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
