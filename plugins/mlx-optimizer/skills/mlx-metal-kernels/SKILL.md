---
name: mlx-metal-kernels
description: Guide MLX Metal profiling, mx.fast escalation, custom Metal kernels, and C++ extensions when profiling proves kernel-level bottlenecks.
license: MIT
---

# MLX Metal Kernels

## When to invoke

Use this skill only after normal MLX-level issues have been checked or when the
user explicitly asks about Metal capture, custom kernels, or native extensions.

## Inputs and evidence

Before any Python execution, use the target repo's `.venv`. Never install
Python packages globally. Require an exact workload, representative shapes and
dtypes, current profiling evidence, correctness checks, and these references:

- `../../references/profiling-and-metal.md`
- `../../references/memory-and-dtypes.md`
- `../../references/compile-and-transforms.md`

## Workflow

1. Confirm MLX can see Metal and the workload is GPU-backed.
2. Check synchronization, dtype, batch, graph-growth, and memory issues first.
3. Ask for or collect profiling evidence.
4. Recommend `mx.fast`, custom Metal kernels, or C++ extensions only when the
   operation is a measured bottleneck and built-in MLX ops are insufficient.
5. Require correctness tests for representative shapes and dtypes.

## Outputs and handoff

State whether custom native work is justified, which evidence supports that
decision, and what maintenance burden it creates.

## Completion evidence

Completion requires a measured kernel-level bottleneck, representative
correctness evidence, and a comparison with built-in MLX alternatives.

## Must not

- Do not recommend custom native code without profiling evidence.
- Do not treat Metal capture availability as proof that a kernel is worthwhile.
