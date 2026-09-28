#!/usr/bin/env python3
"""Verify example package identity after native builds in a disposable copy."""
import argparse
import json
from pathlib import Path
import tarfile
import xml.etree.ElementTree as ET
import zipfile


def check(family: str, root: Path) -> None:
    if family == "javascript":
        with tarfile.open(root / "semver-example-js-0.1.0.tgz") as archive:
            metadata = json.load(archive.extractfile("package/package.json"))
            assert metadata["version"] == "0.1.0"
            assert metadata["name"] == "semver-example-js"
    elif family == "python":
        with zipfile.ZipFile(next((root / "dist").glob("*.whl"))) as archive:
            metadata = archive.read(next(n for n in archive.namelist() if n.endswith("/METADATA"))).decode()
            assert "Version: 0.1.0\n" in metadata
            assert "Name: semver-example-python\n" in metadata
        with tarfile.open(next((root / "dist").glob("*.tar.gz"))) as archive:
            metadata = archive.extractfile(next(n for n in archive.getnames() if n.endswith("/PKG-INFO"))).read().decode()
            assert "Version: 0.1.0\n" in metadata
    elif family == "rust":
        import tomllib
        with tarfile.open(root / "target/package/semver-example-core-0.1.0.crate") as archive:
            metadata = tomllib.loads(archive.extractfile("semver-example-core-0.1.0/Cargo.toml").read().decode())
            assert metadata["package"]["version"] == "0.1.0"
            assert metadata["package"]["name"] == "semver-example-core"
    elif family == "jvm":
        with zipfile.ZipFile(root / "target/semver-example-0.1.0.jar") as archive:
            metadata = archive.read("META-INF/maven/com.example/semver-example/pom.properties").decode()
            assert "version=0.1.0" in metadata
        node = ET.parse(root / ".flattened-pom.xml").getroot()
        assert node.find("{http://maven.apache.org/POM/4.0.0}version").text == "0.1.0"
    elif family == "dotnet":
        with zipfile.ZipFile(next((root / "bin/Release").glob("*.nupkg"))) as archive:
            metadata = ET.fromstring(archive.read(next(n for n in archive.namelist() if n.endswith(".nuspec"))))
            values = {element.tag.rsplit("}", 1)[-1]: element.text for element in metadata.iter()}
            assert values["version"] == "0.1.0"
            assert values["id"] == "SemverExample"
    print(f"{family}: packaged version 0.1.0 verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("family", choices=["javascript", "python", "rust", "jvm", "dotnet"])
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    check(args.family, args.root)
