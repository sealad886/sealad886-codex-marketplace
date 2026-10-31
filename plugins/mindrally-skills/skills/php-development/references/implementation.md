# PHP Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Types and organization

- Enums require PHP8.1, match/named arguments PHP8.0, and other features have their own minimum versions; do not imply all started in8.1.
- strict_types affects scalar coercion at relevant call boundaries; it does not validate arbitrary external payloads or enforce every type globally.
- Use Composer PSR-4 and existing style conventions; Repository layers and full PHPDoc duplication are optional where they add useful information.

## Trust and failures

- Validate input according to expected domain; blanket sanitization can corrupt valid data and is not a universal injection defense.
- Parameterize SQL values and allowlist dynamic identifiers; escape output for HTML/attribute/URL/JS context as appropriate.
- Catch exceptions where recovery/translation is meaningful, redact logs and avoid exposing stack traces/secrets to clients.
- Test CSRF, authorization and persistence invariants at the owning interface rather than inferring safety from types.

## Primary documentation

- [Primary documentation](https://www.php.net/manual/en/language.types.declarations.php) — PHP type declarations and strict scalar coercion have specific per-feature and call-site semantics.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
