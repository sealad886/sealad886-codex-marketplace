---
name: matplotlib-best-practices
description: "Use when creating Matplotlib scientific plots, multi-panel figures, accessible visual encodings, or export artifacts."
---

# Matplotlib Best Practices

## When to invoke

Use for creating Matplotlib scientific plots, multi-panel figures, accessible visual encodings, or export artifacts.

## Inputs and evidence

Inspect data/units, scientific question, output dimensions/format, Matplotlib/backend versions, and accessibility/publication requirements. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose an honest plot type and explicit Figure/Axes ownership.
2. Set units, scales, labels, legends and uncertainty encodings appropriate to the question.
3. Choose layout, fonts and export backend for the final artifact.
4. Render and inspect the saved output at intended size; close only figures owned by the operation.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Saved plots are inspected for data accuracy, labels, clipping, color/contrast and required file properties.

## Must not

Do not hide data through downsampling or report publication quality without inspecting the exported artifact. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
