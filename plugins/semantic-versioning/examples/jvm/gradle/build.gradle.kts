plugins { `java-library`; `maven-publish` }
java { toolchain { languageVersion.set(JavaLanguageVersion.of(17)) } }
publishing { publications { create<MavenPublication>("library") { from(components["java"]) } } }
