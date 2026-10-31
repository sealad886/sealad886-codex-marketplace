# Expo React Native TypeScript: implementation guidance

## Stack and state

Preserve JavaScript or TypeScript and the existing router; Expo Router uses React
Navigation but neither router is mandatory for every app. TypeScript types are not
runtime validation. React 19 removed function-component propTypes checking, so do
not recommend PropTypes as universal JavaScript runtime validation. State, reducers,
Context, and external stores solve different ownership problems; Context is not
a blanket performance replacement for useState/useEffect. Native accessibility
props differ from web ARIA. Handle insets with react-native-safe-area-context and
avoid duplicating padding already applied by navigation containers.

## Images, performance, and delivery

Use SDK-compatible expo-image or the established supported image module rather
than introducing react-native-fast-image blindly into Expo Go. Profile FlatList
window/batch/clipping options; removeClippedSubviews can produce missing-content
issues and is not a universal optimization. Memoization/callback extraction needs
a measured identity/rendering reason. React Suspense alone does not provide native
bundle code splitting, and Web Vitals describe web rendering rather than native
responsiveness. EXPO_PUBLIC variables and app config are bundled public data;
expo-constants is not a secret store. EAS builds/updates require correct native
runtime compatibility, signing/channel controls, and explicit publication authority.

## Primary documentation

- [Public environment variable bundling](https://docs.expo.dev/guides/environment-variables/).
- [Expo-compatible image API](https://docs.expo.dev/versions/latest/sdk/image/).
- [Function component propTypes removal](https://react.dev/blog/2024/04/25/react-19-upgrade-guide).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
