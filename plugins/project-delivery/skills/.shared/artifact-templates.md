# Artifact templates

Use only the sections proportional to the work. Update existing canonical artifacts instead of duplicating them.

## Project brief

```markdown
# Project brief: <outcome>
Status/owner/date:
## Problem and desired outcome
## User and business value
## Scope / non-scope
## Existing context (with evidence)
## Constraints
## Confirmed facts / user requirements / assumptions / agent decisions
## Risks / open questions
## Success measures
## Definition of Ready / Definition of Done
```

## Requirements and traceability

```markdown
| ID | Requirement | Rationale/source | Priority | Acceptance criteria | Status |
|---|---|---|---|---|---|
| REQ-001 | ... | ... | Must | AC-001, AC-002 | proposed |

### AC-001: <observable behavior>
Given <state>, when <event>, then <outcome>.
Evidence method: <test/inspection/metric>
Edge cases: <boundaries/failures>

| Requirement | Design/decision | Risk/response | Work/PR | Test/finding | Release disposition |
|---|---|---|---|---|---|
```

## Solution design / ADR

```markdown
# Design: <change>
## Current state and constraints
## Proposed state and responsibilities
## Interfaces, data, failure contracts
## Alternatives and tradeoffs (including no change when meaningful)
## Compatibility, migration, rollback
## Security, privacy, reliability, observability
## Test and release implications
## Decisions / assumptions / open questions

# ADR-NNNN: <decision>
Status: Proposed | Accepted | Superseded | Rejected
Context / Decision / Alternatives / Consequences / Revisit triggers / References
```

## Delivery plan, RAID, and status

```markdown
| WI | Outcome | Depends on | Owner | Estimate/confidence | Evidence gate | PR/release |
|---|---|---|---|---|---|---|
| WI-001 | ... | ... | unassigned | M / medium | TEST-001 | PR-1 |

Milestones: MS-001 ...
Critical path: WI-... → WI-...
Incremental value/rollback boundaries: ...

| ID | Type | Description | Probability/impact | Owner | Response/trigger | State | Trace links |
|---|---|---|---|---|---|---|---|

Status: Green | Amber | Red
Completed / In progress / Next / Evidence / RAID changes / Decisions needed
```

## Test strategy and evidence

```markdown
| Test ID | Risk/requirement | Level/type | Environment/data | Command or method | Expected | Result/evidence |
|---|---|---|---|---|---|---|
Failures and triage:
Impact / affected requirements and gates:
Response constraints and invariant to restore:
Viable responses / tradeoffs:
Recommended response and next action / owner / authority:
Not run and reason:
Residual gaps:
```

For CI/runtime evidence add: first causal job/step; category; same-revision rerun; retry rationale; focused scenario; revision/device/runtime/build; fresh artifact; baseline/result; limitations.

## Review report

```markdown
Overall decision: approve | approve with residual risk | changes required | blocked
Scope/base/head/environment:
| ID | Severity | Priority | Location | Evidence | Impact | Solution options / tradeoffs | Recommended response / next action | Blocks release? |
|---|---|---|---|---|---|---|---|---|
Assessment mode/snapshot/reviewed surfaces/exclusions/deferred/coverage:
Candidate proof (source → control → sink → reachable boundary), counterevidence, proof gaps, affected-location roles, and disposition:
Response constraints and invariant to restore; owner or authority needed:
Closure record for suppressed/duplicate/not-reproducible candidates: category, rationale, counterevidence, sibling checks, reviewer/date, revalidation trigger, release treatment, residual uncertainty, canonical finding if duplicate:
Residual risks and accepted-by:
Positive evidence (brief):
```

## Release plan and evidence

