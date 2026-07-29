---
name: visual-generation
description: Generate an accessible diagram, chart, illustration, or supported short media item with explicit disclosure, cost and latency controls, and a useful fallback.
license: MIT
metadata:
  short-description: Generate diagrams, charts, and media
---

# Visual Generation

## When to invoke

Use when an original diagram, chart, explanatory illustration, edit, or short
media item communicates the user's intent better than an existing sourced
visual. Invoke directly for explicit generation requests. For inferred needs,
generate low-cost diagrams or charts automatically only when the active
preference permits it; suggest first for images, slides, and video.

## Inputs and evidence

Resolve the concept, factual constraints, intended medium, aspect ratio,
accessibility needs, output location, host tool support, authorization for
writes, provider cost, and latency. Distinguish visual facts that require
sources from creative direction. Confirm referenced images are actually
available before requesting an edit.

## Workflow

1. Choose a deterministic diagram or chart before a generative image when the
   requirement is structural or quantitative.
2. Use an approved host-native generator or renderer. Do not invent a provider
   endpoint, API key, or capability that the current host does not expose.
3. Send only the minimum generation brief needed. Exclude unrelated transcript
   content, personal data, credentials, and private URLs.
4. Require confirmation before paid, slow, high-volume, or video generation
   unless the current request explicitly authorizes that exact operation.
5. For factual charts, retain values, units, dates, and source citations outside
   the image as machine-readable text where practical.
6. Inspect the generated result for correspondence to the brief, legibility,
   misleading labels, obvious artifacts, and unsafe or disallowed content.
7. Label the result `generated`; for mixed sourced/generated work, preserve both
   the source records and generation disclosure.
8. Supply meaningful alt text and a concise explanation of what the viewer
   should notice.
9. On failure or timeout, continue the conversation and fall back to a simpler
   diagram, sourced visual, or textual description.

## Outputs and handoff

Return a normalized generated or mixed visual result with title, relevance,
alt text, a guarded media URL or opaque host-issued `artifact_ref`, generation
disclosure, provider/model only when known, sources for factual inputs, and
warnings. Hand multi-frame work to
`visual-storytelling` and conversational placement to `visual-companion`.

## Completion evidence

The actual artifact is inspected and rendered or linked, generated status is
visible, factual inputs retain citations, and the result satisfies the brief at
the claimed host. A successful provider response without artifact inspection is
not completion.

## Must not

- Present synthetic reconstructions as photographs or documentary evidence.
- Fabricate sources, provider identities, or model names.
- Call a costly provider or create workspace files outside the user's authority.
- Embed credentials, private conversation text, or sensitive metadata in a
  prompt or artifact.
- Claim that a static asset or valid file proves it rendered in a protected UI.
