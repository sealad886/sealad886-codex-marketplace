# Changelog

This file records user-visible marketplace and contained plugin changes. Dates
use ISO 8601 and plugin versions follow Semantic Versioning.

## Build Multi-target Tauri Apps 0.2.0 - 2026-10-31

### Added

- Mobile-first optimization workflow in the existing `tauri-performance` skill,
  covering responsiveness, startup, battery/energy, sustained thermal behavior
  and memory efficiency alongside correctness.
- Focused measurement, lifecycle/energy and memory guidance with dated primary
  sources, platform/tool availability limits and a before/after evidence receipt.

### Changed

- Require causal diagnosis, bounded work/resource ownership and comparable
  scenario measurements before accepting a performance improvement.
- Keep Tauri, frontend and native process attribution explicit; distinguish
  physical-device acceptance from browser, emulator and debug diagnostics.
- Preserve eight shared skills and synchronize Codex/Copilot package metadata
  for the 0.2.0 release.

## Local Translation 0.6.0 - 2026-10-30

### Added

- Centrally maintained Index-Translate input guidance with progressive disclosure:
  role-specific preparation and routing in skills, common input concepts in a
  shared guide, and selected-profile formats, worked MCP calls and language
  lookup in deeper references.
- Explicit caller workflows for native glossary mappings, hard requirements,
  soft preferences, genre/domain, context and approved owner clarifications.
- Shared Translate, Homura and NativeLong references describing their different
  input formats and current transport/decoding limits. No silent claim of full
  NativeLong execution support.
- Optional non-thinking chat-template passthrough for executable caller-prepared
  native requests, without adding a formatter tool or new connection settings.

### Changed

- Teach callers to incorporate approved context and owner answers explicitly,
  rather than assuming workflow query tracking injects them into generation.
- Keep prompt formats and examples in one shared reference tree instead of
  duplicating them across the twenty role skills.
- Preserve the endpoint/key/model configuration, existing job/review gates and
  caller ownership of request contents and output constraints.

## Local Translation 0.5.0 - 2026-10-30

### Added

- Discover models from the endpoint and optional key, then select an actual served
  model from a dropdown.
- Optional advanced sampling controls, plus per-request output-token limits and
  stop sequences. Existing context-size settings remain client capacity limits.
- Caller-managed inference requests with caller-defined JSON/schema constraints
  passed unchanged to the engine; results remain explicitly unreviewed.
- An MCP capabilities resource describing request options, defaults, limits and
  provider-dependent support.

### Changed

- Require only an endpoint and model ID for inference setup, with an optional
  API key. Remove model-revision, runner-version and language-registry fields;
  source and target locales come from each translation request.
- Keep the API key masked in the form for the screen's lifetime, including
  validation errors and failed saves. It is not persisted across screen refresh
  or close. Successful save requests that the host close the configuration form.
- Remove manually declared revision/version metadata from runtime configuration,
  health and job records while retaining model identity and content/configuration
  digests.

### Fixed

- Remove bundled UI console logging that could expose private tool arguments.

### Migration

- Explicitly upgrade older saved settings to the simpler connection schema with
  a private, non-overwriting backup. Preserve the endpoint, model, optional key
  and generation limits; discard retired setup metadata. Existing job storage
  and independent revision/delivery gates are unchanged.

## Local Translation 0.4.0 - 2026-10-30

### Added

- Native plugin settings with a **Configure local inference** action that opens
  the bundled MCP App as an in-app modal. Configuration no longer launches a
  system browser or a local setup website.
- Masked credential entry through app-only settings operations, outside model
  turns and conversation content, with explicit keep/replace/clear controls.
- An explicit in-app upgrade action that backs up retired workspace settings
  before converting them to engine-only settings.

### Changed

- Accept source prose or explicit text segments directly through MCP. Return
  draft, revision and reviewed delivery content to the calling agent, including
  segments and exact digests, so the caller decides where to retain results.
- Keep job files in private temporary storage for the MCP session. Jobs survive
  successive calls and are removed on normal server exit; restarting the server
  invalidates job IDs. Abrupt termination may leave files in the OS temp area.
- Configure only the local inference engine. Remove the translation workspace,
  source-path input and `LOCAL_TRANSLATION_ROOT` environment setting.

### Migration

- This is a breaking pre-1.0 tool and settings change. Callers must pass inline
  source content. Convert old saved settings explicitly with the packaged
  migration script, which preserves an owner-only backup before replacement.
  Historical workspace job files are left untouched.

## Local Translation 0.3.0 - 2026-10-29

### Added

- A local settings form opened from the chat, with persistent workspace and
  inference-engine settings that take effect without an app restart or MCP
  environment edits.
- Bootstrap settings inspection and setup tools, available before configuration.
  Test the exact model and chat tokenization using synthetic text before saving;
  preserve previous settings when validation fails.