```markdown
Change set/version/target and provider capability:
Release unit (commit, artifact/deployment ID or digest, provenance, promotion history):
Environment identity (account/project/service/region/config; never secret values):
Required checks and approvals:
Trace disposition for REQ/AC, RISK, DEC/ADR, TEST, and FIND records:
Preview environment (revision, isolation, parity gaps, TTL/cost, teardown):
Feature flags (key/provider/default/failure behavior/cohorts/owner/ramp/metric/guardrail/kill/expiry/removal):
Config/data migrations, compatibility window, restore evidence:
Deployment state (build → predeploy → capacity → readiness → traffic/ramp → drain → observe) and stop conditions:
Rollback trigger, owner, tested procedure, and data/config limitation:
Monitoring/alerts/support/runbook and telemetry classification/redaction:
Post-release source/query/metric, release marker, baseline, threshold, window, observed result, decision:
Actual results, timestamps, revision/artifact IDs:
Incidents/hotfix/follow-up:
```

## Delivery coordination

```markdown
Source-of-truth map: artifact/field | canonical system + ID/URL | owner | as-of | derived copies | conflict
System inventory: provider | workspace/project | capability | authorization | limitation
Mapping: internal ID | external provider/ID/URL | native status | normalized status | last verified
Sync ledger: proposed action | exact target | authority | result | readback | residual divergence
Meeting brief/record: objective | evidence/pre-read | decisions (confirmed only) | actions/owner/date provenance | unresolved
Communication: audience | channel/recipient | purpose | draft/authorized-to-send | source facts | result
Write receipt: provider | target | actor | timestamp | changed fields | prior/new state | ID/URL | verification
```

## Plugin recovery record

Keep consumer-specific paths and state in the consumer's canonical private artifact. Never record secret values.

```markdown
Identity and display name:
Canonical selector:
Owning control plane:
Pre-action installed and enabled state:
Configured source and immutable source identity:
Marketplace identity and immutable revision:
Cache identity:
Manifest SHA-256:
Payload SHA-256 and deterministic hashing method:
Configuration locations (names/paths only; no secret values):
Supported temporary-disable method:
Supported uninstall method:
Supported reinstall/recovery method and exact version behavior:
Pre-action readback:
Action performed:
Post-action readback:
Fresh-task verification:
Recovery drill result: pass | fail | blocked | not run
Limitations and unresolved control-plane gaps:
Owner and timestamp:
```

## Live semantic route receipt

```markdown
Scenario/prompt:
Plugin source version and commit:
Installed plugin/cache identity:
Task/model identity and timestamp:
Repository revision and relevant instructions:
Discovery evidence: packaged files / Skills UI / initial task list / explicitly loaded specialists
Observation scope and effects performed:
Semantic freeze declaration, complete field scope, evidence, and annotation provenance:
Lead capability and actual route (present activated/applied capabilities only; omit `planned-future` branches):
Required capabilities and dispositions:
Conditional capabilities: trigger / activated | not-applicable | deferred | blocked | planned-future / evidence and rationale
Gate precedence, controller re-entry, and final decision after selected evidence:
Loaded specialist source paths:
Justified extra capabilities:
Scale/risk/authority taxonomy rationale and evidence:
Expected / produced artifacts:
Authority classification and actions refused or deferred:
Legacy dependency check: administrative visibility / invocation / runtime or hook start / branded state
Commands/evidence and actual results:
Route outcome: pass | fail | blocked | insufficient receipt
Delivery outcome: pass | fail | blocked | not run
Residual gaps:
```

Semantic route-policy validation checks required owners, evidence-bearing taxonomy and conditional dispositions, entry precedence, two-sided occurrence-aware controller entry/return, route-only authority, specialist loading, justified extras, and forbidden dependencies. It intentionally allows justified proportional specialists and equivalent unconstrained evidence-owner ordering. A fresh behavioral receipt must declare and evidence that its route, taxonomy and rationale, branch dispositions, extra-capability decisions, evidence, and gaps were all frozen before contract comparison. Post-hoc semantic annotations can establish only historical route-shape compatibility. Record retrospective learning as `planned-future` and omit it from the present route when its outcome trigger has not occurred; that is not present activation. The route-policy checker accepts only no-effect observations with delivery marked not run; delivery artifacts and execution evidence require a separate delivery receipt and review.

