# Training Patterns

Use this reference for MLX training loops.

## Required Review Points

- `nn.value_and_grad` versus `mlx.core.value_and_grad` namespace and placement.
- Optimizer update path.
- Gradient accumulation semantics.
- Validation cadence and synchronization.
- Checkpoint write cadence.
- Dataloader worker, prefetch, and queue depth.
- Progress reporting with ETA for dataset/file loops.
- Memory telemetry at meaningful intervals.

## Verification Command Shape

Use one short smoke run and one representative benchmark run:

```bash
.venv/bin/python -m pytest tests/path/test_training.py -q
.venv/bin/python scripts/benchmark_training.py --steps 50 --batch-size 4
```

If the repo does not use pytest, run the repo's existing test command instead.
Report the exact command, exit code, and key output.
