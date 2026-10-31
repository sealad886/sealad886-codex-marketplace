# Cheerio HTML Parsing: implementation guidance

## Parser and selection semantics

Cheerio parses markup without running browser JavaScript or layout. Current HTML
loading uses parse5; XML uses the documented xml option/htmlparser2. xmlMode:false
does not mean parse-as-XML, and old parser options must not be assumed to affect
parse5. Use fragment mode when wrappers should not be inserted. Scope selectors
to the intended container. attr may be undefined; data may coerce values, so
choose raw attributes when exact strings are needed. hasClass checks a class,
not arbitrary attribute existence.

## Extraction and I/O

Pass the document-bound $ function explicitly to extraction helpers; do not rely
on an unbound this/global. Validate table alignment and rowspan/colspan rather
than silently overwriting or truncating cells. Parse numbers with locale/schema
rules, preserve zero and missing separately, and reject NaN. Missing href must
not become a fetched string undefined. Resolve then allowlist URL schemes/hosts
and redirects, with bounded size/timeouts/concurrency and appropriate rate limits.
Do not return [] for all network/parsing failures: distinguish empty data from
failed extraction. Modern Node fetch may avoid an unnecessary extra HTTP package.

## Primary documentation

- [parse5/htmlparser2 and XML/fragment options](https://cheerio.js.org/docs/advanced/configuring-cheerio/).
- [Loading methods and document scope](https://cheerio.js.org/docs/basics/loading).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
