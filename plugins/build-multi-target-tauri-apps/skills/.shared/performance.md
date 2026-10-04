# Performance, memory and telemetry

Grounding: [R02, R12–R13, R30](research.md), [Tauri logging](https://v2.tauri.app/plugin/logging/), [Android profiling](https://developer.android.com/studio/profile) and [Apple Instruments](https://developer.apple.com/tutorials/instruments). These platform tools supplement Tauri; choose available tools without adding instrumentation by default.

Define one scenario (cold launch, list scroll, import, streaming or resume), workload, boundaries and acceptance metric. Record release/debug status, device/OS/WebView, architecture, thermal/load conditions and app revision. Compare repeated captures under comparable conditions; emulator/debug samples are diagnostic, not physical release-performance acceptance.

## Attribute the layer

- Frontend: WebView inspector performance/heap tools, long tasks, rendering/layout, rerenders, event listeners and image/list allocation.
- Rust: CPU profiles and allocation evidence for domain tasks, blocking executor work, locks, channels, serialization and IPC payload size/frequency.
- Apple native: Instruments Time Profiler/Allocations/Leaks or memory graph, exact executable and UUID-matched symbols. Include WebContent process when relevant, not only the host app.
- Android: Perfetto for startup/frame/scheduler stalls, Simpleperf for sampled CPU when app is debuggable/profileable, gfxinfo for a frame snapshot and meminfo/heap/native tooling for memory. Include WebView/renderer attribution and matching native symbols. If sampling unavailable, report the limit and choose a supported capture; do not call an empty profile success.
- Windows/Linux: available OS profiler and WebView inspector tied to exact process/build; do not assume Apple-only tools exist.

Track JS heap, Rust/native allocation, WebView subprocess memory and OS total separately. A lower memory snapshot alone does not prove a leak fix. Show retained ownership/lifetime, repeated flow growth, removed retaining edge and equivalent recapture. Inspect listener disposal, long-lived state, task handles, caches and native callbacks. Prefer bounded queues and channels over uncontrolled event fanout, move blocking work off UI/executor and paginate/virtualize when workload warrants it. Measure before introducing memoization, pooling or custom native optimizations.

Temporary profiler linking/feature changes must be isolated, recorded and removed or explicitly retained. Match symbol UUID/build IDs before interpreting stacks. Store traces in a unique run directory; never clear global logs, kill unrelated profilers or reuse a shared fixed capture filename.

Use structured operation identifiers and redacted duration/error events across frontend/Rust/native layers. Keep telemetry bounded and user data out; choose existing logging stack or official plugin only when needed. Report baseline/changed metric, run count, variation, hotspot/ownership evidence, correctness checks and unresolved target limits.
