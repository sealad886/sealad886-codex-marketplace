---
name: mlx-performance-audit
description: Audit Python MLX repos for lazy-eval, synchronization, compile, dtype, memory, progress, and benchmark issues.
license: MIT
---

# MLX Performance Audit

## When to invoke

Use this skill for repo-wide MLX performance reviews and unknown bottlenecks.

## Inputs and evidence

Before any Python execution, use the target repo's `.venv`. Never install
Python packages globally. Resolve repository state, dependency files, entry
points, benchmark commands, correctness signals, and these references:

- `../../references/mlx-core-concepts.md`
- `../../references/eval-and-synchronization.md`
- `../../references/compile-and-transforms.md`
- `../../references/memory-and-dtypes.md`
- `../../references/reporting-format.md`

## Workflow

1. Inspect repo state with `git --no-pager status --short`.
2. Locate dependency files, MLX imports, training loops, inference loops,
   dataloaders, benchmark scripts, and progress-reporting patterns.
3. Run `../../scripts/mlx_audit.py` from this plugin repo when
   the target repo is local and scanning is useful.
4. Keep candidate findings separate from verified findings.
5. Recommend measurement before changes: warmup, synchronization, repeated runs,
   memory telemetry, correctness checks, and representative input sizes.

## Outputs and handoff

Use `../../templates/optimization-report.md` as the report structure. Every
finding needs file, line, evidence, candidate impact, confidence, verification,
and residual risk.

## Completion evidence

Completion requires inspected repository coverage, separately labeled candidate
and verified findings, and a bounded verification path for every material item.

## Must not

- Do not present static pattern matches as measured bottlenecks.
- Do not edit target code during an audit-only request.
