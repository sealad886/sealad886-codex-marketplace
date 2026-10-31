# Performance primary-source ledger

Reviewed **2026-10-31**. Original synthesis for the canonical
`tauri-performance` skill. No source examples, third-party code or assets were
copied. Research and package validation do not establish a consumer app's speed,
energy or memory improvement; no consumer device was profiled for this update.

## Version receipt and contradictions

Upstream stable releases observed at review time: Rust `tauri` **2.12.5**,
JavaScript `@tauri-apps/api` **2.12.4**, Rust/npm CLI **2.12.4**. Exact release
sources: [Rust Tauri](https://github.com/tauri-apps/tauri/releases/tag/tauri-v2.12.5),
[JS API](https://github.com/tauri-apps/tauri/releases/tag/%40tauri-apps/api-v2.12.4),
[Rust CLI](https://github.com/tauri-apps/tauri/releases/tag/tauri-cli-v2.12.4),
[npm CLI](https://github.com/tauri-apps/tauri/releases/tag/%40tauri-apps/cli-v2.12.4).
The aggregate release landing page lagged at 2.12.3; exact stable releases and
pinned source resolve that discrepancy. Tauri 3 alpha is not the stable baseline.
Tauri 2.12's published Rust minimum is 1.90. These are research identities, not
commands to upgrade a consumer or require matching component patch numbers.
Inspect its lockfiles, installed CLI help, SDKs and WebView before implementation.

Context7 `/tauri-apps/tauri-docs` supplied command/channel/listener guidance,
corroborated against official docs and stable-tag source. Desktop-rendered
docs.rs omits some `cfg(mobile)` variants: pinned source confirms mobile
`WindowEvent::Suspended`/`Resumed`; the JS suspended/resumed events are documented
Android-only. Do not substitute `RunEvent::Suspended` or promise an iOS JS hook.

Tool availability is part of evidence: Apple Power Profiler needs supported
iOS/iPadOS 26+ devices/tooling; charging and Xcode pairing alter the relevant
power/sleep measurement. Android ODPM is hardware-dependent and device-level;
Battery Historian is no longer actively maintained. Newly documented native
APIs, including beta Android memory budgets, are conditional on the actual SDK,
deployment target and release status, not universal requirements.

## Tauri, Rust and web sources

All rows accessed 2026-10-31. Each supports a decision in the linked guides.

| ID | Primary source | Decision |
| --- | --- | --- |
| T01 | [Tauri process model](https://v2.tauri.app/concept/process-model/) | Attribute core and WebView work/footprints separately |
| T02 | [Tauri 2.12 release](https://v2.tauri.app/blog/tauri-2.12/) | Stable release/toolchain context; inspect consumer constraints |
| T03 | [Calling Rust](https://v2.tauri.app/develop/calling-rust/) | Command scheduling, binary Response and raw requests |
| T04 | [Calling frontend](https://v2.tauri.app/develop/calling-frontend/) | Small events, ordered channels and listener lifetime |
| T05 | [Tauri 2.12.5 app source](https://github.com/tauri-apps/tauri/blob/tauri-v2.12.5/crates/tauri/src/app.rs) | Exact mobile-only Rust lifecycle variants and platform callbacks |
| T06 | [Tauri 2.12.5 JS event source](https://github.com/tauri-apps/tauri/blob/tauri-v2.12.5/packages/api/src/event.ts) | JS suspended/resumed events documented Android-only |
| T07 | [Tauri 2.12.5 runtime source](https://github.com/tauri-apps/tauri/blob/tauri-v2.12.5/crates/tauri/src/async_runtime.rs) | Actual blocking-task API and runtime delegation |
| T08 | [Tokio spawn_blocking](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html) | Explicit CPU concurrency; started blocking work cannot be aborted through its handle |
| T09 | [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html) | Optimization/size/symbol/panic tradeoffs; no universal release recipe |
| T10 | [Tauri application size](https://v2.tauri.app/concept/size/) | Size-oriented examples and conditional unused-command removal |
| T11 | [MDN lazy loading](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Lazy_loading) | Critical path versus deferred feature cost |
| T12 | [MDN animation performance](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Animation_performance_and_frame_rate) | Rendering cost and actual display cadence |
| T13 | [MDN web workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) | Worker lifetime, copying and transferable ownership |
| T14 | [MDN Page Visibility](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API) | Renderer visibility is not native background-execution policy |

## Apple, Android and cross-platform mobile sources

| ID | Primary source | Decision / limit |
| --- | --- | --- |
| M01 | [Apple Power Profiler](https://developer.apple.com/documentation/xcode/measuring-your-app-s-power-use-with-power-profiler) | iOS/iPadOS 26+, power-source, process-selection and pairing limitations |
| M02 | [Apple Instruments power session](https://developer.apple.com/videos/play/wwdc2025/226/) | Comparable power captures and causal investigation |
| M03 | [Apple battery use](https://developer.apple.com/documentation/xcode/analyzing-your-app-s-battery-use) | Correlate energy categories with actual work |
| M04 | [MetricKit](https://developer.apple.com/documentation/metrickit) | Aggregated field evidence, not immediate microbenchmark; deployment availability matters |
| M05 | [Jetsam reports](https://developer.apple.com/documentation/xcode/identifying-high-memory-use-with-jetsam-event-reports) | Pressure termination and process identity, not a normal crash backtrace |
| M06 | [WebKit memory inspection](https://docs.webkit.org/Infrastructure/MemoryInspection.html) | WebContent footprint and memory attribution |
| M07 | [Android profiling](https://developer.android.com/studio/profile/) | Profileable release timing versus debuggable allocation diagnostics |
| M08 | [Android WebView memory](https://developer.android.com/develop/ui/views/layout/webapps/manage-webview-memory) | Native/renderer footprint, owner teardown and reusable caches; updated 2026-10-28 |
| M09 | [Android memory management](https://developer.android.com/topic/performance/memory-management) | RSS/PSS/shared-page accounting and process lifetimes |
| M10 | [Android rendering](https://developer.android.com/topic/performance/vitals/render) | Host rendering counters may cover only part of WebView rendering |
| M11 | [Android Power Profiler](https://developer.android.com/studio/profile/power-profiler) | Supported Pixel hardware/rails; ODPM is device-level and noisy |
| M12 | [Battery Historian status](https://developer.android.com/topic/performance/power/battery-historian) | No longer actively maintained; prefer current supported tools |
| M13 | [Apple networking power](https://developer.apple.com/documentation/xcode/reducing-networking-and-bluetooth-power-usage) | Batching, connection reuse, discretionary work and bounded retries |
| M14 | [Android background battery optimization](https://developer.android.com/develop/background-work/background-tasks/optimize-battery) | Constrained/coalesced durable work and appropriate expedited work |
| M15 | [MDN Page Visibility](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API) | Visibility hints, background timer/rAF behavior and exceptions |
| M16 | [Android process lifecycle](https://developer.android.com/guide/components/activities/process-lifecycle) | Process death without final destruction callback |
| M17 | [Apple location efficiency](https://developer.apple.com/documentation/xcode/accessing-the-device-s-location-efficiently) | Match accuracy/frequency and background purpose |
| M18 | [Android location battery optimization](https://developer.android.com/develop/sensors-and-location/location/battery/optimize) | Stop, time-bound and batch updates |
| M19 | [Android battery technical quality](https://android-developers.googleblog.com/2026/03/battery-technical-quality-enforcement.html) | Avoid redundant continuous wake locks for location delivery |
| M20 | [Apple power notifications](https://developer.apple.com/documentation/xcode/responding-to-power-notifications) | Low Power Mode and thermal response |
| M21 | [Android thermal guidance](https://developer.android.com/games/optimize/adpf/thermal) | Sustained limits, supported API/polling and signal caveats |
| M22 | [web.dev long tasks](https://web.dev/articles/optimize-long-tasks) | Main-thread work and response latency |
| M23 | [MDN requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) | Cadence, timestamps and hidden-page behavior |
| M24 | [Browser memory measurement](https://developer.mozilla.org/en-US/docs/Web/API/Performance/measureUserAgentSpecificMemory) | Experimental/limited API, isolation and comparability limits |
| M25 | [Android app memory budgets](https://developer.android.com/topic/performance/memory/app-memory-budgets) | Android 17 QPR2 beta/API 37.2 at review time; conditional deployment guidance |

## Refresh rule

Recheck affected rows when consumer Tauri/runtime/CLI/plugin versions, WebView,
SDKs, profiler availability, lifecycle behavior or native deployment targets
change. Prefer exact supported source when rolling examples disagree. Record
new evidence and uncertainty in the consumer receipt rather than silently
upgrading dependencies or inventing an unavailable API.
