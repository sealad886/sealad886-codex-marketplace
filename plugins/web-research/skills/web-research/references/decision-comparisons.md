# Decision comparisons

Use when research should distinguish options or support a choice. Start with the
decision and evidence that could change it; a table is useful only if its rows
and columns answer that decision. The optional
[decision matrix](../templates/decision-matrix.md) can hold the evidence.

## Define requirements before scoring

Separate hard constraints from preferences. A hard constraint is a condition
the user requires, such as a supported platform or maximum total cost. A
preference improves fit without automatically excluding an option. Do not turn
your own preference into a hard constraint. Clarify material uncertainty or state
an explicit assumption; keep provisional conclusions conditional on it.

Use the same scope for each option: region, applicable version, availability
date, user group, time horizon, and included services. Identify the feasible
alternatives, including the current approach when relevant. Distinguish an option
failing a requirement from one whose compliance could not be established.

## Build comparable evidence

For each decision-relevant criterion, record:

- The measured or qualitative property and why it matters.
- The unit, denominator, period, conditions, and relevant exclusions.
- Each option's supported value and its direct supporting citation.
- The consulted date/version and material uncertainty or missing evidence.

Normalize only when the conversion is justified and transparent. Monthly and
annual prices need a common period and the same taxes, mandatory fees, minimum
term, currency basis, and usage assumptions. A headline subscription price does
not establish total cost. Benchmark numbers from different workloads do not
become comparable merely because their units match. Use the
[quantitative guide](quantitative-evidence.md) for derived values and estimates.

Put citations in or directly beside material factual cells. One source column
may serve multiple cells only when the mapping is clear and the consulted source
actually supports each value. Mark missing values as **unknown**, with their
decision effect; never fill them with zero, a favorable default, or an invented
estimate. A supported estimate remains an estimate with its basis and range.

## Choose a defensible decision method

Qualitative elimination and dominance are often enough. Eliminate an option only
on an established failure of a hard constraint. Mark an unknown requirement as
unresolved. An option dominates another only on the relevant known criteria,
with no material unknown that could reverse the comparison; otherwise qualify
the claim. Explain tradeoffs directly when different options suit different
priorities.

Use numerical scores or weights only when the user supplied them or when an
explicitly labeled assumption is useful and appropriate to the task. Explain the
scale and direction of each score, how evidence maps to it, and the effect of any
normalization. Weights express priorities; they are not facts discovered in the
sources. Avoid false precision or averaging ordinal labels as if they were
measured quantities. Do not silently renormalize around an unknown cell and make
the option appear better; expose its effect or leave the score unresolved.

## Test what changes the recommendation

Vary plausible unknowns and disputed assumptions, and priorities when relevant.
Report which changes alter the recommendation, the threshold if it can be
justified, and what evidence would resolve the choice. If alternatives remain
indistinguishable, say so; do not manufacture a winning score. Bound sensitivity
work to the decision rather than exploring every imaginable scenario.

For example, suppose two otherwise suitable options are equal on the user's
other criteria. A has a verified annual total of 120 units; B's price is missing.
B is not free or cheaper. The cost comparison remains unresolved. If price alone
decides and the terms are equivalent, B becomes cheaper below 120 units, ties at
120, and costs more above 120. A hard budget of 100 would exclude A but leave B's
eligibility unknown. These are illustrative thresholds, not live product prices.

## Handoff

State the recommendation or unresolved choice, its applicability, decisive
evidence, tradeoffs, and conditions that would change it. Keep preferences and
inference visible. A comparison authorizes neither purchasing nor contacting a
provider, modifying a system, saving a file, or publishing the result; use the
task's existing authority for any such action.
