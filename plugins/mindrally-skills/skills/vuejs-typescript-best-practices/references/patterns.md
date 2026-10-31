# Vue TypeScript implementation review: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Prefer cohesive composables and components over arbitrary file-size or function-syntax rules; Vue supports more than functional components.

- Type props, emits, refs, and returned composable values; validate external data at runtime rather than assuming a type cast validates it.

- Preserve reactive references when destructuring and avoid module-global per-user state during SSR.

- Use computed derivation and bounded watchers with cleanup; VueUse is optional and not automatically faster.

- Use Suspense only for supported async component/setup dependencies and account for its experimental status.

- Choose dynamic imports/chunking from route and dependency evidence; more chunks are not inherently better.

- Retain project styling/design tokens and semantic controls rather than mandating three UI libraries simultaneously.

- Track LCP, INP, and CLS plus real interaction evidence; test localized/long content, focus, and error states.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Vue TypeScript tooling and supported component styles require version-aware checking.](https://vuejs.org/guide/typescript/overview.html)
- [Suspense supports specific async dependencies and remains experimental.](https://vuejs.org/guide/built-ins/suspense.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
