# Quality and acceptance evidence

Agree criteria before production. Distinguish integration correctness, linguistic
quality, product/media behavior and human release authority. Passing one does not
establish the others. The supplied service whitepaper (pp. 15–18, 22) and
architecture proposal recommend those separate controls; neither supplies model
qualification results for this package.

## Required inspection

For each locale, compare the complete commissioned source and target coverage.
Check negation, conditions, modality, actors, sequence, quantities/units, names,
cross-references, omissions and additions. Check terminology by concept and context,
not only substring presence. An unchanged UI label may be intentional; a fluent
translation may still reverse a procedure. Automated literal-number checks can
reject a valid locale rendering and cannot establish numerical meaning; resolve
the discrepancy explicitly rather than deleting the check or waiving it silently.

Use these categories: meaning; omission/addition; terminology; action/instruction;
fluency; locale convention; structure/functional token; final presentation.
Severity follows consequence: a reversed prohibition or destructive-action error
blocks release; a minor style preference is not automatically an error. Distinguish
source defects, target defects, acceptable alternatives and new requirements.

The independent bilingual reviser needs source, target, brief, resources and prior
decisions. A different agent provides a separate AI pass, but may share a model's
systematic errors. Record this limitation. A qualified human's review and any
claimed professional conformity require actual separate evidence.

## Final artifact and product checks

Engineering verifies segment completeness and intended files, current hashes,
encoding and functional-token checks. Any required renderer, layout, reading order,
app procedure, media or player check must inspect the actual final artifact and
declared build/cut. Text checks do not substitute for these checks. Material edits
from later passes return for source comparison and invalidate prior review.

Quality lead records full versus sampled coverage, rubric, findings, adjudication
and remaining limits. Model scores may assist triage; they do not authorize release.
No benchmark or hardware/latency result is implied by model support. Qualify each
actual deployment/pair with representative content, holdout material, adversarial
structure cases and human correction effort before a production claim.

## Delivery gates

`translation_prepare_delivery` checks implemented runtime conditions and emits a
candidate manifest. The PM additionally verifies that all commissioned specialist
work occurred, unresolved material queries are closed by the right owners, and
all evidence names the current files and digests. The actual human release owner
then accepts, rejects, or grants a documented bounded exception. An actor ID,
agent-generated approval or prepared manifest cannot establish that decision.

When reporting completion, separate: tool-tested; model-tested; AI-reviewed;
human-reviewed; final-format/product-tested; human-accepted; and delivered. Claim
only the states supported by evidence. The package does not publish or transmit
delivery candidates on the user's behalf.
