# Shopify theme architecture and editor UX: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- The correct directory is layout/, not layouts/. Only supported theme directories/subdirectories are recognized.

- Theme blocks under blocks/ and section-local blocks have different supported composition contracts; inspect the actual theme features.

- Use supported schema settings and translation keys; keep defaults meaningful and avoid redundant merchant options.

- Liquid filter/tag categories are not a license to invent cart mutation or payment-processing filters; use the exact documented API.

- Make IDs unique across repeated sections/blocks; CamelCase IDs, BEM, for...of, and private # methods are optional conventions.

- Scope JavaScript initialization/cleanup to theme-editor section lifecycle; avoid duplicate listeners after reloads.

- Use logical layout, keyboard operation, native semantics, and color settings appropriate to the theme’s supported design system.

- Measure asset and rendering costs; minification and fewer requests do not guarantee better user performance.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Shopify specifies supported theme directories and component composition.](https://shopify.dev/docs/storefronts/themes/architecture)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
