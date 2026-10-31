# Kubernetes / DevOps: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Workloads and resources

- A StatefulSet is useful for stable identities, ordered lifecycle, or stable storage relationships; persistence alone does not always require it.
- Set requests from workload measurements and limits according to application/OOM/throttling behavior; storage and pod lifetimes differ.
- Separate startup, readiness and liveness purposes; dependency failures in liveness can cause restart cascades.

## Security and operations

- Namespaces organize resources but do not alone provide complete tenant isolation; combine RBAC, network policy, identities and workload controls.
- Use the project’s existing GitOps/Helm/Kustomize path and validate API availability for the cluster version.
- Keep secrets outside plaintext manifests and logs; review service-account permissions and external exposure.
- Shell, Ansible and cloud changes need their own declared toolchains and scopes; Kubernetes guidance does not authorize deployment.

## Primary documentation

- [Primary documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) — StatefulSets serve stable identity/storage and ordered deployment needs and are not required for all persistent workloads.
- [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/) — Startup, readiness and liveness probes have different behavior and purposes.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
