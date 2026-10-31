# React Native implementation: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use functional components and Hooks where they fit; neither `React.FC` nor interface-only props are framework requirements.

- Use `getItemLayout` only when lengths and offsets can be computed correctly, including separators and headers.

- Balance `windowSize`, batch size, and batching period against responsiveness and blank areas on target devices.

- `removeClippedSubviews` can cause missing content with transforms or absolute positioning; it detaches views and does not guarantee large memory savings.

- Stable keys and lightweight list rows matter; memoize rows or callbacks only when prop identity and profiling justify it.

- Choose a maintained image solution already used by the project; do not mandate a particular third-party image library.

- Expo update compatibility depends on runtime version and native code changes; test updates against their compatible binary and obtain publication authority.

- Measure release builds on physical devices, including low-memory conditions; development-mode results differ.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [FlatList tuning has responsiveness, memory, and clipping tradeoffs.](https://reactnative.dev/docs/optimizing-flatlist-configuration)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
