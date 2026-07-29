---
name: visual-storytelling
description: Turn a conversation into a concise, coherent, cited sequence of slides or media frames without sacrificing the spoken or textual explanation.
license: MIT
metadata:
  short-description: Create visual stories and short slide sequences
---

# Visual Storytelling

## When to invoke

Use when the user asks for slides, a storyboard, a visual walkthrough, a
before-and-after sequence, or a short clip, or when several ordered frames are
materially clearer than one image. Do not invoke merely to make a response look
more polished.

## Inputs and evidence

Resolve the audience, purpose, frame count, duration, presentation format,
brand/accessibility constraints, factual sources, host rendering/export
capabilities, and authorization for file writes or costly generation. Preserve
the user's conversational objective rather than turning the exchange into an
unrequested formal deck.

## Workflow

1. Define one communicative purpose and a short narrative arc.
2. Default to three to five frames unless the user requests otherwise: context,
   core explanation, and implication or next step.
3. Keep each frame readable at conversation scale. Use concise labels and one
   dominant visual idea rather than paragraphs of prose.
4. Source existing evidence with `visual-research`; create original explanatory
   media with `visual-generation`. Keep factual citations attached to the frame
   or accompanying text they support.
5. Use presentation tooling only when the host exposes it. Otherwise return an
   inline sequence or storyboard rather than claiming a deck was created.
6. Suggest first before video. State intended duration, purpose, latency, and
   possible cost, then wait for confirmation unless video was explicit in the
   current request.
7. Inspect ordering, visual continuity, typography, citations, alt text, and
   generated-media disclosures.
8. Continue to provide a concise spoken or textual explanation so the result is
   useful when visuals are unavailable, minimized, or unseen.

## Outputs and handoff

Return an inline sequence, slide artifact, storyboard, or supported short clip
plus a concise narrative summary. Each frame has a purpose, accessible
description, provenance, and citations or generation disclosure as applicable.
Hand final placement and host-limit messaging to `visual-companion`.

## Completion evidence

The sequence is rendered or its artifact opens, the order communicates the
intended arc, text is legible, sources resolve, generated media is disclosed,
and the nonvisual summary remains intelligible. File existence alone does not
prove visual quality or UI rendering.

## Must not

- Generate a long deck or video when a single image or diagram suffices.
- Pin incidental wording or layout as a compatibility contract.
- Hide attribution, omit synthetic-media labels, or cite one source for claims
  it does not support.
- Publish, upload, or share an artifact externally without explicit authority.
- Claim native voice playback or synchronized visual timing without direct host
  support and runtime evidence.
