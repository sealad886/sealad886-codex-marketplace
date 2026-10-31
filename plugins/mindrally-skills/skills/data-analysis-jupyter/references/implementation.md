# Data Analysis and Jupyter Notebook Development: implementation guidance

## Transformations and numeric correctness

Use loc/iloc and explicit join/cardinality checks. Choose imputation/removal from
missingness and analysis requirements; do not silently coerce invalid dates or
outliers away. Track newly missing timestamps after to_datetime(errors="coerce").
Specify timezone and categorical grouping semantics deliberately. Broadcasting and
vectorization need checked shapes/dtypes and can allocate large intermediates.
Guard normalization against zero/invalid standard deviation and avoid fitting
statistics on held-out data. Use a local NumPy Generator, e.g. default_rng(seed),
rather than changing global random state; record version/algorithm limits.

## Scale, notebooks, and reporting

Categorical dtype helps some low-cardinality columns, not all strings. Chunked
reading followed by concatenating every chunk still retains the whole result;
use incremental aggregation/output for memory bounds. Profile before adding Dask
or caching; include source/parameter versions in cache identity. Restart and execute
notebooks in order with the recorded environment; notebook magics are backend
choices rather than universal requirements. Preserve useful non-sensitive executed
results when required and remove confidential outputs before sharing. Plots need
units, readable labels, appropriate uncertainty, accessible encodings, and a
text/table interpretation. Use tests whose assumptions match sampling/dependence;
a plot or p-value alone does not establish a causal conclusion.

## Primary documentation

- [Generator and reproducibility semantics](https://numpy.org/doc/stable/reference/random/).
- [Chunking and memory scaling](https://pandas.pydata.org/docs/user_guide/scale.html).
- [Explicit missing-data treatment](https://pandas.pydata.org/docs/user_guide/missing_data.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
