# AutoML and Hyperparameter Optimization: implementation guidance

## Search and validation

Use nested evaluation or a held-out test set when estimating selection performance.
Use group-aware or chronological splits for dependent observations, with gaps when
needed. Do not assume any forecasting library chooses a leakage-safe split for
your data. Include preprocessing within a fold-safe pipeline. Sample log-scale
positive parameters where appropriate; integer constraints and conditional model
families still matter. Track seeds, data versions, failures, and actual resources.

## Tool-specific checks

Optuna pruning requires meaningful intermediate reports during work. Reporting
only once after cross_val_score completes does not save that trial's training;
with n_warmup_steps=5, a report at step zero cannot activate that criterion.
Use per-epoch/fold reports with a justified comparable step definition. Ray's
reporting entry point differs across versions; inspect installed Ray Tune/Train
API before wiring an ASHA loop, and define every training function. PyCaret
finalize_model may refit using the internal holdout: evaluate before finalization
or retain an external untouched test set. AutoML leaderboards do not establish
calibration, latency, robustness, fairness, or production acceptance.

## Primary documentation

- [Warmup and intermediate pruning reports](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html).
- [Current Tune reporting API](https://docs.ray.io/en/latest/tune/api/reporters.html).
- [Finalization refit behavior](https://pycaret.readthedocs.io/en/latest/api/classification.html#pycaret.classification.finalize_model).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
