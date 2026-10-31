# Flutter: implementation guidance

## Architecture and state

Flutter guidance supports UI/data separation and a conditional domain layer;
BLoC, Cubit, Riverpod, GetIt, Freezed and Dartz are optional choices rather than
simultaneous requirements. Match Riverpod/code-generation APIs to installed versions
and retain clear async loading/error/data states. Context is not interchangeable
with web React Context. Use const constructors when arguments qualify, but const
does not prevent every surrounding rebuild. Extract widgets for meaningful boundaries,
not an arbitrary function instruction count or a ban on nested widget trees.

## Lifecycle and platform behavior

Dispose controllers, subscriptions, animation resources and other owned objects.
Guard post-await UI updates against disposed state where required. Choose accessible
error feedback suited to the action; SelectableText.rich is not a universal replacement
for SnackBars. Firebase is optional and still needs rules/authorization, indexes and
offline/conflict behavior. Profile actual build/layout/paint/raster and list/image
costs on representative devices. Check navigation restoration, permissions, text
scale, RTL, safe areas and keyboard behavior for applicable targets. Widget tests
and host checks do not establish physical-device performance or app-store readiness.

## Primary documentation

- [Architecture and conditional domain layer](https://docs.flutter.dev/app-architecture/recommendations).
- [Measured widget/rendering performance](https://docs.flutter.dev/perf/best-practices).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
