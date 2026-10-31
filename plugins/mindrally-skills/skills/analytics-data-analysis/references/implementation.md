# Analytics and Data Analysis: implementation guidance

## Cleaning and aggregation

Choose missing-data treatment from the analysis question and missingness mechanism;
median imputation and target-row removal are not universal defaults. Preserve raw
data and record counts before/after every consequential filter. Use explicit dtypes,
`loc`/`iloc`, and join-cardinality validation. Set grouping options such as observed
categories deliberately because defaults differ across pandas versions. Fit learned
preprocessing on training partitions only when analysis feeds a predictive model.

## Plots and notebooks

Use matplotlib axes and seaborn plot types appropriate to distributions and units.
Keep categorical palettes associated with an explicit hue where required by the
installed seaborn version. Include readable axes, accessible color encodings, and
a text/table alternative. Profile before adding distributed data tooling.
Execute notebooks from a clean kernel in order, record data/environment versions
and random seeds, and remove sensitive outputs before sharing. Preserve useful
non-sensitive results when an executed notebook is a deliverable. Explain effect
sizes and interval assumptions; correlation alone does not establish causality.

## Primary documentation

- [Missing-value representations and treatment](https://pandas.pydata.org/docs/user_guide/missing_data.html).
- [Categorical color and hue changes](https://seaborn.pydata.org/whatsnew/v0.13.0.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
