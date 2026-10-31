# Scikit-learn model workflows: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use pipelines/ColumnTransformer to keep fitted preprocessing and feature selection within training folds; never fit on held-out test data.

- Use group-aware or time-aware validation when rows are dependent; random stratified splits are not suitable for every dataset.

- Choose scaling by estimator and data, not a claim that StandardScaler requires normal features. Trees often do not require scaling.

- Use LabelEncoder for target labels where appropriate, not ordinary categorical input features; choose OneHotEncoder/OrdinalEncoder with explicit unknown-category policy.

- Tune thresholds and hyperparameters without repeatedly consulting the final test set; report relevant metrics and a meaningful baseline.

- Bound n_jobs and nested parallelism to the machine and task budget; n_jobs=-1 is not a universal performance improvement.

- Random seeds aid reproducibility but do not eliminate data/version/hardware variation; preserve feature schema and environment metadata.

- Joblib/pickle artifacts can execute code when loaded; use trusted artifacts only and account for sklearn version compatibility.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Preprocessing and feature selection must be fitted only within training boundaries.](https://scikit-learn.org/stable/common_pitfalls.html)
- [Persisted estimators have trust and version compatibility constraints.](https://scikit-learn.org/stable/model_persistence.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
