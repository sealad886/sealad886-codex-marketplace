---
name: tauri-performance
description: Use when diagnosing or improving Tauri startup, latency, scrolling, IPC throughput, memory growth, retained resources or telemetry.
license: MIT
---

# Tauri Performance and Memory

Read [common operating contract](../.shared/operating-model.md) before work and [performance reference](../.shared/performance.md) for this workflow. Current sources and adaptation rationale: [research ledger](../.shared/research.md).

## When to invoke

Use when diagnosing or improving Tauri startup, latency, scrolling, IPC throughput, memory growth, retained resources or telemetry.

## Inputs and evidence

Slow/leaking flow, target/build identity, timings/traces/heaps, process/symbol identity, ownership code and telemetry configuration.

## Workflow

1. Define one reproducible user scenario and measurable criterion; identify target/build, workload, processes and existing profiler availability.
2. Follow [performance reference](../.shared/performance.md). Choose WebView, Rust or native capture according to question; collect matching symbols and fresh artifacts.
3. Separate renderer/core/native hotspots and memory; inspect blocking work, serialization, message frequency, queues, locks and ownership lifetimes.
4. Implement smallest causal change. For leaks prove retaining edge/type or repeated growth disappears; for speed use comparable repeated measurements with correctness checks.
5. Remove owned temporary instrumentation and rerun scenario. Report baseline/changed metrics, sample count/variation, artifacts and physical/emulator/debug limitations.

## Outputs and handoff

Measured hotspot/ownership diagnosis, bounded fix, comparable captures, correctness results and limitations.

## Completion evidence

Metric improvement or ownership repair supported by matching before/after evidence; instrumentation disposition explicit.

## Must not

Claim leak fix from smaller heap alone, compare unmatched debug/release captures, use emulator timing as physical acceptance or log sensitive payloads.
