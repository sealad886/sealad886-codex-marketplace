from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "project-delivery"
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from check_distribution_bundle import payload_sha256  # noqa: E402
from check_distribution_bundle import select_paths  # noqa: E402

CONTRACT_CHECKER = REPOSITORY_ROOT / "scripts" / "check_routes.py"
RECEIPT_CHECKER = REPOSITORY_ROOT / "scripts" / "check_route_receipts.py"
BLIND_FIXTURE = (
    REPOSITORY_ROOT / "tests" / "fixtures" / "blind-route-observations-v1.3.1.json"
)
TEST_SOURCE_REVISION = "0123456789abcdef0123456789abcdef01234567"
PAYLOAD_HASH_METHOD = "project-delivery length-prefixed path-and-content sha256 v1"
ROUTE_PROFILE_PATH = (
    PLUGIN_ROOT / "skills" / ".shared" / "route-profiles-v1.json"
)


def run_contract_checker() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CONTRACT_CHECKER), str(REPOSITORY_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )


def run_contract_checker_with_contract(
    contract: dict[str, object],
    *,
    route_profiles: dict[str, object] | None = None,
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "tests").mkdir()
        (root / "tests" / "route-contracts.json").write_text(
            json.dumps(contract), encoding="utf-8"
        )
        for skill_file in (PLUGIN_ROOT / "skills").glob("*/SKILL.md"):
            target = (
                root
                / "plugins"
                / "project-delivery"
                / "skills"
                / skill_file.parent.name
            )
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("fixture\n", encoding="utf-8")
        profile_target = (
            root
            / "plugins"
            / "project-delivery"
            / "skills"
            / ".shared"
            / "route-profiles-v1.json"
        )
        profile_target.parent.mkdir(parents=True)
        profile_target.write_text(
            json.dumps(
                load_route_profiles() if route_profiles is None else route_profiles
            ),
            encoding="utf-8",
        )
        return subprocess.run(
            [sys.executable, str(CONTRACT_CHECKER), str(root)],
            check=False,
            capture_output=True,
            text=True,
        )


def run_receipt_checker(
    receipts: dict[str, object],
    *,
    allow_historical: bool = True,
    recompute_fresh_digest: bool = True,
) -> subprocess.CompletedProcess[str]:
    if (
        recompute_fresh_digest
        and receipts.get("evidence_class") == "fresh-task semantic route observation"
    ):
        observation = {
            field: receipts.get(field)
            for field in (
                "observation_scope",
                "effects_performed",
                "legacy_runtime_events",
                "legacy_administrative_visibility",
                "loaded_specialists",
                "scenarios",
            )
        }
        canonical = json.dumps(
            observation,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        receipts["task_identity"]["source_observation_sha256"] = hashlib.sha256(
            canonical
        ).hexdigest()
    with tempfile.TemporaryDirectory() as temporary:
        receipt_path = Path(temporary) / "receipts.json"
        receipt_path.write_text(json.dumps(receipts), encoding="utf-8")
        command = [
            sys.executable,
            str(RECEIPT_CHECKER),
            str(receipt_path),
            "--root",
            str(REPOSITORY_ROOT),
            "--allow-subset",
        ]
        if allow_historical:
            command.append("--allow-historical-annotations")
        if receipts.get("evidence_class") == "fresh-task semantic route observation":
            command.extend(
                [
                    "--allow-unsealed-fresh",
                    "--installed-plugin-root",
                    str(PLUGIN_ROOT),
                    "--expected-source-revision",
                    TEST_SOURCE_REVISION,
                ]
            )
        return subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )


def load_fixture() -> dict[str, object]:
    return json.loads(BLIND_FIXTURE.read_text(encoding="utf-8"))


def load_contracts() -> dict[str, object]:
    return json.loads((REPOSITORY_ROOT / "tests" / "route-contracts.json").read_text())


def load_route_profiles() -> dict[str, object]:
    return json.loads(ROUTE_PROFILE_PATH.read_text(encoding="utf-8"))


