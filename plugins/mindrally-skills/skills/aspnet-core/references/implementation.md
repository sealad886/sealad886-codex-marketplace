# ASP.NET Core Development Guidelines: implementation guidance

## HTTP and middleware

Choose controllers or minimal APIs from the project. Keep transport DTO validation
and domain rules explicit. Propagate CancellationToken to I/O. Place exception
handling early, CORS/authentication/authorization in the documented order, and
custom middleware according to what it depends on; there is no universal slot
for every custom component. Public static-file handling needs explicit review.
Return safe ProblemDetails-style errors without private exception details.

## Authentication, options, and caches

Validate JWT signature, issuer, audience, lifetime, and expected algorithms through
supported authentication middleware; application token issuance is a separate
identity-system decision. Protect endpoints server-side with appropriate policies.
Use validated options and deployment secret storage rather than committing keys
into appsettings. `ResponseCache` sets HTTP caching headers; it does not itself
install a server cache. Response caching requires configured services/middleware
and cacheable requests. Consider output caching for server-controlled policies;
do not cache personalized responses across users. Memory cache is per process,
distributed cache serialization and invalidation are explicit, and concurrent
cache misses may need coordinated population. Use the configured OpenAPI tooling
for the target .NET version rather than requiring Swashbuckle in every project.

## Primary documentation

- [Response-caching services and middleware](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/middleware).
- [Middleware dependency order](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
