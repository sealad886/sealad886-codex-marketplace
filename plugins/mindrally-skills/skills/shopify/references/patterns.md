# Shopify theme implementation: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Shopify theme Liquid does not provide a general {% cache %} tag; use supported tags/filters and platform caching rather than copying another Liquid host’s syntax.

- Use render for reusable snippets and pass explicit inputs; keep loops bounded and use pagination when the resource requires it.

- Use singular layout/ for layout files, sections/ and supported blocks/ for customizable content, and JSON templates as section configuration.

- Use locale-aware Ajax URLs, validate cart inputs, inspect non-2xx responses, and surface inventory/quantity errors.

- Use the image CDN and responsive dimensions; lazy-load suitable below-fold images, but do not delay the primary visible image by default.

- Current responsiveness metrics use INP rather than FID. Theme Check is a static check and does not establish accessibility or checkout correctness.

- Use locale files and money/image/metafield APIs appropriate to their documented value types. Defining store metafield definitions requires an authorized admin/API workflow.

- Cart/theme work and checkout customization have different extension and permission boundaries; do not claim a theme can replace arbitrary checkout behavior.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Official theme Liquid reference defines supported tags and filters.](https://shopify.dev/docs/api/liquid)
- [Theme architecture defines layout, templates, sections, blocks, and supporting directories.](https://shopify.dev/docs/storefronts/themes/architecture)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
