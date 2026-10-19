# Appraise quantitative evidence

Use when a number, rate, effect, estimate, benchmark, or numerical comparison
materially supports the answer. Preserve what was measured and how it applies;
arithmetic cannot repair incompatible inputs or weak source evidence.

## Recover the meaning before using the number

Read the source's definitions, methods, table notes, and qualifications. Retain:

- Numerator and denominator, unit, and whether the value is a count, proportion,
  rate, average, percentile, ratio, or model estimate.
- Population or workload, eligibility/exclusions, sample size when relevant,
  geography/platform/version, observation period, and time at risk.
- Baseline and comparator, including their conditions and measurement method.
- Reported uncertainty, variability, missing data, rounding, and limitations.
- Whether evidence supports description, association, prediction, or a causal
  effect; a source's causal wording does not by itself prove causality.

A percentage without its base can conceal a small absolute change. Rates with
different follow-up times and averages with different populations may answer
different questions. Check whether the denominator is people, events, tasks,
devices, time, or another exposure. Do not confuse percentage points with percent
change, a hazard/odds ratio with a risk ratio, or one percentile with an average.
If the source does not provide needed context, retain the gap rather than inventing
it. Use specialist guidance or state limits when interpretation exceeds the
available evidence; follow the host's high-stakes research requirements.

## Separate reported values from derived figures

Attribute reported values directly with adjacent citations and their applicable
conditions. Label your derived figures as calculations, show the sourced inputs
and equation, and make conversions and assumptions explicit. In a table, use a
short note or footnote mapping the derived cell to its input citations and
arithmetic. A derived value is not a measurement reported by the source.

For a baseline proportion `b` and comparison proportion `c` measured on a
comparable basis:

```text
absolute reduction = b - c
relative reduction = (b - c) / b   [only when b is nonzero]
percentage-point reduction = 100 × (b - c)   [b and c expressed as proportions]
```

Do not present a relative reduction when the baseline is zero or unavailable.
Check signs and direction: reductions may represent improvement or harm depending
on the outcome. Keep the absolute scale beside a relative effect when it matters
to the decision. Round to precision justified by the inputs and evidence, rather
than displaying every calculator digit.

Illustrative arithmetic: suppose a source reports an observed event proportion
of 2 per 1,000 for one group over one year, and a comparable group has 1 per
1,000 over the same year. The absolute reduction is `2/1,000 - 1/1,000 = 1/1,000`,
or **0.1 percentage points**. The relative reduction is `(2 - 1) / 2 = 50%`.
If only the baseline and a 50% relative reduction were reported, deriving
`2/1,000 × (1 - 0.50) = 1/1,000` requires that the relative figure applies to that
same baseline, population, outcome, and period. Label the result as derived.
Neither example establishes causality, statistical significance, uncertainty, or
applicability to another population or period. These invented inputs illustrate
arithmetic, not a real-world research result.

## Evaluate comparability and uncertainty

Compare like with like, or explain why a conversion or adjustment is justified.
Different definitions, populations, periods, configurations, study designs, or
baseline risks may prevent a direct ranking. Preserve ranges or conflicting
results separately when pooling would conceal these differences. Do not compute
an aggregate across incompatible evidence merely because a formula is available.

Report the source's uncertainty on its own terms and distinguish a confidence
interval, prediction interval, observed range, and scenario assumption. Absence
of an uncertainty estimate is not proof of precision or no uncertainty. Do not
claim a statistical difference from point estimates alone, or infer equivalence
because a difference was not established. A larger sample does not automatically
remove selection bias, measurement error, or an applicability mismatch.

When estimating from uncertain inputs, use a justified range or bounded scenario
and explain how it affects the conclusion. Do not manufacture error bars,
independence assumptions, or a formal meta-analysis. Mark missing quantities
unknown rather than treating them as zero. If the decision depends on them,
identify the missing evidence or threshold using the
[comparison guide](decision-comparisons.md).

## Report what the numbers support

State the result with its unit, population/workload, period, comparator, and
material uncertainty. Distinguish source findings from your calculation and
inference. Explain whether plausible assumptions or evidence gaps could reverse
the recommendation. A transparent numerical summary can remain inconclusive;
do not let numerical presentation imply stronger evidence than was consulted.
