# RTL and bidirectional interfaces: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Set document language and base direction explicitly from supported locale/script data; checking only ar/he misses Persian, Urdu, and other RTL scripts.

- Use logical inline/block properties where layout should follow reading direction. Keep physical coordinates where location must remain physical.

- Use bdi or explicit isolation for unknown-direction interpolations and dir=auto for suitable user-content regions.

- Do not reverse strings or force DOM order to imitate visual mirroring; preserve meaningful reading and keyboard order.

- Mirror navigation arrows when their meaning follows reading direction; do not automatically mirror clocks, media playback, mathematical plots, or every chart axis.

- Choose chart/time axis direction from domain and locale conventions, then label it clearly.

- React Native direction uses I18nManager and platform style behavior; verify restart and layout behavior for the installed version.

- Use locale-aware message and Intl formatting; test punctuation, digit shaping, truncation, and mixed identifiers with real content.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [HTML dir establishes base direction; logical properties follow direction but physical positioning may remain intentional.](https://www.w3.org/International/questions/qa-html-dir)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