The orchestrator selects common intent semantics from installed [`route-profiles-v1.json`](route-profiles-v1.json). Maintainer-only canary contracts add blind prompt text and must remain in validator-enforced parity with those profiles; a route task uses the installed profiles and does not inspect repository-only expected-contract data.

### Machine-comparable route receipt

Use schema v3 for a fresh machine-comparable route observation. The exact closed schema is [`live-route-receipt-v3.schema.json`](live-route-receipt-v3.schema.json); do not invent fields, shorten names, or use the deprecated schema-v2 self-attestation as candidate evidence. Placeholder strings below are deliberately invalid and must be replaced with inspected evidence.

Fresh canary evidence has three separately owned records:

1. Before task creation, the coordinator generates and seals the one canonical blind task prompt from the prompt-only manifest, public receipt slug, installed identity, and projectless/no-effect rules. The blind route task returns one schema-v3 observation without opening the expected contract. The coordinator preserves its exact raw bytes before comparison.
2. The coordinator—not the route task—records task freshness, prompt-manifest and canonical task-prompt identities, exact source/prepared/cache identity, projectless instruction boundaries, the raw-byte SHA-256, and a private task-binding digest. The private binding includes the exact task-prompt hash. The public record contains no task, thread, host, session, absolute home, or secret identifier.
3. An independent grader compares the captured observation with the expected contract and records the raw-observation, coordinator-attestation, contract, and checker digests. A failed observation is preserved; no semantic field is edited into a pass.

The route task's freeze declaration and instruction-closure state remain structured behavioral self-report. File hashes prove inspected byte identity, not model attention. The coordinator's before/after evidence bounds observable local effects; it cannot prove that an unobservable external call never occurred. State those limitations instead of overstating proof.

`source_observation_sha256` is a deterministic semantic-envelope digest, separate from the coordinator's exact raw-byte digest. Compute it over every schema-v3 top-level field except `task_identity`, using UTF-8 JSON with recursively sorted keys, compact separators, direct Unicode, and no trailing newline. Finalize every included field first, compute and insert the digest only after the three blind partitions have been merged, then independently recompute it from the completed object while again excluding all of `task_identity`. Do not revise an included field after hashing; if any field changes, discard the old digest and repeat both computations. Identity fields may be supplied by the coordinator in the sealed task prompt before launch or mechanically enriched before capture, but every scenario, observation, instruction-closure, and route-semantic value must be frozen before contract access.

