# Performance Optimization: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Metrics and rendering

- Current Core Web Vitals are LCP, INP and CLS; FID has been replaced and Time to Interactive is not a current Core Web Vital.
- SSR, static generation, streaming and client rendering each have workload tradeoffs; server rendering is not universally fastest.
- Avoid layout thrashing by separating reads/writes; transform/opacity often help but do not guarantee GPU/compositor behavior.

## Assets, caches and runtime

- Prioritize critical resources and avoid lazy loading the main LCP image; use responsive sizes and measured format/quality tradeoffs.
- Choose font loading/subsetting with script coverage and layout-shift considerations; font-display swap is not universally optimal.
- Cache only with correct user/tenant/locale keys, expiry and invalidation; service workers add update/offline complexity.
- Bound workers, debouncing and code splitting to the actual workload; CSS naming/specificity preferences are not substitutes for profiling.

## Primary documentation

- [Primary documentation](https://web.dev/articles/vitals) — Core Web Vitals currently covers LCP, INP and CLS and distinguishes field and laboratory measurement.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
