# Changelog

This file records user-visible marketplace, Project Delivery, and Conversation
Visuals changes. Dates use ISO 8601 and plugin versions follow Semantic
Versioning.

## Unreleased

### Added

- MLX Optimizer `0.2.1`, migrated from its standalone repository with six
  progressive-disclosure skills, nine MLX reference guides, three stdlib helper
  scripts, three verification templates, package tests, and immutable
  marketplace distribution metadata.

### Fixed

- Included the required `.codexignore` file in clean Git checkouts after a
  developer-global ignore rule omitted it from the superseded `0.2.0` tag.

## 0.1.1 - 2026-07-30

### Fixed

- Made Conversation Visuals' complete manifest metadata, branding, starter
  prompts, skills, and MCP capability visible in Codex before installation.

## 0.1.0 - 2026-07-30

### Added

- Conversation Visuals `0.1.0` package with four skills for
  conservative conversational visual selection, sourced-media research,
  disclosed visual generation, and short visual storytelling.
- A dependency-free local MCP server that plans visual treatments and validates
  accessibility, originating-source, generated-media disclosure, and public-URL
  invariants without reading files, accessing the network, or calling providers.
- Package, behavioral, protocol, URL-safety, distribution, and CI validation for
  Conversation Visuals, including a separate pinned HOL scanner job.

### Changed

- Generalized distribution validation so independently versioned marketplace
  plugins can declare different skill counts and local MCP script dependencies
  while preserving Project Delivery's exact 13-skill shared-runtime contract.

## 1.4.1 - 2026-07-29

### Changed

- Aligned Project Delivery's canonical package boundary, manifest, documentation, security links, and route-receipt schema identifier with the sealad886 Codex Marketplace repository.
- Reframed the repository documentation and validator as a multi-plugin marketplace, with unique contained plugin entries and resolvable immutable `git-subdir` sources whose pinned package identity is inspected.

### Fixed

- Rejected marketplace entries whose immutable-looking Git reference does not resolve, lacks the advertised plugin subtree, or contains a mismatched package identity.
- Preserved the existing 13-skill lifecycle and route contracts while fixing the installed package's canonical source metadata.

## 1.4.0 - 2026-07-21

### Added

- Semantic route-contract schema v3 plus an installed canonical route-profile schema v1, with required and conditional capabilities, evidence-resolved runtime scale/risk ranges, narrower blind-canary tolerances, partial-order safety edges, two-sided controller entry and return contracts, and 24 canonical scenarios including separate performance, packaging, signing/notarization, distribution, direct-retrospective, release-execution, and workflow-decommission variants.
- Dependency-free validation for no-effect contract-blind route receipts, including a closed schema-v3 observation, structured trigger/outcome/effect/gap records, complete installed-instruction closure, deterministic semantic and raw-byte digests, installed-plugin identity and skill-byte binding, public receipt identities, an all-semantic-field freeze declaration, evidence-bearing taxonomy rationale, explicit separation of fresh observations from post-hoc historical annotations, and adversarial tests for missing ownership/loading/evidence, route-only authority effects, unexplained conditional omissions, invalid controller entry/return/final disposition, cyclic precedence, contradictory policy, unjustified extras, and legacy dependencies.
- A prompt-only export command that derives blind canary inputs from the canonical route contracts without disclosing expected owners, ordering, or artifacts.
- A sealed three-record live-canary protocol: coordinator-generated canonical task prompt and private task binding, publishable byte/launch attestation, and independent digest-linked route grade.
- Plugin Creator-generated repository marketplace metadata for the canonical `plugins/project-delivery/` package subtree, plus hosted validation of marketplace containment, identity, policy, category, and exact MIT-license parity.
- Guarded distribution materialization with deterministic payload hashing; exact file-and-directory inventories; symlink, executable, forbidden, unsupported, and undeclared-entry rejection; clean-destination proof; checkout/environment ancestry protection; recoverable atomic replacement; installed-cache parity; progress/ETA reporting; and adversarial regression tests.

### Changed

