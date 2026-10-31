# Stripe payment and subscription integrity: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Derive amount/currency/price from trusted server-side order/catalog state; never accept a client-supplied amount as payment authority.

- Bind Stripe customer and subscription IDs to the authenticated application account. Looking up a customer by email alone does not prove ownership.

- Pin/test a supported API version matching the SDK and integration; blindly selecting latest or keeping a hardcoded 2023 example is unsafe.

- Initialize PaymentElement with the required supported Elements options/client secret or documented deferred flow; a bare provider is not sufficient for every integration.

- Use idempotency keys tied to stable business operations and protect duplicate/order concurrency at the application boundary.

- Verify webhook signatures over the raw body, deduplicate events, handle out-of-order delivery, and acknowledge only after durable processing/queueing.

- A redirect or client confirmation callback does not establish fulfillment entitlement; verify authoritative payment/subscription state and asynchronous events.

- Use framework-version-correct request header APIs and secret storage. Test-mode success does not prove live payment, tax, refund, or compliance acceptance.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [PaymentIntent lifecycle and idempotency must be tied to the purchase.](https://docs.stripe.com/payments/payment-intents)
- [Webhook signatures, duplicate handling, and delivery semantics require explicit processing.](https://docs.stripe.com/webhooks)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
