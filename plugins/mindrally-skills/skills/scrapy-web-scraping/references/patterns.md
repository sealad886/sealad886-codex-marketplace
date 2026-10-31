# Scrapy extraction workflows: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Modern Scrapy supports async start(); start_requests() belongs to older-version patterns. Choose the installed version’s entrypoint rather than copying old guidance.

- Scrapy accepts dictionaries and item-like objects; Item and ItemLoader are useful options rather than mandatory for all extraction.

- Use CSS/XPath scoped to meaningful content and handle missing fields, duplicate URLs, pagination cycles, and normalized output deliberately.

- Set robots behavior, concurrency, delay, and AutoThrottle from site policy and observed service limits; no universal 1–3 second threshold proves compliance.

- Use an honest crawler identity where appropriate. Proxy/user-agent rotation is not permission to bypass access restrictions.

- JavaScript rendering and distributed scheduling add dependencies and complexity; add them only when the source and scale require it.

- Check reactor/async pipeline compatibility and close resources; async declarations do not make blocking database clients nonblocking.

- HTTP caches and persisted jobs may retain personal or authenticated data; scope storage and expiry and never treat cached development responses as fresh live facts.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Current spider startup supports async start with version-specific older entrypoints.](https://docs.scrapy.org/en/latest/topics/spiders.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
