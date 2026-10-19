# Refactor evidence

Use for a multi-slice refactor when a resumable record helps. Omit irrelevant
fields or capture equivalent evidence in the task's existing tracker.

## Target and accepted behavior

- Repository/revision and authorized paths:
- Surviving operation and canonical owner:
- Outputs, errors, ordering, resource/cancellation and consumer contracts:
- Baseline checks and existing failures:
- Unrelated changes preserved:

## Slices and consumers

| Slice/cohort | Old → new path or responsibility | Required proof | State |
| --- | --- | --- | --- |

For state changes, capture consequential reachable states, trigger, observation
point and cleanup obligation. For caller migrations, distinguish direct calls,
resolved aliases/generators, intentional differences and uncertain consumers.

## Verification

| Check | Revision/input scope | Observed result | Limits |
| --- | --- | --- | --- |

- Representative path/ownership improvement:
- Remaining old occurrences and their disposition:
- Repeat-run preview, if the transformation is intended to be idempotent:
- Excluded file/hunk preservation result:
- Independent review scope and outcome, if applicable:
- Residual unknowns and required next decision:

Keep static search, synthetic fixtures, real-input behavior and runtime
measurements distinct. Fewer lines or a clean search are not completion proof.