- Optional runner authentication entered in the local form and stored in a
  private per-user settings file, omitted from tool responses and job records.

### Fixed

- Make first-run setup usable from desktop-launched Codex and Copilot. Explicit
  launch-environment configuration remains a whole-configuration override.

## Local Translation 0.2.0 - 2026-10-29

### Added

- Nineteen specialist skills alongside the Translation Project coordinator,
  covering every whitepaper function and separate editing, proofreading,
  media-coordination and conformance work.
- Explicit installed-skill loading receipts, role-specific methods and expert
  handoffs for actual subagents, with findings, counterpart replies,
  adjudication and recheck evidence.

### Changed

- Centralize shared references and templates beneath `skills/.shared/` and route
  coordinator assignments to named specialist skills. Retain distinct translator
  and reviser agents and actual human scope, content and release decisions.
- Discover and package all twenty skills in both clients. Runtime text/segment
  tools remain shared; role instructions do not add media-processing tools or
  establish professional qualifications.

## Local Translation 0.1.0 - 2026-10-28

### Added

- A professional translation workflow covering sixteen expert responsibilities,
  actual host-agent delegation, attributed exchanges, independent bilingual AI
  revision, shared queries, correction rounds and human acceptance authority.
- Eight local MCP tools for multilingual text/segment jobs, Index-Translate
  drafting, provenance, digest-bound corrections and review, and delivery
  candidates. Local runner/model installation and linguistic qualification are
  separate prerequisites.
- Matching logo, composer and skill icons, README artwork, dual-marketplace
  discovery, portable/Codex manifests, packaged examples, and validation coverage.

The initial runtime supports UTF-8 prose and explicit JSON segments through a
configured local vLLM-compatible runner. Audiovisual production, arbitrary
document reconstruction and qualified human acceptance require additional work.

## Repository Guidance 0.1.0 - 2026-10-27

### Added

- A reusable, single-skill plugin for creating or auditing agent instructions
  grounded in the target repository's structure, commands, ownership, and policy.
- An original adaptation of engineering principles researched from Multica's
  agent guide, with explicit provenance and a worked marketplace example.
- Codex and GitHub Copilot catalog entries, portable manifests, packaged support
  material, and security-scanner coverage.

## Iterating PR Bot Fixes 0.2.1 - 2026-10-27

### Fixed

- Batch coherent repairs after a settled review round and validate the complete
  change locally before pushing, reducing avoidable CI and review executions.
- Record push/review triggers and distinguish measured Actions billing from job
  runtime estimates, including private-repository Copilot review consumption.
- Prefer bounded failed-job retries and interruptible status waits while keeping
  required sources, new-finding dispositions, final-revision validation,
  approvals, protections, merge queues and the ten-round ceiling intact.

## Repository Consolidation 0.3.0 - 2026-10-25

### Changed

- Make accepted useful outcomes on the verified default branch the goal of
  consolidation. Branches and commits provide evidence, rather than a checklist
  to replay wholesale. Choose a canonical implementation and adapt missing
  behavior while preserving required caller differences and deliberate reverts.
- Prune verified obsolete tracked code, snippets, abandoned artifacts and their
  callers, configuration, assets, dependencies, tests and documentation within
  each reviewed integration candidate. Inspect dynamic/public consumers and
  generator inputs before removing source.
- Distinguish source pruning from branch/worktree retirement and unique-content
  disposal. Existing preservation, ownership, review and authorization checks
  remain in force, including separate authority for superseded unmerged branches.
- Update the existing guides, ledger and prompts without adding another skill,
  runtime, helper or mandatory dependency on Simplify Code. Retain the catalog's
  local package source so default installs use the marketplace checkout's version.

## iCloud Mail 0.4.0 - 2026-10-23

### Added

- Optional read-only Streamable HTTP service using the pinned official MCP SDK,
  per-user OAuth/OIDC access tokens and tenant-bound encrypted credentials.
- Private user-run device-flow onboarding and authenticated disconnection,
  separate read/attachment/watch/configuration scopes, and bounded concurrency.
- Encrypted, tenant-bound expiring identifiers and durable watch pagination,
  UIDVALIDITY recovery, overlapping scans and explicit delivered/no-alert receipts.
- Remote deployment/onboarding/rollback guidance and mocked HTTP, authentication,
  tenant isolation, redaction and checkpoint regression coverage in CI.

Local stdio and Keychain use remain available. This release supplies self-hosted
server code, not a live hosted endpoint. Hosting/OIDC setup, live credentials and
a cloud-runner read with the Mac offline remain separate deployment prerequisites.
No monitoring is started or resumed by installation.

## Camofox Browser 0.1.1 - 2026-10-21

### Added

- Camofox Browser: 46 MCP tools for headless browsing, page interaction,
  structured extraction, screenshots, uploads, downloads and service diagnostics.
