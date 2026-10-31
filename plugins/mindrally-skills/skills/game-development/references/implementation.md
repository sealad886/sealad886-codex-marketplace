# Game Development: implementation guidance

## Unity path

Use MonoBehaviour lifecycle only where needed, ScriptableObjects for suitable
asset/configuration data, and explicit runtime mutable state ownership. Coroutines
execute on the main thread and do not make blocking work asynchronous. Physics
and render update timing differ. Jobs/Burst require supported data/APIs and correct
dependency/disposal handling; most Unity object APIs are not general thread-safe.
Pool objects only with proper reset/lifetime and measured allocation pressure.
Addressables/AssetBundles, batching, LOD and UI systems depend on project version
and rendering/asset needs, not a fixed universal set. Check TryGetComponent's bool.

## Lua and shared reliability

Use locals/modules and explicit nil handling. pcall/xpcall catches Lua errors but
does not enforce authorization or undo effects. Weak tables need correct weak-key/
value semantics and are not a guaranteed persistent cache. In concatenation loops,
collect fragments and table.concat when appropriate; string.format is formatting,
not a universal concatenation optimization. Validate save formats, inputs and
network data and avoid secret-bearing logs. Compare platform builds and real
performance; a passing editor/unit test does not establish shipped gameplay quality.

## Primary documentation

- [Coroutine main-thread execution](https://docs.unity3d.com/Manual/Coroutines.html).
- [Lua errors, weak tables and table.concat](https://www.lua.org/manual/5.4/manual.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
