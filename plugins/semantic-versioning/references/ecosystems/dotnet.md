# .NET

Read when MSBuild or Git-version tooling publishes NuGet packages.

## Sources and ownership

`Version` supplies general package/product versioning; `PackageVersion` explicitly controls NuGet identity. Shared Directory.Build.props can centralize values, while project overrides and conditional properties affect evaluation. `AssemblyVersion` governs assembly identity and follows numeric CLR rules; `FileVersion` is a numeric file identifier; `InformationalVersion` may include source/build data. They need not all change in lockstep.

Git-derived tools such as Nerdbank.GitVersioning or MinVer own evaluated metadata when installed. Preserve that owner and inspect generated MSBuild properties. NuGet normalizes versions and does not treat arbitrary build metadata as a distinct publishable identity; confirm registry collision behavior before publication.

## Example and checks

[Shared props and project](../../examples/dotnet/Directory.Build.props) demonstrate a static owner and explicitly separate assembly identity. `dotnet pack --configuration Release` produces `SemverExample.0.1.0.nupkg`. Unzip its `.nuspec` and compare ID/version to the release record. `dotnet msbuild -getProperty:Version,PackageVersion,AssemblyVersion,FileVersion` verifies evaluated values with a compatible SDK.

Pin an SDK via the host project's global.json and selected CI SDK setup. Test package consumption from an isolated local NuGet feed. For multiple projects, identify which are packable and whether shared props imply a fixed release group; shared build settings alone do not establish that policy.

## Sources

[NuGet versioning](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning), [MSBuild pack properties](https://learn.microsoft.com/en-us/nuget/reference/msbuild-targets), [MinVer](https://github.com/adamralph/minver), [Nerdbank.GitVersioning](https://github.com/dotnet/Nerdbank.GitVersioning).