- Managed setup installs the pinned npm client, upstream server and browser
  engine. Private loopback services, isolated sessions and explicit lifecycle
  commands support local macOS/Linux use and existing-server connections.
- Distribute the canonical plugin from `sealad886/camofox-mcp` without copying
  its server implementation into the marketplace. Node MCP launchers receive
  the same contained distribution validation as existing Python launchers.

## Workflow plugin expansions 0.2.0 - 2026-10-19

### Added

- Iterating PR Bot Fixes: failed-check diagnosis and revision/merge-queue
  recovery, with source retirement and current-head review kept distinct.
- Repository Consolidation: overlap/prerequisite planning and verification of
  committed, dirty, untracked and special-file recovery content.
- Conventional Commit: automation-aware message decisions and a constrained
  procedure for committing a verified subset of already-staged text hunks.
- Simplify Code: state/control-flow reduction and previewed caller migrations
  with explicit exclusions, repeat-run checks and optional evidence capture.
- Adversarial Audit: bounded failure/recovery experiments and differential or
  property-based verification using an explicitly justified comparison oracle.
- Web Research: decision/sensitivity comparisons, claim-scoped refreshes and
  quantitative evidence appraisal with source-versus-calculation separation.

### Changed

- All six remain independent one-skill packages. New runbooks are conditionally
  routed from their existing entrypoints; complex work can use optional templates
  or extensions to existing ledgers. No new server or runtime is required.
- Each package advances to 0.2.0 with its existing identity, starter prompts,
  local/cloud eligibility and authority boundaries preserved.

## Conventional Commit 0.1.1 - 2026-10-19

### Fixed

- Use the installed namespaced skill in direct cleanup examples, matching the
  plugin's starter prompt and guide after standalone-skill removal.
- Clarify local and cloud installation and execution requirements in the guide.

## Standalone workflow plugins 0.1.0 - 2026-10-18

### Added

- Iterating PR Bot Fixes `0.1.0`: bounded review rounds, attributable reviewer
  outcomes, scoped root-cause fixes, merge gates, and verified cleanup.
- Repository Consolidation `0.1.0`: complete source accounting, preservation,
  serial PR integration, destination verification, and eligible cleanup.
- Conventional Commit `0.1.0`: selective commit grouping, preservation of
  unrelated index and working-tree content, and explicit cleanup controls.
- Simplify Code `0.1.0`: behavior-preserving removal of unnecessary layers,
  canonical shared ownership, and verification of dynamic and public consumers.
- Adversarial Audit `0.1.0`: evidence-backed finding validation, proportional
  specialist investigation, and an authorized remediation loop.
- Web Research `0.1.0`: source evaluation, dated and version-aware evidence,
  adjacent citations, independent corroboration, and explicit uncertainty.
- Each package exposes one independently usable skill, with contained
  references, original artwork, display metadata, catalog discovery, and
  pinned hosted security scanning.

### Changed

- New workflow packages include portable Agent Plugins 1.0 root manifests and
  matching Codex overlays. Existing plugin layouts remain supported; the
  standalone source skills are not modified or automatically replaced.
- Package validators check portable manifest agreement and retain root
  manifests in exact distribution payloads. CI validates source and distribution
  structure for every catalog package while retaining specialized checks.

## MLX Optimizer 0.2.5 - 2026-10-18

### Security

- Isolate environment-probe child imports from repository files and inherited
  Python search paths while preserving the selected virtual environment.
- Reject symlink and non-regular audit inputs, and bound each source read to
  2 MiB so crafted files cannot block or exhaust the scanner.

## iCloud Mail 0.3.1 - 2026-10-18

### Security

- Replace backtracking HTML stripping with bounded forward-only conversion.
  Malformed message markup no longer monopolizes read, thread-read or forward
  processing; operation deadlines and visible message content are preserved.

## Marketplace tooling - 2026-10-18

### Security

- Bound validator input reads and reject symlinks and special files across
  marketplace, package and route-evidence checks.
- Build artwork helpers in private temporary directories and stop on compiler
  failure instead of reusing executables at predictable temporary paths.

## iCloud Mail 0.3.0 - 2026-10-15

### Changed

- Return fixed ten-result pages from search, draft listing, folder listing, and
  thread reads, with `page_token`, `next_page_token`, `has_more`, `page_size`, and
  `returned`. Replace the public `max_results` argument; callers must refresh
  tool discovery and follow tokens while retaining their original filters.
- Continue search through older UIDs beyond the former newest-80 candidate
  window, preserving bounded work per call and progress after empty filtered
  pages. New arrivals do not displace later pages.
- Sort folders by name and page thread messages chronologically, including the
  requested anchor once on its chronological page. Reject stale discovery
  tokens and keep truncation/processing limits distinct from continuation.
