# Blazor Development Guidelines: implementation guidance

## Lifecycle and rendering

Load data that depends on route/component parameters in OnParametersSetAsync,
not only OnInitializedAsync. Initialization may run again across prerendering and
interactive startup; prevent duplicate effects or persist the appropriate state.
DOM interop belongs after interactive rendering, not prerendering. Dispose timers
and subscriptions, and marshal external notifications with InvokeAsync. Use @key
for identity when needed, virtualization for supported large collections, and
ShouldRender only after profiling. @if controls rendering; it is not code splitting.

## State, errors, and security

Choose scoped state according to server circuit, browser, or static rendering
lifetimes; never make per-user server state a shared singleton. ErrorBoundary and
ErrorBoundaryBase are documented extension points; do not invent IErrorBoundary.
Do not show raw exception messages to users. AuthorizeView hides UI but does not
secure the event handler or API; enforce authorization server-side. WebAssembly
does not automatically work offline: service-worker caching and data synchronization
need deliberate implementation. Server versus WebAssembly is a deployment tradeoff,
not a fixed internal-versus-public audience rule.

## Primary documentation

- [Parameter and prerender lifecycle](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/lifecycle).
- [ErrorBoundary handling and recovery](https://learn.microsoft.com/en-us/aspnet/core/blazor/fundamentals/handle-errors).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
