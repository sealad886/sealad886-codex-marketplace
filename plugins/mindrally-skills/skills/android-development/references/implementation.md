# Android Development Best Practices: implementation guidance

## Architecture and UI

Use repositories for data ownership and ViewModels for screen state where suitable.
A domain layer is optional and justified by complexity or reuse; do not mandate
MVI or extra layers. Prefer unidirectional data flow and immutable exposed state.
For new UI, current Android guidance recommends Jetpack Compose; retain Views
when the project requires them and use ViewBinding only for that stack.
Choose navigation APIs compatible with the app. Safe Args is not a requirement
for Compose navigation. Use Kotlin's `Any`, not a TypeScript `any` type, and
follow Kotlin naming and type inference rather than arbitrary instruction limits.

## Lifecycle and validation

Collect flows with lifecycle-aware APIs; distinguish ViewModel state from state
that must survive process death. Preserve coroutine cancellation and avoid
blocking the main thread. Use WorkManager for eligible persistent deferrable work,
not every asynchronous task. Scope injected dependencies to actual lifetimes.
Use unit tests for state/data logic, Compose tests for Compose, and Espresso for
Views where appropriate. Include deep links, configuration changes, accessibility,
and Android permission/background restrictions in relevant runtime checks.

## Primary documentation

- [Current Android architecture and Compose recommendations](https://developer.android.com/topic/architecture/recommendations).
- [Lifecycle-aware cancellable coroutine work](https://developer.android.com/kotlin/coroutines/coroutines-best-practices).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