```json
{
  "schema_version": 3,
  "contract_schema_version": 3,
  "evidence_class": "fresh-task semantic route observation",
  "semantic_fields_were_frozen_before_contract_comparison": true,
  "semantic_freeze_scope": [
    "actual_route",
    "authority",
    "conditional_dispositions",
    "evidence",
    "extra_capability_justifications",
    "gaps",
    "outcome_observation",
    "risk",
    "scale",
    "scenario_observation",
    "taxonomy_evidence",
    "taxonomy_rationale"
  ],
  "semantic_freeze_evidence": [
    "Describe the blind-task merge and semantic-envelope hashing boundary before expected-contract access."
  ],
  "annotation_provenance": {
    "semantic_fields_origin": "blind-before-contract-comparison",
    "contract_access": "after-capture-only",
    "post_freeze_enrichment_fields": [
      "plugin_identity",
      "repository_identity",
      "task_identity.public_receipt_id",
      "task_identity.selected_at",
      "task_identity.source_observation_sha256"
    ],
    "semantic_fields_revised_after_comparison": false
  },
  "plugin_identity": {
    "name": "project-delivery",
    "installed_version": "REPLACE_WITH_ACTUAL_INSTALLED_VERSION",
    "source_revision": "REPLACE_WITH_7_TO_64_LOWERCASE_HEX_REVISION",
    "manifest_sha256": "REPLACE_WITH_64_LOWERCASE_HEX_SHA256",
    "payload_sha256": "REPLACE_WITH_64_LOWERCASE_HEX_SHA256",
    "payload_hash_method": "project-delivery length-prefixed path-and-content sha256 v1",
    "cache_relative_path": "plugins/cache/personal/project-delivery/REPLACE_WITH_VERSION"
  },
  "task_identity": {
    "public_receipt_id": "REPLACE_WITH_NONSECRET_STABLE_RECEIPT_ID",
    "selected_at": "REPLACE_WITH_ISO_8601_TIMESTAMP",
    "source_observation_sha256": "REPLACE_WITH_64_LOWERCASE_HEX_SHA256"
  },
  "repository_identity": {
    "name": "REPLACE_WITH_REPOSITORY_OR_PROJECTLESS_SCOPE",
    "revision": "REPLACE_WITH_REVISION_OR_NOT_APPLICABLE",
    "working_tree_state": "REPLACE_WITH_INSPECTED_STATE_OR_NO_REPOSITORY_IN_SCOPE",
    "instructions_evidence": "REPLACE_WITH_APPLICABLE_INSTRUCTION_EVIDENCE"
  },
  "observation_scope": "route-only-no-effects",
  "effects_performed": [],
  "legacy_administrative_visibility": [],
  "legacy_invocations": [],
  "legacy_runtime_events": [],
  "legacy_branded_state_created": [],
  "loaded_specialists": [
    {
      "skill": "delivery-orchestrator",
      "relative_path": "skills/delivery-orchestrator/SKILL.md",
      "state": "loaded",
      "skill_sha256": "REPLACE_WITH_SHA256_OF_THE_INSTALLED_SKILL_MD",
      "instruction_closure": {
        "state": "complete",
        "files": [
          {
            "relative_path": "skills/delivery-orchestrator/SKILL.md",
            "role": "skill-root",
            "sha256": "REPLACE_WITH_64_LOWERCASE_HEX_SHA256",
            "state": "read-completely-before-route-freeze"
          },
          {
            "relative_path": "skills/.shared/operating-model.md",
            "role": "required-reference",
            "sha256": "REPLACE_WITH_64_LOWERCASE_HEX_SHA256",
            "state": "read-completely-before-route-freeze"
          },
          {
            "relative_path": "skills/.shared/route-profiles-v1.json",
            "role": "required-reference",
            "sha256": "REPLACE_WITH_64_LOWERCASE_HEX_SHA256",
            "state": "read-completely-before-route-freeze"
          },
          {
            "relative_path": "skills/.shared/artifact-templates.md",
            "role": "required-reference",
            "sha256": "REPLACE_WITH_64_LOWERCASE_HEX_SHA256",
            "state": "read-completely-before-route-freeze"
          },
          {
            "relative_path": "skills/.shared/live-route-receipt-v3.schema.json",
            "role": "required-reference",
            "sha256": "REPLACE_WITH_64_LOWERCASE_HEX_SHA256",
            "state": "read-completely-before-route-freeze"
          }
        ],
        "unresolved_references": []
      }
    }
  ],
  "scenarios": [
    {
      "id": "REPLACE_WITH_SCENARIO_ID",
      "prompt": "REPLACE_WITH_THE_EXACT_BLIND_PROMPT",
      "scale": "REPLACE_WITH_NORMALIZED_SCALE",
      "risk": "REPLACE_WITH_NORMALIZED_RISK",
      "authority": "REPLACE_WITH_NORMALIZED_AUTHORITY",
      "taxonomy_rationale": "Explain the classification and any bounded uncertainty.",
      "taxonomy_evidence": [
        "Use non-empty strings that distinguish prompt/repository facts from assumptions and gaps."
      ],
      "actual_route": [
        "delivery-orchestrator"
      ],
      "conditional_dispositions": {
        "REPLACE_WITH_CONTRACT_DECLARED_CONDITIONAL_SKILL": {
          "state": "not-applicable",
          "trigger_evaluation": {
            "trigger_statement": "REPLACE_WITH_THE_TRIGGER_DERIVED_FROM_INSTALLED_RUNTIME_INSTRUCTIONS",
            "source": "installed-runtime",
            "result": "not-met"
          },
          "rationale": "Explain why the trigger is or is not satisfied.",
          "evidence": [
            "Record non-empty trigger evidence."
          ]
        }
      },
      "extra_capability_justifications": {
        "REPLACE_ONLY_WITH_GENUINELY_ADDITIONAL_SKILL": {
          "rationale": "Explain the proportional need.",
          "evidence": [
            "Record non-empty supporting evidence."
          ]
        }
      },
      "delivery_result": "not-run",
      "evidence": [
        "Record non-empty route and no-effect evidence."
      ],
      "gaps": [],
      "outcome_observation": {
        "state": "no-meaningful-outcome-observed",
        "evidence": [
          "Distinguish pre-existing lifecycle outcome evidence from delivery work, which remains not run."
        ]
      },
      "scenario_observation": {
        "observation_scope": "route-only-no-effects",
        "effects_performed": [],
        "legacy_administrative_visibility": [],
        "legacy_invocations": [],
        "legacy_runtime_events": [],
        "legacy_branded_state_created": []
      }
    }
  ]
}
```

