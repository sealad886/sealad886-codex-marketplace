# BeautifulSoup HTML Parsing: implementation guidance

## Parsing and navigation

BeautifulSoup parses markup; it does not execute JavaScript. Choose html.parser,
lxml, html5lib, or XML behavior from required parsing semantics, not a universal
fastest/most-lenient claim. Different parsers can produce different trees.
find/select_one may return None. get_text with a separator can preserve boundaries
between adjacent text nodes. str(tag) includes the outer tag; decode_contents()
returns inner markup. next_element follows parse order and may be text or a
descendant: it does not skip whitespace to the next sibling element. Use documented
sibling searches when that is the actual requirement.

## Extraction and fetching

Validate table headers/cell counts and handle rowspan/colspan before constructing
records; zip can silently truncate. Preserve numeric/currency locale and missing
versus zero rather than coercing arbitrary price text to float. Resolve URLs with
urljoin, then enforce permitted schemes/hosts and redirect policy before fetching.
Set connection/read timeouts, status/content-size checks, bounded retries and
rate limits for authorized requests. Parser filtering is parser-dependent and
select returns a list; wrapping a list loop in yield does not make parsing
streaming. Close sessions and preserve extraction failures separately from emptiness.

## Primary documentation

- [Parser differences, traversal and decode_contents](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
