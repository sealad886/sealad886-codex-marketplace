# NativeLong / Index-Nailong document recipe

Read this after [common input preparation](index-inputs.md) only when the
commission requires NativeLong full-document translation. The published model
IDs use `Index-Nailong-2B` and `Index-Nailong-9B`. Confirm the actual served family
and the exact supported direction: Chinese→English, English→Chinese,
Chinese→Japanese or Japanese→Chinese. This profile consumes a complete document;
independent segment translation is not its native workflow.

## Execution boundary in this plugin

The existing `translation_request` transport is bounded and non-streaming. It
cannot express the full official NativeLong decoding profile: negative `top_k`,
`stop_token_ids`, `ignore_eos` and streaming are not supported request fields.
Do not drop or approximate these controls and claim an official-equivalent run.
Do not substitute string stops for token IDs. There is no native profile executor,
input-builder tool or workbench document mode in this release.

If the commission requires the official document workflow, report the gap to the
coordinator and obtain a suitable separately authorized executor. Do not submit
a generic workbench job or invent a delivery receipt. A permitted experimental
partial-profile request must be explicitly commissioned as such and cannot be
represented as full NativeLong support.

## Prepare the fixed direction-specific input

Select exactly one template below. Replace only its final source placeholder
with the complete commissioned document. Preserve the constraints-before-source
ordering, chapter/paragraph sequence and full document. The official client uses
one user message and `enable_thinking: false`. These fixed templates have no
separate general glossary/context/hard-soft input slots. Resolve a mandatory
extra requirement rather than quietly removing it or modifying the template and
claiming that modification is native support.

### Chinese to English

```text
请将以下中文小说翻译成英语，并且严格遵循所有约束要求。

这是一段长篇连续文本，请完整处理全部内容，并在全文范围内保持译名和表达一致。

【约束要求】

1. 完整翻译所有内容，不要遗漏、概括、合并或添加内容。
2. 保持人名、地名、称谓和术语在全文中一致。
3. 保持原文的章节、段落和内容顺序。

只输出译文，不要有任何额外说明。

【源文】

（在这里放入需要翻译的完整中文原文）
```

### English to Chinese

```text
请将以下英文小说翻译成中文，并且严格遵循所有约束要求。

这是一段长篇连续文本，请完整处理全部内容，并在全文范围内保持译名和表达一致。

【约束要求】

1. 完整翻译所有内容，不要遗漏、概括、合并或添加内容。
2. 保持人名、地名、称谓和术语在全文中一致。
3. 保持原文的章节、段落和内容顺序。

只输出译文，不要有任何额外说明。

【源文】

（在这里放入需要翻译的完整英文原文）
```

### Chinese to Japanese

```text
请将以下中文小说翻译成日语，并且严格遵循所有约束要求。

这是一段长篇连续文本，请完整处理全部内容，并在全文范围内保持译名和表达一致。

【约束要求】

1. 完整翻译所有内容，不要遗漏、概括、合并或添加内容。
2. 保持人名、地名、称谓和术语在全文中一致。
3. 保持原文的章节、段落和内容顺序。

只输出译文，不要有任何额外说明。

【源文】

（在这里放入需要翻译的完整中文原文）
```

### Japanese to Chinese

```text
请将以下日文小说翻译成中文，并且严格遵循所有约束要求。

这是一段长篇连续文本，请完整处理全部内容，并在全文范围内保持译名和表达一致。

【约束要求】

1. 完整翻译所有内容，不要遗漏、概括、合并或添加内容。
2. 保持人名、地名、称谓和术语在全文中一致。
3. 保持原文的章节、段落和内容顺序。

只输出译文，不要有任何额外说明。

【源文】

（在这里放入需要翻译的完整日文原文）
```

## Reference decoding profile

The upstream document client specifies these controls. This is reference metadata,
**not an accepted `translation_request` argument object**:

```json
{
  "temperature": 0,
  "top_p": 1,
  "top_k": -1,
  "min_p": 0,
  "presence_penalty": 0,
  "repetition_penalty": 1,
  "seed": 42,
  "stop_token_ids": [248044, 248046],
  "ignore_eos": false,
  "stream": true,
  "chat_template_kwargs": {"enable_thinking": false}
}
```

The reference client omits `max_tokens` by default; the MCP requires a bounded
output budget. Do not infer that this transport can produce the complete document
because a source fits its character limit. Both actual tokenized input and enough
output must fit a suitable executor's verified context/capacity.

## Review and attribution

After any separately commissioned execution, retain the exact complete input,
actually applied decoding controls, termination evidence and output identity.
A different reviser checks chapter/paragraph coverage, omissions/additions,
consistent entities and terminology across the whole document, references,
continuity and meaning. Formatting a template or reaching an end marker does not
establish completeness or human acceptance.

The four templates are reproduced unchanged from the official
[direction-template directory](https://github.com/bilibili/Index-Translate/tree/912e86c8325d6c7c29a6a0b09c5f53482c6602f6/inference/llm/prompts).
The [document client](https://github.com/bilibili/Index-Translate/blob/912e86c8325d6c7c29a6a0b09c5f53482c6602f6/inference/llm/doc_translate.py)
defines decoding and request behavior. These upstream excerpts retain
[Apache License 2.0](index-upstream-LICENSE.md); this guide adds execution limits
and review instructions. No model weights are bundled or qualified by this text.
