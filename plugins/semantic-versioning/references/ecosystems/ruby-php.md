# Ruby and PHP

Read when gems or Composer libraries release from constants or tags.

## Sources and ownership

Ruby gems commonly source `spec.version` from a module VERSION constant. The gemspec is executable Ruby; read-only discovery must report expressions rather than evaluate them. Bundler's lockfile records resolved dependencies. Gem::Version comparison is ecosystem-specific; test prerelease representation against RubyGems.

Composer ordinarily derives package versions from VCS tags. Avoid an explicit composer.json version for a tag-managed library because it creates drift. Composer constraints and branch aliases are not independent release versions. composer.lock describes an installed dependency graph; library and application lockfile policies differ.

## Examples and checks

[Gem and Composer examples](../../examples/ruby-php/semver_example.gemspec). `gem build semver_example.gemspec` produces `semver_example-0.1.0.gem`; `gem specification semver_example-0.1.0.gem version` verifies packaged metadata. Test loading it from a disposable GEM_HOME before publication.

`composer validate --strict` validates the PHP manifest; `composer archive --format=zip` packages it locally. `php -l src/Greeting.php` checks syntax. A local archive without release tags does not prove registry-derived version metadata. For Packagist or a private Composer repository, confirm the immutable tag and read back the indexed version after authorized publication.

Observe existing release tools and automation. Do not rewrite all constants or tags simply because they resemble a version; identify the actual package owner first.

## Sources

[RubyGems specification](https://guides.rubygems.org/specification-reference/), [RubyGems patterns](https://guides.rubygems.org/patterns/), [Composer version field](https://getcomposer.org/doc/04-schema.md#version), [Composer versions](https://getcomposer.org/doc/articles/versions.md).
