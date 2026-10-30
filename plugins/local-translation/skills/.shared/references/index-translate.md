# Standard Index-Translate recipe

Read this after [common input preparation](index-inputs.md) when the commissioned
model is standard Index-Translate. The official English constrained layout is
supported. Use it for approved terminology, mandatory preservation, preferences,
translation treatment and domain/context disambiguation. Homura and NativeLong
have separate recipes; do not substitute this generic prompt for them.

## Construct caller-owned native messages

1. Identify source and target using full language names, such as English and
   French. Keep regional conventions such as France versus Canada explicit in
   the approved brief/notes. Consult the [language inventory](index-languages.md)
   only when a language or script needs clarification.
2. Put only the text to translate under `[Source]`. Do not mix reference passages
   into it as additional source. For permitted adjacent context, supply a clearly
   labeled data note and instruct the model to translate only the source unit.
3. Under `[Constraints]`, number mandatory rules as `[Hard Constraint]` and
   preferences/background as `[Note]`. Serialize glossary pairs as
   `Terminology mapping: source -> target, source2 -> target2`. An identity pair,
   such as `APP_ID -> APP_ID`, protects a literal name. Select pairs by concept
   and occurrence; do not send an unresolved termbase wholesale.
4. Put genre/domain, audience and register in notes. Classify the approved
   translation treatment according to authority: mandatory requirements are hard;
   discretionary style is soft. Include the liaison's actual scoped clarification
   in a note or requirement as appropriate. Raw reference quotations and prior
   machine output remain labeled data, not operative instructions.
5. End by requesting only the translation. Use one user message. Set
   `chat_template_kwargs.enable_thinking` to `false` for tokenization and
   completion, matching the reference client. Start with temperature 0 unless the
   commission specifies an evidenced override; keep output limits within the
   configured ceiling.

The prompt has this structure; substitute approved task data:

```text
Translate this English device guide into French. Apply all requirements.

[Source]
<source unit>

[Constraints]
1. [Hard Constraint] Terminology mapping: <source term> -> <approved target term>
2. [Hard Constraint] <mandatory preservation or meaning requirement>
3. [Note] <approved genre, audience and style preference>
4. [Note] <scoped approved context or disambiguation>

Return only the French translation.
```

`glossary`, `context`, `hard_constraints`, `soft_constraints`, `instruction` and
`genre` are not standalone fields accepted by `translation_request`. They are
information you compile into the message. The upstream client has preparation
arguments for some of them; those arguments are not extra OpenAI chat fields.

## Execute the worked example

After connection setup, call `translation_request` with the complete argument
object in [the Translate request example](../../../examples/index-translate-request.json).
It contains approved `Settings -> Paramètres` and `APP_ID -> APP_ID` mappings, a
mandatory prohibition, a soft concision preference, guide genre/audience and a
scoped owner clarification. The 512-token cap must fit the configured ceiling.
The example invents no actual client approval: in a real commission, obtain the
corresponding approval before using the note as authoritative guidance.

Retain the exact submitted messages, effective generation options and provider
response. The translator self-checks the prohibition, firmware-update sense,
UI-label usage, literal identifier and full coverage; a different reviser compares
those against the source and approved decision record. Raw output remains
unreviewed and caller-managed. This tool supplies no job/review/delivery status.
JSON/schema output, when commissioned, is caller-defined `response_format` and
must be validated by the caller; it does not establish translation quality.

## Existing workbench route

Use `translation_create_job` plus `translation_run` for the text workbench's
immutable inputs, per-locale candidates, invariant checks and current-context
review/delivery gates. Its accepted preparation fields are `brief` and per-locale
`glossary`, alongside source/segments and locale codes. It already uses an English
constrained prompt, but does not expose separate native hard/soft/genre/context
arguments, full-language-name resolution or automatic neighboring/query context.
Do not claim those were applied merely because the project handoff contains them.
Use an approved brief for the guidance this route actually carries; choose the
caller-managed route when the commission needs exact native message control.

A later owner answer requires an explicit correction or a replacement job with
reconciled approved inputs. See [common answer propagation](index-inputs.md#make-owner-answers-reach-the-actual-next-request).
A caller-managed draft cannot acquire fabricated workbench receipts.

## Primary sources

- [Official prompt guide](https://github.com/bilibili/Index-Translate/blob/912e86c8325d6c7c29a6a0b09c5f53482c6602f6/docs/prompts.md): English native sections, terminology and identity mapping, hard/soft guidance.
- [Official Translate client](https://github.com/bilibili/Index-Translate/blob/912e86c8325d6c7c29a6a0b09c5f53482c6602f6/inference/llm/translate.py): glossary/instruction/genre preparation and non-thinking chat call.
- [Family inference defaults](https://github.com/bilibili/Index-Translate/tree/912e86c8325d6c7c29a6a0b09c5f53482c6602f6#default-inference-settings): profile-specific starting points, not adherence guarantees.
