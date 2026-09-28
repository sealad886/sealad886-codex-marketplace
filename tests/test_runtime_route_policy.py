from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "project-delivery"
SHARED = PLUGIN_ROOT / "skills" / ".shared"


class RuntimeRoutePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contracts = json.loads(
            (REPOSITORY_ROOT / "tests" / "route-contracts.json").read_text(
                encoding="utf-8"
            )
        )
        cls.operating_model = (SHARED / "operating-model.md").read_text(
            encoding="utf-8"
        )
        cls.templates = (SHARED / "artifact-templates.md").read_text(
            encoding="utf-8"
        )
        cls.orchestrator = (
            PLUGIN_ROOT / "skills" / "delivery-orchestrator" / "SKILL.md"
        ).read_text(encoding="utf-8")
        cls.route_profiles = json.loads(
            (SHARED / "route-profiles-v1.json").read_text(encoding="utf-8")
        )

    def test_runtime_taxonomy_covers_every_contract_value(self) -> None:
        scenarios = self.contracts["scenarios"]
        accepted_fields = {
            "scale": "accepted_scales",
            "risk": "accepted_risks",
        }
        for field in ("scale", "risk", "authority"):
            with self.subTest(field=field):
                values = {scenario[field] for scenario in scenarios}
                accepted_field = accepted_fields.get(field)
                if accepted_field is not None:
                    values.update(
                        value
                        for scenario in scenarios
                        for value in scenario[accepted_field]
                    )
                for value in sorted(values):
                    self.assertIn(f"`{value}`", self.operating_model)

    def test_orchestrator_uses_canonical_runtime_route_profiles(self) -> None:
        required_fragments = (
            "Read `../.shared/operating-model.md` and `../.shared/route-profiles-v1.json` before routing.",
            "Select exactly one canonical profile",
            "Required and conditional owners are disjoint.",
            "incident-hotfix",
            "preview-migration-delivery",
            "`allowed_scales` or `allowed_risks`",
            "release-execution",
            "workflow-decommission",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.orchestrator)

        profiles = self.route_profiles["profiles"]
        self.assertEqual(len(profiles), 25)
        self.assertEqual(len({profile["id"] for profile in profiles}), 25)

    def test_runtime_taxonomy_is_broader_than_blind_canary_tolerance(self) -> None:
        profiles = {
            profile["id"]: profile for profile in self.route_profiles["profiles"]
        }
        strict_subsets = 0
        for contract in self.contracts["scenarios"]:
            profile = profiles[contract["profile_id"]]
            for accepted_field, allowed_field in (
                ("accepted_scales", "allowed_scales"),
                ("accepted_risks", "allowed_risks"),
            ):
                with self.subTest(
                    route=contract["id"],
                    accepted=accepted_field,
                    allowed=allowed_field,
                ):
                    accepted = set(contract[accepted_field])
                    allowed = set(profile[allowed_field])
                    self.assertLessEqual(accepted, allowed)
                    strict_subsets += accepted < allowed

        medium_feature = profiles["medium-feature-change"]
        medium_contract = next(
            item for item in self.contracts["scenarios"] if item["id"] == "ROUTE-002"
        )
        self.assertIn("high", medium_feature["allowed_risks"])
        self.assertNotIn("high", medium_contract["accepted_risks"])
        self.assertGreater(strict_subsets, 0)

    def test_profiles_define_semantic_boundaries_without_canary_prompts(self) -> None:
        serialized_profiles = json.dumps(self.route_profiles, ensure_ascii=False)
        self.assertNotIn("ROUTE-", serialized_profiles)
        self.assertNotIn("Requests whose semantic intent is", serialized_profiles)
        for profile in self.route_profiles["profiles"]:
            with self.subTest(profile=profile["id"]):
                intent = profile["intent"].casefold()
                self.assertIn("select when", intent)
                self.assertTrue(
                    any(
                        boundary in intent
                        for boundary in ("do not use", "rather than", "instead of")
                    )
                )
        for contract in self.contracts["scenarios"]:
            with self.subTest(prompt=contract["id"]):
                self.assertNotIn(contract["prompt"], serialized_profiles)

    def test_profiles_have_no_superseded_runtime_dependency(self) -> None:
        superseded = {"boss", "epic", "epic-harness", "superpowers"}
        for profile in self.route_profiles["profiles"]:
            routed = set(profile["required_capabilities"])
            routed.update(
                item["skill"] for item in profile["conditional_capabilities"]
            )
            with self.subTest(profile=profile["id"]):
                self.assertFalse(routed.intersection(superseded))

    def test_specialist_boundaries_match_evidence_claim_routes(self) -> None:
        testing = (
            PLUGIN_ROOT / "skills" / "testing-quality" / "SKILL.md"
        ).read_text(encoding="utf-8")
        release = (
            PLUGIN_ROOT / "skills" / "release-change" / "SKILL.md"
        ).read_text(encoding="utf-8")
        security = (
            PLUGIN_ROOT / "skills" / "security-operations" / "SKILL.md"
        ).read_text(encoding="utf-8")
        documentation = (
            PLUGIN_ROOT / "skills" / "documentation-knowledge" / "SKILL.md"
        ).read_text(encoding="utf-8")
        coordination = (
            PLUGIN_ROOT / "skills" / "delivery-coordination" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Lead flaky-CI triage", testing)
        self.assertIn("Lead package-artifact and distribution/installability", release)
        self.assertIn("Lead signing/notarization claim audits", security)
        self.assertIn("never sign", security)
        self.assertIn("publishing, deploying, distributing, installing", release)
        self.assertIn("Route executable or measurable validation through `testing-quality`", documentation)
        self.assertIn("operational or stakeholder handoff", coordination)

    def test_machine_receipt_template_matches_closed_schema_v3_envelope(self) -> None:
        match = re.search(
            r"### Machine-comparable route receipt.*?```json\n(.*?)\n```",
            self.templates,
            re.DOTALL,
        )
        self.assertIsNotNone(match, "machine route receipt JSON template missing")
        envelope = json.loads(match.group(1))

        schema = json.loads(
            (SHARED / "live-route-receipt-v3.schema.json").read_text(
                encoding="utf-8"
            )
        )
        required_root_fields = set(schema["required"])
        self.assertEqual(set(envelope), required_root_fields)
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(envelope["schema_version"], 3)
        self.assertEqual(envelope["contract_schema_version"], 3)
        self.assertEqual(
            envelope["evidence_class"], "fresh-task semantic route observation"
        )
        self.assertTrue(
            envelope["semantic_fields_were_frozen_before_contract_comparison"]
        )
        self.assertEqual(envelope["observation_scope"], "route-only-no-effects")
        self.assertEqual(envelope["effects_performed"], [])
        self.assertEqual(envelope["legacy_runtime_events"], [])
        self.assertEqual(
            envelope["plugin_identity"]["payload_hash_method"],
            "project-delivery length-prefixed path-and-content sha256 v1",
        )

        expected_freeze_scope = {
            "actual_route",
            "authority",
            "conditional_dispositions",
            "evidence",
            "extra_capability_justifications",
            "gaps",
            "outcome_observation",
            "risk",
            "scale",
            "scenario_observation",
            "taxonomy_evidence",
            "taxonomy_rationale",
        }
        self.assertEqual(set(envelope["semantic_freeze_scope"]), expected_freeze_scope)
        self.assertEqual(envelope["legacy_invocations"], [])
        self.assertEqual(envelope["legacy_branded_state_created"], [])
        disposition = next(iter(envelope["scenarios"][0]["conditional_dispositions"].values()))
        self.assertEqual(
            set(disposition["trigger_evaluation"]),
            {"trigger_statement", "source", "result"},
        )
        self.assertEqual(disposition["trigger_evaluation"]["source"], "installed-runtime")

    def test_orchestrator_template_instruction_closure_is_complete(self) -> None:
        envelope_match = re.search(
            r"### Machine-comparable route receipt.*?```json\n(.*?)\n```",
            self.templates,
            re.DOTALL,
        )
        self.assertIsNotNone(envelope_match)
        envelope = json.loads(envelope_match.group(1))
        template_files = {
            item["relative_path"]
            for item in envelope["loaded_specialists"][0]["instruction_closure"]["files"]
        }
        references = {
            (
                PLUGIN_ROOT / "skills" / "delivery-orchestrator" / match
            ).resolve().relative_to(PLUGIN_ROOT.resolve()).as_posix()
            for match in re.findall(
                r"`(\.\./\.shared/[a-z0-9._-]+\.(?:json|md))`",
                self.orchestrator,
            )
        }
        self.assertEqual(
            template_files,
            {"skills/delivery-orchestrator/SKILL.md", *references},
        )

    def test_prospective_retrospective_is_not_present_activation(self) -> None:
        self.assertIn(
            "never activate retrospective merely because the canary imagines a future delivery",
            self.orchestrator,
        )
        self.assertIn(
            "omit it from `actual_route`",
            self.orchestrator,
        )
        self.assertIn(
            "`planned-future` is reserved for a profile-declared retrospective branch",
            self.operating_model,
        )


if __name__ == "__main__":
    unittest.main()
