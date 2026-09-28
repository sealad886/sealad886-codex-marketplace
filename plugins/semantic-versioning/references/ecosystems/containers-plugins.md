# Containers, Helm, and plugins

Read when releases produce images, charts, or installable plugin bundles.

## Sources and ownership

OCI tags are mutable names; content digests identify immutable images. Preserve the source commit, release version, platform set, and resulting manifest digest. Attach standard OCI version/revision labels; labels alone do not prove image contents. A multi-platform index has its own digest in addition to platform-image digests.

Helm Chart.yaml `version` identifies the chart package and follows SemVer; `appVersion` describes the application and is an independent string. Quote appVersion. Chart changes may require a chart release even when the image version stays unchanged. Prefer image digests in deployed values where operational policy requires immutable deployment.

Codex plugin manifests contain plugin name/version; a marketplace release reference identifies distribution. Keep source manifest, archive manifest, tag, and catalog reference consistent. A cached installation identity is separate from the source checkout. Use the repository's plugin packaging/validation workflow.

## Examples and checks

[Helm chart](../../examples/containers-plugins/chart/Chart.yaml): run `helm lint chart`, `helm template check chart`, and `helm package chart`; inspect Chart.yaml in the resulting archive. The Dockerfile packages only a text file into a scratch image and demonstrates labels without introducing a moving base-image tag. Build with explicit VERSION and REVISION arguments; inspect image labels and digest. It is a data image, not a runnable application.

The plugin-manifest.json file is a naming/version fragment, not a complete installable plugin. Put adopted metadata in `.codex-plugin/plugin.json`, supply required skill/assets structure, and run canonical plugin validators. Hosted chart/image/plugin publication remains an unverified path until exercised with authorized real targets.

## Sources

[OCI annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md), [Helm charts](https://helm.sh/docs/topics/charts/), [Helm registries](https://helm.sh/docs/topics/registries/).
