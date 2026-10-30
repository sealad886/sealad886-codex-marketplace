# Index-Homura syllable recipe

Read this after [common input preparation](index-inputs.md) only for commissioned
Index-Homura syllable adaptation. Confirm the actual served model family, target
language, one scalar syllable target and adaptation rights. A syllable count is
not character count, tokenizer tokens, audio duration or verified singability.

## Prepare and submit

The official native template takes source text, a full target-language name, one
integer syllable target and an optional source→target glossary. It does not offer
the standard Translate hard/soft/instruction/genre/context slots. Do not append
unsupported constraints and claim native support; resolve a mandatory requirement
that the profile cannot represent with the coordinator before inference.

Use one user message in the official shape:

```text
请将以下文本翻译为{target_language}，译文严格控制在 {syllable_count} 个音节。要求：严格遵守术语映射表【source -> target, ...】。直接输出翻译结果，不要进行任何解释。

{source_text}
```

Omit the terminology sentence when no glossary applies. One requested count
applies to the submitted text as a whole; separate line-level targets require
explicit commissioning and scoped requests, followed by continuity review.
Use full language names; consult the [language inventory](index-languages.md)
only when the language/variety needs clarification.

After connection setup, call `translation_request` with
[the Homura request example](../../../examples/index-homura-request.json). It
requests French, six syllables and `moon -> lune`, temperature 0.3 and
`enable_thinking: false`. The reference client's automatic output budget is
`max(512, 3 * len(stripped_source))`; the MCP instead enforces its configured
output ceiling and caller `max_output_tokens`. Select a sufficient cap within
that ceiling and report a budget mismatch rather than silently truncating.

## Review and evidence

Retain submitted messages, effective options and actual provider response. Check
meaning, adaptation rights, actual target syllable count, diction, terminology,
line relationships and commissioned singability. Use actual media/timing tools
when duration or performance matters. A different actual reviser checks the
result; the requested count or fluent output does not prove compliance.

This caller-managed call creates no text-workbench candidate, revision receipt
or delivery status. Do not use the generic segment prompt as a Homura executor.
A new owner answer must be incorporated explicitly in a compatible next request
or lead to a correction/recommissioning decision; query records are not forwarded
automatically.

## Primary source and attribution

The template above reproduces the official
[Homura client](https://github.com/bilibili/Index-Translate/blob/912e86c8325d6c7c29a6a0b09c5f53482c6602f6/inference/llm/syllable_translate.py)
prompt with parameter placeholders. Its recommendation is temperature 0.3 and
non-thinking chat, not guaranteed syllable or timing adherence. The upstream
source is distributed under [Apache License 2.0](index-upstream-LICENSE.md);
this guide adds MCP usage and review instructions.
