# React Three Fiber across web and native: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- For React Native, import `Canvas` and Hooks from `@react-three/fiber/native`; native Drei abstractions use `@react-three/drei/native`. Web imports are separate.

- Native rendering relies on Expo GL/assets and Metro-compatible assets; Next.js error files and DOM styling do not apply to a native scene.

- Use `useFrame` for frame-local updates and mutate refs rather than driving React state every frame.

- Call `useThree`, `useFrame`, and loader Hooks within the Canvas context.

- Reuse geometries/materials and consider instancing for repeated meshes; compare draw-call and memory measurements.

- Dispose manually managed GPU resources when ownership ends; account for shared resources to avoid premature disposal.

- Use target-appropriate gesture controls, pixel-ratio limits, and asset error/loading fallbacks.

- Validate native GL on physical hardware where simulator support is incomplete; a web preview does not establish native acceptance.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Native Fiber and Drei imports and Expo-backed GL/assets differ from web setup.](https://r3f.docs.pmnd.rs/getting-started/installation)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