The envelope-level `loaded_specialists` list equals the distinct union of present route skills—no exploratory, omitted, or future-only skill. Each closure contains exactly the skill root plus every backticked local instruction reference from that `SKILL.md`, with current installed hashes, one `skill-root`, complete-read state, and no unresolved reference. That is self-report bound to inspected bytes, not cognition proof.

Every scenario repeats its exact blind prompt. Its `scenario_observation` makes effects, invocation, runtime, branded-state, and administrative-visibility claims local rather than hiding them behind an empty root list; each root list is the sorted unique scenario union. Any effect, legacy invocation/runtime, branded state, blocked branch, blocking gap, incomplete closure, or unresolved identity prevents a route-policy pass.

Conditional dispositions carry the trigger statement derived blind from installed runtime instructions, its source, and a structured result. The blind task must not copy expected-contract text. `activated` requires `met` and presence in the route; `not-applicable` requires `not-met` and absence; `deferred` uses `met` or `unknown` and remains absent; `blocked` cannot pass; `planned-future` is only for outcome-triggered conditional retrospective work with `future-pending` and absence from the current route. An `unknown` trigger requires a linked structured gap: use `related_field: conditional_dispositions.<skill>` or a descendant and cite the exact gap ID in that disposition's `evidence`. Model a pre-existing outcome separately: meaningful outcome, no meaningful outcome yet, or unknown. A direct retrospective route may retain its required intake owner with an unknown outcome only when a nonblocking gap links to `outcome_observation`, its ID is cited in `outcome_observation.evidence`, and no findings are claimed. Route-only `delivery_result: not-run` says the canary performed no delivery; it does not erase an already observed success, failure, cancellation, or recovery.

Each structured gap uses `id`, `kind`, `summary`, `related_field`, `route_effect`, and `next_action`. A `blocks-route` gap cannot pass. Missing repository, artifact, or provider evidence needed for later delivery is `nonblocking` when the prompt, profile, authority, and route remain truthfully classifiable; `blocks-route` is only for an unknown that prevents safe route selection itself. `extra_capability_justifications` contains only selected skills that are neither required nor declared conditional. Use the coordinator-provided public receipt slug and UTC timestamp; never expose internal task identifiers or private paths in a public record.

## Retrospective

```markdown
Expected vs actual outcome:
What helped / what hindered (with evidence):
Escaped defects or surprises and root causes:
Decisions worth retaining:
Debt/follow-ups (owner, priority, target, evidence):
Process experiment and success measure:
Canonical artifacts updated:
```
