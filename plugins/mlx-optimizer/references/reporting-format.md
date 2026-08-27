# Reporting Format

Every MLX optimization report must include these sections.

## Summary

One paragraph with target repo, target workload, and verdict.

## Findings

Each finding includes severity, file, line, evidence, candidate impact, and
confidence.

## Suggested Actions

List bounded edits or experiments. Avoid automatic rewrites without active
code-path evidence.

## Verification

Record commands, exit codes, timing, memory telemetry, correctness checks, MLX
version, Python executable, and hardware details.

## Residual Risks

State what was not measured, what may be workload-specific, and what should be
rechecked after larger input sizes or longer runs.
