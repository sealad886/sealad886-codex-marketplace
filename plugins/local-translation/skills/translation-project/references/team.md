# Interaction and correction protocol

Professional interaction is an exchange of evidence and decisions, not a chain
of agents approving one another's prose. The PM keeps a single project brief,
assignment map, decision log and release record. The runtime keeps immutable job
inputs, candidates and supported review/query state. Do not create a second job
database in ad hoc scripts.

## Dispatch and capacity

Inspect the host's exposed collaboration APIs and slot limits. In Codex, actual
agent creation, messaging and follow-up calls provide agent IDs; another client
must supply its own equivalent. A plugin cannot add a missing delegation API.
Queue work when slots are scarce. Avoid launching all language models together
without a measured memory/capacity budget. The configured runner owns inference
capacity; plugin installation does not load several models or create fallback.

Give each assignment: role; actor ID; job and locale; current source/reference
digests; exact segment coverage; brief and glossary; permitted data/tool access;
owned output; handoff recipient; query route; and stop conditions. A specialist
must report missing evidence, not invent it. The PM owns state-changing shared
actions. Parallel workers can investigate independent locale issues, but must not
write the same candidate or shared resource at the same time.

## Required conversations

1. **Preparation conference:** engineer reports source coverage; terminologist
   proposes concepts; domain reviewer checks them; PM routes unresolved content
   decisions to the actual owner. Locale translators receive the resulting brief.
2. **Draft handoff:** translator provides candidate digest, self-check findings,
   uncertain segments, terminology decisions and local-tool provenance to reviser.
3. **Revision dialogue:** reviser identifies segment, defect category/severity,
   source evidence and proposed remedy. Translator responds with acceptance and
   correction, or a supported disagreement. Valid alternatives remain alternatives.
4. **Adjudication:** language lead resolves expression/consistency within brief;
   domain reviewer resolves concept evidence; human content owner resolves source
   meaning or new requirements. PM records attribution and broadcasts global answers.
5. **Final-format feedback:** engineer/proofreader reports output defect to linguist
   when wording is involved. Corrected candidates return to source comparison,
   structural validation and current-digest review.
6. **Release conference:** quality lead reports coverage/severity; PM presents the
   exact candidate package to the actual release owner with any remaining limits.

Use direct inter-agent messages when provided by the host. Otherwise PM relays
attributed messages and collects responses. Do not claim direct conversation if
only relay occurred. Never send messages to external people or services without
the required user authorization.

## Bounded dispute handling

Default to two correction rounds per issue, then escalate. Each round adds new
evidence or a concrete revision. Do not ask agents to debate indefinitely or
resolve truth by majority. While a locale is blocked, proceed with unrelated
locales and source preparation. A blocker stays in the query log until its owner
answers or explicitly authorizes a recorded exception.

## Change propagation

Classify each finding as target defect, shared-input defect, valid alternative,
new requirement or unsupported format/tool gap. A target-only repair produces a
new candidate digest and invalidates that target's review. A source, glossary or
brief change produces a replacement job, explicitly superseding the old job in
the project record. Find all affected occurrences and locales; re-review those
derivatives and the resulting final files. Never transplant approval records to
different bytes. Retain evidence of the old decision for investigation.
