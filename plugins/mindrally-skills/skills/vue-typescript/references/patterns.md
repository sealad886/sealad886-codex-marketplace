# Vue and TypeScript integration: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use vue-tsc for SFC-aware command-line type checking; Vite transformation alone does not prove template/type correctness.

- Composition API/script setup is useful but Options API with defineComponent remains supported and typed.

- Use defineProps/defineEmits and reactive APIs supported by the installed compiler; imported/complex type support varies by Vue version.

- Choose interfaces or aliases by semantics; enum bans and functional-component-only rules are not TypeScript safety requirements.

- Do not introduce Headless UI, Element Plus, Tailwind, VueUse, or Pinia without an actual task need.

- Vue Suspense remains experimental in current documentation and only manages supported async dependencies; it is not a required wrapper for every async operation.

- Use computed state for derivations and watchers for deliberate effects, with cleanup for external resources.

- Measure current Web Vitals including INP; optimize actual rendering/network bottlenecks rather than assuming a helper library improves reactivity.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Vue supports SFC-aware vue-tsc and typed Options API as well as Composition API.](https://vuejs.org/guide/typescript/overview.html)
- [Vue Suspense remains experimental and targets async dependencies.](https://vuejs.org/guide/built-ins/suspense.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
