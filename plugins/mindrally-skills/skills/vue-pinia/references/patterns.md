# Pinia state ownership and lifecycle: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Setup and options stores are both supported; choose the existing style. Return state from setup stores so SSR/devtools/plugins can track it.

- Use storeToRefs when destructuring reactive state/getters; bound actions can be destructured directly.

- Pinia does not impose React Hook conditional-call rules; the important outside-component constraint is an appropriate active Pinia instance, especially with SSR.

- Use request-scoped Pinia in SSR and avoid reading browser storage on the server. Pass the correct instance in guards when injection is unavailable.

- Persist only intentional fields, validate stored data, and define schema migration/hydration behavior; do not treat persisted auth decisions as authority.

- createTestingPinia stubs actions by default. Use a real Pinia or stubActions:false to test their implementation.

- Manage sockets/timers/subscriptions through explicit ownership and cleanup; async actions need stale-result and error handling where requests overlap.

- Cart drafts require positive bounded quantities and authoritative server pricing; the source subtotal example is display state, not a checkout authority.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [createTestingPinia stubs actions unless stubActions:false is selected.](https://pinia.vuejs.org/cookbook/testing.html)
- [Outside-component store access depends on correct active Pinia and SSR scope.](https://pinia.vuejs.org/core-concepts/outside-component-usage.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
