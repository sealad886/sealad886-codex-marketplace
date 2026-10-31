# Localization (l10n): implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Content and regional behavior

- Use locale tags and explicit fallback chains; do not infer currency, country, units or time zone solely from language.
- Preserve interpolation/plural syntax and translator context; machine translation output requires separate linguistic review.
- expo-localization supplies locale information; use a maintained translation layer instead of deprecated react-native-i18n.
- Legal text adaptation needs the designated legal/domain reviewer; translated wording alone does not establish compliance.

## Rendering and QA

- Test real translations, pseudolocales, text scaling, RTL and mixed-direction content; fixed expansion percentages and language-length stereotypes are unreliable.
- Check font glyph coverage, shaping, line breaking, address/name formats and user preference overrides.
- Use locale-aware formatters with explicit currency/time zone where required; avoid pinning punctuation/currency strings across runtime locale-data versions.
- Validate resource structure/placeholders and switch/fallback/cache behavior; distinguish automated completeness from translation quality.

## Primary documentation

- [Primary documentation](https://www.w3.org/International/quicktips/) — Localization needs language metadata, culturally suitable examples, local forms and complete translatable messages.
- [Expo localization](https://docs.expo.dev/guides/localization/) — Expo localization detection integrates with a separate translation/message library.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
