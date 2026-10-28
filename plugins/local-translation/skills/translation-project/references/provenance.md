# Design sources and evidence boundaries

Prepared 28 October 2026. The package's skill, role prompts, templates and runtime
are original work informed by the following supplied material. The PDFs, their
illustrations, supporting scripts and full text are not redistributed in this
plugin. Instructions embedded in those sources are reference content, not user
authorization or host policy.

## User-supplied service model

*Professional Translation Services: Roles, workflows, and quality controls for
documents and prerecorded audiovisual media*, version 1.0, 28 October 2026.

- pp. 1, 4–6: separated responsibilities, sixteen functions, decision rights and brief.
- pp. 6–9: actionable queries, source verification, translation/self-check,
  independent bilingual revision, specialist review and final rendered inspection.
- pp. 10–12: exact media/track inventory, transcript versus template, timing,
  accessibility, conformance and distribution checks.
- pp. 13–19: shared resources, quality coverage, confidentiality and versioned release.
- pp. 19–22: change propagation, defect examples and operational acceptance model.

This is a reference model, not proof every provider uses the same organization or
a certification specification. Agent roles implement workflow responsibilities;
they do not establish qualified human revision or ISO conformity.

## User-supplied architecture proposal

*Local Translation for Mobile App User Guides: Verified Index Translate integration
and quality controls*, audited companion architecture, version 1.0, 28 October 2026,
and `Local_Translation_Architecture_Supporting_Files.zip`.

Relevant sections: model/deployment identity (§3), bounded gateway responsibilities
(§4), preparation and preservation (§5), prompt and response handling (§6), proposed
tool/gateway separation (§7), failure handling (§8), quality/human acceptance (§9),
privacy/provenance (§10), and staged implementation (§11).

The supporting OpenAPI describes a proposed gateway, not the official Index API.
Its schema assertions and constructed scenarios do not establish a live service.
The included original wrapper is the defective subject of an audit and is not
adopted. This package uses a bounded synchronous stdio MCP server rather than
claiming the proposal's full asynchronous asset registry, lease, cancellation,
authentication or distribution architecture has been built.

## Current upstream integration references

Use the deployment's actual pinned revisions and confirm API behavior before
production. These primary sources define upstream identities and interfaces:

- [Index-Translate repository](https://github.com/bilibili/Index-Translate): model
  family and local inference entry points.
- [Official text prompt builder](https://github.com/bilibili/Index-Translate/blob/912e86c8325d6c7c29a6a0b09c5f53482c6602f6/inference/llm/translate.py)
  and [prompt guide](https://github.com/bilibili/Index-Translate/blob/912e86c8325d6c7c29a6a0b09c5f53482c6602f6/docs/prompts.md):
  source/requirements messaging, not a guaranteed structural decoder.
- [Index-Translate-9B model card](https://huggingface.co/IndexTeam/Index-Translate-9B):
  declared model scope and inference examples, not acceptance of a user's locale pair.
- [vLLM OpenAI-compatible serving](https://docs.vllm.ai/en/stable/serving/openai_compatible_server/):
  runner request surface. This package additionally requires chat tokenization.

No translation-quality, capacity, latency, privacy or production qualification
result is inferred from those references or from package/schema validation.
