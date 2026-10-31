"""Review coverage must reject omissions, mismatched source, and unsafe routes."""

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("mindrally_coverage", SCRIPTS / "check_mindrally_skills.py")
coverage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coverage)


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.evidence = self.root / "docs/reviews/mindrally-skills"
        self.evidence.mkdir(parents=True)
        self.skill = self.root / "plugins/mindrally-skills/skills/example"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("Read [patterns](references/patterns.md) when implementing.\n")
        (self.skill / "references/patterns.md").write_text("Use the project's tested implementation.\n")
        digest = hashlib.sha256(b"synthetic upstream skill").hexdigest()
        self.inventory = {"source_commit": "a" * 40, "skill_count": 1, "skills": [
            {"skill": "example", "source_path": "example/SKILL.md", "source_sha256": digest}
        ]}
        self.audit = {"source_commit": "a" * 40, "records": [{
            "skill": "example", "source_sha256": digest,
            "reviewed_source_sections": ["Workflow"],
            "corrections": ["Corrected the documented boundary condition."],
            "primary_sources": [{"url": "https://docs.python.org/3/", "checked_claim": "Versioned APIs require matching documentation."}],
            "verification_limits": ["No target application runtime executed."],
            "references": ["references/patterns.md"],
        }]}

    def check(self):
        (self.evidence / "source-inventory.json").write_text(json.dumps(self.inventory))
        (self.evidence / "audit-batch-1.json").write_text(json.dumps(self.audit))
        with patch.object(coverage, "EXPECTED_SKILLS", 1):
            return coverage.validate(self.root)[0]

    def test_complete_review_and_routed_package_pass(self):
        self.assertEqual([], self.check())

    def test_missing_skill_or_review_cannot_pass(self):
        (self.skill / "SKILL.md").unlink()
        self.audit["records"] = []
        errors = self.check()
        self.assertTrue(any("missing packaged skill" in item for item in errors))
        self.assertTrue(any("missing individual review" in item for item in errors))

    def test_wrong_revision_and_duplicate_review_cannot_pass(self):
        self.audit["records"][0]["source_sha256"] = "b" * 64
        self.audit["records"] *= 2
        errors = self.check()
        self.assertTrue(any("hash mismatch" in item for item in errors))
        self.assertTrue(any("duplicate review" in item for item in errors))

    def test_source_and_claim_evidence_required(self):
        self.audit["records"][0]["primary_sources"] = [{"url": "https://docs.python.org/3/"}]
        self.assertTrue(any("checked claim" in item for item in self.check()))

    def test_references_must_be_contained_and_directly_routed(self):
        self.audit["records"][0]["references"] = ["../other.md", "references/unrouted.md"]
        (self.skill / "references/unrouted.md").write_text("Conditional detail.\n")
        errors = self.check()
        self.assertTrue(any("escapes" in item for item in errors))
        self.assertTrue(any("not directly routed" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
