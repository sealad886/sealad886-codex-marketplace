# Salesforce Apex and Lightning: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Bulkify queries and DML across record collections and respect transaction governor limits; avoid SOQL/DML per item.

- with sharing governs record sharing but does not by itself enforce CRUD/FLS. Use supported user-mode operations or explicit accessible-field handling as appropriate.

- A single static recursion boolean can skip valid records or later trigger chunks; use operation/record-aware idempotency and document trigger order assumptions.

- LWC navigation uses lightning/navigation where supported, rather than Aura force:navigateToComponent events.

- Expose an LWC on Flow screens with the lightning__FlowScreen target in js-meta.xml; lightning:availableForFlowScreens is an Aura interface.

- Use Lightning Data Service/wire adapters for their supported data access; imperative Apex remains appropriate for mutations or unsupported operations.

- Use accessible base components and structured error UI; lightning-card alone is not error handling.

- Treat required deployment coverage as a platform gate, not a sufficient quality target; test permissions, bulk operations, callouts, and failures.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [LWC Flow exposure uses lightning__FlowScreen metadata.](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-flow-screen.html)
- [LWC navigation is provided through platform navigation services.](https://developer.salesforce.com/docs/platform/lwc/guide/use-navigate)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
