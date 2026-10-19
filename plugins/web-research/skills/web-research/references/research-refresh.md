# Refresh an existing research brief

Use when the user asks what changed, whether earlier advice still applies, or to
update a brief. The previous brief supplies a claim inventory and historical
context; it does not establish current truth. A recent retrieval date on one
source does not revalidate every claim in the document.

## Bound the refresh

Identify the prior document/version, its original scope, and the requested
refresh date, geography, version, and decision. Determine which claims could
affect that decision. Separate factual premises from inference, recommendations,
and background. Reuse stable claim IDs when useful, especially if the brief
already has them. Do not impose a new ledger for a short update; the optional
[claim ledger](../templates/claim-ledger.md) extends an existing claim map.

Record the set to be checked and its boundary. A request to recheck software
version claims does not require silently expanding to unrelated prices, laws,
or historical background. Follow host requirements for any high-stakes or
current claims you do include in the new answer. If a new dependency changes
the decision, recheck that dependency or mark the resulting conclusion unresolved.

## Revisit the supporting evidence

Reopen decision-relevant sources and check their applicable passages. Look for
corrections, replacement documents, later rules/releases, withdrawn findings,
and changed definitions or conditions. Seek current primary evidence as the
claim requires. An unchanged URL or page title is not proof of unchanged content.
Record consulted dates and versions, not only a new document-level timestamp.

For a software upgrade, identify the earlier and target version and use relevant
versioned docs, release notes, and upstream source. A current general guide may
describe a different version from the user's pinned dependency. Preserve the
difference between a cited API claim and a command tested in the user's project.

If the original source is unavailable, record the access failure. An archive may
establish what it said historically; it cannot by itself establish the current
claim. Seek a suitable replacement and cite the source actually read. Without
adequate current evidence, use unresolved status even if the old claim sounds
plausible. Do not convert an access failure into proof that the claim is false.

## Assign a claim-level outcome

| Outcome | Evidence needed and reporting |
| --- | --- |
| Confirmed current | Applicable evidence was consulted and still supports the claim within the checked scope and date. |
| Changed | Current evidence supports a different value, condition, or conclusion. Give the old and new statement and the decision effect. |
| Withdrawn | Evidence shows the claim was retracted or no longer supported; withdraw it from the refreshed conclusion. State the basis, without treating withdrawal as proof of the opposite claim. |
| Unresolved | Access, applicability, conflicting evidence, or insufficient support prevents a current conclusion. State what remains unknown and its decision effect. |

Claims outside the refresh boundary are **not checked**. Keep that coverage label
separate from the four outcomes; do not mark an unchecked claim confirmed current
or silently restate it as current evidence. If an old claim is outside the new
scope, label it as removed from scope rather than pretending a source withdrew it.

Update dependent calculations, comparisons, and recommendations when their
premises change. Preserve supported qualifications and unresolved conflicts.
Report a concise change summary with citations beside the changed or confirmed
claims, the checked scope, and unchecked areas that could matter to the reader.

## Worked scope example

A brief has ten factual claims. Only C03 and C04 concern an API whose pinned
version changed. The requested refresh checks those two against applicable
versioned sources: C03 is confirmed current; C04 changes. Re-evaluate any advice
depending on C04. Report "checked C03 and C04 for the target version; the other
eight factual claims were not revalidated." Do not label the whole brief
"verified current." If C03's only current source cannot be accessed and no
suitable alternative is available, C03 remains unresolved instead.

## Save or deliver within authority

Deliver the scoped result in the conversation unless saving is authorized. When
updating a file, preserve unrelated content, retain useful source/history context,
and follow the task's overwrite or backup instructions. Refreshing a brief does
not enroll the user in recurring monitoring, schedule follow-ups, contact sources,
or authorize publication. Those actions require their own applicable authority.
