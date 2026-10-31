# Measurement and platform tools

Grounding: [T01–T10 and M01–M12](research.md). Choose tools from the actual app,
SDK and device. No profiler or native bridge is a hidden dependency of this skill.

## Comparable before/after protocol

1. Name the user task, useful output, workload and visible completion boundary.
   Select relevant cold/warm launch, input/scroll, sustained work, idle,
   background/screen-off, resume or repeated-cycle scenarios. Define app-derived
   acceptance criteria and resource guardrails before optimizing.
2. Record revision, packaged artifact, release/debug/profileable state,
   optimization/instrumentation settings, ABI and matching dSYM/build IDs. Record
   device/OS/WebView, refresh rate, native plugins and host/renderer process IDs.
   Re-identify processes after restart; do not attribute a stale PID's data.
3. Match power source, charge state, brightness/display settings, power-saving
   mode, thermal state/ambient conditions, radio/network conditions, caches,
   warm-up and unrelated background load. Record differences you cannot control.
   Let devices cool between sustained runs; alternate baseline/candidate order
   where practical. Do not manufacture a clean run by resetting user data.
4. Capture repeated equivalent work. Report run count, variation and sustained
   duration; use distributions only when the sample count supports them. Do not
   dress a few runs up as dependable tail percentiles. A result within run noise
   is inconclusive. Preserve artifacts and explain excluded samples.
5. Use optimized packaged builds on authorized physical devices for mobile
   performance acceptance. Debug/emulator/browser captures can diagnose causes;
   allocation instruments may require a different diagnostic build. Repeat the
   appropriate production-equivalent check after the repair. Keep invasive
   profiling and screen recording separate from low-overhead acceptance runs.
6. Verify equivalent output, error/retry behavior, cancellation, durability,
   accessibility and lifecycle recovery. Inspect all affected resource guardrails
   so faster launch does not merely move work into first navigation or resume.

Use interaction-to-visible-result and missed deadlines at the device's actual
cadence; do not impose one universal FPS target. A web long-task threshold is not
an entire frame budget. Distinguish app launch, first visible frame, first usable
interaction and completion of deferred initialization.

Energy is integrated power over the scenario. Report the tool's actual units,
attribution and interval; normalize by useful work only when workloads/results
are equivalent. Shorter execution and lower average power are separate facts.
CPU time, wakeup counts and battery percentage are proxies, not measured joules
or proof of longer battery life. A transient power reduction can still consume
more total energy over a longer task.

## Capture the responsible layer

| Question | Useful evidence | Important limit |
| --- | --- | --- |
| JS tasks/layout/paint/rerenders | Actual WebView inspector and framework profiler, operation markers, JS heaps | Browser preview is not embedded WebView proof; inspector overhead changes timing |
| Rust/native CPU, locks or blocking | Symbolized CPU sampling, scheduler/operation traces and queue/concurrency evidence | Match binary/build IDs; async labels do not identify the actual stalled thread |
| Apple CPU/memory | Instruments Time Profiler, Allocations/Leaks, memory graph, WebContent footprint and jetsam reports | Host and WebContent are distinct; jetsam is pressure termination, not a normal crash backtrace |
| Apple power/sleep | Supported Power Profiler and unpaired on-device Performance Trace; field MetricKit when already integrated | Power Profiler is iOS/iPadOS 26+; charging reports zero overall system power; pairing keeps the SoC awake, so paired traces do not prove sleep behavior |
| Android timing/rendering | Release-derived profileable build, Perfetto/system trace, sampled native CPU, WebView inspector | Some heap/allocation tasks need debuggable builds; host `gfxinfo`/Vitals may not cover WebView paint/compositing |
| Android power | Supported Power Profiler/ODPM or platform power metrics; available battery-gauge counters separately labeled | ODPM depends on supported hardware/rails and is device-level; other apps contribute noise. Counter availability is not per-app attribution |
| Android memory | Host/renderer/native/JVM tools, meminfo and appropriate heap/capture evidence | Java wrappers exclude much WebView native/graphics memory; RSS/PSS/USS are different quantities |
| Windows/Linux/macOS desktop | Available OS profiler and actual WebView inspector with process/symbol identity | Do not assume Apple/mobile-only tools or APIs exist on another target |

Apple All Processes selection omits app power metrics; keep system and selected
app attribution distinct. MetricKit is aggregated field evidence, normally at
most daily, not an immediate microbenchmark. Check deployment availability of
newer APIs instead of assuming the newest documentation applies to every app.
Android Power Profiler's current ODPM support is restricted to supported Pixel
6-and-later hardware with documented OS/tool requirements and varying rails;
verify the actual device instead of promising support from an API level alone.
Battery Historian is no longer actively maintained; do not install it as the
default route when current platform tracing/power tools answer the question.

For thermal or low-power behavior, use supported platform signals and validate
them on the device. An unavailable or misleading sensor does not establish
absence of thermal pressure. Brief fast bursts cannot establish sustained
throughput or energy performance.

## Capture hygiene

Use a unique run directory outside package source. Scope capture to the selected
device/app/process, redact sensitive payloads and retain raw artifacts with their
identity receipt. Never clear global battery history/shared logs, kill unrelated
profilers or change global power settings merely for cleaner data. Verify each
capture contains useful samples from the intended process; an empty profile is
not success. Remove owned temporary instrumentation and test-only debug access,
or explicitly document retained bounded telemetry and its cost.
