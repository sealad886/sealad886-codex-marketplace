# Java and Kotlin

Read when Maven or Gradle builds publish JVM artifacts.

## Sources and ownership

Maven may use literal `project.version`, an inherited parent, or supported CI-friendly placeholders `${revision}`, `${sha1}`, `${changelist}`. Resolve the effective model before selecting an owner. Parent/child versions and dependency references must agree. A `-SNAPSHOT` is a mutable development coordinate, not an immutable stable release.

Gradle commonly takes `version` from gradle.properties, a build script, or a Git-version plugin. Both Groovy `version = '0.1.0'` and Kotlin `version = "0.1.0"` are executable configuration; static inspection must not guess evaluated values. Kotlin multiplatform can emit many publications from one logical release.

## Example and checks

[Maven example](../../examples/jvm/pom.xml) uses `${revision}` and a pinned flatten plugin so consumer POMs contain concrete coordinates. `mvn -B package` builds the JAR; `mvn help:evaluate -Dexpression=project.version -q -DforceStdout` resolves the source version. Inspect the flattened POM and JAR `META-INF/maven` metadata before deployment. For a multi-module reactor use `${revision}` in parents and `${project.version}` for synchronized sibling dependencies; inspect each deployed POM.

[Gradle alternative](../../examples/jvm/gradle/build.gradle.kts) uses gradle.properties as source. Adopt through a checked Gradle wrapper; `bash ./gradlew jar generatePomFileForLibraryPublication` produces the JAR and publication POM. This fixture omits wrapper binaries deliberately; use an installed compatible Gradle for local checks. Validate API/binary compatibility separately; successful compilation does not prove old consumers remain compatible.

## Sources

[Maven CI-friendly versions](https://maven.apache.org/guides/mini/guide-maven-ci-friendly.html), [Gradle Maven Publish](https://docs.gradle.org/current/userguide/publishing_maven.html), [Gradle project properties](https://docs.gradle.org/current/userguide/project_properties.html).
