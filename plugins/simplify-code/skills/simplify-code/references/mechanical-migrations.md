# Migrate repeated callers to the canonical operation

Use after the task has established the surviving API/rule and authorized its
caller scope. A text match supplies candidates, not proof that every occurrence
has the same semantics. This workflow migrates source; it does not authorize
changing user data, persisted formats, installed tools, or repository history.

## Define and preview the cohort

Record the old and new contract: inputs, outputs, defaults, errors, units,
evaluation timing, ownership and caller-specific policy. Identify the canonical
definition and all intended in-scope consumers. Prefer an existing repository
transform when it represents that contract; design a task-local transformation
only when repeated work justifies it. Installing an AST framework is not a
prerequisite.

Classify candidates before applying the change:

| Cohort | Example | Action |
| --- | --- | --- |
| Proven direct use | Import and call resolve to the old API | Migrate after checking the new contract |
| Resolvable variant | Imported alias, qualified call, generated consumer | Trace binding/generator input; migrate when proved |
| Intentional difference | Similar name with different units, timing or policy | Exclude with its concrete reason |
| Uncertain consumer | String registration, reflection, external caller | Inspect canonical registration/consumer or retain and report the gap |

Search exports, command/config routing, registrations and generator inputs as
well as ordinary calls. For generated source, change the canonical generator
input and regenerate using the declared workflow. Do not edit only its output.

Preview the eligible paths and a representative change from each shape. Check
dirty files against the baseline and isolate intended hunks. If a tool can only
rewrite a whole mixed file and preservation cannot be demonstrated, leave that
file intact while completing safe independent cohorts. Do not use reset/restore
as automatic cleanup for an overbroad transformation.

## Pilot, apply, and inspect

1. Apply a small representative slice and run the relevant existing consumer
   checks. Inspect the actual diff for changed evaluation order, error handling,
   imports, resource lifetime and unrelated formatting.
2. Correct the transform or match criteria before broad application. Stop on an
   unhandled shape; do not silently treat a partial rewrite as success.
3. Apply only the approved cohort, with one writer per affected file. Track
   completed and remaining groups when the batch is noticeable. No dependency
   or progress-bar framework is needed.
4. Remove verified obsolete declarations, imports, re-exports and dependencies
   through their callers. Keep externally required boundaries or unresolved
   consumers explicit; do not leave active equivalent copies beside a new helper.

Regex can be sufficient for an unambiguous textual contract. It is insufficient
when syntax, binding or language semantics determine eligibility. Select a tool
based on the actual shapes and repository environment, and inspect its preview
and failure behavior before trusting a batch operation.

## Prove coverage and repeat-run behavior

Run consumer behavior checks at the stable boundaries and search again for the
old API through its relevant exports, registrations and generator inputs. Explain
remaining occurrences as intentional, unsupported or blocked. Zero text matches
alone does not prove consumer coverage.

If the transformation is intended to be repeatable, preview a second run against
the completed candidate. It should propose no additional changes for the same
cohort. Perform that check in a safe copy or dry-run mode; do not repeatedly run
a mutating command just to see whether it stabilizes. Idempotence establishes
repeat-run behavior, not semantic equivalence.

Compare excluded files/hunks to their recorded baseline, inspect the complete
diff, and report actual migrated/retained counts. For a direct-call/alias/dynamic
registration example, migrate the direct call and alias only after binding is
proved; retain/report the registration until its dispatch contract is understood.
The [optional evidence sheet](../templates/refactor-evidence.md) can capture the
cohort and checks without creating another mandatory project artifact.
