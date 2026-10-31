---
name: meta-prompt
description: "Use when evaluating AI responses or supplied action traces with evidence-based rubrics and prompt revisions."
---

# Meta-Prompt

## When to invoke

Use for evaluating AI responses or supplied action traces with evidence-based rubrics and prompt revisions.

## Inputs and evidence

Inspect the original task, candidate output, allowed actions, supplied trace/evidence, and evaluation rubric. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define observable correctness/completeness criteria and any required output schema.
2. Compare candidate claims and actions against provided evidence and reliable sources.
3. Report concise findings, calibrated scores if requested, and unresolved evidence.
4. Evaluate prompt revisions against representative cases without inventing tool execution or hidden reasoning.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Every completion judgment is tied to observable criteria and available evidence; evaluation limits are explicit.

## Must not

Do not invent missing trace steps or treat self-reflection as independent verification. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
