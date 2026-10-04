# Build Multi-target Tauri Apps delivery

Scope: a self-contained Codex skills plugin for building and validating Tauri 2 applications on Windows, Linux, macOS, iOS and Android, with an optional browser deployment. User authorized implementation and local milestone commits, then authorized push, PR creation/updates and live marketplace publication after iterating-pr-bot-fixes. That skill grants task PR merge and scoped post-merge cleanup when reviews and CI gates pass. Installation remains isolated validation only.

Baseline: clean `main` at `3c5d13c`, matching `origin/main`; existing checkout only. No worktree or dependencies needed. Repository provenance policy requires original synthesis, not copied source-plugin text or assets.

## Route and gates

Profile: `medium-feature-change`; scale medium, risk medium because instructions guide privileged IPC and release tooling. Orchestrator 1.5.0 used because requested 1.4.1 installation is absent. Required owners: context, acceptance, solution design, delivery planning, implementation, quality, documentation, independent review, release preparation. Security/operations activated for IPC, credentials and automation boundaries. External coordination activated after publication authorization for exact GitHub PR, review and marketplace receipts. Retrospective planned-future: no consumer outcome observed yet.

Ready: requested plugin, source capability inventory, repository contracts and packaging validators inspected. Design: eight focused skills, shared references inside the skill tree to survive distribution, no MCP servers or required companion plugins. Repository checks remain canonical. Existing plugins remain unchanged.

## Acceptance

- AC-1: manifest, original artwork, skill interface metadata, README, license, security guidance, ignore rules and catalog-local source form a valid self-contained package.
- AC-2: original workflows adapt build/run/debug, frontend design/accessibility, native integration, profiling, signing and Android QA capabilities from all four named plugins.
- AC-3: official sources support decisions across project layout, configuration, IPC, state, permissions, persistence, mobile, desktop, testing and distribution; dated source registry and adaptation matrix remain in the package.
- AC-4: native targets and optional browser target have explicit support/evidence limits; tools are detected, pinned-version help/docs checked and unavailable tools have concrete fallback paths.
- AC-5: security checks cover custom-command defaults, merged capabilities, remote origins, CSP, scoped resources, secrets and test-only instrumentation.
- AC-6: CI and local package/distribution/catalog checks validate shipped references; milestone commits exclude unrelated work.

## Work and milestones

1. Research official guidance and source-plugin capability inventory; commit evidence/design milestone.
2. Implement eight skills and shared references, package and catalog integration.
3. Run structure, distribution, marketplace and regression checks; independently review; correct findings and commit complete plugin milestone.

## Design decisions and bounded risks

- Use project package manager and local CLI; never require global tools, another build plugin or invented MCP APIs.
- Browser deployment requires an explicit browser service implementation for native features or visible unsupported states. A browser preview cannot exercise Rust IPC.
- Do not blanket-copy SwiftUI, AppKit, Compose, Stripe or Supabase advice into Tauri. Native extensions or service-specific guidance apply only when actual requirements call for them.
- Current upstream WebDriver guidance includes macOS through embedded WebdriverIO instrumentation. Direct official `tauri-driver` still supports Windows/Linux only. Tool versions and provider choice must be reverified; no paid provider required.
- This deliverable is a skills package, not a sample application. Static validation cannot establish future agent routing, physical-device acceptance, signed app viability or storefront readiness.
- Catalog uses local source, matching existing pre-install discovery convention. No unpublished tag is invented; version 0.1.0 identifies initial package intent, not a published release.
