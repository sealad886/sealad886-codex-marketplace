---
name: mlx-inference-optimizer
description: Optimize Python MLX inference and generation loops with warmup, batching, cache handling, synchronization, quantization, and memory checks.
---

# MLX Inference Optimizer

## When to invoke

Use this skill for MLX inference, generation, serving loops, batch scoring,
streaming output, or latency/throughput questions.

## Inputs and evidence

Before any Python execution, use the target repo's `.venv`. Never install
Python packages globally. Identify the inference entry point, representative
inputs, correctness rule, benchmark command, and MLX version. Read:

- `../../references/inference-patterns.md`
- `../../references/eval-and-synchronization.md`
- `../../references/memory-and-dtypes.md`

## Workflow

1. Identify the exact inference entry point and representative inputs.
2. Separate first-output latency from steady-state throughput.
3. Inspect warmup, batching, scalar extraction, streaming sync, cache growth,
   quantized model loading, and dtype policy.
4. Confirm the benchmark forces completion before stopping timers.
5. Verify output correctness or equivalence before accepting speedups.

## Outputs and handoff

- Prompt/input shape and batch size.
- Warmup and measured run counts.
- Synchronization boundary.
- Median and range of wall time.
- Memory telemetry.
- Correctness or output-equivalence rule.

Hand verified changes back with before/after results and residual risks.

## Completion evidence

Completion requires representative correctness plus synchronized timing and
memory evidence for the exact changed workload.

## Must not

- Do not accept unsynchronized timings or dummy-array synchronization.
- Do not trade output correctness for throughput without explicit authority.
