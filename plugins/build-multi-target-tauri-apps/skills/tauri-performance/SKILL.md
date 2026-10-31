---
name: tauri-performance
description: Use when optimizing Tauri mobile or desktop startup, UI responsiveness, scrolling, IPC, battery drain, power, thermal throttling, peak memory, memory growth or background resource use.
license: MIT
---

# Tauri Performance, Battery and Memory

Improve a real user task while preserving correctness and controlling its CPU,
energy and memory costs. Mobile is the default emphasis; retain desktop behavior
when it is part of the app's supported targets.

Read the [common operating contract](../.shared/operating-model.md) and
[optimization map](../.shared/performance.md). Load focused references as needed:

- [Measurement and platform tools](../.shared/performance/measurement.md): establish a baseline, choose captures and interpret limits.
- [Battery, thermal and lifecycle work](../.shared/performance/mobile-energy.md): idle drain, background activity, network, sensors and sustained load.
- [Memory and ownership](../.shared/performance/memory.md): peaks, retained resources, WebView processes and pressure recovery.
- [Measurement receipt](../.shared/performance/receipt.md): record before/after evidence and tradeoffs.
- [Dated primary research](../.shared/performance/research.md): version-sensitive APIs and refresh triggers.

## When to invoke

Use for Tauri startup/input/scroll latency, battery drain, thermal slowdown,
background resource use, IPC throughput, allocation peaks or retained memory.
The same workflow supports a measured optimization request and a causal defect
investigation; load only the references needed for that scenario.

## Inputs and evidence

Inspect the affected flow and expected result, app revision, manifests/lockfiles,
Tauri/CLI/plugin versions, supported devices, OS/WebView versions, build profile,
existing telemetry and available profiler capabilities. Ask only for missing
information that blocks the next useful action. Do not install SDKs, change
system settings or require a new profiler merely to begin source diagnosis.

## Workflow

1. **Choose a scenario and acceptance criteria.** Define useful work and its
   visible completion boundary. Select relevant launch, interaction, sustained,
   idle, background, resume or repeated-cycle scenarios. Set a primary metric
   and memory/energy/responsiveness guardrails from app requirements and
   representative devices; do not invent universal budgets.
2. **Capture a matched baseline.** Use the measurement guide. Identify the host,
   WebView renderer and native/Rust work, exact artifact and matching symbols.
   Record power, thermal, network, display and instrumentation conditions. If
   only source, browser, emulator or debug evidence is available, continue useful
   diagnosis and label physical-device acceptance as not run.
3. **Find the causal cost.** Trace the user operation across frontend, IPC, Rust
   and native plugins. Inspect redundant work, main-thread stalls, serialization,
   copied buffers, queue/concurrency growth, cache ownership and hidden activity.
   Distinguish a leak from allocation churn, retained capacity and legitimate
   caches; distinguish app-attributed energy from device-level signals/proxies.
4. **Implement the smallest useful optimization.** Remove unnecessary work
   first. Bound producers, buffers, workers and caches; preserve final results,
   durability and required freshness. Use the optimization map rather than
   automatically adding memoization, threads, a framework, a plugin or an IPC
   wrapper. Make cancellation and resource teardown actually stop their owners.
5. **Check behavior and cost together.** Verify equal results, errors,
   cancellation, accessibility, offline/retry behavior and relevant lifecycle
   transitions. Repeat comparable measurements, including sustained and idle
   phases when affected. Check for shifted cost: later navigation, peak memory,
   background wakeups, energy, thermal throttling or resume storms.
6. **Keep or reject the change from evidence.** Report improvement, regression
   or inconclusive results with sample count and variation. A shorter run, lower
   heap snapshot or smaller binary alone is insufficient. Remove only owned
   temporary instrumentation, or explicitly retain justified bounded telemetry.
7. **Hand off the result.** Use the receipt. Include measured before/after data,
   causal explanation, correctness checks, tradeoffs and per-target limitations.
   Do not present a proposed optimization or unrun physical check as completion.

## Outputs and handoff

Produce the measurement receipt with the implemented change or diagnostic
conclusion, causal evidence, comparable results, behavior checks and tradeoffs.
Name unavailable targets/tools, remaining physical-device acceptance and the
location/disposition of owned captures and instrumentation.

## Completion evidence

An implemented causal change has matching before/after evidence and behavior
checks, with no unexplained regression against the chosen guardrails. A diagnostic
handoff may instead conclude no supported fix or inconclusive measurements; name
what was established and what evidence is still missing. Native power and memory
claims require the corresponding target evidence, not only a successful build.

## Must not

- Claim longer battery life from CPU time, battery percentage or emulator timing.
- Equate `async` with nonblocking CPU work, a Tauri channel with backpressure, or
  aborting a started blocking task with actual cancellation.
- Treat browser visibility as app-wide native suspension or rely on a final
  callback to save critical state before process death.
- Sum incompatible memory counters, call a lower single snapshot a leak repair,
  or claim host-only metrics cover the WebView renderer.
- Weaken permissions, CSP, durability or security for a benchmark; log sensitive
  payloads; clear global logs; kill unrelated captures; reset device/app data
  without exact authority; or leave profiling-only access enabled in production.
