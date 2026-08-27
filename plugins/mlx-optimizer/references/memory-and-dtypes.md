# Memory And Dtypes

Use this reference for MLX memory telemetry, cache behavior, dtype policy, and
OOM triage.

## Memory APIs To Check

- `mx.get_active_memory()`
- `mx.get_peak_memory()`
- `mx.get_cache_memory()`
- `mx.set_memory_limit(bytes)`
- `mx.set_cache_limit(bytes)`
- `mx.set_wired_limit(bytes)`
- `mx.clear_cache()`

`mx.set_wired_limit(bytes)` is only useful on macOS 15.0 or higher. Check
`mx.device_info()` for `"max_recommended_working_set_size"` and `"memory_size"`
before changing it. The wired limit should remain strictly below total memory;
setting it above the system wired limit is an error.

## Dtype Policy

- Keep model parameters, activations, and optimizer state dtype choices explicit.
- BF16 is often a good training target on Apple Silicon when supported by the
  workload.
- FP16 can reduce memory but may need numerical checks.
- FP32 is safest for correctness baselines and sensitive reductions.

## OOM Triage Order

1. Reproduce with a small command and record input shape, batch size, dtype, and
   peak memory.
2. Reduce batch residency, prefetch depth, and validation batch size.
3. Remove avoidable graph growth by adding measured evaluation boundaries.
4. Test checkpointing on memory-heavy blocks.
5. Consider cache limits only after confirming graph and batch behavior.
