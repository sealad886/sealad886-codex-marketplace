# Pixi.js Game Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Versioned APIs and rendering

- PixiJSv8 Application initialization is asynchronous; match setup and canvas APIs to the installed version.
- v8 cacheAsTexture replaces older cacheAsBitmap and needs explicit refresh when cached content changes.
- Federated event/eventMode and ParticleContainer APIs differ across versions; do not assume the old interaction manager or particle model.
- WebGPU support does not guarantee faster results than WebGL; benchmark representative scenes and supported fallbacks.

## Lifecycle and resources

- Use ticker timing values correctly for the installed API and cap/clamp elapsed simulation time when needed.
- Destroy only textures/assets owned by the scene; shared atlases/resources may be used elsewhere.
- Culling, pooling, atlases and compressed textures have workload/platform tradeoffs; measure draw calls, allocations and memory.
- Pause/throttle hidden/background work appropriately and test pointer/touch/keyboard accessibility paths and orientation changes.

## Primary documentation

- [Primary documentation](https://pixijs.com/8.x/guides/components/scene-objects/container/cache-as-texture) — PixiJSv8 documents cacheAsTexture and explicit cache refresh rather than the older cacheAsBitmap API.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
