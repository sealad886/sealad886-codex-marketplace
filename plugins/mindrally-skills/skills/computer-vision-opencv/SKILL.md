---
name: computer-vision-opencv
description: "Use when building OpenCV image/video processing, feature matching, detection, tracking, or neural vision pipelines."
---

# Computer Vision and OpenCV Development

## When to invoke

Use when building OpenCV image/video processing, feature matching, detection, tracking, or neural vision pipelines. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect image/video formats, dtype/range/color order, model preprocessing, OpenCV build capabilities, devices, and expected outputs. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Validate decoding, geometry, channels, timestamps, and color/range contracts before choosing algorithms.
2. Implement the selected filtering, transformation, matching/detection/tracking, or model path with owned resources.
3. Check known images and malformed inputs, geometric/box conversions, video failure handling, and measured accuracy/performance.

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
