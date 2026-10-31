# Battery, thermal pressure and lifecycle

Grounding: [T03–T08, T14 and M13–M23](research.md). Optimize useful work per energy
while preserving required behavior. Removing needless work usually precedes
adding concurrency or moving work between JavaScript and Rust.

## Trace activity to an owner

Within the affected scenario, for each timer, poll, reconnect loop, listener, stream, worker, task, socket,
location/sensor subscription, camera/microphone, media session and wake/screen
lock, record its owner, active purpose, stop condition, resume policy and durable
state. Exercise repeated route entry/exit and foreground/background transitions.
Find duplicated observers and producers that outlive their screens or sessions.

Pause optional rendering, animation and polling when hidden; use page visibility
as a renderer hint. It does not stop Rust work, native plugins, sockets, sensors
or workers. Browser timer/rAF throttling is not an app-wide background policy.
CSS-hidden content also needs an ownership decision. Resume must not replay a
backlog of obsolete ticks, start duplicate listeners or create a retry storm.

## Tauri lifecycle is version and platform specific

In Rust Tauri 2.12.5 source, mobile lifecycle variants are
`tauri::WindowEvent::Suspended` and `Resumed` under `cfg(mobile)`, not a
`RunEvent::Suspended` API. Android maps to Activity `onPause`/`onResume` with the
initial creation-time resume ignored; iOS maps to `applicationWillResignActive`
and `applicationWillEnterForeground`. These are different platform transitions,
not interchangeable proof of screen-off, OS suspension or permission to keep
running. Desktop-rendered docs.rs can omit mobile-only variants.

The pinned JS event API documents `TauriEvent.WINDOW_SUSPENDED` and
`WINDOW_RESUMED` as Android-only, never emitted on other platforms. Do not teach
an iOS JS lifecycle hook from those names. Inspect the consumer's exact version
and existing native integration, use its real lifecycle owner, and test relevant
interruption, lock/unlock, background/foreground and process recreation. Add a
narrow native bridge only for a demonstrated missing consumer capability.

Processes can die without a final callback. Persist important state during normal
operation, before acknowledging durable completion. Do not rely on `unload`,
`onDestroy`, a final JS event or a late large background flush to finish a critical
write. Make restart/retry/resume idempotent. Distinguish ending optional
screen-owned work from safely checkpointing a durable user operation.

## Reduce expensive wakeups and active work

| Resource | Bounded optimization | Preserve and verify |
| --- | --- | --- |
| Network/radios | Coalesce related deferrable requests, reuse connections, cache/revalidate and bound retry/backoff; avoid constant health polls | Required freshness, authentication, delivery/error semantics, offline behavior and peak buffered bytes |
| Deferred background work | Use the consumer's supported OS scheduling with appropriate deadline/charging/unmetered constraints and checkpoints | JS fetch or an arbitrary Rust task is not iOS background URLSession; Android expedited work is not a restriction workaround |
| Location and sensors | Match accuracy/rate/latency to task, stop unused watches, use finite lifetimes/timeouts and batch where allowed | Navigation/safety requirements, visible permission state and correct restart; avoid redundant location wake locks |
| Camera/mic/media/Bluetooth | Stop or reduce work when its purpose ends; close owned sessions and scanning, bound decoding/buffering | Intentional background playback/recording and user expectations; do not silently cancel an explicitly required service |
| Display/rendering | Remove unnecessary loops, update only changed content and stop optional animation; check expensive blur/composition from traces | Accessibility, reduced motion and actual display cadence; smaller update frequency must still meet interaction requirements |
| CPU/concurrency | Avoid repeated decoding/compression/computation and cap parallel work from measured resource budgets | Completion time, peak memory, power and sustained thermal behavior; moving work to Rust or workers can add copies and wakeups |
| Storage/logging | Batch related work, use appropriate transactions, bound caches and telemetry | Crash durability and acknowledged writes; defer optional work without losing completed user transactions |

A durable background feature may require OS/native integration and permissions;
this skill does not supply those APIs. Reuse an existing integration before
adding dependencies. Observe stop/expiration and checkpoint behavior rather than
trying to defeat platform scheduling and battery restrictions.

## Low-power and sustained operation

Use supported Low Power Mode/thermal signals to reduce optional quality,
concurrency, polling or update frequency while preserving essential results.
Define how normal quality resumes without oscillation or catch-up work. Do not
assume the newest native API is exposed by Tauri or supported by every device.

Compare both short-task and sustained results: a quick parallel burst can heat
the device, grow working sets and throttle later work. Include foreground idle
and background/screen-off intervals when affected. Follow the measurement guide
for power attribution, charge state, pairing and noise limits. Report measured
energy separately from CPU/wakeup proxies and unavailable instrumentation.
