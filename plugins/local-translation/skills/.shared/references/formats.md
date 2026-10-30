# Product and format boundaries

## Implemented document path

The installed tool receives UTF-8 plain text through `source_text` or an explicit
`segments` array through MCP. It keeps only temporary session artifacts and
returns translated content through MCP. The calling agent handles any authorized
source-file reading and result retention. Stable segment identifiers preserve
source-target linkage.
The tool does not parse, reconstruct, render or validate arbitrary Markdown,
HTML, PDF, DOCX, slide decks, Android XML, Apple string catalogs or ICU messages.
Placeholders/number checks cover defined patterns; they are structural heuristics,
not a complete document parser, token budget guarantee or proof of fidelity.

For another format, use a separately verified extraction/reconstruction tool only
within the user's scope. Inventory body text, tables, footnotes, image labels,
comments and other meaningful content; compare extracted content to the original.
Freeze the resulting supported source. After translation, reconstruct and inspect
the actual rendered deliverable. Do not describe text output as a completed PDF
or app localization file. Platform string grammars need their own parser and tests.

For mobile guides, bind the brief to actual app build and localized UI resources.
A product reviewer follows representative steps against that build. Protect
literal code, paths, links and arguments through an appropriate preparation route.
Do not translate a code block or change an action/measurement to make prose flow.

## Conditional audiovisual path

The whitepaper's prerecorded audiovisual workflow (pp. 10–12) remains a useful
role and handoff model. This plugin does not implement a media pipeline. A request
for any product below must first supply the exact media/reference versions and
the additional tools/review capacity it needs:

| Requested product | Governing reference and additional acceptance |
| --- | --- |
| Transcript/dialogue list | Verify actual speech/speakers against recording; preserve uncertainty |
| Interlingual subtitles | Original audio/picture, approved adaptation, events/timing and full watchback |
| Same-language captions/SDH | Selected soundtrack, meaningful non-speech audio and speaker information |
| Translated accessibility captions | Original context plus target accessibility specification |
| Captions for a dub | Final dubbed performance and picture, not merely original-dialogue translation |
| Forced narrative track | Selected essential dialogue/on-screen information and player selection rules |

The source-language proofer verifies the spoken source. The spotter/template
editor supplies timed events and annotations. The translator adapts within the
approved constraints; the accessibility specialist authors required information.
The independent reviser compares against media; the subtitle engineer validates
the delivery profile and conforms the exact cut. Final playback/player testing
checks the actual delivered track. Character-per-line or reading-speed limits are
project/platform rules, not universal constants.

If these inputs or capabilities are absent, produce a clearly labeled text-only
translation candidate from an already verified transcript and list the missing
work. Do not invent transcription certainty, timing, accessibility cues, media
conformance or playback results. Pivot text needs original-language access or an
explicit limitation; a subtitle template is not necessarily a verbatim transcript.
