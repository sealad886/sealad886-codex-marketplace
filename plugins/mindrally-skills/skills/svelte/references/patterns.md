# Svelte component reactivity: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Runes are compiler syntax and are not imported from svelte; import ordinary utilities such as tick or untrack only when needed.

- Use $state for reactive source values and $derived for computed values; $effect is not a direct universal replacement for all legacy reactive logic and does not run during SSR.

- Svelte 5 supports legacy components; migrate a component deliberately rather than claiming all legacy event modifiers or slots ceased to exist.

- Use callback props/snippets for current patterns where appropriate and retain documented legacy compatibility when maintaining an older component.

- State in .svelte.js/.svelte.ts may be shared, but directly reassigned exported reactive bindings are restricted; expose an object or accessors with deliberate ownership.

- Do not put per-user SSR state in module globals; use request/component context and loader data boundaries.

- Use scoped CSS or the existing styling system; Tailwind/@apply and a particular i18n package are optional.

- Test effect cleanup, derived updates, event propagation, and keyboard/focus behavior rather than relying on compilation alone.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Shared reactive state cannot be directly exported when reassigned.](https://svelte.dev/docs/svelte/$state)
- [Effects have browser/runtime and cleanup semantics distinct from derived state.](https://svelte.dev/docs/svelte/$effect)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
