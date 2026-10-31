# Astro: implementation guidance

## Pages, content, and islands

File routes live in src/pages. Prerendered dynamic routes need getStaticPaths;
on-demand routes follow the installed adapter/runtime contract. Use Astro.props
for supplied props, not as a general data-fetching API. Use content collections
and getCollection for structured content; use Vite import.meta.glob for source
files. Do not introduce deprecated Astro.glob. Select client:load, client:idle,
client:visible, or another supported hydration directive by interaction timing.
Framework islands without client directives render HTML without client hydration.

## Styling and validation

Use scoped component styles or the project's existing CSS framework. Tailwind 4
uses its Vite plugin; @astrojs/tailwind belongs to the older Tailwind integration
and must not be recommended unconditionally. Compose ordinary HTML head elements
through layouts for canonical URLs and metadata; there is no special Astro head
component. Check optimized image dimensions/loading, content validation, and 404
behavior separately. Measure LCP, INP, and CLS; FID is no longer the current Core
Web Vitals responsiveness metric. Server islands and private content require
cache/authentication review before deployment.

## Primary documentation

- [Tailwind 4 Vite integration](https://docs.astro.build/en/guides/styling/).
- [Content loading and collections](https://docs.astro.build/en/guides/content-collections/).
- [Client-side scripts and island boundaries](https://docs.astro.build/en/guides/client-side-scripts/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
