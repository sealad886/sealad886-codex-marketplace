# Ionic Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## UI and navigation

- Choose Ionic Angular/React/Vue routing APIs according to the project; NavController examples are Angular-specific.
- Use ion-header/content/footer structure and supported component theming; inspect shadow parts where CSS variables are insufficient.
- Cached routed pages have Ionic lifecycle behavior beyond ordinary component mount/unmount; clean subscriptions in the appropriate owner.

## Native integration and performance

- Capacitor is the current official Ionic native runtime; existing Cordova integrations require their own supported plugin checks.
- Use supported Capacitor plugins such as @capacitor/camera only when selected; configure permissions and cancellation/error handling.
- Do not recommend removed ion-virtual-scroll; use a maintained framework-compatible virtualizer when long-list measurements justify one.
- Test hardware back behavior, keyboard insets, screen-reader focus, offline behavior, and platform build configuration.

## Primary documentation

- [Ionic Angular overview](https://ionicframework.com/docs/angular/overview) — Capacitor is Ionic Angular’s official native runtime; integration versions are framework-specific.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
