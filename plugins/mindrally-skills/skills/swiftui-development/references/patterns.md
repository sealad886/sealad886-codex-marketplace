# SwiftUI state, tasks, and rendering: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- With Observation, a view can own an @Observable reference using @State and form bindings with @Bindable where needed; @State is not restricted to small value types.

- For ObservableObject, StateObject owns initialization/lifetime and ObservedObject observes externally owned models; retain availability-correct patterns.

- Key .task(id:) to a stable request identity such as selected record/filter, not the fetched collection’s count, which can trigger repeated fetch/cancel loops.

- Task cancellation is cooperative. Check cancellation and request identity before publishing a stale response; disappearing views do not instantly terminate arbitrary underlying work.

- Do not default heavy work to Task.detached or all escaping closures to weak self; choose actor/sendability and ownership deliberately.

- View models may be MainActor-isolated while services use appropriate off-actor work; nonisolated annotations require actual isolation analysis.

- Stable IDs must reflect domain identity; self identity is valid for suitable immutable unique values. body line counts are a readability heuristic, not a correctness rule.

- Use semantic colors, adaptive layout, Dynamic Type, VoiceOver, Reduce Motion, and supported previews; withAnimation and animation(value:) have different valid scopes.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Observation requires the @Observable macro rather than protocol conformance alone.](https://docs.swift.org/latest/documentation/observation/observable/)
- [Cancellation and task lifetime are cooperative and explicit.](https://docs.swift.org/latest/documentation/the-swift-programming-language/concurrency/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
