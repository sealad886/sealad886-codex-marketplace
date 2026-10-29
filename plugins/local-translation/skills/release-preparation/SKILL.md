---
name: release-preparation
description: Prepare exact translation delivery artifacts and an evidence-based release handoff for the human acceptance owner. Use after reviews and corrections, when reconciling current candidates or when an amended deliverable must return for acceptance.
---

# Release Preparation

Read the [shared expert contract](../.shared/references/expert-contract.md).
Acknowledge this skill, actual actor identity, remit, inputs and missing evidence.
Prepare the release decision; the authorized human remains the release owner.

## When to invoke

Use when reviewed translations are ready for delivery-candidate assembly, when a
candidate's evidence is stale, or when corrected outputs need a new release
handoff. You can assess supplied files directly and report absent job evidence.

## Inputs and evidence

- Approved brief, exact target locales/products and named human release authority.
- Current source, configuration, candidate hashes and shared-context revision.
- Translator/reviser identities, assigned review scope, queries and decisions.
- Engineering, final-proofreading, quality and commissioned media-check results.
- Proposed delivery location, filenames, formats and remaining authorized actions.

## Workflow

1. Reconcile requested products with actual files. Check that every locale and
   track has the intended source/version and final format. List absent outputs
   individually; a complete language list is not proof of a complete track matrix.
2. Verify evidence currency. Reviews must identify the current candidate and
   required context; changed source, configuration or resources require a
   replacement job. Follow the [runtime guide](../.shared/references/runtime.md)
   and preserve predecessor history instead of editing stored job state.
3. Review unresolved queries and severity with the quality lead. Distinguish a
   confirmed defect, valid alternative, new requirement and known tool gap.
   A required review or format check that did not run remains missing evidence.
4. Confirm the actual final files received their commissioned checks. For a
   rendered document inspect the exported artifact; for media require the exact
   final cut/audio and applicable playback record. Earlier working-text approval
   cannot substitute for evidence about changed production output.
5. Through the coordinator's serialized mutation route, call
   `translation_prepare_delivery` only when runtime gates pass. Read its returned
   manifest and current status; it is a candidate with human acceptance separate.
   If the runtime cannot represent the commissioned product, report that gap and
   require the appropriate external production evidence rather than fabricating it.
6. Present the exact candidate and a concise acceptance brief to the actual human
   owner: files/hashes, coverage, open limits, decisions needed and proposed next
   action. Record an actual acceptance, rejection or requested amendment with
   attribution, then route approved actions through applicable authorization.

A tool-generated manifest is useful release evidence. It cannot sign the client's
acceptance or authorize publishing files to a destination not approved by the user.

## Outputs and handoff

Use the [expert handoff](../.shared/templates/expert-handoff.md) and shared
[release record](../.shared/templates/release-record.md). Return the current
candidate manifest, exact artifact inventory, evidence matrix, supersession
links, unresolved limits and concrete human decision request.

## Completion evidence

The human can inspect the identified files and understand what was checked and
what remains uncertain. State whether a delivery candidate was prepared and,
separately, whether an actual human decision was received. Retain amendment and
superseded-candidate history.

## Must not

Do not manufacture acceptance, human signatures, certification or publication
readiness. Do not send, publish or overwrite deliverables without the user's
applicable authorization. Do not transfer reviews to different bytes or hide an
absent required check behind a passing aggregate status.
