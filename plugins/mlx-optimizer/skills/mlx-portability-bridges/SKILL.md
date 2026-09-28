---
name: mlx-portability-bridges
description: Advise on Python-first MLX integration with Swift, C, C++, and non-native language boundaries.
license: MIT
---

# MLX Portability Bridges

## When to invoke

Use this skill when the user asks how MLX work should cross language or app
runtime boundaries.

## Inputs and evidence

Before any Python execution, use the target repo's `.venv`. Never install
Python packages globally. Resolve target language/runtime, deployment boundary,
latency and memory constraints, model format, and these references:

- `../../references/portability-bridges.md`
- `../../references/profiling-and-metal.md`

## Workflow

1. Identify whether the target needs native MLX execution, app integration,
   service integration, or exported model deployment.
2. Prefer MLX Python for optimization work in v1.
3. Use MLX Swift for Apple app integration when runtime MLX execution is needed.
4. Use C/C++ for extension or low-level integration boundaries.
5. For other languages, recommend subprocess, service, C ABI, or Core ML/export
   boundaries, then include data marshaling costs in benchmarks.

## Outputs and handoff

Report selected boundary, data flow, marshaling and lifecycle costs,
compatibility constraints, verification plan, and alternatives.

## Completion evidence

Completion requires a feasible boundary tied to the target runtime and a plan
to measure correctness, transfer overhead, memory, and failure behavior.

## Must not

Do not claim equal-depth MLX optimization support for languages without a
first-class MLX API.
