# Azure Cloud Development: implementation guidance

## Provisioning and identities

Extend the existing IaC tool rather than introducing a second source of truth.
Use environment parameters and review what-if/plan results. Managed identity removes
static service credentials but still requires correctly scoped authorization.
On AKS, separate cluster identity, Kubernetes API access, and pod-to-Azure Microsoft
Entra Workload ID; workload identity does not by itself provide pod isolation or
Kubernetes permissions. StatefulSets provide identity/order, not automatic durable
backups; storage classes, PVCs, availability, and recovery need explicit design.

## Pipelines and operations

Use approved YAML templates and environment approvals; this skill does not change
subscription, repository, or production gates. Keep secrets in approved Key Vault
or protected integration mechanisms. Check actual Application Insights/Monitor
configuration and redact telemetry. Use tags, budgets, and measured utilization;
reserved capacity is a financial commitment, not an automatic optimization.
Test the language/runtime actually deployed rather than requiring pytest for all
Azure projects. Validate network access, scale limits, and failover separately.

## Primary documentation

- [AKS identity scenarios](https://learn.microsoft.com/azure/aks/managed-identity-overview).
- [Pod-to-Azure Workload ID](https://learn.microsoft.com/azure/aks/workload-identity-overview).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
