# Evaluation And Synchronization

Use this reference for `mx.eval`, `mx.async_eval`, `.item()`, printing, NumPy
conversion, and benchmark timing.

## Rules

- `mx.eval` is a synchronization boundary. Place it intentionally.
- `.item()`, `.tolist()`, NumPy conversion, and printing values can force CPU
  reads. Inside hot loops they often dominate runtime.
- A benchmark must warm up, run the workload, then force completion before
  stopping the timer.
- Too little evaluation can build large graphs and increase memory pressure.
- Too much evaluation can serialize work and hide MLX scheduling benefits.

## Suspicious Patterns

```python
for batch in batches:
    loss = step(batch)
    print(loss.item())
```

Prefer collecting periodic scalar metrics outside the hottest part of the loop:

```python
for step_index, batch in enumerate(batches):
    loss = step(batch)
    if step_index % log_every == 0:
        mx.eval(loss)
        print(float(loss.item()))
```

## Verification

Record before/after wall time, correctness result, active memory, peak memory,
cache memory when available, input shape, batch size, and MLX version.
