#!/usr/bin/env python3
"""Read-only SemVer 2.0 validation, precedence, and baseline-based release checks."""
import argparse
import json
import re
import sys
from dataclasses import dataclass


PATTERN = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?", re.ASCII)


@dataclass(frozen=True)
class Version:
    core: tuple
    prerelease: tuple = ()

    @classmethod
    def parse(cls, value):
        match = PATTERN.fullmatch(value)
        if not match:
            raise ValueError(f"Invalid SemVer: {value!r}")
        pre = tuple((match[4] or "").split(".")) if match[4] else ()
        if any(p.isdigit() and len(p) > 1 and p.startswith("0") for p in pre):
            raise ValueError(f"Numeric prerelease identifier has a leading zero: {value!r}")
        return cls(tuple(int(match[i]) for i in (1, 2, 3)), pre)

    def compare(self, other):
        if self.core != other.core:
            return (self.core > other.core) - (self.core < other.core)
        if not self.prerelease or not other.prerelease:
            return (not self.prerelease) - (not other.prerelease)
        for left, right in zip(self.prerelease, other.prerelease):
            if left == right:
                continue
            if left.isdigit() and right.isdigit():
                return (int(left) > int(right)) - (int(left) < int(right))
            if left.isdigit() != right.isdigit():
                return -1 if left.isdigit() else 1
            return (left > right) - (left < right)
        return (len(self.prerelease) > len(other.prerelease)) - (len(self.prerelease) < len(other.prerelease))


def check(base, proposed, impact, pre1_policy):
    """Validate a target against cumulative impact from a supplied baseline."""
    old, new = Version.parse(base), Version.parse(proposed)
    major, minor, patch = old.core
    if impact == "none":
        expected = old.core
        valid = old.compare(new) == 0
    else:
        effective = "minor" if major == 0 and impact == "major" and pre1_policy == "minor" else impact
        expected = {"patch": (major, minor, patch + 1), "minor": (major, minor + 1, 0), "major": (major + 1, 0, 0)}[effective]
        # A prerelease baseline represents an already selected release target.
        # Promotion/iteration must retain that target; a different target needs
        # the preceding stable baseline to establish cumulative impact.
        if old.prerelease:
            expected = old.core
        valid = new.core == expected and new.compare(old) > 0
    return {"valid": valid, "baseline": base, "proposed": proposed,
            "impact": impact, "pre1_policy": pre1_policy,
            "expected_core": ".".join(map(str, expected)),
            "note": "Impact is supplied by the caller; this helper does not infer API compatibility. Prerelease baselines permit only iteration or promotion of the selected core."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit schema_version=1 JSON")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("versions", nargs="+")
    compare = commands.add_parser("compare")
    compare.add_argument("left")
    compare.add_argument("right")
    assess = commands.add_parser("check")
    assess.add_argument("baseline")
    assess.add_argument("proposed")
    assess.add_argument("--impact", choices=("none", "patch", "minor", "major"), required=True)
    assess.add_argument("--pre1-policy", choices=("minor", "semver"), default="minor")
    for command in (validate, compare, assess):
        command.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            for value in args.versions:
                Version.parse(value)
            result = {"valid": True, "versions": args.versions}
        elif args.command == "compare":
            result = {"precedence": Version.parse(args.left).compare(Version.parse(args.right)), "left": args.left, "right": args.right}
        else:
            result = check(args.baseline, args.proposed, args.impact, args.pre1_policy)
        code = 0 if result.get("valid", True) else 1
    except ValueError as error:
        result, code = {"error": str(error)}, 2
    envelope = {"schema_version": 1, "command": args.command, **result}
    print(json.dumps(envelope, indent=2) if args.json else "\n".join(f"{key}: {value}" for key, value in result.items()))
    return code


if __name__ == "__main__":
    sys.exit(main())
