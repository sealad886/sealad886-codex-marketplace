require_relative "lib/semver_example/version"
Gem::Specification.new do |spec|
  spec.name = "semver_example"
  spec.version = SemverExample::VERSION
  spec.summary = "Semantic version reference"
  spec.authors = ["Example"]
  spec.license = "MIT"
  spec.files = Dir["lib/**/*.rb"]
  spec.require_paths = ["lib"]
end
