---
name: locale-translation
description: Draft and self-check a translation for an assigned language direction and locale, using local Index-Translate tools when configured. Use for locale translator or audiovisual translator assignments, correction replies, terminology research, and source-meaning queries.
---

# Locale Translation

Own target wording proposals for the assigned locale and coverage. Work from the
approved meaning, audience and resources; fluent output still needs source checks.
Read the [shared expert contract](../.shared/references/expert-contract.md) and
acknowledge this skill, your language direction, scope and evidence gaps first.

## When to invoke

Use for drafting, translator self-check, response to reviser findings and approved
corrections. For audiovisual work, use verified scene/transcript context and the
commissioned constraints; this skill does not supply recording or timing tools.

## Inputs and evidence

- Exact source revision and units, source language, target locale and audience.
- Brief, adaptation rights, approved terminology, style and contextual references.
- Job and actual actor identity, assigned units, previous decisions and query route.
- Local runner health, deployment/pair qualification and authorized tool access.
- For corrections: candidate digest, findings and current shared-context revision.

Read the [runtime guide](../.shared/references/runtime.md) before tool use. Confirm
that source/target disclosure to your host provider is permitted before reading it.

## Workflow

### 1. Interpret before drafting

Read the complete assigned source in context. Identify propositions, responsible
actors, actions, conditions, exceptions, modality and chronology. Resolve ordinary
terms from approved references before escalating. Distinguish a concept from a
source spelling: different senses may require different target equivalents.

Record material source ambiguities with stable locations, plausible readings,
evidence and the decision needed. Send these through the coordinator/content
liaison; do not record your preferred interpretation as the client's answer.

### 2. Produce the declared draft

For the local-tool route, require a successful health check and an existing frozen
job. Call `translation_run` for your assigned locale and observed actor identity
only in the coordinator's serialized writing slot. Keep its candidate digest,
context revision, served-model/configuration identity and visible failures. Inspect
the `content` and `segments` returned through MCP; a temporary path is not the
candidate handoff. Do not substitute an invented completion if the configured
runner cannot produce a draft.

When directly assigned an existing candidate, identify it as supplied and work
within that remit. A different drafting route needs explicit commissioning.
For AV adaptation, propose compression that preserves required meaning and note
tradeoffs; do not invent timecodes or call dialogue-only text an accessibility track.

### 3. Perform a source-led self-check

Compare every assigned unit, including reused or exact-match material. Check
negation, obligations/permissions, conditional scope, actor, sequence, numbers,
units, names, links and omissions/additions. Then examine terminology in context,
register, idiom and locale conventions. Check protected spans separately from
linguistic meaning. Do not waive a numeric invariant silently to fit local notation.

For example, “Do not close the valve until pressure is zero” must retain both
the prohibition and the condition; natural phrasing alone cannot establish that.

### 4. Respond to independent findings

For each reviser issue, accept and propose a correction, supply evidence for a
reasoned disagreement, or identify a new requirement/valid alternative. Discuss
concept disputes with terminology and subject specialists. Escalate source intent
to the actual owner. Follow the shared correction-round limit rather than debating
indefinitely. Apply authorized replacements through `translation_apply_revision`
with the current `expected_target_sha256` in a serialized slot; return the new identity.

## Outputs and handoff

Use the [expert handoff](../.shared/templates/expert-handoff.md). Return candidate
identity and coverage, self-check results, terminology choices, uncertainties,
query references and responses to each finding. Give the independent reviser the
source, brief, candidate and current context revision through permitted channels.

## Completion evidence

The declared draft exists or its failure is explicit. All assigned units received
a documented self-check. Corrections are linked to findings and current artifact
identity; unresolved meaning is visible. A distinct actual agent performs any
commissioned independent revision after your handoff.

## Must not

Do not change source facts or adaptation rights, manufacture local-tool output,
self-approve independent revision, treat model identity as language qualification,
force one equivalent across different concepts, or claim human acceptance. Your
self-check and an independent bilingual revision remain separate work products.
