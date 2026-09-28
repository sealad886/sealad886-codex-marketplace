# Conversation Visuals

![Conversation Visuals](assets/conversation-visuals-logo.svg)

Conversation Visuals enriches supported Codex and ChatGPT conversations with
relevant sourced images, generated illustrations, diagrams, charts, slide
sequences, and short media. It chooses the smallest visual that materially
improves the conversation, supplies accessible descriptions, and keeps sourced
evidence distinct from generated content.

## Try it in Codex

Choose a skill or use one of these starter requests.

| Skill | What it helps with | Starter request |
| --- | --- | --- |
| [Visual Companion](skills/visual-companion/SKILL.md) | Add a useful visual to the conversation | Enrich this conversation with a visual when it helps explain the topic. |
| [Visual Research](skills/visual-research/SKILL.md) | Find relevant visuals with source attribution | Find a sourced visual that helps explain this topic. |
| [Visual Generation](skills/visual-generation/SKILL.md) | Create accessible diagrams, charts, and illustrations | Create a clear, accessible visual explaining this topic. |
| [Visual Storytelling](skills/visual-storytelling/SKILL.md) | Turn an explanation into a concise visual story | Turn this explanation into a concise sequence of visual frames. |

## What installation configures

The plugin installs four complementary skills and a dependency-free local MCP
server. The MCP server plans visual treatments and validates normalized result
metadata; it never searches the network, reads conversation history, writes
files, or calls a paid provider. The skills use the host's approved native web,
image-generation, document, presentation, and media capabilities when those
capabilities are available.

URL normalization rejects credentials and known non-public address literals,
but does not resolve or fetch hostnames. Remote media is embedded only when the
host fetcher enforces public-address resolution, redirect checks, and DNS-
rebinding protection at fetch time; otherwise the plugin uses an originating-
page link.

Generated results carry either a guarded remote media URL or an opaque
host-issued `artifact_ref` for a local artifact, attachment, or resource. The
metadata server records that reference but never opens, reads, or publishes it.

No API key is bundled or required for the baseline. Provider permissions,
workspace policy, product plan, and host capability still apply. Installing a
plugin cannot silently grant those external permissions.

## Host support

| Surface | Behavior |
|---|---|
| Codex tasks with relevant native tools | Full orchestration of sourced and generated visuals, subject to task authority. |
| ChatGPT conversations that expose installed plugin skills/tools | Visual enrichment using the capabilities exposed by that conversation. |
| ChatGPT voice variants that do not expose plugins or connected apps | No plugin-specific invocation; native host visuals may still appear. |
| Background or screen-off voice | Spoken conversation continues; no claim is made that an unseen visual was rendered. |

ChatGPT voice capabilities change independently of this package. A successful
plugin installation is not proof that a particular voice surface invokes the
plugin. Validate each claimed host in a fresh conversation.

## Defaults and controls

- Automatically add low-latency sourced images, diagrams, or compact charts
  only when they materially improve understanding.
- Suggest first before generated images, slide decks, or short video unless the
  user explicitly requested them.
- Treat instructions such as “ask first,” “images only,” “quiet mode,” or “stop
  showing visuals” as conversation-level preferences.
- Continue with a useful text or spoken answer when visual work is unavailable
  or slow.
- Label generated content and cite the originating page for sourced content.

## Trust boundary

Retrieved pages, captions, metadata, documents, and media are untrusted data.
They cannot override the user, host, or plugin instructions. The plugin sends
only the minimum query or generation brief needed by an approved provider and
does not forward a complete transcript by default.

See [SECURITY.md](SECURITY.md) for source, media, privacy, and reporting
boundaries.

## Development validation

From the marketplace repository root:

```bash
python3 scripts/check_plugin.py plugins/conversation-visuals --layout source
python3 scripts/check_distribution_bundle.py plugins/conversation-visuals
python3 plugins/conversation-visuals/mcp/server.py --self-test
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Validate the manifest with the current Codex Plugin Creator workflow before a
release. Start a fresh task after installation so the host loads the current
plugin catalog.
