# Contributing

Contributions that make Andrew Cox's Codex Plugin Marketplace or one of its contained plugins clearer, safer, more evidence-driven, or more adaptable are welcome.

## Choose the owning scope

- Marketplace-level changes own catalog metadata, repository policy, shared CI, issue templates, and cross-plugin documentation.
- Plugin changes belong under the canonical `plugins/<plugin-id>/` package and must follow that plugin's documented contracts and validation workflow.
- Do not create cross-plugin runtime dependencies merely to share prompts, assets, terminology, or implementation details.

Project Delivery is currently the only published plugin. The guidance below is its contribution contract; future plugins must document an equivalent self-contained contract in their own package.

## Before changing Project Delivery

1. Open or reference an issue when the change affects lifecycle semantics, artifact contracts, compatibility, or safety.
2. Inspect the shared operating model and the owning skill before adding a new concept.
3. Extend the canonical skill or shared reference instead of creating an overlapping skill.
4. Keep the core provider-neutral and independently useful. Integrations may be optional adapters, never hidden dependencies.

## Originality and provenance

Submit original work. Do not copy another plugin's skill text, prompts, code, icons, templates, manifests, or proprietary schemas. Capability-level research may inform a contribution, but the result must be an independently written synthesis that fits Project Delivery's terminology and operating model. Any incorporated third-party code or asset must have a compatible license, retain required notices, and be identified in the pull request.

Do not include credentials, private repository material, personal data, generated session transcripts, downloaded binaries, or another project's branded state.

## Skill contract

Every skill must retain clear answers to:

- when it is invoked;
- what inputs and repository evidence it inspects;
- what workflow and authority boundary it follows;
- what outputs and handoff it produces;
- what evidence completes it; and
- what it must not do.

Prefer a small number of substantial, non-overlapping skills. Update the operating model and templates only for conventions genuinely shared across the lifecycle.

## Validation

Run from the repository root:

```bash
python3 scripts/check_plugin.py plugins/project-delivery --layout source
python3 scripts/check_routes.py .
python3 scripts/check_distribution_bundle.py plugins/project-delivery
python3 scripts/check_installed_parity.py <prepared-plugin-source> <installed-cache-version-dir>
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

When the Codex Plugin Creator skill is available, also run its manifest validator and validate every changed skill with Skill Creator. Release candidates must pass the pinned HOL scanner workflow with no high or critical finding.

Record exact commands, results, revision, and any checks not run. Static route-contract validation must never be described as proof of interactive agent behavior.

## Pull requests and releases

Use focused Conventional Commits. Explain the problem, user impact, design choice, validation evidence, compatibility, and residual risk in the pull request. Version releases with Semantic Versioning based on the public plugin contract. Only maintainers publish tags and releases.
