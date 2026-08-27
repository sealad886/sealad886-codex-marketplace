---
name: mlx-training-optimizer
description: Optimize Python MLX training loops with value_and_grad, accumulation, checkpointing, dtype, validation cadence, memory telemetry, and progress reporting.
license: MIT
---

# MLX Training Optimizer

## When to invoke

Use this skill when the user points to MLX model training, fine-tuning,
pretraining, loss computation, optimizer updates, or validation throughput.

## Inputs and evidence

Before any Python execution, use the target repo's `.venv`. Never install
Python packages globally. Resolve training entry point, baseline command,
correctness signal, representative workload, MLX version, and these references:

- `../../references/training-patterns.md`
- `../../references/eval-and-synchronization.md`
- `../../references/compile-and-transforms.md`
- `../../references/memory-and-dtypes.md`

## Workflow

1. Identify the exact training entry point and the hot step function.
2. Check the `value_and_grad` namespace and placement, optimizer state, and
   `mx.eval` usage.
3. Inspect gradient accumulation, checkpointing, validation cadence, data
   loading, prefetching, dtype casts, and scalar logging.
4. If code loops over files or folders, require progress output with ETA.
5. Propose changes only after the baseline command and correctness signal are
   known.
6. Verify with a short smoke run and a representative benchmark run.

## Outputs and handoff

- Command and exit code.
- Steps per second or wall time.
- Active, peak, and cache memory where available.
- Input shape, batch size, dtype policy, and MLX version.
- Correctness signal and residual risk.

Hand verified changes back with before/after results and any native-run gap.

## Completion evidence

Completion requires a representative correctness check plus comparable
throughput and memory evidence for the exact changed training path.

## Must not

- Do not optimize only a synthetic step while claiming end-to-end improvement.
- Do not approve scientific or listening-quality gates for the user.
