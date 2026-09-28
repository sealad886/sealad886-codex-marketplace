#!/usr/bin/env python3
"""Validate authored semantic route contracts without claiming delivery behavior."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path


ALLOWED_SCALES = {
    "large",
    "medium",
    "medium-or-large",
    "risk-dependent",
    "small",
    "small-or-medium",
}
ALLOWED_RISKS = {
    "critical",
    "high",
    "low",
    "low-or-risk-dependent",
    "medium",
    "medium-or-high",
    "risk-dependent",
}
ALLOWED_AUTHORITIES = {
    "change",
    "coordination-only",
    "design-only",
    "documentation-change",
    "incident",
    "planning-only",
    "report-only",
    "release-preparation",
    "release-execution",
    "review-only",
}
REQUIRED_SCENARIO_FIELDS = {
    "accepted_risks",
    "accepted_scales",
    "id",
    "prompt",
    "profile_id",
    "scale",
    "risk",
    "authority",
    "lead_capability",
    "required_capabilities",
    "conditional_capabilities",
    "precedence",
    "allowed_reentry",
    "forbidden_capabilities",
    "expected_artifacts",
    "required_evidence",
    "stop_conditions",
}
OPTIONAL_SCENARIO_FIELDS = {
    "required_final_after",
    "required_reentry",
    "required_reentry_after",
    "required_reentry_before",
}
ALLOWED_SCENARIO_FIELDS = REQUIRED_SCENARIO_FIELDS | OPTIONAL_SCENARIO_FIELDS
CONTRACT_TOP_LEVEL_FIELDS = {
    "comparison_policy",
    "evidence_class",
    "forbidden_runtime_dependencies",
    "limitations",
    "runtime_profile_source",
    "scenarios",
    "schema_version",
}
CONTRACT_CONDITIONAL_FIELDS = {"skill", "when"}
PROFILE_TOP_LEVEL_FIELDS = {
    "evidence_class",
    "profiles",
    "schema_version",
    "selection_policy",
    "taxonomy_policy",
}
PROFILE_FIELDS = {
    "allowed_risks",
    "allowed_scales",
    "allowed_reentry",
    "authority",
    "conditional_capabilities",
    "expected_artifacts",
    "forbidden_capabilities",
    "id",
    "intent",
    "lead_capability",
    "precedence",
    "preferred_risk",
    "preferred_scale",
    "required_capabilities",
    "required_evidence",
    "required_final_after",
    "required_reentry",
    "required_reentry_after",
    "required_reentry_before",
    "stop_conditions",
}
PROFILE_PARITY_FIELDS = {
    "allowed_reentry": "allowed_reentry",
    "authority": "authority",
    "conditional_capabilities": "conditional_capabilities",
    "expected_artifacts": "expected_artifacts",
    "forbidden_capabilities": "forbidden_capabilities",
    "lead_capability": "lead_capability",
    "precedence": "precedence",
    "preferred_risk": "risk",
    "preferred_scale": "scale",
    "required_capabilities": "required_capabilities",
    "required_evidence": "required_evidence",
    "required_final_after": "required_final_after",
    "required_reentry": "required_reentry",
    "required_reentry_after": "required_reentry_after",
    "required_reentry_before": "required_reentry_before",
    "stop_conditions": "stop_conditions",
}
PROFILE_DEFAULTS = {
    "required_final_after": {},
    "required_reentry": [],
    "required_reentry_after": {},
    "required_reentry_before": {},
}
CANONICAL_RUNTIME_PROFILE_SOURCE = (
    "plugins/project-delivery/skills/.shared/route-profiles-v1.json"
)
REQUIRED_SCENARIO_IDS = {f"ROUTE-{index:03d}" for index in range(1, 18)} | {
    "ROUTE-017A",
    "ROUTE-017B",
    "ROUTE-017C",
    "ROUTE-017D",
    "ROUTE-018",
    "ROUTE-019",
    "ROUTE-020",
    "ROUTE-021",
}
REQUIRED_SUPERSEDED_IDENTITIES = {"boss", "epic", "epic-harness", "superpowers"}
SCENARIO_ID = re.compile(r"^ROUTE-[0-9]{3}[A-D]?$")
PROFILE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TAUTOLOGICAL_INTENT_FRAGMENTS = {
    "requests whose semantic intent is",
    "select by meaning and lifecycle state",
}
REQUIRED_PROFILE_PRECEDENCE = {
    "incident-hotfix": {("solution-design", "security-operations")},
}
REQUIRED_COORDINATION_RETURNS = {
    "meeting-follow-up": {
        "requirements-acceptance",
        "delivery-planning",
        "documentation-knowledge",
    },
    "source-status-reconciliation": {
        "project-context",
        "documentation-knowledge",
        "delivery-planning",
    },
}


def duplicates(values: list[str]) -> set[str]:
    return {value for value in values if values.count(value) > 1}


def precedence_is_acyclic(edges: list[tuple[str, str]]) -> bool:
    nodes = {node for edge in edges for node in edge}
    outgoing = {node: set() for node in nodes}
    indegree = {node: 0 for node in nodes}
    for before, after in edges:
        if after not in outgoing[before]:
            outgoing[before].add(after)
            indegree[after] += 1
    ready = [node for node, degree in indegree.items() if degree == 0]
    visited = 0
    while ready:
        node = ready.pop()
        visited += 1
        for successor in outgoing[node]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                ready.append(successor)
    return visited == len(nodes)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=str(Path(__file__).parents[1]),
        help="plugin root",
    )
    return parser.parse_args(argv)


def validate(root: Path) -> tuple[list[str], int, set[str]]:
    errors: list[str] = []
    contract_path = root / "tests" / "route-contracts.json"
    plugin_root = root / "plugins" / "project-delivery"
    if not plugin_root.is_dir():
        plugin_root = root
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [f"invalid route contract file: {error}"], 0, set()

    if not isinstance(contract, dict):
        return ["route contract root must be an object"], 0, set()
    missing_contract_fields = CONTRACT_TOP_LEVEL_FIELDS.difference(contract)
    extra_contract_fields = set(contract).difference(CONTRACT_TOP_LEVEL_FIELDS)
    if missing_contract_fields:
        errors.append(
            "route suite missing fields: "
            + ", ".join(sorted(missing_contract_fields))
        )
    if extra_contract_fields:
        errors.append(
            "route suite has unsupported fields: "
            + ", ".join(sorted(extra_contract_fields))
        )

    if contract.get("schema_version") != 3:
        errors.append("route suite must use semantic schema version 3")
    if contract.get("evidence_class") != "semantic authored-route contract":
        errors.append("route suite must identify itself as semantic authored-route evidence")
    if not isinstance(contract.get("comparison_policy"), str) or not contract[
        "comparison_policy"
    ].strip():
        errors.append("route suite must define its semantic comparison policy")
    if not isinstance(contract.get("limitations"), str) or not contract[
        "limitations"
    ].strip():
        errors.append("route suite must state its behavioral-proof limitation")

    runtime_profile_source = contract.get("runtime_profile_source")
    profiles_by_id: dict[str, dict[str, object]] = {}
    profile_document: object | None = None
    if runtime_profile_source != CANONICAL_RUNTIME_PROFILE_SOURCE:
        errors.append(
            "route suite must name the canonical installed runtime profile source"
        )
    else:
        profile_path = root / runtime_profile_source
        if profile_path.is_symlink() or not profile_path.is_file():
            errors.append(
                "installed route profile source must be a regular non-symlink file"
            )
            profile_document = None
        else:
            try:
                profile_document = json.loads(
                    profile_path.read_text(encoding="utf-8")
                )
            except (OSError, UnicodeError, json.JSONDecodeError) as error:
                errors.append(f"invalid installed route profile file: {error}")
                profile_document = None
        if isinstance(profile_document, dict):
            missing_profile_root = PROFILE_TOP_LEVEL_FIELDS.difference(profile_document)
            extra_profile_root = set(profile_document).difference(PROFILE_TOP_LEVEL_FIELDS)
            if missing_profile_root:
                errors.append(
                    "installed route profiles missing fields: "
                    + ", ".join(sorted(missing_profile_root))
                )
            if extra_profile_root:
                errors.append(
                    "installed route profiles have unsupported fields: "
                    + ", ".join(sorted(extra_profile_root))
                )
            if profile_document.get("schema_version") != 1:
                errors.append("installed route profiles must use schema version 1")
            if profile_document.get("evidence_class") != "installed canonical route profiles":
                errors.append("installed route profiles have the wrong evidence class")
            for field in ("selection_policy", "taxonomy_policy"):
                value = profile_document.get(field)
                if not isinstance(value, str) or len(value.strip()) < 20:
                    errors.append(f"installed route profiles field {field} must be substantive")
            raw_profiles = profile_document.get("profiles")
            if not isinstance(raw_profiles, list) or not raw_profiles:
                errors.append("installed route profiles must contain a non-empty profile list")
            else:
                for profile_index, profile in enumerate(raw_profiles, 1):
                    if not isinstance(profile, dict):
                        errors.append(f"installed route profile {profile_index} must be an object")
                        continue
                    missing_profile_fields = PROFILE_FIELDS.difference(profile)
                    extra_profile_fields = set(profile).difference(PROFILE_FIELDS)
                    profile_id = profile.get("id")
                    label = profile_id if isinstance(profile_id, str) else str(profile_index)
                    if missing_profile_fields:
                        errors.append(
                            f"installed route profile {label} missing fields: "
                            + ", ".join(sorted(missing_profile_fields))
                        )
                    if extra_profile_fields:
                        errors.append(
                            f"installed route profile {label} has unsupported fields: "
                            + ", ".join(sorted(extra_profile_fields))
                        )
                    if not isinstance(profile_id, str) or not PROFILE_ID.fullmatch(profile_id):
                        errors.append(f"installed route profile {label} has an invalid ID")
                    elif profile_id in profiles_by_id:
                        errors.append(f"duplicate installed route profile ID: {profile_id}")
                    else:
                        profiles_by_id[profile_id] = profile
                    intent = profile.get("intent")
                    if not isinstance(intent, str) or len(intent.strip()) < 20:
                        errors.append(f"installed route profile {label} intent must be substantive")
                    elif any(
                        fragment in intent.casefold()
                        for fragment in TAUTOLOGICAL_INTENT_FRAGMENTS
                    ):
                        errors.append(
                            f"installed route profile {label} intent must define a semantic selection boundary"
                        )
                    elif "select when" not in intent.casefold() or not any(
                        marker in intent.casefold()
                        for marker in ("do not use", "rather than", "instead of")
                    ):
                        errors.append(
                            f"installed route profile {label} intent must state both selection and exclusion criteria"
                        )
                    for allowed_field, normalized_values, preferred_field in (
                        ("allowed_scales", ALLOWED_SCALES, "preferred_scale"),
                        ("allowed_risks", ALLOWED_RISKS, "preferred_risk"),
                    ):
                        allowed_value = profile.get(allowed_field)
                        if (
                            not isinstance(allowed_value, list)
                            or not allowed_value
                            or not all(
                                isinstance(item, str) and item in normalized_values
                                for item in allowed_value
                            )
                        ):
                            errors.append(
                                f"installed route profile {label} field {allowed_field} "
                                "must be a non-empty normalized list"
                            )
                        elif duplicates(allowed_value):
                            errors.append(
                                f"installed route profile {label} field {allowed_field} "
                                "must not contain duplicates"
                            )
                        elif profile.get(preferred_field) not in allowed_value:
                            errors.append(
                                f"installed route profile {label} {preferred_field} "
                                f"must be included in {allowed_field}"
                            )
        elif profile_document is not None:
            errors.append("installed route profile root must be an object")
        if isinstance(profile_document, dict) and re.search(
            r"\bROUTE-[0-9]{3}",
            json.dumps(profile_document, ensure_ascii=False, sort_keys=True),
        ):
            errors.append(
                "installed route profiles must not contain maintainer scenario identifiers"
            )

    legacy_names = contract.get("forbidden_runtime_dependencies")
    if (
        not isinstance(legacy_names, list)
        or not all(isinstance(item, str) and item.strip() for item in legacy_names)
        or not REQUIRED_SUPERSEDED_IDENTITIES.issubset(set(legacy_names))
    ):
        errors.append("route suite must forbid the known superseded runtime dependencies")
        legacy_names = (
            [item for item in legacy_names if isinstance(item, str)]
            if isinstance(legacy_names, list)
            else []
        )
    elif duplicates(legacy_names):
        errors.append("forbidden_runtime_dependencies must not contain duplicates")

    available_skills = {
        path.parent.name for path in (plugin_root / "skills").glob("*/SKILL.md")
    }
    scenarios = contract.get("scenarios")
    if not isinstance(scenarios, list):
        return errors + ["scenarios must be a list"], 0, set()
    seen_ids: set[str] = set()
    referenced_skills: set[str] = set()
    started = time.monotonic()
    for index, scenario in enumerate(scenarios, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(scenarios) - index)
        raw_scenario_id = scenario.get("id") if isinstance(scenario, dict) else None
        scenario_id = (
            raw_scenario_id
            if isinstance(raw_scenario_id, str) and raw_scenario_id.strip()
            else f"index-{index}"
        )
        print(f"ROUTE [{index}/{len(scenarios)}] id={scenario_id} eta={eta:.1f}s", flush=True)
        if not isinstance(scenario, dict):
            errors.append(f"scenario {index} is not an object")
            continue
        missing = REQUIRED_SCENARIO_FIELDS.difference(scenario)
        extra = set(scenario).difference(ALLOWED_SCENARIO_FIELDS)
        if missing:
            errors.append(f"{scenario_id} missing fields: {', '.join(sorted(missing))}")
        if extra:
            errors.append(
                f"{scenario_id} has unsupported fields: {', '.join(sorted(extra))}"
            )
        for field in ("id", "profile_id", "prompt", "scale", "risk"):
            value = scenario.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{scenario_id} field {field} must be a non-empty string")
        if isinstance(raw_scenario_id, str) and raw_scenario_id.strip() and not SCENARIO_ID.fullmatch(
            raw_scenario_id
        ):
            errors.append(f"{scenario_id} has malformed scenario ID")
        if scenario_id in seen_ids:
            errors.append(f"duplicate scenario ID: {scenario_id}")
        seen_ids.add(scenario_id)
        if scenario.get("authority") not in ALLOWED_AUTHORITIES:
            errors.append(f"{scenario_id} has unsupported authority: {scenario.get('authority')}")
        if scenario.get("scale") not in ALLOWED_SCALES:
            errors.append(f"{scenario_id} has unsupported scale: {scenario.get('scale')}")
        if scenario.get("risk") not in ALLOWED_RISKS:
            errors.append(f"{scenario_id} has unsupported risk: {scenario.get('risk')}")
        profile_id = scenario.get("profile_id")
        if not isinstance(profile_id, str) or not PROFILE_ID.fullmatch(profile_id):
            errors.append(f"{scenario_id} has an invalid profile_id")
        for field, allowed, preferred_field in (
            ("accepted_scales", ALLOWED_SCALES, "scale"),
            ("accepted_risks", ALLOWED_RISKS, "risk"),
        ):
            value = scenario.get(field)
            if (
                not isinstance(value, list)
                or not value
                or not all(isinstance(item, str) and item in allowed for item in value)
            ):
                errors.append(f"{scenario_id} field {field} must be a non-empty normalized list")
            elif duplicates(value):
                errors.append(f"{scenario_id} field {field} must not contain duplicates")
            elif scenario.get(preferred_field) not in value:
                errors.append(
                    f"{scenario_id} preferred {preferred_field} must be accepted by {field}"
                )

        profile = profiles_by_id.get(profile_id) if isinstance(profile_id, str) else None
        if profile is None:
            errors.append(f"{scenario_id} does not resolve an installed route profile")
        else:
            for profile_field, scenario_field in PROFILE_PARITY_FIELDS.items():
                scenario_value = scenario.get(
                    scenario_field, PROFILE_DEFAULTS.get(scenario_field)
                )
                if profile.get(profile_field) != scenario_value:
                    errors.append(
                        f"{scenario_id} field {scenario_field} drifts from installed profile {profile_id}"
                    )
            for accepted_field, allowed_field in (
                ("accepted_scales", "allowed_scales"),
                ("accepted_risks", "allowed_risks"),
            ):
                accepted_value = scenario.get(accepted_field)
                allowed_value = profile.get(allowed_field)
                if isinstance(accepted_value, list) and isinstance(allowed_value, list):
                    outside_runtime_policy = set(accepted_value).difference(allowed_value)
                    if outside_runtime_policy:
                        errors.append(
                            f"{scenario_id} field {accepted_field} exceeds installed profile "
                            f"{profile_id} {allowed_field}: "
                            + ", ".join(sorted(outside_runtime_policy))
                        )

            required_edges = REQUIRED_PROFILE_PRECEDENCE.get(profile_id, set())
            profile_edges = {
                tuple(edge)
                for edge in profile.get("precedence", [])
                if isinstance(edge, list)
                and len(edge) == 2
                and all(isinstance(item, str) for item in edge)
            }
            missing_required_edges = required_edges.difference(profile_edges)
            if missing_required_edges:
                formatted_edges = ", ".join(
                    f"{before}->{after}"
                    for before, after in sorted(missing_required_edges)
                )
                errors.append(
                    f"installed route profile {profile_id} lacks required precedence: "
                    f"{formatted_edges}"
                )

            coordination_return_owners = REQUIRED_COORDINATION_RETURNS.get(profile_id)
            if coordination_return_owners is not None:
                controller = "delivery-coordination"
                required_reentry = profile.get("required_reentry", [])
                return_before = profile.get("required_reentry_before", {})
                return_after = profile.get("required_reentry_after", {})
                before_owners = (
                    return_before.get(controller, [])
                    if isinstance(return_before, dict)
                    else []
                )
                after_owners = (
                    return_after.get(controller, [])
                    if isinstance(return_after, dict)
                    else []
                )
                if (
                    not isinstance(required_reentry, list)
                    or controller not in required_reentry
                    or not coordination_return_owners.issubset(set(before_owners))
                    or not coordination_return_owners.issubset(set(after_owners))
                ):
                    errors.append(
                        f"installed route profile {profile_id} must require "
                        "delivery-coordination entry and return around every downstream conditional"
                    )

            prompt = scenario.get("prompt")
            if isinstance(prompt, str) and isinstance(profile_document, dict):
                installed_profile_text = json.dumps(
                    profile_document, ensure_ascii=False, sort_keys=True
                )
                if prompt in installed_profile_text:
                    errors.append(
                        f"installed route profiles must not contain exact maintainer prompt for {scenario_id}"
                    )
        for field in (
            "required_capabilities",
            "allowed_reentry",
            "forbidden_capabilities",
            "expected_artifacts",
            "required_evidence",
            "stop_conditions",
        ):
            value = scenario.get(field)
            allow_empty = field in {"allowed_reentry", "forbidden_capabilities"}
            if not isinstance(value, list) or (not value and not allow_empty) or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                qualifier = "a string list" if allow_empty else "a non-empty string list"
                errors.append(f"{scenario_id} field {field} must be {qualifier}")

        lead = scenario.get("lead_capability")
        if not isinstance(lead, str) or not lead.strip():
            errors.append(f"{scenario_id} lead_capability must be a skill name")
        required_value = scenario.get("required_capabilities", [])
        required = required_value if isinstance(required_value, list) else []
        conditional = scenario.get("conditional_capabilities", [])
        conditional_names: list[str] = []
        if not isinstance(conditional, list):
            errors.append(f"{scenario_id} conditional_capabilities must be a list")
        else:
            for conditional_index, item in enumerate(conditional, 1):
                if not isinstance(item, dict):
                    errors.append(
                        f"{scenario_id} conditional capability {conditional_index} is not an object"
                    )
                    continue
                missing_conditional = CONTRACT_CONDITIONAL_FIELDS.difference(item)
                extra_conditional = set(item).difference(CONTRACT_CONDITIONAL_FIELDS)
                if missing_conditional:
                    errors.append(
                        f"{scenario_id} conditional capability {conditional_index} "
                        "missing fields: " + ", ".join(sorted(missing_conditional))
                    )
                if extra_conditional:
                    errors.append(
                        f"{scenario_id} conditional capability {conditional_index} "
                        "has unsupported fields: " + ", ".join(sorted(extra_conditional))
                    )
                skill = item.get("skill")
                when = item.get("when")
                if not isinstance(skill, str) or not skill.strip():
                    errors.append(
                        f"{scenario_id} conditional capability {conditional_index} lacks a skill"
                    )
                else:
                    conditional_names.append(skill)
                if not isinstance(when, str) or len(when.strip()) < 12:
                    errors.append(
                        f"{scenario_id} conditional capability {conditional_index} lacks a substantive trigger"
                    )

        allowed_reentry_value = scenario.get("allowed_reentry", [])
        allowed_reentry = allowed_reentry_value if isinstance(allowed_reentry_value, list) else []
        forbidden_value = scenario.get("forbidden_capabilities", [])
        forbidden = forbidden_value if isinstance(forbidden_value, list) else []
        required_reentry_value = scenario.get("required_reentry", [])
        required_reentry = (
            required_reentry_value if isinstance(required_reentry_value, list) else []
        )
        if not isinstance(required_reentry_value, list) or not all(
            isinstance(item, str) and item.strip() for item in required_reentry
        ):
            errors.append(f"{scenario_id} required_reentry must be a string list")
        if not set(required_reentry).issubset(set(allowed_reentry)):
            errors.append(f"{scenario_id} required_reentry must be allowed re-entry")
        for field_name, values in (
            ("required_capabilities", required),
            ("conditional_capabilities", conditional_names),
            ("allowed_reentry", allowed_reentry),
            ("required_reentry", required_reentry),
            ("forbidden_capabilities", forbidden),
        ):
            repeated_values = duplicates(values)
            if repeated_values:
                errors.append(
                    f"{scenario_id} repeats {field_name}: "
                    + ", ".join(sorted(repeated_values))
                )
        route_skills = [
            item
            for item in [
                lead,
                *required,
                *conditional_names,
                *allowed_reentry,
                *required_reentry,
                *forbidden,
            ]
            if isinstance(item, str)
        ]
        referenced_skills.update(
            item
            for item in [lead, *required, *conditional_names]
            if isinstance(item, str)
        )
        unknown = set(route_skills).difference(available_skills)
        if unknown:
            errors.append(f"{scenario_id} references unknown skills: {', '.join(sorted(unknown))}")
        if isinstance(lead, str) and lead not in required:
            errors.append(f"{scenario_id} lead_capability must be required")
        overlap = set(required).intersection(conditional_names)
        if overlap:
            errors.append(
                f"{scenario_id} capabilities cannot be both required and conditional: "
                f"{', '.join(sorted(overlap))}"
            )
        required_forbidden = set(required).intersection(forbidden)
        conditional_forbidden = set(conditional_names).intersection(forbidden)
        if required_forbidden:
            errors.append(
                f"{scenario_id} capabilities cannot be both required and forbidden: "
                f"{', '.join(sorted(required_forbidden))}"
            )
        if conditional_forbidden:
            errors.append(
                f"{scenario_id} capabilities cannot be both conditional and forbidden: "
                f"{', '.join(sorted(conditional_forbidden))}"
            )
        selectable = set(required).union(conditional_names)
        invalid_allowed_reentry = set(allowed_reentry).difference(selectable)
        if invalid_allowed_reentry:
            errors.append(
                f"{scenario_id} allows re-entry for unselectable capabilities: "
                f"{', '.join(sorted(invalid_allowed_reentry))}"
            )

        reentry_after_value = scenario.get("required_reentry_after", {})
        if not isinstance(reentry_after_value, dict):
            errors.append(f"{scenario_id} required_reentry_after must be an object")
            reentry_after_value = {}
        missing_return_contracts = set(required_reentry).difference(reentry_after_value)
        extra_return_contracts = set(reentry_after_value).difference(required_reentry)
        if missing_return_contracts:
            errors.append(
                f"{scenario_id} required re-entry lacks return-after owners: "
                f"{', '.join(sorted(missing_return_contracts))}"
            )
        if extra_return_contracts:
            errors.append(
                f"{scenario_id} return-after contract has no required re-entry: "
                f"{', '.join(sorted(extra_return_contracts))}"
            )
        for controller, owners_value in reentry_after_value.items():
            owners = owners_value if isinstance(owners_value, list) else []
            if (
                not isinstance(controller, str)
                or not isinstance(owners_value, list)
                or not owners
                or not all(isinstance(owner, str) and owner.strip() for owner in owners)
            ):
                errors.append(
                    f"{scenario_id} return-after contract for {controller} must name owners"
                )
                continue
            repeated_owners = duplicates(owners)
            if repeated_owners:
                errors.append(
                    f"{scenario_id} repeats return-after owners for {controller}: "
                    f"{', '.join(sorted(repeated_owners))}"
                )
            invalid_owners = set(owners).difference(selectable)
            if invalid_owners:
                errors.append(
                    f"{scenario_id} return-after contract for {controller} references "
                    "unselectable capabilities: " + ", ".join(sorted(invalid_owners))
                )
            if controller in owners:
                errors.append(
                    f"{scenario_id} return-after controller {controller} cannot depend on itself"
                )

        reentry_before_value = scenario.get("required_reentry_before", {})
        if not isinstance(reentry_before_value, dict):
            errors.append(f"{scenario_id} required_reentry_before must be an object")
            reentry_before_value = {}
        missing_entry_contracts = set(required_reentry).difference(reentry_before_value)
        extra_entry_contracts = set(reentry_before_value).difference(required_reentry)
        if missing_entry_contracts:
            errors.append(
                f"{scenario_id} required re-entry lacks entry-before owners: "
                f"{', '.join(sorted(missing_entry_contracts))}"
            )
        if extra_entry_contracts:
            errors.append(
                f"{scenario_id} entry-before contract has no required re-entry: "
                f"{', '.join(sorted(extra_entry_contracts))}"
            )
        for controller, owners_value in reentry_before_value.items():
            owners = owners_value if isinstance(owners_value, list) else []
            if (
                not isinstance(controller, str)
                or not isinstance(owners_value, list)
                or not owners
                or not all(isinstance(owner, str) and owner.strip() for owner in owners)
            ):
                errors.append(
                    f"{scenario_id} entry-before contract for {controller} must name owners"
                )
                continue
            repeated_owners = duplicates(owners)
            if repeated_owners:
                errors.append(
                    f"{scenario_id} repeats entry-before owners for {controller}: "
                    f"{', '.join(sorted(repeated_owners))}"
                )
            invalid_owners = set(owners).difference(selectable)
            if invalid_owners:
                errors.append(
                    f"{scenario_id} entry-before contract for {controller} references "
                    "unselectable capabilities: " + ", ".join(sorted(invalid_owners))
                )
            return_owners = reentry_after_value.get(controller, [])
            if isinstance(return_owners, list):
                not_return_owners = set(owners).difference(return_owners)
                if not_return_owners:
                    errors.append(
                        f"{scenario_id} entry-before owners for {controller} are not "
                        "return-after owners: " + ", ".join(sorted(not_return_owners))
                    )
            if controller in owners:
                errors.append(
                    f"{scenario_id} entry-before controller {controller} cannot depend on itself"
                )

        final_after_value = scenario.get("required_final_after", {})
        if not isinstance(final_after_value, dict):
            errors.append(f"{scenario_id} required_final_after must be an object")
            final_after_value = {}
        for controller, owners_value in final_after_value.items():
            owners = owners_value if isinstance(owners_value, list) else []
            if (
                not isinstance(controller, str)
                or not isinstance(owners_value, list)
                or not owners
                or not all(isinstance(owner, str) and owner.strip() for owner in owners)
            ):
                errors.append(
                    f"{scenario_id} final-after contract for {controller} must name owners"
                )
                continue
            if controller not in selectable:
                errors.append(
                    f"{scenario_id} final-after controller {controller} must be selectable"
                )
            repeated_owners = duplicates(owners)
            if repeated_owners:
                errors.append(
                    f"{scenario_id} repeats final-after owners for {controller}: "
                    f"{', '.join(sorted(repeated_owners))}"
                )
            invalid_owners = set(owners).difference(selectable)
            if invalid_owners:
                errors.append(
                    f"{scenario_id} final-after contract for {controller} references "
                    "unselectable capabilities: " + ", ".join(sorted(invalid_owners))
                )
            if controller in owners:
                errors.append(
                    f"{scenario_id} final-after controller {controller} cannot depend on itself"
                )

        precedence = scenario.get("precedence")
        precedence_edges: list[tuple[str, str]] = []
        if not isinstance(precedence, list):
            errors.append(f"{scenario_id} precedence must be a list")
        else:
            for pair_index, pair in enumerate(precedence, 1):
                if (
                    not isinstance(pair, list)
                    or len(pair) != 2
                    or not all(isinstance(item, str) and item.strip() for item in pair)
                ):
                    errors.append(f"{scenario_id} precedence item {pair_index} must contain two skills")
                    continue
                if not set(pair).issubset(selectable):
                    errors.append(
                        f"{scenario_id} precedence item {pair_index} references a capability "
                        "that is neither required nor conditional"
                    )
                    continue
                before, after = pair
                if before == after:
                    errors.append(f"{scenario_id} precedence item {pair_index} is a self-edge")
                precedence_edges.append((before, after))
            repeated_edges = {
                edge for edge in precedence_edges if precedence_edges.count(edge) > 1
            }
            if repeated_edges:
                errors.append(f"{scenario_id} repeats precedence edges")
            if precedence_edges and not precedence_is_acyclic(precedence_edges):
                errors.append(f"{scenario_id} precedence graph contains a cycle")

        forbidden_in_route = selectable.intersection(set(legacy_names or []))
        if forbidden_in_route:
            errors.append(
                f"{scenario_id} routes through forbidden dependencies: "
                f"{', '.join(sorted(forbidden_in_route))}"
            )

    missing_scenarios = REQUIRED_SCENARIO_IDS.difference(seen_ids)
    unexpected_scenarios = seen_ids.difference(REQUIRED_SCENARIO_IDS)
    if missing_scenarios:
        errors.append(
            "canonical route suite is missing scenarios: "
            + ", ".join(sorted(missing_scenarios))
        )
    if unexpected_scenarios:
        errors.append(
            "canonical route suite has unexpected scenarios: "
            + ", ".join(sorted(unexpected_scenarios))
        )

    scenario_profile_ids = {
        scenario.get("profile_id")
        for scenario in scenarios
        if isinstance(scenario, dict) and isinstance(scenario.get("profile_id"), str)
    }
    missing_profiles = scenario_profile_ids.difference(profiles_by_id)
    unused_profiles = set(profiles_by_id).difference(scenario_profile_ids)
    if missing_profiles:
        errors.append(
            "canonical route scenarios lack installed profiles: "
            + ", ".join(sorted(missing_profiles))
        )
    if unused_profiles:
        errors.append(
            "installed route profiles lack canonical scenario coverage: "
            + ", ".join(sorted(unused_profiles))
        )

    missing_skill_coverage = available_skills.difference(referenced_skills)
    if missing_skill_coverage:
        errors.append(
            "canonical route suite does not exercise skills: "
            + ", ".join(sorted(missing_skill_coverage))
        )
    return errors, len(scenarios), referenced_skills


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).expanduser().resolve()
    errors, scenario_count, referenced_skills = validate(root)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(
        f"PASS scenarios={scenario_count} referenced_skills={len(referenced_skills)} "
        "evidence=semantic-contracts"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