def make_fresh_receipts(receipts: dict[str, object]) -> dict[str, object]:
    receipts["contract_schema_version"] = load_contracts()["schema_version"]
    receipts["evidence_class"] = "fresh-task semantic route observation"
    receipts["semantic_fields_were_frozen_before_contract_comparison"] = True
    receipts["semantic_freeze_scope"] = [
        "actual_route",
        "authority",
        "conditional_dispositions",
        "evidence",
        "extra_capability_justifications",
        "gaps",
        "risk",
        "scale",
        "taxonomy_evidence",
        "taxonomy_rationale",
    ]
    receipts["semantic_freeze_evidence"] = [
        "Synthetic fresh-task fixture froze every semantic field before comparison."
    ]
    receipts["annotation_provenance"] = (
        "Synthetic fresh-task regression record with all semantic fields fixed before comparison."
    )
    receipts["task_identity"] = {
        field: receipts["task_identity"][field]
        for field in (
            "public_receipt_id",
            "selected_at",
            "source_observation_sha256",
        )
    }
    manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    receipts["plugin_identity"] = {
        "name": manifest["name"],
        "installed_version": manifest["version"],
        "source_revision": TEST_SOURCE_REVISION,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "payload_sha256": payload_sha256(
            PLUGIN_ROOT,
            sorted(select_paths(PLUGIN_ROOT)),
        ),
        "payload_hash_method": PAYLOAD_HASH_METHOD,
        "cache_relative_path": "plugins/project-delivery",
    }
    prompts = {
        item["id"]: item["prompt"] for item in load_contracts()["scenarios"]
    }
    for item in receipts["scenarios"]:
        item["prompt"] = prompts[item["id"]]
        route = item["actual_route"]
        if "retrospective-improvement" in route:
            item["actual_route"] = [
                skill for skill in route if skill != "retrospective-improvement"
            ]
        dispositions = item["conditional_dispositions"]
        if "retrospective-improvement" in dispositions:
            dispositions["retrospective-improvement"] = {
                "state": "planned-future",
                "rationale": (
                    "Synthetic route-only fixture has no observed delivery outcome yet."
                ),
                "evidence": ["Synthetic delivery result remains not run."],
            }
    selected_skills = {
        skill.removeprefix("project-delivery:")
        for item in receipts["scenarios"]
        for skill in item["actual_route"]
    }
    receipts["loaded_specialists"] = [
        loaded
        for loaded in receipts["loaded_specialists"]
        if loaded["skill"] in selected_skills
    ]
    for loaded in receipts["loaded_specialists"]:
        skill_path = PLUGIN_ROOT / loaded["relative_path"]
        loaded["skill_sha256"] = hashlib.sha256(skill_path.read_bytes()).hexdigest()
        loaded["evidence"] = [
            "Synthetic fresh-task fixture records a complete read of this exact installed skill."
        ]
    return receipts


def set_fresh_scenarios(
    receipts: dict[str, object],
    scenarios: list[dict[str, object]],
) -> None:
    receipts["scenarios"] = scenarios
    selected_skills = {
        skill.removeprefix("project-delivery:")
        for item in scenarios
        for skill in item["actual_route"]
    }
    loaded_items = receipts["loaded_specialists"]
    assert isinstance(loaded_items, list)
    receipts["loaded_specialists"] = [
        item for item in loaded_items if item["skill"] in selected_skills
    ]
    retained_skills = {
        item["skill"] for item in receipts["loaded_specialists"]
    }
    for skill in sorted(selected_skills.difference(retained_skills)):
        skill_path = PLUGIN_ROOT / "skills" / skill / "SKILL.md"
        receipts["loaded_specialists"].append(
            {
                "skill": skill,
                "relative_path": f"skills/{skill}/SKILL.md",
                "state": "loaded",
                "skill_sha256": hashlib.sha256(skill_path.read_bytes()).hexdigest(),
                "evidence": [
                    "Synthetic fresh-task fixture records a complete read of this exact installed skill."
                ],
            }
        )
    retained_skills = {
        item["skill"] for item in receipts["loaded_specialists"]
    }
    assert retained_skills == selected_skills


def scenario(receipts: dict[str, object], scenario_id: str) -> dict[str, object]:
    scenarios = receipts["scenarios"]
    assert isinstance(scenarios, list)
    return next(item for item in scenarios if item["id"] == scenario_id)


def synthetic_policy_scenario(contract: dict[str, object]) -> dict[str, object]:
    required = list(contract["required_capabilities"])
    edges = [
        (before, after)
        for before, after in contract["precedence"]
        if before in required and after in required
    ]
    remaining = list(required)
    route: list[str] = []
    while remaining:
        eligible = [
            skill
            for skill in remaining
            if all(before in route for before, after in edges if after == skill)
        ]
        assert eligible, f"cyclic synthetic contract: {contract['id']}"
        selected = eligible[0]
        remaining.remove(selected)
        route.append(selected)
    for controller in contract.get("required_reentry", []):
        owners = contract.get("required_reentry_after", {}).get(controller, [])
        if any(owner in route for owner in owners):
            route.append(controller)
    for controller, owners in contract.get("required_final_after", {}).items():
        selected_owners = [owner for owner in owners if owner in route]
        if controller in route and selected_owners and max(
            index for index, skill in enumerate(route) if skill == controller
        ) <= max(
            max(index for index, skill in enumerate(route) if skill == owner)
            for owner in selected_owners
        ):
            route.append(controller)
    return {
        "id": contract["id"],
        "prompt": contract["prompt"],
        "scale": contract["scale"],
        "risk": contract["risk"],
        "authority": contract["authority"],
        "taxonomy_rationale": (
            "Synthetic classification rationale fixed before contract comparison for this "
            "route-policy regression scenario."
        ),
        "taxonomy_evidence": ["Synthetic pre-comparison taxonomy evidence."],
        "actual_route": route,
        "conditional_dispositions": {
            item["skill"]: {
                "state": (
                    "planned-future"
                    if item["skill"] == "retrospective-improvement"
                    else "not-applicable"
                ),
                "rationale": (
                    "Synthetic route-only fixture has no observed delivery outcome yet."
                    if item["skill"] == "retrospective-improvement"
                    else "Synthetic policy test leaves this evidence-triggered branch inactive."
                ),
                "evidence": ["Synthetic route-policy regression fixture."],
            }
            for item in contract["conditional_capabilities"]
        },
        "extra_capability_justifications": {},
        "delivery_result": "not-run",
        "evidence": ["Synthetic route-policy regression fixture."],
        "gaps": [],
    }


