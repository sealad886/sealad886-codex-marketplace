# Mobile performance skill enhancement

Task date: 2026-10-31. Baseline: `77b64e0` on marketplace main; released
Build Multi-target Tauri Apps 0.1.0. Planned release: 0.2.0, adding substantial
mobile optimization guidance to the existing public skill contract.

## Outcome and ownership

Expand `tauri-performance` rather than add an overlapping skill. Preserve eight
skills, the package identity, existing desktop coverage and the canonical shared
implementation for Codex and GitHub Copilot. Performance includes user-visible
speed and responsiveness, sustained memory, energy and thermal behavior.

The skill must help an agent implement and verify a causal improvement, not
merely list profilers or suggest optimizations. Retain the consumer's framework,
locked versions and existing native integrations.

## Acceptance

- Use dated primary Tauri, Rust/runtime, Apple, Android and Web guidance; record
  source scope, version-sensitive APIs and refresh triggers within the package.
- Start with one reproducible user task and an app-derived objective plus
  correctness, battery and memory guardrails. Attribute the bottleneck to
  WebView, Rust or native work before choosing a repair.
- Cover startup, frame/input latency, payload/IPC and task queues, CPU work,
  lifetime/cancellation, background/foreground behavior, network/sensor/media
  work, cache/image budgets, memory pressure and sustained thermal effects.
- Distinguish energy from power and elapsed time; explain available device/tool
  metrics, capture overhead, charging/pairing effects and unsupported hardware.
- Use matched repeated before/after runs with equivalent useful work, build,
  physical device and environmental conditions. Record variation and durability,
  accessibility, offline/error and lifecycle correctness alongside performance.
- Keep detailed platform instructions behind progressive references. Include a
  concise measurement/handoff receipt. Avoid universal numeric targets,
  unbounded instrumentation or unsupported claims from mocks/emulators.
- Synchronize portable/Codex manifests and skill metadata; regenerate the
  Copilot catalog using the existing tool. Verify packaged reference closure.
- Verify isolated discovery/installation in both clients with real user settings
  and credentials untouched. Keep native app performance acceptance separate
  from instruction-package validation and discovery.

## Delivery checklist

1. Research and acceptance: active; primary-source specialists preparing evidence.
2. Implement canonical skill, focused references and coherent 0.2.0 metadata.
3. Validate package/catalogs, existing regression checks and both client installs.
4. Run iterative independent/configured PR review, then merge under current gates.
5. Tag the exact validated merge, publish plugin release and verify the generated
   independent marketplace snapshot becomes GitHub Latest; clean task refs.

## Boundaries

No consumer application is supplied. This task cannot demonstrate a native app's
actual frame, energy or memory improvement. No SDK/device installation or reset,
new runtime/MCP dependency, framework migration or unrelated plugin modification
is required. PR #47's optional Parallel research contribution is separate work.

The working checkout was clean before creating `codex/tauri-mobile-performance`
from remote main; no worktree was created. Existing branches remain outside this
task's cleanup scope. Publish authority comes from the user's explicit request;
review and release identity remain required evidence.
