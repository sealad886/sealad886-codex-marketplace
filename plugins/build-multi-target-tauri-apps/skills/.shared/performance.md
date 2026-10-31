# Optimize useful work across Tauri layers

Start with the [measurement protocol](performance/measurement.md). For mobile
work also check [energy/lifecycle](performance/mobile-energy.md) and
[memory ownership](performance/memory.md) where the scenario can affect them.
Version-sensitive decisions are grounded in the
[2026-10-31 primary-source ledger](performance/research.md).

## Choose the repair from the bottleneck

| Observed cost | Inspect and implement | Verify the tradeoff |
| --- | --- | --- |
| Slow launch or first interaction | Separate native launch, frontend loading and first useful result; remove duplicate initialization, defer optional features and split critical assets | Cold/warm launch plus first deferred navigation, offline behavior and peak memory; a splash screen does not shorten readiness |
| Scroll/input stalls | Attribute JS tasks, framework updates, layout, paint/composition and IPC contention; paginate/virtualize measured large lists, reduce invalidation and batch DOM reads/writes | Interaction-to-visible result, trace/frame deadlines at actual refresh rate, accessibility/focus and representative list sizes |
| High IPC cost | Reduce payload bytes and message frequency; scope receivers, coalesce replaceable progress and avoid JSON/Base64 bulk transfer when a suitable binary path exists | Serialization/copy time, outstanding bytes, queue latency, final/error delivery and cancellation |
| CPU saturation or thermal slowdown | Remove repeated computation; use async I/O for I/O and bounded workers for genuinely blocking/CPU work | Completion latency, UI stalls, sustained throughput, peak memory and measured energy; more threads are not automatically better |
| Hidden/idle drain | Find owned timers, polls, retries, listeners, native tasks, sensors, media and wake locks; stop optional work and use supported scheduling for durable deferred work | Foreground idle, background/screen-off and resume; observe native producers as well as JS |
| Memory growth or peaks | Find allocation/retention ownership, redundant images/buffers, unbounded queues and caches; bound working sets and release resources at their actual lifetime | Peak plus repeated-cycle steady state, pressure/restart behavior and equivalent workload; do not require allocator RSS to drop immediately |

## Frontend responsiveness

Use the existing framework and its profiler. Fix measured expensive renders and
state invalidation before adding memoization. Avoid synchronous heavy work in
interaction handlers; break it into bounded units or use an owned worker when
that actually improves the complete task. Worker startup, separate heaps and
message copies have costs. Transfer buffers only when supported and when losing
sender ownership is correct. Terminate workers when their owner ends.

Use the real WebView's feature support, not desktop Chrome as a capability
promise. `requestAnimationFrame` is display-aligned scheduling, not a reason to
run a permanent animation loop. Stop unnecessary animation and respect reduced
motion. Compositor-friendly properties can reduce layout/paint, but extra layers
and indiscriminate `will-change` increase memory. Check both responsiveness and
memory after changing rendering strategy.

## IPC and Rust scheduling

Use finite commands for request/response, small events for notifications and
channels for measured ordered streaming needs. Scope delivery to the intended
owner. Tauri channels do not supply an application-level byte budget, producer
backpressure, acknowledgements or cancellation automatically. Bound upstream
queues and outstanding work; define overflow and cancellation behavior. Coalesce
replaceable progress, while preserving durable results and terminal transitions.

For a measured bulk-transfer problem, inspect the pinned command API:
`tauri::ipc::Response` can avoid ordinary JSON response serialization; raw invoke
request bodies can carry `ArrayBuffer`/`Uint8Array` into `Request`/`InvokeBody::Raw`.
These are not end-to-end zero-copy guarantees. Bound chunk sizes and in-flight
buffers, and measure transient copies before changing transport.

Ordinary synchronous command handlers run on the main thread unless configured
otherwise in the actual Tauri version. Async handlers schedule async tasks;
CPU-heavy loops and synchronous I/O inside them can still block an executor.
Use the app's existing bounded worker/semaphore design when appropriate before
scheduling blocking work. Do not hold synchronous locks across `await` or across
long I/O/codec/database work.

Tauri's `async_runtime::spawn_blocking` delegates to the runtime's blocking pool.
Its pool limit is not an app resource budget. A started blocking task cannot be
stopped merely by aborting its join handle. Use cooperative checkpoints, bounded
chunks or a cancellable dependency and prove shutdown/cancellation behavior.
Dropping a JS promise or ignoring a stale result does not stop backend work.
Long-lived blocking loops need an explicit owner and shutdown path.

Dispose listeners even when asynchronous registration resolves after the owner
has already ended. Correlate operations/session generations so resumed or
remounted views cannot accept stale results or create duplicate producers.

## Build and storage work

Evaluate release-profile changes only after measuring runtime bottlenecks.
Cargo `opt-level`, LTO and codegen-unit choices have workload-dependent size,
speed and build-time effects; `s`/`z` are not universal mobile performance
settings. Smaller downloads or binaries do not prove lower steady-state memory
or energy. Preserve matching symbols before stripping. `panic = "abort"` changes
failure semantics; do not apply it as a routine optimization.

Tauri unused-command removal has minimum component versions and dynamic-ACL
reachability limitations; inspect the linked size guidance before using it.
Never weaken capabilities to shrink an artifact.

Batch genuinely related storage writes/transactions and avoid synchronous work
on the UI path, while retaining acknowledged-write durability and crash/restart
correctness. Bound disk caches and retry work. Deferral must not turn a completed
user transaction into unsaved data. Use bounded, redacted operation IDs and
latency/error events; telemetry itself must not create unbounded logs or a busy
background loop.
