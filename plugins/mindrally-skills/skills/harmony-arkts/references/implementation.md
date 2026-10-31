# HarmonyOS ArkTS Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## ArkTS and component state

- ArkTS builds on TypeScript syntax but restricts dynamic behavior; validate language features against the configured API level.
- For state management V1, @State owns component state, @Prop provides one-way synchronization, and @Link provides intentional two-way linkage within supported types.
- State management V2 uses different decorators; follow the project generation instead of mechanically mixing examples.

## Resources and UI lifecycle

- Keep build focused on declarative composition; extract reusable components/builders based on complexity rather than mandated method order.
- Use $r resources for localized strings and theme values; verify referenced resources exist.
- Use vp for layout dimensions and platform text sizing conventions; test font scaling, RTL, and foldable/tablet layouts.
- Page-only lifecycle callbacks are not generic component hooks. Release subscriptions/timers in the appropriate owner lifecycle.
- Prefer existing accessible names from native components; add labels and focus attributes when needed rather than unconditionally forcing tab order.

## Primary documentation

- [ArkTS introduction](https://developer.huawei.com/consumer/en/doc/harmonyos-guides/arkts-get-started) — ArkTS strengthens static checks and constrains runtime object layout compared with TypeScript.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
