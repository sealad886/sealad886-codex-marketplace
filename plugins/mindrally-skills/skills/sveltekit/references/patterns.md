# SvelteKit route and server boundaries: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use installed-version component syntax: runes/$props for appropriate Svelte 5 components, while export let and $app/stores are older patterns to migrate deliberately.

- Use $app/state when supported by the installed SvelteKit/Svelte version; do not mix migration APIs without checking requirements.

- Load functions must check fetch status and validate params/data. Server-only load output becomes client-visible when returned.

- Use fail(status, data) for expected action validation failures; a plain success:false object does not itself set an error status.

- Use the framework error/redirect APIs and generated types; supported versions may throw internally without an explicit throw keyword.

- Rendering/prerender options can be exported from supported page/layout modules; choose the installed adapter’s supported behavior and dynamic entries.

- Use post-update measurement timing when reading updated DOM; $effect.pre runs before updates and is not a universal final-layout measurement hook.

- Avoid module-global per-user stores during SSR and forceful keyed remounts unless lifecycle reset is intended.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Rendering/prerender settings are page/layout options with adapter and route behavior.](https://svelte.dev/docs/kit/page-options)
- [Form actions support typed failures and progressive enhancement.](https://svelte.dev/docs/kit/form-actions)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
