# Profiling And Metal

Use this reference when normal MLX-level optimization is not enough.

## Escalation Order

1. Verify the workload is actually MLX/Metal-backed.
2. Fix obvious synchronization, dtype, batch, and graph-growth issues.
3. Measure active, peak, and cache memory.
4. Use MLX Metal capture APIs for GPU profiling.
5. Consider `mx.fast` primitives, custom Metal kernels, or C++ extensions only
   after profiling identifies a kernel-level bottleneck.

## Metal Capture Prerequisites

- Run with `MTL_CAPTURE_ENABLED=1` for GPU trace capture.
- Start capture with `mx.metal.start_capture(path)`.
- Stop capture with `mx.metal.stop_capture()`.
- Ensure the trace path does not already exist before capture starts.

## Custom Kernel Gate

Recommend custom Metal kernels only when all are true:

- Built-in MLX operations cannot express the operation efficiently.
- Profiling shows the operation is a major runtime or memory bottleneck.
- Correctness tests exist for representative shapes and dtypes.
- The repo can maintain Metal code and native build tooling.
