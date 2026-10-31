# DevOps Engineering: implementation guidance

## Automation and configuration

Choose Bash or POSIX sh explicitly; quote operands and avoid eval. Scope temporary
cleanup to owned resources, preserve error status, and use bounded locks/timeouts.
Ansible idempotency depends on module/task semantics, not merely YAML: use native
modules, appropriate changed_when/failed_when, handlers, and scoped inventories.
Check mode is not a proof that every module/action is side-effect free. Vault
encrypts stored values, but logs and execution still need no_log/redaction and
protected credentials. Do not hardcode a universal naming style or pytest runtime.

## Workloads and operations

Kubernetes workload identity covers an identity integration, not all pod-to-service
security. Review RBAC, network policy, secret access and admission separately.
StatefulSets need explicit storage/backup/recovery; Helm, Kustomize, and GitOps
are tool choices, not simultaneous requirements. Use readiness/liveness/startup
semantics correctly and protect rollout gates. Capture first meaningful CI errors,
artifact/revision identity and real costs; retries do not waive failures. Blue/green
or canary needs data compatibility and rollback evidence. Changes to infrastructure,
monitoring services, alerts or paid resources require task authority.

## Primary documentation

- [Check-mode limits](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html).
- [StatefulSet guarantees and limits](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
