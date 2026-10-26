# Audit method

Use this reference to choose useful evidence, not to create mandatory busywork.

## Surface and hypotheses

| Dimension | Ask | Strong evidence |
| --- | --- | --- |
| Correctness and accuracy | Which invariant can fail silently? What defines a correct result? | Reproduction, independent oracle, representative metric comparison |
| Ownership and concurrency | Who owns mutable state, files, handles, tasks, cancellation, and cleanup? | Lifecycle trace, race reproduction, resource observations |
| Performance and memory | Which path dominates cost, and under which input scale? | Comparable benchmark, profiler/trace, peak and steady-state memory |
| Tests and reproducibility | Which required behavior lacks reliable proof? | Failing public-boundary check, flaky reproduction, explicit coverage gap |
| Contracts and documentation | Do defaults, errors, CLI/API/schema, configuration, and docs agree? | Executed interface, schema checks, source-to-doc comparison |
| Operations | What happens on partial failure, retries, exhaustion, restart, or interruption? | Safe failure injection, recovery test, relevant logs and state |

Choose likely consequential cases. A speculative rare case should not consume
the audit while core behavior remains unchecked. Record useful deferred questions.

## Evidence quality

Direct reproduction, focused tests, benchmark/profile output, source paths, and
inference answer different questions. Prefer reproducible runtime evidence for
runtime claims, but a complete code path can establish a defect even when the
environment cannot run it. Label the limitation rather than discarding the finding.

Bind evidence to a revision/artifact, environment, exact inputs, and result. Tests
from a prior revision are historical until their applicability is re-established.
Record exit status and assertions as well as the command; a command alone is a plan.

For performance, preserve required accuracy and output semantics. Record warmup,
input shape/size, concurrency, repetitions, measurement method, device/runtime,
and relevant noise. A faster synthetic case does not prove real-world throughput.
Avoid universal percentage claims from one uncontrolled run.

## Severity and confidence

- `critical`: demonstrated severe data loss/corruption, exposure, or unusable core path.
- `high`: substantial broken contract, regression, availability, or resource failure.
- `medium`: meaningful bounded defect or reproducible operational deficiency.
- `low`: minor confirmed inconsistency with limited impact.

Severity describes consequence under credible conditions. Confidence describes
evidence strength. A high-impact hypothesis with weak evidence remains a question
to investigate, not automatically a critical finding. Explain prerequisites,
frequency, affected users, and blast radius when they change prioritization.

## Finding quality

Provide one clear claim per finding, with expected/observed behavior, affected
entrypoints, causal path, evidence, consequence, and a proportionate repair/proof.
Group same-root-cause instances without hiding different effects or ownership.
Separate product decisions, absent capabilities, and defects against established
requirements. A preference for another architecture is not itself a defect.

Report a clean assessed slice as "no confirmed findings in this scope" with its
coverage limits. Do not promise that every possible defect was excluded.
