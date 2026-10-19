# Web Research

Version: **0.2.0**. One skill for researching a question, comparing decisions,
refreshing existing briefs, and checking quantitative evidence with citations and
honest uncertainty.

[The web-research skill](skills/web-research/SKILL.md) discovers available search,
retrieval, PDF/document, and official documentation capabilities. It reads the
supporting material, checks applicability and independent corroboration, explains
conflicts, and cites material claims where they appear.
Advanced runbooks separate hard constraints from preferences, expose decisions
that depend on unknown evidence, update individual claims without overstating
coverage, and make units, denominators, and calculations inspectable.

## Use

```bash
codex plugin add web-research@sealad886-codex-marketplace
```

Example requests:

- "Use $web-research:web-research to research this question using current primary sources and explain unresolved gaps."
- "Use $web-research:web-research to compare these options for Ireland. Separate required conditions from preferences and show which missing prices could change the decision."
- "Use $web-research:web-research to refresh the version-dependent claims in this API brief against the repository's pinned version. State which other claims remain unchecked."
- "Use $web-research:web-research to check the units, denominators, baseline, and uncertainty behind these numerical claims. Show sourced inputs separately from calculations."
- "Use $web-research:web-research to research the supplied documents and save a cited brief at the requested location."

Provide the question, decision, geography/date/version constraints, and desired
depth. Saving a local brief is supported when requested. Research does not silently
authorize implementation, external writes, outreach, or publication.

## Evidence and requirements

The host supplies browsing or document tools; this package includes no crawler,
server, credentials, paid data source, or required sibling plugin. Missing access
is reported. Search snippets are leads, and copied reports are not independent
corroboration. An unavailable current source cannot establish a current fact.

Use the [research method](skills/web-research/references/research-method.md) and
conditional guides for [decision comparisons](skills/web-research/references/decision-comparisons.md),
[refreshing research](skills/web-research/references/research-refresh.md), and
[quantitative evidence](skills/web-research/references/quantitative-evidence.md).
Optional templates cover a [brief](skills/web-research/templates/research-brief.md),
[decision matrix](skills/web-research/templates/decision-matrix.md), or
[claim ledger](skills/web-research/templates/claim-ledger.md). Reuse existing
records rather than filling every template.
See [security and privacy boundaries](SECURITY.md). The plugin guides research;
it adds no tool permissions and does not guarantee source accuracy or completeness.

Local and cloud hosts supply their own tools and authorized source access; the
same skill runs in either without a bundled runtime. Refreshing a brief is a
bounded task, not enrollment in recurring monitoring or permission to publish.

## Package validation

The portable and Codex manifests agree on identity, version, and presentation.
Exactly one skill and its contained support files form the runtime payload.
Maintainers use the current [contribution and validation guide](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/CONTRIBUTING.md)
for source/skill checks, distribution closure, native discovery, and installed
parity. Static checks cannot establish that sources were read or a research
conclusion is correct; those require evidence from the actual research task.
