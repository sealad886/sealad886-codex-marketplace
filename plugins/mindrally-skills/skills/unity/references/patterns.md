# Unity game and application behavior: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use MonoBehaviour for GameObject components and plain C# or ScriptableObjects for appropriate data/services; ScriptableObject assets are not per-session mutable state by default.

- TryGetComponent reports availability but callers must handle false; it does not automatically eliminate every null/lifetime issue.

- Cache stable references where needed instead of repeated searches in hot paths; avoid premature broad caching of short-lived objects.

- Select uGUI/TextMeshPro or UI Toolkit according to installed features and project needs; TextMeshPro is not mandatory for every Unity UI system.

- Use the configured Input System or legacy input intentionally and respect update/fixed-update semantics for physics.

- Object pooling, batching, LOD, and allocation reduction should follow profiler evidence and preserve activation/reset behavior.

- Dispose native collections and subscriptions and handle scene unload/domain reload ownership; do not use try/catch to hide repeated lifecycle bugs.

- Naming prefixes and state-machine architecture are project choices. Validate builds on target hardware before performance claims.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Unity provides UI Toolkit alongside uGUI/IMGUI for different project needs.](https://docs.unity3d.com/2023.2/Documentation/Manual/UIElements.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
