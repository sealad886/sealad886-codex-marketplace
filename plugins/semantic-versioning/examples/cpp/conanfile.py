from conan import ConanFile
class ExampleRecipe(ConanFile):
    name = "semver-example"
    version = "0.1.0"
    package_type = "shared-library"
    settings = "os", "arch", "compiler", "build_type"
# Configuration fragment: add CMake build/package methods before distribution.
