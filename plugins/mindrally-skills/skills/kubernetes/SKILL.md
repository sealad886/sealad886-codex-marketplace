---
name: kubernetes
description: "Use when designing Kubernetes manifests, workloads, resource/probe configuration, identities, or deployment validation."
---

# Kubernetes / DevOps

## When to invoke

Use for designing Kubernetes manifests, workloads, resource/probe configuration, identities, or deployment validation.

## Inputs and evidence

Inspect cluster version, workload controller, storage lifecycle, namespaces/RBAC, image provenance, manifests and rollout ownership. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose the workload controller from identity and lifecycle requirements.
2. Set resource requests, probes, service routing, identities, and storage policies deliberately.
3. Render and validate existing Helm/Kustomize/manifests without changing the live cluster.
4. Under explicit deployment authority, verify rollout, readiness and recovery on the target cluster.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Rendered manifests validate and any claimed rollout has current target-cluster status and recovery evidence.

## Must not

Do not run kubectl apply or alter cluster credentials under inspection-only authority. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
