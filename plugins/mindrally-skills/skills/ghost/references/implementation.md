# Ghost CMS Theme Development: implementation guidance

## Templates and assets

Use layouts/partials and supported helper context; keep ghost_head and ghost_foot
in their expected layout positions. Do not place Handlebars expressions in an
ordinary external CSS file and expect Ghost to interpolate it. Use documented
accent-color/theme variables or template-generated configuration. Tailwind/Alpine
are optional and their build/API versions must match. Configure image sizes before
using img_url size names, provide meaningful alt text or empty decorative alt,
dimensions, srcset/sizes, and avoid lazy-loading the key above-the-fold image blindly.

## Membership, metadata and validation

Use the post access/visibility model and content helper behavior for entitlements;
@member.paid alone does not represent every tier/post-access rule. Avoid exposing
private content through theme/API/cache paths. Portal/member form attributes need
complete loading/error/accessibility states. ghost_head supplies substantial metadata;
avoid duplicate/conflicting JSON-LD. HTML escaping of Handlebars text is not the
same as JSON string escaping in script content, so construct structured data safely.
Validate the actual engines constraint, package assets and current gscan checks.
Theme validation does not prove installed-site membership or visual correctness;
site changes/publication require authorization.

## Primary documentation

- [Post access, visibility and content helper behavior](https://docs.ghost.org/themes/members).
- [Theme helper contracts](https://docs.ghost.org/themes/helpers).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
