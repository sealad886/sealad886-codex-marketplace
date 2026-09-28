from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
EXPORTER = REPOSITORY_ROOT / "scripts" / "export_route_prompts.py"


class PromptExportTests(unittest.TestCase):
    def test_prompt_manifest_is_derived_without_expected_semantics(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXPORTER), "--root", str(REPOSITORY_ROOT)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        exported = json.loads(result.stdout)
        contracts = json.loads(
            (REPOSITORY_ROOT / "tests" / "route-contracts.json").read_text(
                encoding="utf-8"
            )
        )

        expected = [
            {"id": scenario["id"], "prompt": scenario["prompt"]}
            for scenario in contracts["scenarios"]
        ]
        self.assertEqual(exported["scenarios"], expected)
        self.assertEqual(exported["source_contract_schema_version"], 3)
        self.assertEqual(exported["evidence_class"], "prompt-only blind canary input")
        self.assertTrue(
            all(set(item) == {"id", "prompt"} for item in exported["scenarios"])
        )
        self.assertIn("PROMPT [25/25] id=ROUTE-021", result.stderr)


if __name__ == "__main__":
    unittest.main()
