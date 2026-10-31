---
name: blender-python-addon
description: "Use when building Blender bpy operators, panels, properties, registration, or extension packages."
---

# Blender Python Add-on Development

## When to invoke

Use when building Blender bpy operators, panels, properties, registration, or extension packages. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Blender version, extension/add-on format, scene/context/mode, data ownership, and operator side effects. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Choose the target extension format and define context requirements and owned registrations.
2. Implement data/operator/UI boundaries with reversible registration and context-safe mesh/data changes.
3. Test clean-profile install, enable, operators, undo, disable, re-enable, and representative scene behavior.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
