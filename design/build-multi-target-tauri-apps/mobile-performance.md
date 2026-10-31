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

1. Research and acceptance: complete; dated primary-source guidance is packaged.
2. Implementation complete: canonical skill, five progressive references and coherent 0.2.0 metadata.
3. Local validation complete: both catalogs, all 15 packages, regressions and both isolated client installs.
4. PR review/integration: active preparation; independent/configured outcomes and CI remain required.
5. Publication pending: tag the exact validated merge, publish plugin release and verify the generated
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

## Local validation receipt

- Both canonical Codex and generated Copilot catalogs validate (15 packages).
- All 15 packages pass source and exact distribution checks using clean temporary
  copies; pre-existing ignored files are preserved.
- Tauri payload: 46 files, eight skills; payload SHA-256
  `5e72a71d20d7eb514bdfc9bf14929e81eb592f291aae0817970ff18ffe580df9`.
- Marketplace, Copilot, distribution and installed-parity regression suites:
  16 + 6 + 27 + 4 = 53 tests passed. Existing route checks pass.
- Updated skill passes Skill Creator; pinned OpenAI Plugin Creator validator
  passes (the same checksum-verified validator used by repository CI).
- Codex CLI 0.166.0: isolated pre-install `plugin/read` reports eight skills and
  `installed=false`; installation and `skills/list` load eight skills with the
  new performance description/interface. Cache matches all 46 payload files.
- Copilot CLI 1.0.105: isolated marketplace browse/install/list reports enabled
  version 0.2.0 with eight skills. Local marketplace installs use a live source,
  explicitly copying nothing; its resolved distribution files match the payload.
  Git-backed published installation remains a later release check.
- These are package/discovery checks, not autonomous skill-routing, rendered
  plugin-card, physical-device, battery, memory or app-performance acceptance.
- Full repository regression suite and HOL security scan remain hosted CI gates.
