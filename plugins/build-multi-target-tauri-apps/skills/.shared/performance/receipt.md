# Performance change receipt

Use only fields relevant to the change; mark unavailable evidence explicitly.
Do not copy sensitive payloads into the report. Keep raw traces outside package
source and link their unique run directory.

## Scenario and criteria

- User task, useful output, start/end boundaries and relevant lifecycle states:
- Baseline/candidate revisions, exact packaged artifacts and build profiles:
- Device/OS/ABI/WebView, refresh rate, native plugins and process identities:
- Symbols/build IDs, tools/versions, capture scope and instrumentation differences:
- Workload/cache/warm-up state, network/background load, charge/power source,
  display/power-saving settings, thermal/ambient conditions and run order:
- App-derived primary target and responsiveness/energy/memory guardrails:

## Comparable results

| Metric / actual units and attribution | Baseline | Candidate | Runs / variation / sustained duration | Conclusion |
| --- | --- | --- | --- | --- |
| Launch or operation / interaction-to-visible latency | | | | |
| Frame/deadline or main-thread evidence at actual cadence | | | | |
| Peak / steady-state / repeated-cycle memory by consistent counter/process | | | | |
| Measured energy / average power / interval / useful work | | | | |
| CPU, wakeup or battery-gauge proxy, explicitly labeled | | | | |
| Idle/background and resume work, thermal/sustained behavior | | | | |

Use improvement/regression/inconclusive, rather than hiding noisy or unavailable
results. Explain shifted cost and exclusions. No invented tail percentiles from
small samples, summed incompatible memory totals or battery-life inference from
a short CPU benchmark.

## Causal change and correctness

- Measured bottleneck/retaining owner and bounded implementation:
- Equal output, error/retry/offline behavior and acknowledged-write durability:
- Accessibility, cancellation/checkpointing, repeated enter/leave and resume:
- Listener/timer/worker/task/native subscription ownership and teardown proof:
- Memory-pressure/process-recreation evidence where relevant:
- Tradeoffs, guardrail regressions and rollback/rejected alternatives:
- Raw artifacts and temporary instrumentation removed/retained with reason:

## Evidence limits and handoff

For each target state verified, failed, blocked or not run with reason. Separate
source/unit/browser/debug/emulator evidence from physical packaged-app evidence.
Name any missing power tool, native lifecycle integration, field telemetry or
physical-device acceptance. State whether a change was implemented, proposed,
rejected or remains inconclusive, and what evidence would resolve uncertainty.
