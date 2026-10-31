# React Router v7 framework mode: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Framework mode normally declares routes in `app/routes.ts`; filesystem discovery requires its configured integration. A file under routes/ is not automatically a route in every setup.

- Use generated Route types when the build supplies them. Loaders read; actions own mutations. Server authorization belongs in the server handlers, not only in components.

- HTML navigation forms can progressively enhance without JavaScript; `useFetcher` and `useSubmit` are client APIs and do not independently work without JavaScript.

- Do not assume `fetcher.Form` submissions retain identical no-JavaScript behavior to navigation forms; test the actual fallback.

- Use `isRouteErrorResponse` for router-normalized HTTP errors rather than assuming an error is an instance of Response.

- Keep credentials and privileged data access in server-only modules. Validate redirect targets to avoid open redirects.

- Use supported promise/Await streaming for the installed v7 version; do not import removed legacy defer helpers.

- Test nested error recovery, validation failures, pending state, reload/deep links, and automatic loader revalidation after actions.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Framework routing declares route configuration; use the version selector for v7.](https://reactrouter.com/start/framework/routing)
- [Router error responses should be recognized with isRouteErrorResponse.](https://reactrouter.com/how-to/error-boundary)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
