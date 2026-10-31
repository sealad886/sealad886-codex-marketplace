# Search discoverability: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Current Core Web Vitals are LCP, INP, and CLS; FID is no longer the current responsiveness metric.

- SSR can help content availability but is not mandatory for every indexable site; inspect what crawlers receive and rendered JavaScript behavior.

- Use framework metadata APIs only for the installed framework/version; React Server Components and Suspense are not universal SEO requirements.

- Use accurate titles and descriptions; fixed character counts are editorial heuristics, not guaranteed search-result boundaries.

- Canonical URLs consolidate signals but are not a guarantee of indexing; redirects and robots/noindex directives have different purposes.

- Use structured data matching visible content and supported types; rich results are not guaranteed.

- Decorative images need appropriate empty alt text rather than compulsory descriptive alt text; preserve accessible meaning.

- Measure field and lab performance separately. Use current Search Console/Rich Results diagnostics instead of retired testing products.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Google identifies LCP, INP, and CLS as current Core Web Vitals.](https://developers.google.com/search/docs/appearance/core-web-vitals)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
