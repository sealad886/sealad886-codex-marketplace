# Swift, Apple, Android, and Flutter

Read when platform applications or Swift packages have both release and build identities.

## Sources and ownership

Swift packages ordinarily use Git SemVer tags; Package.swift does not contain the package's own release version. Apple applications use MARKETING_VERSION / CFBundleShortVersionString for the marketing release and CURRENT_PROJECT_VERSION / CFBundleVersion for the build. Android uses user-facing versionName and monotonically increasing integer versionCode. Flutter's `version: 0.1.0+1` maps release/build components into platform metadata.

Store rules constrain allowed syntax and build-number reuse. SemVer prerelease identifiers cannot simply be inserted into every platform field. Keep release channels and build counters explicit. A build retry may require a new platform build number without changing public release impact.

## Examples and checks

[Platform configurations](../../examples/mobile/Version.xcconfig) are fragments for an existing app; attach the xcconfig to relevant configurations and verify generated plist values. [Swift library](../../examples/mobile/swift/Package.swift) is buildable with `swift build --package-path swift` from the mobile directory.

Apple: inspect `xcodebuild -showBuildSettings` and the built bundle's Info.plist, including extensions. Android: use the existing Gradle wrapper to assemble/bundle, then inspect the final APK/AAB manifest using platform tooling. Flutter: use native `flutter build` for the target and inspect resulting platform artifacts. Check flavor/scheme overrides. Source values alone do not prove shipped metadata.

Signing, store upload, device installation, and release submission require their own authorization. Honor physical-device-only repository rules. Distribution recipes do not prove store acceptance or runtime compatibility.

## Sources

[Swift package creation](https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html), [Apple build settings](https://developer.apple.com/documentation/xcode/build-settings-reference), [Android versioning](https://developer.android.com/studio/publish/versioning), [Flutter Android releases](https://docs.flutter.dev/deployment/android).
