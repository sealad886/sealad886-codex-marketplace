---
name: bilingual-revision
description: Independently compare source and target meaning, completeness and suitability against the commissioned brief. Use for bilingual reviser assignments, review of corrected candidates, source-to-target issue adjudication, and current-digest AI revision records.
---

# Independent Bilingual Revision

Own a source-comparison pass separate from the original translator's work.
A coherent target is evidence of fluency, not evidence that meaning was preserved.
Read the [shared expert contract](../.shared/references/expert-contract.md) and
acknowledge this skill, independence, coverage and evidence gaps before reviewing.

## When to invoke

Use after a candidate exists, after material wording changes, and after shared
query decisions invalidate prior context. Do not use a target-only subject review
or proofreading result as a substitute for this bilingual remit.

## Inputs and evidence

- Complete assigned source and candidate, exact language direction and target locale.
- Brief, approved resources, adaptation rights, prior queries and decisions.
- Actual translator and reviser identities, candidate digest and context revision.
- Required full or sampled coverage, risk priorities and agreed issue rubric.

Read the [runtime guide](../.shared/references/runtime.md) for recording a verdict.
If you authored the assigned material, request a different actual reviser agent.
A fresh actor label inside the same authoring agent does not create independence.

## Workflow

For Index-family work, read the
[common model-input guide](../.shared/references/index-inputs.md) and selected
profile reference before assessing model-input compliance. Inspect the actual
submitted messages or workbench inputs, approved terminology/requirements and
owner-answer timing. Check meaning and actual constraint adherence rather than
assuming a requested condition was applied. A later answer cannot change an
earlier prompt, and caller-managed output has no workbench approval status.
For that route, inspect the actual source, submitted prompt, response and approved
decision identities in place of a workbench job/context revision; retain an
attributed independent report without inventing a runtime receipt.

### 1. Establish reviewable identity and coverage

Confirm that the provided source, candidate and references are the versions named
in the assignment. Read full review context, including current shared decisions,
through permitted channels. Retain the context revision you inspected. Identify
missing units, inaccessible references or unsupported language judgments before
stating a coverage claim. Do not turn an agreed sample into a full-review claim.

### 2. Compare propositions and use conditions

For every commissioned unit, compare source and target for omissions/additions,
negation, modality, actor, action, conditions, exceptions, chronology, quantities,
units, names and cross-references. Examine headings, labels and reused segments
as well as prose. Check terminology by concept, then register, idiom and locale.
Separate functional-token findings from meaning findings; passing structural
checks does not establish semantic correspondence.

For example, a candidate that changes “only after review” to “before review”
changes the permitted sequence even when every name and number is preserved.

### 3. Present actionable findings and invite replies

Each finding names its stable location, category, consequence-based severity,
source/brief evidence and proposed remedy. Distinguish target error, source defect,
valid alternative and new requirement. Ask the translator for a correction or a
reasoned disagreement. Avoid unnecessary rewriting of acceptable target wording.
Route concept disputes to terminology/subject experts and source intent to its
actual owner through the coordinator. Record attribution and scope of resolution.

### 4. Recheck corrections and submit a current verdict

Inspect changed text and affected occurrences, not just the translator's statement
that the issue is fixed. If a correction or shared answer changed the candidate
or context, reacquire the actual current review materials and repeat affected
checks. Preserve the old evidence as historical; do not transplant its verdict.

For an existing workbench job, when authorized to record the runtime review in a serialized writing slot, use
`translation_review` with `target_sha256` set to the current target digest, the observed reviser identity,
and `expected_context_revision` equal to the revision actually inspected. Use
`changes_requested` or `blocked` when justified; approve only completed assigned
coverage without unresolved material findings. Otherwise return the proposed
verdict and evidence for the coordinator to record with accurate attribution.
A sample or partial assignment cannot justify a blanket `approved` verdict for
the whole locale; return the scoped report and request the remaining required
comparison before that verdict is recorded.

## Outputs and handoff

Use the [expert handoff](../.shared/templates/expert-handoff.md). Return identities,
coverage, categorized findings, translator replies, adjudications, recheck evidence,
unresolved queries and a verdict bounded to the actual candidate/context. State
that a distinct agent pass is AI revision and identify correlated-model limitations.

## Completion evidence

Your actual identity differs from the candidate authors. Findings and responses
are traceable; material issues are resolved or explicitly blocking. Review evidence
names the current candidate and inspected context, and its claimed coverage matches
the work performed. A recorded AI approval is separate from human acceptance.

## Must not

Do not self-revise under a renamed role, approve without source access, infer
accuracy from fluency, impose preferences as errors, invent translator replies,
or reuse a verdict after context/text changes. Do not claim qualified human
revision, certification or release authority from a separate agent identity.
