---
name: mlx-optimizer
description: Route Python-first MLX optimization work on Apple Silicon to focused audit, training, inference, Metal, or bridge workflows.
license: MIT
---

# MLX Optimizer

## When to invoke

Use this skill when the user asks Codex to optimize, audit, benchmark, profile,
or explain MLX code on Apple Silicon.

## Inputs and evidence

Resolve the target repository or file, active workload, local Python/MLX
environment, baseline command, correctness signal, and user authority.

## Workflow

1. Identify the target repo or file.
2. Check for a repo-local `.venv` before any Python execution.
3. Inspect project structure before proposing new modules.
4. Treat static observations as candidate findings until verified.
5. Require concrete evidence for optimization claims.
6. For version-sensitive MLX API behavior, retrieve current authoritative MLX
   docs before implementation or recommendations.

## Routing

- Repo-wide or unknown performance issue: read `../mlx-performance-audit/SKILL.md`.
- Training loop issue: read `../mlx-training-optimizer/SKILL.md`.
- Inference or generation issue: read `../mlx-inference-optimizer/SKILL.md`.
- Metal capture, custom kernel, or C++ extension question: read `../mlx-metal-kernels/SKILL.md`.
- Swift/C/C++ or other language integration: read `../mlx-portability-bridges/SKILL.md`.

## Core References

Read only the files needed for the routed task:

- `../../references/mlx-core-concepts.md`
- `../../references/eval-and-synchronization.md`
- `../../references/compile-and-transforms.md`
- `../../references/memory-and-dtypes.md`
- `../../references/reporting-format.md`

## Outputs and handoff

Report routed specialist, inspected paths, changes or recommendations, commands
and outcomes, performance and correctness evidence, and residual risks.

## Completion evidence

Completion requires concrete evidence for the requested optimization claim, or
an explicit bounded proof gap when native validation cannot run.

## Must not

- Never install Python packages globally.
- Preserve unrelated user changes.
- Prefer existing repo abstractions.
- Do not recommend automatic rewrites without active code-path evidence.
- Include commands, outcomes, and residual risks in the final handoff.
