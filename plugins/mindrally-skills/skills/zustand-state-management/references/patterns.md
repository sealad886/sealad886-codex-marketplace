# Zustand shared state and hydration: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Zustand v5 selector outputs must remain stable; returning fresh arrays/objects can cause update loops, not merely extra renders. Use supported useShallow or equality APIs where appropriate.

- Use functional set when deriving from current state; merge is shallow, so update nested objects immutably unless using appropriate Immer middleware.

- A store may contain state and actions in one interface or slices; a fixed split-interface/file architecture is not required.

- Use persist only for intentional durable state with partialize/version/migrate and validation. Storage is untrusted and not authority for permissions.

- Create request-scoped vanilla stores when initializing SSR state; do not read/write a browser singleton from Server Components.

- Hydration and asynchronous storage may require explicit readiness handling to avoid server/client mismatches.

- Own and unsubscribe non-React subscriptions/timers/resources; handle stale async completion and cancellation at the correct workflow boundary.

- Use real store behavior for integration tests and reset state between cases; automatically mocking every store/server cache can hide defects.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Zustand v5 requires stable selector outputs and changes persistence/replace typing behavior.](https://github.com/pmndrs/zustand/blob/main/docs/reference/migrations/migrating-to-v5.md)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
