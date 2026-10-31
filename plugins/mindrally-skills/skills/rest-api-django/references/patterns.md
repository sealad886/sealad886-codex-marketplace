# Django REST API boundaries: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Choose APIView, generic views, or viewsets by endpoint needs; class-based views and model-only business logic are not compulsory for all APIs.

- Use serializer validation and explicit writable fields; protect ownership and nested relationship access server-side.

- Filter querysets by access scope and apply object permissions where needed; authentication alone does not authorize records.

- Choose authentication from the application’s clients and threat model. JWT and SimpleJWT are optional integrations rather than DRF defaults.

- SessionAuthentication requires CSRF validation for authenticated unsafe requests; CORS configuration does not replace it.

- Use select_related for suitable single-valued relationships and prefetch_related for suitable multi-valued relationships; verify query counts before adding eager loading.

- Use transaction.atomic around coherent writes; do not assume database rollback undoes external side effects.

- Retain the established error schema and status semantics; pagination, indexing, caching, and connection pooling require database and deployment evidence.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [DRF supports multiple authentication schemes and session authentication requires CSRF handling.](https://www.django-rest-framework.org/api-guide/authentication/)
- [Endpoint and object permissions require explicit enforcement.](https://www.django-rest-framework.org/api-guide/permissions/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
