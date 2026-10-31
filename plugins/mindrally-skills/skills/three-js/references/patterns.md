# Three.js scenes and GPU resources: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Three.js works independently of React, Tailwind, Next UI, or a specific bundler; keep the project’s renderer architecture.

- Removing a mesh from a scene does not dispose GPU geometry, material, or textures. Track ownership and dispose obsolete resources explicitly.

- Textures can be shared across materials; disposing a material does not dispose its textures. Release shared resources only when no owner needs them.

- Stop animation loops and remove event/control listeners on teardown; dispose render targets and relevant renderer/control resources.

- Measure draw calls, triangles, texture memory, and frame time before adding instancing, merging, pooling, LOD, or custom culling.

- Use renderer-supported pixel ratio/color-space/lighting APIs matching the installed version and target.

- In Fiber, frame hooks run inside Canvas; avoid React state updates every animation frame and account for framework-managed disposal.

- Use responsive canvas/camera sizing and asset loading/error fallbacks; a screenshot alone does not establish stable resource use.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [GPU resources require explicit disposal; material and texture lifetimes are separate.](https://threejs.org/manual/pages/how-to-dispose-of-objects.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
