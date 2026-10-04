# Frontend experience across targets

Grounding: [R06–R07, R28, R30](research.md). Keep existing framework and design system. Use Vite for a new uncomplicated SPA when appropriate; do not mandate React, shadcn or a meta-framework. Tauri serves static output, so SSR frameworks need a supported static-export mode or a separately designed remote service.

Choose user task, layout and interaction states before components. Share domain flows across targets while adapting navigation, density and input to actual platform. Keep IPC calls in the owning service rather than scattered render effects; loading, empty, error, permission-denied, offline and retry states must be visible and testable. Browser-only fallback must not report fictitious native success.

## Interaction review

Check desktop keyboard traversal, shortcuts, focus restoration, dialogs, resize, zoom and multiple windows where supported. Check touch target sizes, safe areas, orientation, virtual-keyboard occlusion, scroll ownership, back navigation and foreground/background recovery on mobile. Use semantic controls, accessible names, visible focus, screen-reader reading order, contrast, reduced motion and text scaling. Verify these in the actual WebView because Chrome preview does not establish WebKit behavior.

Custom titlebars/drag regions must preserve usable controls; grant only the window command permissions actually invoked. Keep native titlebar/menu behavior where it fits. CSS blur is not evidence of native Liquid Glass. If genuine native material or extension work is requested, isolate that integration and test it separately.

## Rendered validation loop

Define entry → interaction → expected visible state. Discover existing dev server and exact URL from scripts/process evidence. When an available browser capability is used, read its skill and use its documented runtime; otherwise use configured project browser tests or an available Playwright workflow. Record fallback and limitations. A browser inspection tool is optional, not a hidden prerequisite.

Before and after the change check correct page, meaningful content, absence of build overlay, relevant console errors, target interaction and a fresh screenshot. Use semantic locators or accessible identifiers, not stale screenshot coordinates. Inspect narrow mobile and desktop layouts where changed. For native-dependent flows repeat against a real packaged app with IPC and permissions active; keep mocked evidence labeled.

For React, inspect effect dependencies, state ownership, async cleanup and expensive rerenders before memoization. For any framework, lazy-load expensive optional features where measured or obvious to startup cost; avoid redundant caches/wrappers. Reuse existing components without importing another design system. Stripe, Supabase and similar integrations require actual requested service design, server-side authorization and primary version-specific docs; they are not standard Tauri dependencies.
