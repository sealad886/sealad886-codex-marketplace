# WooCommerce store extensions: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use WooCommerce CRUD/query APIs for orders rather than hardcoding wc_orders or posts storage; HPOS configuration changes physical tables.

- Classic woocommerce_checkout_fields hooks do not cover every Checkout Block extension; use the supported block/store API integration when applicable.

- WordPress nonces mitigate CSRF but do not authenticate/authorize; check capabilities and object ownership separately.

- Check input existence/type, unslash where required, validate business constraints, sanitize stored values, and escape output for its context.

- A REST permission_callback returning true is suitable only for intentionally public data; map products/orders to stable response schemas rather than exposing internal objects.

- Price-display filters do not change server-authoritative cart/checkout prices; payment/order state must come from trusted server logic.

- Order status hooks can run more than once; external fulfillment/payment actions need idempotency and durable failure handling.

- Use transients/object cache with invalidation and scope; cached false and cache miss semantics require care. Never execute real purchases/refunds under a code-review task.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [HPOS uses WooCommerce CRUD/data stores over configurable order storage.](https://developer.woocommerce.com/docs/features/high-performance-order-storage/)
- [WordPress nonces are not authentication or authorization.](https://developer.wordpress.org/apis/security/nonces/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