- Bound ordinary fresh-task smoke callbacks to the exact expected installed cachebuster version, while keeping sealed JSON route receipts schema-valid through `plugin_identity.installed_version`.
- Instructed the orchestrator to load selected sibling specialists directly from the installed plugin bundle when Codex's global initial skill-metadata budget omits their catalog entries, with unreadable specialists blocking the route.
- Replaced exact total-array route grading with semantic capability, gate, authority, and evidence comparison.
- Strengthened implementation and testing preflight for wrapper side effects such as signing, fixed temporary paths, deletion, credentials, network/provider access, packaging, publication, and deployment.
- Split structural skill completeness, Skills UI presentation, initial-list visibility, explicit invocation, orchestrated loading, and runtime behavior into distinct evidence classes.
- Added a reusable recovery-record template and expanded decommission rollback guidance to distinguish CLI, remote-synced, direct-registration, symlink, standalone-source, and cache identities.
- Reclassified preserved `1.3.1` receipts as historical route-shape compatibility evidence rather than current-policy or candidate-behavior proof, including explicit future-only retrospective branches.
- Normalized route vocabulary for scale, risk, authority, and conditional state; future-triggered retrospectives are now dispositions only and are omitted from the present route and load claims.
- Made quality, security, release, documentation, and coordination ownership explicit for flaky CI, operational handoff, documentation validation, preview migration, combined-platform, performance, package, signing/notarization, and distribution routes.
- Made installed `route-profiles-v1.json` the runtime semantic source for common intent profiles and required validator parity with maintainer-only route contracts, preventing runtime instructions and canary expectations from drifting independently.
- Required the declared lead to open fresh routes after the optional orchestrator, exact loaded-skill records for present routes, and final release dispositions after all selected decision-bearing evidence.
- Moved the canonical installable plugin into `plugins/project-delivery/` so local and Git `git-subdir` marketplace sources exclude repository metadata, CI, tests, audit evidence, validator tooling, and development environments.
- Added an explicit, non-destructive 1.3.x checkout-layout migration and forward/back recovery sequence.
- Required authorization, minimum necessary scope, and untrusted-content handling when project context uses external systems or private records.

### Fixed

- Clarified direct-retrospective intake when outcome evidence is unavailable, exact unknown-branch gap citation, and the distinction between missing delivery inputs and route-selection blockers.
- Made sealed grader tests independent of developer-specific global Git ignore configuration.
- Prevented Codex's unfiltered local-source cache copy from installing `.git`, `.venv`, bytecode, repository workflows, tests, and maintainer-only evidence with Project Delivery.
- Prevented an unsafe distribution refresh from erasing unrelated destination content or ignoring empty forbidden/undeclared directories.
- Corrected missing coordination ownership for operational handoff, missing quality ownership for documentation validation, missing security ownership for distribution validation, premature release ordering, stale candidate-identity acceptance, blanket specialist-load claims, and prospective retrospective activation found by fresh-task and adversarial RC canaries.

### Release-candidate provenance

- Promoted the validated `1.4.0-rc.1` package and its incorporated canary remediations to the stable `1.4.0` contract without changing the plugin's public capability surface.

## 1.3.2 - 2026-07-19

### Changed

- Rewrote installation and usage guidance for Project Delivery as a standalone source plugin, with Plugin Creator handling supported local registration, cache refresh, and reinstall steps.
- Renamed the installable-bundle validator to `scripts/check_distribution_bundle.py` and aligned contributor, CI, template, audit, and validation terminology.

### Fixed

- Replaced environment-dependent installation guidance with a source-first standalone workflow.
- Updated quick-start examples to use the installed plugin's fully qualified skill names.

## 1.3.1 - 2026-07-19

### Changed

- Added explicit MIT metadata to all 13 skill manifests so hosted skill scanners can resolve each skill's license without inferring it from the plugin root.

## 1.3.0 - 2026-07-19

### Added

- Reproducible, machine-readable contracts for all 17 canonical routing scenarios.
- Standard-library regression tests for source and installed-cache validation.
- Pinned validation and HOL security-scanner workflows, Dependabot configuration, a security policy, and contribution guidance.
- Live route-receipt fields that distinguish static contract checks from fresh agent behavior.

### Changed

- Security finding suppression now requires counterevidence, closure authority, sibling analysis, revalidation triggers, release treatment, and explicit residual uncertainty.
- Risk and decision records now participate in requirement-to-release traceability.
- Public documentation now explains installation, verification, trust boundaries, and migration claims more precisely.

### Fixed

- Installed-cache validation now recognizes the versioned Codex cache layout without weakening source-layout checks.
- Validation evidence no longer presents static routing analysis as interactive proof or reports a stale file count.

## 1.2.2 - 2026-07-19

### Added

- Initial public release with 13 lifecycle skills, shared artifacts, migration guidance, validation references, and a complete plugin and per-skill icon family.
- MIT License with copyright assigned to Andrew Cox.
