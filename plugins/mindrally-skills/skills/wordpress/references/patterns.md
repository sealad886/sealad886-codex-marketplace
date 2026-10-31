# WordPress plugin and theme boundaries: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Do not edit WordPress core or a dependency plugin to implement an extension; use hooks, a maintained plugin, or appropriate theme overrides.

- Nonces help with CSRF but are neither one-time replay prevention nor authorization; require current_user_can and resource checks.

- Use wpdb prepare with the documented placeholder/identifier support for the installed version; escaping is not equivalent to validation.

- Choose PHP syntax from the actual minimum supported target; strict_types can affect callback coercion and should not be imposed blindly.

- dbDelta has formatting/alteration constraints and does not implement every migration safely; version and test schema changes explicitly.

- WP-Cron scheduling is traffic-triggered by default and not a guaranteed precise/durable worker; use supported scheduling and deployment infrastructure for the need.

- Classic WooCommerce template overrides normally belong under the child theme’s woocommerce directory; a plugin/woocommerce folder alone is not automatically loaded. Block themes differ.

- Use enqueue/i18n APIs and deliberate transient invalidation; logs are diagnostics, not error handling, and must not expose sensitive data.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Nonces must not replace authentication/capability authorization.](https://developer.wordpress.org/apis/security/nonces/)
- [Classic template overrides use child-theme woocommerce paths and differ from block themes.](https://developer.woocommerce.com/docs/theming/theme-development/template-structure/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
