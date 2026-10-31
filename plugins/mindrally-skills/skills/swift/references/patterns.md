# Swift implementation on Apple platforms: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use the configured language mode and deployment target rather than assuming the newest toolchain/API is available.

- Prefer value types where appropriate, but classes, protocols, actors, and framework interop have legitimate ownership roles. MVVM is optional.

- Swift concurrency cancellation is cooperative; inspect cancellation and prevent cancelled/stale work from updating newer UI state.

- Unstructured/detached tasks have explicit lifetime responsibilities and do not inherit every parent context; do not use them as a universal background-work recipe.

- Keep UI-isolated state on the appropriate actor and avoid blocking work there; select supported off-actor execution without violating Sendable/ownership.

- Use Keychain for appropriate credential storage and platform data-protection APIs; biometrics gate local access but do not replace server authorization.

- SwiftUI state wrappers depend on Observation versus ObservableObject and OS availability; do not mix ownership rules between them.

- Use Swift Testing or XCTest as the project supports, plus UI/device checks where relevant; previews are different evidence from runtime acceptance.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Swift cancellation is cooperative and unstructured tasks require explicit lifetime management.](https://docs.swift.org/latest/documentation/the-swift-programming-language/concurrency/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
