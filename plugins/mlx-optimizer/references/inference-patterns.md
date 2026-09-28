# Inference Patterns

Use this reference for MLX inference, generation, and serving loops.

## Review Points

- Warmup before timing.
- Batch size and prompt/input shape.
- KV-cache or recurrent-state growth.
- Quantized model loading and dtype consistency.
- Streaming output synchronization.
- Scalar extraction inside token or frame loops.
- Long-running memory growth and cache behavior.

## Benchmark Rules

- Time representative input sizes.
- Force completion before stopping the timer.
- Separate first-token or first-output latency from steady-state throughput.
- Record correctness or output-equivalence criteria.
- Report MLX version, hardware, Python executable, and memory telemetry.
