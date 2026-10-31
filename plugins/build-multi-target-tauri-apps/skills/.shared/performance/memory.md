# Memory budgets, ownership and pressure

Grounding: [T01, T03–T09, T14 and M05–M09, M24–M25](research.md).

## Count the right footprint

Record host, WebView renderer and relevant native/helper process identities.
Separate JS heap, Rust/native allocations, JVM/Objective-C objects, decoded
media/graphics and OS footprint. Java wrappers and JS heap snapshots do not cover
the entire WebView. Browser memory APIs are partial, engine/version dependent
and sometimes experimental; do not call them native or OS total memory.
`measureUserAgentSpecificMemory()` has limited availability and isolation
requirements. Do not weaken CSP or change isolation simply to manufacture a
measurement.

Use consistent platform counters and units. RSS includes shared pages, so adding
process RSS can double-count. PSS apportions sharing and can change when sharing
changes; footprint/USS/heap metrics answer other questions. Do not compare a
host-only number with a multiprocess total or claim that incompatible counters
represent one budget.

Measure peak allocation during the operation, post-operation steady state and
repeated-cycle growth separately. Define active/idle/background working-set
budgets from representative devices and app tasks, not a universal MB limit.
Record allocator caches/reserved capacity and native reusable caches where they
explain resident memory after objects are freed.

## Implement the ownership repair

1. Reproduce growth over equivalent route/work/background cycles. Capture
   retained types/paths, task/handle counts or allocation stacks at matching
   checkpoints; allow comparable quiescence and GC behavior without forcing a
   production-only conclusion from a diagnostic collection.
2. Identify the retaining owner or oversized live working set. Inspect async
   listener-registration races, closures, global state, native callbacks, worker
   heaps, detached tasks, cache keys and queued/in-flight buffers.
3. Release resources when their actual owner ends. Stop producers as well as
   ignoring results; close subscriptions, cancel/checkpoint work, terminate owned
   workers and discard stale operation generations. Do not destroy Tauri's owned
   shell/WebView whenever a frontend route hides.
4. Bound caches by bytes/items and lifetime, queues by capacity/bytes and
   concurrency by resource budget. Choose an overflow/eviction policy that
   preserves durable results and user-visible correctness. Preload/prefetch only
   where the measured latency benefit justifies memory and energy cost.
5. Repeat equivalent captures. Show removed retaining edges or bounded repeated
   growth alongside equivalent results. Lowering a single snapshot or requesting
   GC is not leak proof; expecting immediate RSS return can misdiagnose retained
   allocator capacity as a leak.

## Reduce transient peaks

- Decode/downsample media to the actual use where supported; avoid retaining
  full-resolution originals, decoded copies, thumbnails and Base64/JSON buffers
  without need. Decoded dimensions and graphics surfaces can dominate compressed
  file size. Preserve required export/fidelity behavior.
- Stream or chunk large files/data where the consumer stack supports it; bound
  outstanding chunks and avoid collecting an entire stream before processing.
  Binary IPC can reduce serialization but does not guarantee zero copies.
- Paginate or virtualize large lists with bounded backing data and image caches;
  fewer DOM nodes alone does not bound an ever-growing model/cache.
- Measure the cost of workers, memoization, object pools and parallel jobs before
  adding them. They can trade latency for separate heaps, retained objects and
  larger simultaneous working sets.

## Pressure, termination and recovery

Use platform-supported memory-pressure callbacks or existing native integration
to trim recomputable caches and optional work where appropriate. Backgrounding
is not the only pressure case; test relevant foreground allocation peaks too.
Recomputable data may be evicted, but committed user data must remain durable.

Inspect iOS jetsam/WebContent termination evidence and Android process/renderer
termination separately from normal exceptions. Validate restored navigation,
reload/retry, saved operation state and idempotent resume after actual supported
pressure/recreation testing. A host that remains alive does not prove its
renderer survived. Do not force a crash or reset app/device data without the
consumer's exact authority.

The newly documented Android app memory-budget mechanism was Android 17 QPR2
beta/minor API 37.2 at this review date. Its manifest/API is conditional, not a
universal prerequisite. Check actual SDK/release status and deployment targets
before using it; budget and pressure-test the working set on supported devices
regardless of whether that newer mechanism is available.
