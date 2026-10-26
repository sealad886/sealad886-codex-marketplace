# Finding, pattern, and scope decisions

Treat a reported line as an observation point. Before editing, form a falsifiable
claim: which observable invariant fails, under which input/state, and why? Read
the full surrounding flow and relevant tests; reviewer wording is a lead.

1. **Local:** inspect the reported symbol/file, adjacent branches, direct
   callers/callees, ownership and cleanup, and nearby tests.
2. **Regional:** inspect sibling entrypoints/implementations, the feature's
   package/layer, shared helpers, generation, configuration, and adapters.
3. **Global:** search the repository for semantic equivalents, copied patterns,
   other consumers, or a missing central invariant. Include generated outputs
   and dynamic registration where they affect behavior.

Use available indexed code intelligence when ready, confirming index scope and
freshness. Resolve symbols/callers/callees and impact when supported, then read
source. When unavailable or unsuitable, record that limit and use repository
search such as `rg` plus configuration/test inspection. No indexer is required.
Search results, similar syntax, and an empty search do not prove semantics.

Classify credible matches as same root cause, same symptom/different cause,
intentional exception, or unrelated lookalike. Choose the smallest justified
repair owner: isolated code, repeated pattern, shared invariant, architectural
boundary, or a process/generation/test gap. An isolated defect is a conclusion
supported by all three searches, not an assumption from one comment.

Ask whether a reasonable engineer would include this repair in the PR's intended
behavior. Global discovery does not authorize global edits. Fix the common cause
and affected instances only where coherent with scope. Safe local containment
may accompany a linked systemic follow-up, but must not mask the defect,
duplicate policy, or create divergent behavior. Otherwise surface the scope
conflict and continue independent safe work while awaiting direction.

For each cluster, retain reported IDs, invariant/hypothesis, evidence from three
scopes, classified matches, repair boundary, in/out-of-scope decisions, and proof.
Several comments can map to one cluster, but every thread still needs its own
honest reply/disposition. Disagree with incorrect findings using evidence rather
than changing code to appease them. Do not resolve a thread until its actual
request is addressed. No-change, duplicate, obsolete, and follow-up outcomes need
explicit rationale. In read-only modes propose external replies/issues instead
of publishing them.

Verify the repaired invariant at its owner and representative caller paths,
including meaningful failure/boundary cases. Do not write tests that merely pin
the patch's private structure or exact prose. For a procedural cause, verify the
durable guard that should prevent recurrence. Recheck relevant interactions
after the whole cluster is repaired.
