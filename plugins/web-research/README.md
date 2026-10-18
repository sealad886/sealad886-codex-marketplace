# Web Research

Version: **0.1.0**. One skill for researching a question, checking sources, and
producing a decision-ready brief with citations and honest uncertainty.

[The web-research skill](skills/web-research/SKILL.md) discovers available search,
retrieval, PDF/document, and official documentation capabilities. It reads the
supporting material, checks applicability and independent corroboration, explains
conflicts, and cites material claims where they appear.

## Use

```bash
codex plugin add web-research@sealad886-codex-marketplace
```

Example requests:

- "Research this question using current primary sources and explain unresolved gaps."
- "Compare these options for Ireland, using the relevant dates and conditions."
- "Verify this API guidance against the version pinned in this repository."
- "Research the supplied documents and save a cited brief at the requested location."

Provide the question, decision, geography/date/version constraints, and desired
depth. Saving a local brief is supported when requested. Research does not silently
authorize implementation, external writes, outreach, or publication.

## Evidence and requirements

The host supplies browsing or document tools; this package includes no crawler,
server, credentials, paid data source, or required sibling plugin. Missing access
is reported. Search snippets are leads, and copied reports are not independent
corroboration. An unavailable current source cannot establish a current fact.

Use the [research method](skills/web-research/references/research-method.md) and
[optional brief template](skills/web-research/templates/research-brief.md).
See [security and privacy boundaries](SECURITY.md). The plugin guides research;
it adds no tool permissions and does not guarantee source accuracy or completeness.

## Package validation

The portable and Codex manifests agree on identity, version, and presentation.
Exactly one skill and its contained support files form the runtime payload.
Maintainers use the current [contribution and validation guide](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/CONTRIBUTING.md)
for source/skill checks, distribution closure, native discovery, and installed
parity. Static checks cannot establish that sources were read or a research
conclusion is correct; those require evidence from the actual research task.
