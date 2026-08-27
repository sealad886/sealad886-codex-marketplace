---
name: security-operations
description: Assess and improve security, privacy, risk, reliability, observability, supportability, and operational readiness across requirements, design, implementation, review, or release.
license: MIT
---

# Security, Risk, and Operational Readiness

Read `../.shared/operating-model.md`.

## When to invoke

Use for sensitive data, authentication/authorization, public/privileged interfaces, dependencies, infrastructure, migrations, high blast radius, reliability/incident work, explicit security review, or production release. Lead signing/notarization claim audits; participate as a required evidence owner for combined platform and distribution/installability claims. Scale a compact checklist into a formal threat model/readiness review as risk rises.

## Inputs and evidence

Inspect repository/security/privacy policies, data flows/classification/retention, trust boundaries and deployment topology, identities/permissions/secrets, dependencies/lockfiles/SBOM or provenance, config/IaC, failure history, SLOs/runbooks/on-call ownership, telemetry/alerts, backups/restore/DR, tests/scans, and current authoritative standards/vendor docs.

## Workflow

1. Choose assessment mode (design threat model, change/diff review, scoped assessment, or repository assessment) and pin revision or deterministic snapshot. Define reviewed surfaces, exclusions, deferred/not-applicable areas, coverage completeness, assets, actors, attacker capabilities, entry points, trust boundaries, sensitive data, privileges, invariants, and assumptions.
2. Analyze abuse paths and controls: authentication, authorization and tenant isolation, validation/encoding, injection, filesystem/network boundaries, cryptography/session handling, secrets, least privilege, auditability, dependency/supply chain, build/deploy integrity, and denial/resource exhaustion.
3. Analyze privacy: collection/minimization, purpose, consent where applicable, retention/deletion, residency, access/export, logs/telemetry, third parties, and migration/backfill exposure. Escalate legal conclusions to qualified owners.
4. Maintain candidate evidence through closure. For material security paths record source, control, sink, reachable boundary, counterevidence/proof gaps, attack preconditions, concrete outcome, stable root-cause identity, and affected-location roles. Choose static/dynamic validation deliberately and distinguish setup failure from counterevidence.
5. Analyze failure modes and reliability: dependency/timeouts/retries/backoff/circuit breaking, idempotency, consistency, capacity, graceful degradation, readiness versus liveness behavior, request/worker/queue/connection drain, backups and tested restore, DR, partial rollout, config skew, one-way data changes, and human error.
6. Define operational readiness: classified/redacted/access-controlled telemetry, secret-free logs, authenticated ingestion, actionable alerts/dashboards, ownership/on-call/support, runbooks, preview data/secrets isolation and teardown, incident/hotfix path, cost/capacity signals, and post-release verification.
7. Validate with appropriate static/dynamic/dependency/config/IaC/permission tests, graceful-shutdown checks, and recovery/restore exercises. Calibrate severity using reachability, exploitability, impact, existing controls, and evidence.
8. Close every candidate under the shared finding lifecycle. For each reportable candidate, assess impact and no-action consequences, then provide viable remediation or containment options, material security/operational tradeoffs, a recommended response, and next action/owner or authority need. Suppression is evidence-based closure of a false positive, duplicate, or invalidated candidate—not risk acceptance—and requires closure category, exact rationale/counterevidence, affected sibling/variant checks, qualified reviewer/date, expiry or revalidation trigger, release treatment, residual uncertainty, and a canonical finding link for duplicates. Material uncertainty stays open or becomes deferred/blocked with an owner and next proof action. Specify remediation invariant, regression evidence, rollback, residual risk authority, and release-blocking decision.
9. For signing/notarization or distribution evidence, inspect signatures, certificate/notarization state, provenance, permissions, access boundaries, and supply-chain exposure without private material. Under review authority, never sign, access signing credentials, submit for notarization, publish, deploy, install, or mutate the provider.

## Outputs and handoff

Threat/readiness model, finding/risk ledger, required controls, validation evidence, operational checklist, residual risk/acceptance needs, and release decision. Handoff implementation to `implementation-execution`, tests to `testing-quality`, findings to `review-audit`, and gates to `release-change`.

## Completion evidence

Material assets/boundaries/data/permissions/failure modes/operations are covered; mitigations and tests map to risks; severity/confidence are evidence-based; acceptance authority and residual risk are explicit.

## Must not

- Guarantee security/compliance/reliability, run intrusive tests outside authorization, expose credentials/personal data, or add dependencies/integrations by default.
- Treat a scanner’s output as validated or accept security risk on behalf of an unknown owner.
