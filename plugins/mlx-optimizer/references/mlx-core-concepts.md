# MLX Core Concepts

Use this reference when reasoning about why MLX code behaves differently from
eager CPU/GPU frameworks.

## Optimization Facts

- MLX uses lazy evaluation. Array operations build a graph until evaluation is
  requested.
- MLX graphs are dynamic. Shape changes and Python control flow can affect
  compilation and benchmarking.
- MLX uses unified memory on Apple Silicon. CPU and GPU share memory, so copying
  costs differ from discrete-GPU systems, but synchronization still matters.
- MLX can execute on different devices and streams. Device/stream decisions
  should be measured on the target workload.

## Audit Questions

- Where is the first forced evaluation in the hot path?
- Is the graph allowed to grow too large before `mx.eval`?
- Are CPU reads, printing, or NumPy conversions forcing sync in loops?
- Is benchmark timing measuring scheduled work or completed work?
- Are model, optimizer, and data arrays using a consistent dtype policy?

## Evidence Required

Use timing, memory telemetry, representative inputs, and correctness checks.
Do not treat static observations as proven performance regressions.
