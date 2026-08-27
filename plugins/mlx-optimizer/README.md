# MLX Optimizer

`mlx-optimizer` helps Codex audit, benchmark, and optimize Python-first
[MLX](https://github.com/ml-explore/mlx) projects on Apple Silicon. It combines
six progressively disclosed skills with focused MLX references, conservative
static-analysis scripts, and before/after verification templates.

Static findings remain candidates until representative workload evidence proves
them. The plugin never installs Python globally, treats lazy evaluation and
synchronization as correctness concerns, and requires concrete timing, memory,
and output evidence for optimization claims.

## Install

```bash
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add mlx-optimizer@sealad886-codex-marketplace
```

Start a fresh Codex task after installation so the current skill catalog loads.

## Skills

| Skill | Purpose |
|---|---|
| `mlx-optimizer` | Route MLX audit, optimization, profiling, benchmark, and explanation work. |
| `mlx-performance-audit` | Review a repository for unknown MLX bottlenecks and invalid measurements. |
| `mlx-training-optimizer` | Improve training loops, optimizer state, accumulation, checkpointing, dtype policy, and validation cadence. |
| `mlx-inference-optimizer` | Improve generation, batching, caches, quantization, streaming, latency, and throughput. |
| `mlx-metal-kernels` | Escalate to Metal capture, `mx.fast`, custom kernels, or C++ extensions when profiling justifies it. |
| `mlx-portability-bridges` | Design Swift, C, C++, service, subprocess, C ABI, and Core ML boundaries. |

Example prompts:

```text
Audit this repository for MLX performance issues.
Optimize this MLX training loop and verify it with a representative smoke run.
Check whether this benchmark times scheduled MLX work or completed work.
Decide whether this bottleneck justifies a custom Metal kernel.
```

## Included tools

- `scripts/mlx_audit.py` scans Python sources for candidate synchronization,
  evaluation, and benchmark-boundary problems without modifying target code.
- `scripts/mlx_env_probe.py` reports repository-local Python, MLX, Metal,
  device, and memory-API evidence.
- `scripts/mlx_benchmark_template.py` supplies warmup, synchronization,
  correctness, memory, repeated-run, JSON, and progress-reporting hooks.

Run scripts through the target repository's `.venv` Python. For example:

```bash
.venv/bin/python /path/to/mlx_audit.py . --format markdown
.venv/bin/python /path/to/mlx_env_probe.py . --format json
.venv/bin/python /path/to/mlx_benchmark_template.py --runs 5 --warmup 2 --format json
```

## Package boundary

```text
mlx-optimizer/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── .cursor-plugin/plugin.json
├── references/
├── scripts/
├── skills/
└── templates/
```

The Codex manifest is canonical for this marketplace. Claude Code and Cursor
compatibility manifests remain packaged for consumers that materialize the same
plugin subtree through those hosts; their marketplace registration is outside
this repository's Codex publication contract.

## Verification

From the marketplace repository root:

```bash
python3 scripts/check_plugin.py plugins/mlx-optimizer --layout source
python3 scripts/check_distribution_bundle.py plugins/mlx-optimizer
python3 -m unittest tests.test_mlx_optimizer -v
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/mlx-optimizer
```

The script tests do not require MLX. Native MLX optimization claims still
require an Apple Silicon host with the target project's actual MLX environment.

## Security and support

The scripts inspect user-selected repositories and write only requested report
outputs. Review generated advice before applying it, preserve unrelated work,
and never expose secrets in reports. Report vulnerabilities through GitHub
Security Advisories; see [SECURITY.md](SECURITY.md). General support guidance is
in the marketplace [support guide](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/SUPPORT.md).

## License

MIT. See [LICENSE](LICENSE).
