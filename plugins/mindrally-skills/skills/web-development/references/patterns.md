# Server-rendered web features: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use Bootstrap grid/utilities only in Bootstrap projects and match the installed version’s Sass/module integration.

- Django views must scope records to authorized users and validate forms; get_object_or_404 on an unrestricted queryset does not enforce ownership.

- Django template autoescaping helps HTML output but does not make every script/URL/HTML injection context safe.

- HTMX request handlers usually return appropriate HTML fragments; hx-target/hx-swap do not automatically turn a JSON API response into UI.

- Include framework CSRF tokens/headers for unsafe HTMX requests and keep server checks enabled.

- Search requests need a named field or explicit included values; an input without name does not reliably submit the intended query.

- Handle non-2xx responses, validation errors, loading state, focus, and history according to HTMX configuration; test the no-JavaScript fallback if promised.

- Use the existing stack rather than introducing Bootstrap, Django, and HTMX together merely because this skill lists them.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [HTMX requests require deliberate response swapping and backend CSRF integration.](https://htmx.org/docs/)
- [Django security primitives require correct application use.](https://docs.djangoproject.com/en/stable/topics/security/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
