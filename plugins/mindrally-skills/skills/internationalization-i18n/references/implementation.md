# Internationalization (i18n): implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Messages and runtime

- Select the established i18next, framework, or native message system; ICU syntax is not interchangeable with every library’s plural syntax.
- Use complete messages with translator context and interpolation escaping; plural categories depend on locale, not English singular/plural alone.
- expo-localization detects locale information but does not itself translate messages; choose a maintained message library supported by the app.
- Keep SSR locale state per request and include locale in content cache keys when it changes results.

## Formatting and layout

- Intl formatters require deliberate locale, currency, and time zone; currency choice is a business value, not inferred from language alone.
- Store instants with an unambiguous zone/offset; preserve date-only civil dates as such.
- Set document and changed-fragment language, use logical layout properties, and isolate mixed-direction text when needed.
- Test expansion and text scaling instead of assuming a fixed percentage fits every translation; mirror directional affordances selectively.

## Primary documentation

- [W3C language metadata](https://www.w3.org/International/questions/qa-lang-why) — Document/fragment language metadata enables language-sensitive browser and assistive behavior.
- [Expo localization](https://docs.expo.dev/guides/localization/) — Device locale detection and translated message libraries are distinct capabilities.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
