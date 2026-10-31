---
name: nextjs-react-typescript
description: "Use when developing typed Next.js App Router components, rendering boundaries, URL state, or responsive accessible UI."
---

# Next.js React TypeScript

## When to invoke

Use for developing typed Next.js App Router components, rendering boundaries, URL state, or responsive accessible UI.

## Inputs and evidence

Inspect Next.js/React versions, App versus Pages Router, component imports, route params, data/caching contracts and existing UI libraries. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose server rendering for server capabilities and client boundaries for interactivity/browser state.
2. Implement typed route/data contracts and runtime validation at external boundaries.
3. Use loading/error/Suspense and URL state only where the interaction requires them.
4. Build and test hydration, navigation, access control and measured Core Web Vitals.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Actual framework build and interaction/hydration tests pass; any Web Vitals claims include measurements.

## Must not

Do not force server-only patterns onto interactive components or claim performance from code style. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