- Retain stateless, dependency-free operation without a local mail cache.

## iCloud Mail 0.2.2 - 2026-10-06

### Fixed

- Put a Connect to iCloud Mail starter first on the plugin page. It starts a
  chat that opens private local setup for the Apple app-specific password.

## iCloud Mail 0.2.1 - 2026-10-06

### Fixed

- Include the matching marketplace catalog reference in the release snapshot
  before tagging. Mail functionality is unchanged from 0.2.0.

## Build Multi-target Tauri Apps 0.1.0 - 2026-10-04

### Added

- Eight original Tauri 2 skills for architecture, frontend UX, native builds,
  IPC security, target QA, performance and release preparation.
- Shared target-specific references and a dated 43-source primary research
  ledger mapping capabilities from the four platform build/test plugins.
- Plugin and skill display metadata, original artwork, catalog discovery,
  self-contained distribution validation and hosted security scanning.
- Explicit browser/native evidence boundaries and current macOS embedded
  WebdriverIO guidance with production instrumentation exclusion.

## iCloud Mail 0.2.0 - 2026-10-03

### Added

- A temporary local connection page with Apple password-generation guidance,
  direct IMAP and SMTP validation, and native macOS Keychain storage.
- Serialized account saves, stale-session rejection, credential rollback, and
  clear recovery feedback when settings cannot be restored.
- Bundle, privacy, and setup coverage for local authentication and the absence
  of a plugin-managed email repository.

### Changed

- macOS credential reads and writes share the native Keychain helper; saved
  credentials take precedence over an older launch-environment password.
- Setup guidance now distinguishes saved configuration from live verification
  and explains that requested mail enters Codex without local mailbox syncing.

## Plugin display updates - 2026-09-28

### Fixed

- Conversation Visuals 0.1.2, Semantic Versioning 0.1.1, MLX Optimizer 0.2.4,
  and iCloud Mail 0.1.1 now include skill display names, descriptions, brand
  colors, and starter prompts through `agents/openai.yaml`.
- Package guides include artwork and linked skill summaries with example requests.
- Semantic Versioning now supplies the plugin detail page website link.

## Semantic Versioning 0.1.0 - 2026-09-28

### Added

- Three progressively loaded skills for cumulative release assessment, native
  version ownership, release configuration, and publication verification.
- Read-only repository discovery and strict SemVer helpers; ten ecosystem
  references, native examples, and inactive GitHub release workflow templates.
- Example build/package CI, workflow validation, behavioral regression tests,
  and distribution through the marketplace catalog.

## Project Delivery 1.5.0 - 2026-09-28

### Added

- A compact `small-feature-change` route for bounded, low-risk implementation,
  with conditional design, security, coordination, documentation, review, and
  release ownership when evidence calls for them.
- Simplicity-first guidance across requirements, design, planning, implementation,
  and review; corrective simplification rewrites remain subject to explicit scope.
- Guidance to reuse canonical implementations, extract helpers for stable repeated
  behavior, and follow the repository's language and framework idioms.

### Changed

- Findings and failed checks now include impact, viable responses, material
  tradeoffs, a recommendation, and the next action or required authority.
- Route validation covers the new compact path alongside the existing lifecycle
  profiles, with regression checks for required quality evidence and escalation.

## MLX Optimizer 0.2.3 - 2026-09-06

### Added

- Original slate, beveled-metal, and electrified-glass branding, including the
  256-pixel composer icon and 1024-pixel plugin logo.
- Editable Apple Icon Composer document and reproducible Swift artwork sources.

### Changed

- Plugin metadata and README now show the approved layered MLX Optimizer identity.
  The six optimization skills and their runtime behavior are unchanged.

## iCloud Mail 0.1.0 - 2026-09-28

### Added

- iCloud Mail `0.1.0`, a local dependency-free MCP integration for searching,
  reading, organizing, drafting, and sending iCloud email through Apple's
  documented TLS IMAP and SMTP endpoints.
- Saved non-secret account configuration, macOS Keychain guidance,
  app-specific-password authentication, bounded message and attachment reads,
  recoverable mailbox mutations, and package-specific CI and HOL scanning.

### Changed

- Documented repository-relative package sources as subtrees of the
  GitHub-fetched marketplace checkout rather than paths into a user's
  development checkout.

## Unreleased

### Added

- MLX Optimizer `0.2.2`, migrated from its standalone repository with six
  progressive-disclosure skills, nine MLX reference guides, three stdlib helper
  scripts, three verification templates, package tests, and immutable
  marketplace distribution metadata.

### Fixed

- Included the required `.codexignore` file in clean Git checkouts after a
  developer-global ignore rule omitted it from the superseded `0.2.0` tag.
- Preserved MLX evaluation synchronization through an explicit callable lookup
  so security scanners do not confuse `mx.eval` with Python dynamic evaluation.

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