class RouteSemanticTests(unittest.TestCase):
    def test_authored_semantic_contracts_pass(self) -> None:
        result = run_contract_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("evidence=semantic-contracts", result.stdout)

    def test_contract_drift_from_installed_runtime_profile_fails(self) -> None:
        contracts = load_contracts()
        large_initiative = scenario(contracts, "ROUTE-003")
        large_initiative["risk"] = "medium-or-high"

        result = run_contract_checker_with_contract(contracts)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "ROUTE-003 field risk drifts from installed profile large-initiative-planning",
            result.stdout,
        )

    def test_installed_runtime_profile_drift_from_contract_fails(self) -> None:
        profiles = load_route_profiles()
        profile = next(
            item
            for item in profiles["profiles"]
            if item["id"] == "large-initiative-planning"
        )
        profile["preferred_risk"] = "medium-or-high"

        result = run_contract_checker_with_contract(
            load_contracts(),
            route_profiles=profiles,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "ROUTE-003 field risk drifts from installed profile large-initiative-planning",
            result.stdout,
        )

    def test_blind_canary_taxonomy_must_be_subset_of_runtime_policy(self) -> None:
        contracts = load_contracts()
        scenario(contracts, "ROUTE-003")["accepted_risks"].append("low")

        result = run_contract_checker_with_contract(contracts)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "ROUTE-003 field accepted_risks exceeds installed profile "
            "large-initiative-planning allowed_risks: low",
            result.stdout,
        )

    def test_checker_preserves_hotfix_design_security_boundary_under_parallel_drift(self) -> None:
        contracts = load_contracts()
        profiles = load_route_profiles()
        edge = ["solution-design", "security-operations"]
        scenario(contracts, "ROUTE-010")["precedence"].remove(edge)
        profile = next(
            item for item in profiles["profiles"] if item["id"] == "incident-hotfix"
        )
        profile["precedence"].remove(edge)

        result = run_contract_checker_with_contract(
            contracts,
            route_profiles=profiles,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "installed route profile incident-hotfix lacks required precedence: "
            "solution-design->security-operations",
            result.stdout,
        )

    def test_checker_preserves_coordination_return_under_parallel_drift(self) -> None:
        cases = {
            "ROUTE-011": "meeting-follow-up",
            "ROUTE-012": "source-status-reconciliation",
        }
        for scenario_id, profile_id in cases.items():
            with self.subTest(scenario=scenario_id):
                contracts = load_contracts()
                profiles = load_route_profiles()
                contract = scenario(contracts, scenario_id)
                profile = next(
                    item
                    for item in profiles["profiles"]
                    if item["id"] == profile_id
                )
                for field, default in (
                    ("required_reentry", []),
                    ("required_reentry_before", {}),
                    ("required_reentry_after", {}),
                    ("required_final_after", {}),
                ):
                    profile[field] = copy.deepcopy(default)
                    contract.pop(field, None)

                result = run_contract_checker_with_contract(
                    contracts,
                    route_profiles=profiles,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    f"installed route profile {profile_id} must require "
                    "delivery-coordination entry and return around every downstream conditional",
                    result.stdout,
                )

    def test_checker_rejects_tautological_runtime_intent(self) -> None:
        profiles = load_route_profiles()
        profile = next(
            item
            for item in profiles["profiles"]
            if item["id"] == "medium-feature-change"
        )
        profile["intent"] = (
            "Requests whose semantic intent is medium feature change; "
            "select by meaning and lifecycle state."
        )

        result = run_contract_checker_with_contract(
            load_contracts(),
            route_profiles=profiles,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "installed route profile medium-feature-change intent must define "
            "a semantic selection boundary",
            result.stdout,
        )

    def test_fresh_receipt_accepts_normalized_taxonomy_alternative(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-006")
        item = synthetic_policy_scenario(contract)
        item["scale"] = "medium-or-large"
        item["risk"] = "risk-dependent"
        set_fresh_scenarios(receipts, [item])

        result = run_receipt_checker(receipts, allow_historical=False)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fresh_receipt_rejects_taxonomy_value_outside_accepted_set(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-003")
        item = synthetic_policy_scenario(contract)
        item["risk"] = "critical"
        set_fresh_scenarios(receipts, [item])

        result = run_receipt_checker(receipts, allow_historical=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "ROUTE-003 risk is outside the accepted contract taxonomy",
            result.stdout,
        )

    def test_hotfix_rejects_security_before_solution_design(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-010")
        hotfix = synthetic_policy_scenario(contract)
        hotfix["actual_route"] = [
            "delivery-orchestrator",
            "release-change",
            "project-context",
            "requirements-acceptance",
            "security-operations",
            "solution-design",
            "implementation-execution",
            "testing-quality",
            "release-change",
        ]
        set_fresh_scenarios(receipts, [hotfix])

        result = run_receipt_checker(receipts, allow_historical=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "ROUTE-010 violates precedence: solution-design must precede security-operations",
            result.stdout,
        )

    def test_coordination_profiles_return_after_activated_downstream_work(self) -> None:
        cases = {
            "ROUTE-011": [
                "delivery-coordination",
                "requirements-acceptance",
                "delivery-planning",
                "documentation-knowledge",
                "delivery-coordination",
            ],
            "ROUTE-012": [
                "delivery-coordination",
                "project-context",
                "documentation-knowledge",
                "delivery-planning",
                "delivery-coordination",
            ],
        }
        contracts = load_contracts()
        for scenario_id, actual_route in cases.items():
            with self.subTest(scenario=scenario_id):
                receipts = make_fresh_receipts(load_fixture())
                item = synthetic_policy_scenario(scenario(contracts, scenario_id))
                item["actual_route"] = actual_route
                for skill, disposition in item["conditional_dispositions"].items():
                    disposition.update(
                        {
                            "state": "activated",
                            "rationale": (
                                "Synthetic source evidence activates this downstream "
                                "coordination branch before comparison."
                            ),
                            "evidence": [
                                f"Synthetic activation evidence for {skill}."
                            ],
                        }
                    )
                set_fresh_scenarios(receipts, [item])

                result = run_receipt_checker(receipts, allow_historical=False)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

                item["actual_route"].pop()
                set_fresh_scenarios(receipts, [item])
                result = run_receipt_checker(receipts, allow_historical=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    f"{scenario_id} misses required controller re-entry: delivery-coordination",
                    result.stdout,
                )

    def test_coordination_profiles_reject_reversed_downstream_precedence(self) -> None:
        cases = {
            "ROUTE-011": (
                [
                    "delivery-coordination",
                    "delivery-planning",
                    "requirements-acceptance",
                    "documentation-knowledge",
                    "delivery-coordination",
                ],
                "requirements-acceptance must precede delivery-planning",
            ),
            "ROUTE-012": (
                [
                    "delivery-coordination",
                    "documentation-knowledge",
                    "project-context",
                    "delivery-planning",
                    "delivery-coordination",
                ],
                "project-context must precede documentation-knowledge",
            ),
        }
        contracts = load_contracts()
        for scenario_id, (actual_route, expected) in cases.items():
            with self.subTest(scenario=scenario_id):
                receipts = make_fresh_receipts(load_fixture())
                item = synthetic_policy_scenario(scenario(contracts, scenario_id))
                item["actual_route"] = actual_route
                for disposition in item["conditional_dispositions"].values():
                    disposition.update(
                        {
                            "state": "activated",
                            "rationale": (
                                "Synthetic source evidence activates this downstream "
                                "coordination branch before comparison."
                            ),
                            "evidence": ["Synthetic activation evidence."],
                        }
                    )
                set_fresh_scenarios(receipts, [item])

                result = run_receipt_checker(receipts, allow_historical=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"{scenario_id} violates precedence: {expected}", result.stdout)

    def test_blind_v131_routes_pass_historical_shape_compatibility(self) -> None:
        result = run_receipt_checker(load_fixture())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("historical_route_shape_records=17", result.stdout)
        self.assertIn("current_policy_claim=not-established", result.stdout)
        self.assertIn("historical contract-blind route", result.stdout)

    def test_historical_annotations_require_explicit_flag(self) -> None:
        result = run_receipt_checker(load_fixture(), allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("require --allow-historical-annotations", result.stdout)

    def test_fresh_receipt_requires_all_semantic_fields_frozen(self) -> None:
        receipts = load_fixture()
        receipts["evidence_class"] = "fresh-task semantic route observation"
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "requires all semantic fields frozen before contract comparison",
            result.stdout,
        )
        self.assertIn("fresh-task semantic freeze omits fields", result.stdout)

    def test_missing_required_capability_fails(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-001")["actual_route"]
        assert isinstance(route, list)
        route.remove("delivery-planning")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("misses required capabilities: delivery-planning", result.stdout)

    def test_authority_forbidden_capability_fails(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-001")["actual_route"]
        assert isinstance(route, list)
        route.append("implementation-execution")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("uses authority-forbidden capabilities", result.stdout)

    def test_missing_conditional_disposition_fails(self) -> None:
        receipts = load_fixture()
        dispositions = scenario(receipts, "ROUTE-004")["conditional_dispositions"]
        assert isinstance(dispositions, dict)
        del dispositions["testing-quality"]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("omits conditional dispositions: testing-quality", result.stdout)

    def test_required_controller_reentry_fails_when_omitted(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-005")["actual_route"]
        assert isinstance(route, list)
        route.pop()
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("misses required controller re-entry: release-change", result.stdout)

    def test_controller_return_before_evidence_fails(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-005")["actual_route"] = [
            "release-change",
            "release-change",
            "testing-quality",
            "documentation-knowledge",
            "review-audit",
            "security-operations",
        ]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("controller release-change does not return after", result.stdout)

    def test_controller_must_enter_before_recovery_owners(self) -> None:
        cases = {
            "ROUTE-005": [
                "delivery-orchestrator",
                "testing-quality",
                "documentation-knowledge",
                "review-audit",
                "security-operations",
                "release-change",
                "release-change",
            ],
            "ROUTE-015": [
                "delivery-orchestrator",
                "security-operations",
                "release-change",
                "release-change",
            ],
        }
        for scenario_id, malformed_route in cases.items():
            with self.subTest(scenario=scenario_id):
                receipts = load_fixture()
                scenario(receipts, scenario_id)["actual_route"] = malformed_route
                result = run_receipt_checker(receipts)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("does not enter before", result.stdout)

        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-017B")
        package = synthetic_policy_scenario(contract)
        package["actual_route"] = [
            "testing-quality",
            "release-change",
            "release-change",
        ]
        set_fresh_scenarios(receipts, [package])
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not enter before: testing-quality", result.stdout)

    def test_late_incident_controller_fails(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-010")["actual_route"] = [
            "delivery-orchestrator",
            "project-context",
            "requirements-acceptance",
            "solution-design",
            "security-operations",
            "implementation-execution",
            "testing-quality",
            "release-change",
            "release-change",
            "delivery-planning",
            "documentation-knowledge",
            "review-audit",
            "security-operations",
            "delivery-coordination",
            "retrospective-improvement",
        ]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "violates precedence: release-change must precede project-context",
            result.stdout,
        )

    def test_incident_planning_after_implementation_fails(self) -> None:
        receipts = load_fixture()
        incident = scenario(receipts, "ROUTE-010")
        route = incident["actual_route"]
        assert isinstance(route, list)
        route.remove("delivery-planning")
        route.insert(route.index("testing-quality") + 1, "delivery-planning")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "violates precedence: delivery-planning must precede implementation-execution",
            result.stdout,
        )

    def test_equivalent_evidence_owner_order_passes(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-005")
        item = synthetic_policy_scenario(contract)
        item["actual_route"] = [
            "release-change",
            "security-operations",
            "review-audit",
            "documentation-knowledge",
            "testing-quality",
            "release-change",
        ]
        for skill in (
            "review-audit",
            "documentation-knowledge",
            "testing-quality",
        ):
            item["conditional_dispositions"][skill] = {
                "state": "activated",
                "rationale": (
                    "Synthetic evidence activates this owner before contract comparison."
                ),
                "evidence": ["Synthetic evidence-owner ordering fixture."],
            }
        set_fresh_scenarios(receipts, [item])

        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_precedence_violation_fails(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-001")["actual_route"] = [
            "delivery-orchestrator",
            "project-context",
            "requirements-acceptance",
            "delivery-planning",
            "solution-design",
        ]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "violates precedence: solution-design must precede delivery-planning",
            result.stdout,
        )

    def test_legacy_dependency_fails(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-008")["actual_route"]
        assert isinstance(route, list)
        route.append("superpowers")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("uses forbidden dependencies: superpowers", result.stdout)

    def test_undeclared_reentry_fails(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-001")["actual_route"]
        assert isinstance(route, list)
        route.append("project-context")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repeats capabilities without a re-entry contract", result.stdout)

    def test_blocked_conditional_cannot_pass_route_policy(self) -> None:
        receipts = load_fixture()
        disposition = scenario(receipts, "ROUTE-004")["conditional_dispositions"][
            "testing-quality"
        ]
        disposition["state"] = "blocked"
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("blocked conditional branch", result.stdout)

    def test_fresh_planned_future_retrospective_is_omitted_from_route(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-016")
        preview = synthetic_policy_scenario(contract)
        preview["conditional_dispositions"]["retrospective-improvement"] = {
            "state": "planned-future",
            "rationale": "Learning remains conditional on a future preview outcome.",
            "evidence": ["No delivery result exists in this route-only observation."],
        }
        set_fresh_scenarios(receipts, [preview])

        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        preview["actual_route"].append("retrospective-improvement")
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "fresh receipt includes future-only capability retrospective-improvement",
            result.stdout,
        )

    def test_conditional_disposition_requires_substantive_rationale(self) -> None:
        receipts = load_fixture()
        disposition = scenario(receipts, "ROUTE-004")["conditional_dispositions"][
            "testing-quality"
        ]
        disposition["rationale"] = "x"
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lacks a substantive rationale", result.stdout)

    def test_conditional_disposition_requires_evidence(self) -> None:
        receipts = load_fixture()
        disposition = scenario(receipts, "ROUTE-004")["conditional_dispositions"][
            "testing-quality"
        ]
        disposition["evidence"] = []
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("disposition for testing-quality lacks evidence", result.stdout)

    def test_route_only_checker_rejects_delivery_pass(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-001")["delivery_result"] = "pass"
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("this checker is route-only", result.stdout)

    def test_route_evidence_cannot_be_empty(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-001")["evidence"] = []
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence must be a non-empty string list", result.stdout)

    def test_extra_capability_requires_justification(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-001")["actual_route"]
        assert isinstance(route, list)
        route.append("documentation-knowledge")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lacks justification for extra capabilities", result.stdout)

    def test_unloaded_specialist_fails(self) -> None:
        receipts = load_fixture()
        loaded = receipts["loaded_specialists"]
        assert isinstance(loaded, list)
        loaded[:] = [item for item in loaded if item["skill"] != "solution-design"]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("without load evidence: solution-design", result.stdout)

    def test_route_only_observation_rejects_effects(self) -> None:
        receipts = load_fixture()
        receipts["effects_performed"] = ["ad-hoc signing"]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty effects_performed", result.stdout)

    def test_legacy_runtime_event_fails(self) -> None:
        receipts = load_fixture()
        receipts["legacy_runtime_events"] = ["epic hook started"]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no legacy runtime events", result.stdout)

    def test_contract_cycle_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["precedence"].append(["delivery-planning", "project-context"])
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("precedence graph contains a cycle", result.stdout)

    def test_conditional_forbidden_contradiction_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["forbidden_capabilities"].append("solution-design")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("both conditional and forbidden: solution-design", result.stdout)

    def test_duplicate_required_capability_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["required_capabilities"].append("project-context")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repeats required_capabilities: project-context", result.stdout)

    def test_required_forbidden_contradiction_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["forbidden_capabilities"].append("project-context")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("both required and forbidden: project-context", result.stdout)

    def test_unselectable_allowed_reentry_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["allowed_reentry"].append("documentation-knowledge")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("allows re-entry for unselectable capabilities", result.stdout)

    def test_missing_return_after_contract_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-005")
        del route["required_reentry_after"]
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required re-entry lacks return-after owners", result.stdout)

    def test_missing_entry_before_contract_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-005")
        del route["required_reentry_before"]
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required re-entry lacks entry-before owners", result.stdout)

    def test_contract_requires_all_superseded_runtime_identities(self) -> None:
        contracts = load_contracts()
        dependencies = contracts["forbidden_runtime_dependencies"]
        assert isinstance(dependencies, list)
        dependencies.remove("epic-harness")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must forbid the known superseded runtime dependencies", result.stdout)

    def test_contract_rejects_empty_scenario_metadata(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["prompt"] = ""
        route["scale"] = ""
        route["risk"] = ""
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("field prompt must be a non-empty string", result.stdout)
        self.assertIn("field scale must be a non-empty string", result.stdout)
        self.assertIn("field risk must be a non-empty string", result.stdout)

    def test_contract_rejects_unknown_nested_fields(self) -> None:
        contracts = load_contracts()
        contracts["unexpected_root_metadata"] = True
        item = scenario(contracts, "ROUTE-001")
        item["unexpected_scenario_metadata"] = True
        item["conditional_capabilities"][0]["unexpected_trigger_metadata"] = True

        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "route suite has unsupported fields: unexpected_root_metadata",
            result.stdout,
        )
        self.assertIn(
            "ROUTE-001 has unsupported fields: unexpected_scenario_metadata",
            result.stdout,
        )
        self.assertIn(
            "has unsupported fields: unexpected_trigger_metadata",
            result.stdout,
        )

    def test_contract_rejects_noncanonical_taxonomy_tokens(self) -> None:
        cases = (
            ("scale", "Medium", "unsupported scale"),
            ("risk", "medium/high", "unsupported risk"),
            ("authority", "analysis-only", "unsupported authority"),
        )
        for field, value, expected in cases:
            with self.subTest(field=field, value=value):
                contracts = load_contracts()
                scenario(contracts, "ROUTE-001")[field] = value
                result = run_contract_checker_with_contract(contracts)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stdout)

    def test_contract_rejects_invalid_final_after_policy(self) -> None:
        cases = (
            (
                {"release-change": ["unknown-owner"]},
                "references unselectable capabilities: unknown-owner",
            ),
            (
                {"documentation-knowledge": ["testing-quality"]},
                "final-after controller documentation-knowledge must be selectable",
            ),
        )
        for final_after, expected in cases:
            with self.subTest(final_after=final_after):
                contracts = load_contracts()
                scenario(contracts, "ROUTE-014")["required_final_after"] = final_after
                result = run_contract_checker_with_contract(contracts)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stdout)

    def test_fresh_receipt_requires_declared_lead_to_open_route(self) -> None:
        cases = {
            "ROUTE-014": ["release-change", "testing-quality", "release-change"],
            "ROUTE-017": ["release-change", "testing-quality", "security-operations"],
            "ROUTE-017C": ["testing-quality", "security-operations", "release-change"],
        }
        contracts = load_contracts()
        for scenario_id, malformed_route in cases.items():
            with self.subTest(scenario=scenario_id):
                receipts = make_fresh_receipts(load_fixture())
                contract = scenario(contracts, scenario_id)
                item = synthetic_policy_scenario(contract)
                item["actual_route"] = malformed_route
                set_fresh_scenarios(receipts, [item])
                result = run_receipt_checker(receipts, allow_historical=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("does not open with lead capability", result.stdout)

    def test_fresh_receipt_binds_exact_prompt(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        scenario(receipts, "ROUTE-010")["prompt"] = (
            "Investigate this incomplete idea and tell me what to build."
        )
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("prompt does not match the canonical blind prompt", result.stdout)

    def test_fresh_observation_digest_is_recomputed(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        receipts["task_identity"]["source_observation_sha256"] = "0" * 64
        result = run_receipt_checker(
            receipts,
            allow_historical=False,
            recompute_fresh_digest=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match the canonical fresh observation", result.stdout)

    def test_fresh_loaded_specialist_binds_bytes_and_read_evidence(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        loaded = receipts["loaded_specialists"][0]
        loaded["skill_sha256"] = "0" * 64
        loaded["evidence"] = []
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lacks read evidence", result.stdout)
        self.assertIn("does not match the inspected plugin", result.stdout)

    def test_fresh_loaded_specialists_match_present_routes_exactly(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-014")
        item = synthetic_policy_scenario(contract)
        all_load_records = copy.deepcopy(receipts["loaded_specialists"])
        set_fresh_scenarios(receipts, [item])
        selected = set(item["actual_route"])
        extra_record = next(
            load for load in all_load_records if load["skill"] not in selected
        )
        receipts["loaded_specialists"].append(extra_record)

        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "loaded_specialists contains skills absent from every actual route",
            result.stdout,
        )

    def test_fresh_envelope_requires_exact_top_level_fields(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        del receipts["legacy_administrative_visibility"]
        receipts["unexpected_internal_metadata"] = []

        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "fresh-task envelope missing fields: legacy_administrative_visibility",
            result.stdout,
        )
        self.assertIn(
            "fresh-task envelope has unsupported fields: unexpected_internal_metadata",
            result.stdout,
        )

    def test_fresh_envelope_requires_exact_nested_fields(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        receipts["plugin_identity"]["unexpected_secret_metadata"] = "reject-me"
        receipts["task_identity"]["thread_id"] = (
            "019f7eca-80d8-7560-b47a-ef20a7dfbf96"
        )
        receipts["repository_identity"]["absolute_path"] = "/private/path"
        receipts["loaded_specialists"][0]["tool_event"] = "unverified"
        item = scenario(receipts, "ROUTE-014")
        item["effects_performed"] = ["deployed-production"]
        disposition = next(iter(item["conditional_dispositions"].values()))
        disposition["unexpected_trigger_claim"] = True
        item["actual_route"].append("documentation-knowledge")
        item["extra_capability_justifications"]["documentation-knowledge"] = {
            "rationale": "Synthetic extra route owner for nested-schema validation.",
            "evidence": ["Synthetic evidence."],
            "internal_task_id": "should-not-pass",
        }

        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        for expected in (
            "plugin_identity has unsupported fields: unexpected_secret_metadata",
            "task_identity has unsupported fields: thread_id",
            "repository_identity has unsupported fields: absolute_path",
            "loaded specialist 1 has unsupported fields: tool_event",
            "ROUTE-014 receipt has unsupported fields: effects_performed",
            "has unsupported fields: unexpected_trigger_claim",
            "has unsupported fields: internal_task_id",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, result.stdout)

    def test_fresh_route_only_receipt_rejects_activated_retrospective(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-016")
        preview = synthetic_policy_scenario(contract)
        set_fresh_scenarios(receipts, [preview])
        preview["actual_route"].append("retrospective-improvement")
        preview["conditional_dispositions"]["retrospective-improvement"] = {
            "state": "activated",
            "rationale": "Synthetic mutation activates retrospective before an outcome exists.",
            "evidence": ["Delivery remains not run in this route-only receipt."],
        }

        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "route-only retrospective must remain planned-future",
            result.stdout,
        )

    def test_fresh_plugin_identity_is_bound_to_inspected_install(self) -> None:
        cases = (
            (
                "installed_version",
                "1.3.1",
                "installed_version does not match the installed manifest",
            ),
            (
                "source_revision",
                "abcdef0123456789",
                "source_revision does not match the expected release revision",
            ),
            (
                "manifest_sha256",
                "0" * 64,
                "manifest_sha256 does not match the installed manifest",
            ),
            (
                "payload_sha256",
                "0" * 64,
                "payload_sha256 does not match the installed payload",
            ),
            (
                "payload_hash_method",
                "unspecified hash",
                "payload_hash_method does not match the canonical method",
            ),
            (
                "cache_relative_path",
                "plugins/cache/personal/project-delivery/wrong-version",
                "cache_relative_path does not match the inspected root",
            ),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                receipts = make_fresh_receipts(load_fixture())
                receipts["plugin_identity"][field] = value
                result = run_receipt_checker(receipts, allow_historical=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stdout)

    def test_task_identity_rejects_internal_ids_and_non_utc_time(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        receipts["task_identity"]["public_receipt_id"] = (
            "019f7eca-80d8-7560-b47a-ef20a7dfbf96"
        )
        receipts["task_identity"]["selected_at"] = "July 20, 2026"
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("without an internal identifier", result.stdout)
        self.assertIn("must be a UTC ISO-8601 timestamp", result.stdout)

    def test_observed_required_owner_omissions_fail(self) -> None:
        cases = {
            "ROUTE-006": "delivery-coordination",
            "ROUTE-009": "testing-quality",
            "ROUTE-017D": "security-operations",
            "ROUTE-021": "testing-quality",
        }
        contracts = load_contracts()
        for scenario_id, omitted in cases.items():
            with self.subTest(scenario=scenario_id, omitted=omitted):
                receipts = make_fresh_receipts(load_fixture())
                contract = scenario(contracts, scenario_id)
                item = synthetic_policy_scenario(contract)
                item["actual_route"] = [
                    skill for skill in item["actual_route"] if skill != omitted
                ]
                set_fresh_scenarios(receipts, [item])
                result = run_receipt_checker(receipts, allow_historical=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"misses required capabilities: {omitted}", result.stdout)

    def test_final_release_disposition_must_follow_evidence_owners(self) -> None:
        malformed_routes = {
            "ROUTE-014": [
                "testing-quality",
                "release-change",
                "testing-quality",
            ],
            "ROUTE-016": [
                "delivery-orchestrator",
                "project-context",
                "requirements-acceptance",
                "solution-design",
                "security-operations",
                "delivery-planning",
                "implementation-execution",
                "release-change",
                "testing-quality",
                "documentation-knowledge",
                "review-audit",
            ],
            "ROUTE-017": [
                "testing-quality",
                "release-change",
                "security-operations",
            ],
            "ROUTE-017C": [
                "security-operations",
                "testing-quality",
                "release-change",
                "testing-quality",
            ],
        }
        contracts = load_contracts()
        for scenario_id, malformed_route in malformed_routes.items():
            with self.subTest(scenario=scenario_id):
                receipts = make_fresh_receipts(load_fixture())
                contract = scenario(contracts, scenario_id)
                item = synthetic_policy_scenario(contract)
                item["actual_route"] = malformed_route
                set_fresh_scenarios(receipts, [item])
                result = run_receipt_checker(receipts, allow_historical=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    f"{scenario_id} final release-change disposition does not follow",
                    result.stdout,
                )

    def test_final_release_disposition_follows_activated_conditional_evidence(self) -> None:
        cases = {
            "ROUTE-017": (
                [
                    "testing-quality",
                    "security-operations",
                    "release-change",
                    "documentation-knowledge",
                ],
                ["documentation-knowledge"],
            ),
            "ROUTE-017A": (
                [
                    "testing-quality",
                    "release-change",
                    "security-operations",
                ],
                ["release-change", "security-operations"],
            ),
            "ROUTE-017B": (
                [
                    "release-change",
                    "testing-quality",
                    "release-change",
                    "security-operations",
                ],
                ["security-operations"],
            ),
            "ROUTE-017C": (
                [
                    "security-operations",
                    "testing-quality",
                    "release-change",
                    "review-audit",
                ],
                ["review-audit"],
            ),
            "ROUTE-017D": (
                [
                    "release-change",
                    "testing-quality",
                    "security-operations",
                    "release-change",
                    "review-audit",
                ],
                ["review-audit"],
            ),
        }
        contracts = load_contracts()
        for scenario_id, (malformed_route, activated) in cases.items():
            with self.subTest(scenario=scenario_id):
                receipts = make_fresh_receipts(load_fixture())
                contract = scenario(contracts, scenario_id)
                item = synthetic_policy_scenario(contract)
                item["actual_route"] = malformed_route
                for skill in activated:
                    item["conditional_dispositions"][skill] = {
                        "state": "activated",
                        "rationale": (
                            "Synthetic evidence activates this decision-bearing branch "
                            "before contract comparison."
                        ),
                        "evidence": ["Synthetic conditional-owner ordering evidence."],
                    }
                set_fresh_scenarios(receipts, [item])
                result = run_receipt_checker(receipts, allow_historical=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    f"{scenario_id} final release-change disposition does not follow",
                    result.stdout,
                )

    def test_contract_rejects_malformed_scenario_id(self) -> None:
        contracts = load_contracts()
        scenario(contracts, "ROUTE-001")["id"] = "route one"
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("has malformed scenario ID", result.stdout)

    def test_natural_package_controller_return_passes(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-017B")
        set_fresh_scenarios(receipts, [
            {
                "id": "ROUTE-017B",
                "prompt": contract["prompt"],
                "scale": contract["scale"],
                "risk": contract["risk"],
                "authority": contract["authority"],
                "taxonomy_rationale": (
                    "Synthetic package classification fixed before contract comparison for "
                    "the route-policy regression scenario."
                ),
                "taxonomy_evidence": ["Synthetic pre-comparison taxonomy evidence."],
                "actual_route": [
                    "release-change",
                    "testing-quality",
                    "release-change",
                ],
                "conditional_dispositions": {
                    item["skill"]: {
                        "state": "not-applicable",
                        "rationale": "Synthetic policy test leaves this evidence-triggered branch inactive.",
                        "evidence": ["Synthetic route-policy regression fixture."],
                    }
                    for item in contract["conditional_capabilities"]
                },
                "extra_capability_justifications": {},
                "delivery_result": "not-run",
                "evidence": ["Synthetic route-policy regression fixture."],
                "gaps": [],
            }
        ])
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_release_execution_and_decommission_routes_pass_bounded_policy(self) -> None:
        contracts = load_contracts()
        for scenario_id in ("ROUTE-019", "ROUTE-020"):
            with self.subTest(scenario=scenario_id):
                receipts = make_fresh_receipts(load_fixture())
                item = synthetic_policy_scenario(scenario(contracts, scenario_id))
                set_fresh_scenarios(receipts, [item])

                result = run_receipt_checker(receipts, allow_historical=False)

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                if scenario_id == "ROUTE-019":
                    self.assertEqual(item["authority"], "release-execution")
                    self.assertEqual(item["actual_route"][0], "release-change")
                    self.assertEqual(item["actual_route"][-1], "release-change")
                else:
                    self.assertEqual(item["authority"], "change")
                    self.assertEqual(item["actual_route"][0], "delivery-orchestrator")
                    self.assertLess(
                        item["actual_route"].index("security-operations"),
                        item["actual_route"].index("implementation-execution"),
                    )
                    self.assertLess(
                        item["actual_route"].index("testing-quality"),
                        item["actual_route"].index("release-change"),
                    )

    def test_synthetic_route_policy_matrix_passes_all_25_contracts(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contracts = load_contracts()["scenarios"]
        set_fresh_scenarios(receipts, [
            synthetic_policy_scenario(contract) for contract in contracts
        ])
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("route_policy_records=25", result.stdout)

    def test_mutation_does_not_modify_source_fixture(self) -> None:
        first = load_fixture()
        second = copy.deepcopy(first)
        scenario(second, "ROUTE-001")["actual_route"] = []
        self.assertNotEqual(
            scenario(first, "ROUTE-001")["actual_route"],
            scenario(second, "ROUTE-001")["actual_route"],
        )


if __name__ == "__main__":
    unittest.main()
