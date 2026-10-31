---
name: optimized-nextjs-typescript
description: "Use when profiling and optimizing Next.js TypeScript rendering, bundles, data loading, images, or interactive responsiveness."
---

# Optimized Next.js TypeScript Best Practices

## When to invoke

Use for profiling and optimizing Next.js TypeScript rendering, bundles, data loading, images, or interactive responsiveness.

## Inputs and evidence

Inspect framework/router versions, production baseline, route traces, bundle reports, cache semantics and measurable performance targets. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Reproduce a user-visible bottleneck in a production-representative build.
2. Change the owning data/rendering/asset boundary with an explicit hypothesis.
3. Preserve correctness, authorization, hydration and accessibility while optimizing.
4. Compare before/after metrics under equivalent conditions and report tradeoffs.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Equivalent before/after production measurements show the intended improvement and critical behavior checks still pass.

## Must not

Do not claim faster performance solely from fewer effects, classes, dependencies or client components. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
