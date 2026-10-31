# Meta-Prompt: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Response evaluation

- Separate accuracy, task completion, relevance, clarity and verbosity rather than letting a fluent answer dominate the score.
- found_solution can be true only when the required evidence and actions are complete; confidence or a numeric score alone is insufficient.
- Define scoring anchors and evaluate repeated cases; uncalibrated 0–10 self-scores are not objective quality measurements.

## Trace analysis and prompting

- Analyze only the supplied observations, actions and visible justifications; do not request or fabricate private chain-of-thought.
- Search/Lookup/Finish labels are examples from a trace format, not tools made available by this skill.
- Use concise outcome rationales, few-shot examples and explicit constraints when they help; self-consistency can repeat shared errors.
- Compare prompt changes on held-out cases and record failure examples, evaluator limits and any human adjudication.

## Primary documentation

- [Primary documentation](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Evaluations should use task-specific criteria, representative datasets and calibrated feedback.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
