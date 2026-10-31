# Drupal Development: implementation guidance

## Standards and extension points

Follow Drupal's own coding standards and the actual core/PHP compatibility matrix;
PSR-12 is not a replacement and PHP 8.1 is not a universal supported baseline.
Use the service container and supported discovery for the installed version,
including hooks where appropriate; do not impose repository wrappers over entities.
Use Entity/Field and database APIs with parameterized values. Entity query access
checking must be deliberate; access control is not automatically implied by using
an entity API. Route access and object-level permissions need explicit tests.

## Rendering, queues, and updates

Use render arrays/Twig with contextual escaping and proper cache tags, contexts,
and max-age, including access-result cacheability. Generic input sanitization
cannot replace output escaping or authorization. Form API handles its token and
validation lifecycle, but custom routes/webhooks need their own controls. Queue
processing has retry/duplicate semantics; effects should be safe to repeat.
Choose schema/update/post-update/configuration mechanisms for the type of change
and test upgrades against existing data. Preserve generated configuration ownership
and never import/export production configuration without task authority.

## Primary documentation

- [Drupal coding standards](https://www.drupal.org/docs/develop/standards/coding-standards).
- [Explicit entity-query access checking](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21Query%21QueryInterface.php/function/QueryInterface%3A%3AaccessCheck/11.x).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
