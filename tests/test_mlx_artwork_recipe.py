import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTWORK_README = ROOT / "design" / "mlx-optimizer" / "README.md"


class MlxArtworkRecipeTests(unittest.TestCase):
    def run_recipe(self, fixture, fail_compiler=""):
        recipe = ARTWORK_README.read_text(encoding="utf-8").split("```sh\n", 1)[1].split("```", 1)[0]
        # Keep the old vulnerable recipe safe to execute during its RED regression.
        recipe = recipe.replace("/private/tmp/mlx-rebuild-render", str(fixture / "stale-render"))
        recipe = recipe.replace("/private/tmp/mlx-icon-finish", str(fixture / "stale-finish"))
        # Exercise shell control flow without Swift, images, or native applications.
        recipe = recipe.replace("'/Applications/Icon Composer.app/Contents/Executables/ictool'", "ictool")
        command_dir = fixture / "commands"
        command_dir.mkdir()
        temporary_builds = fixture / "builds"
        temporary_builds.mkdir()
        log = fixture / "commands.jsonl"
        compiler = command_dir / "swiftc"
        compiler.write_text(
            f"#!{sys.executable}\n"
            "import json, os, stat, sys\n"
            "from pathlib import Path\n"
            "output = Path(sys.argv[sys.argv.index('-o') + 1])\n"
            "kind = 'render' if 'render' in output.name else 'finish'\n"
            "with open(os.environ['ARTWORK_LOG'], 'a') as handle:\n"
            "    handle.write(json.dumps({'compiled': str(output), 'mode': stat.S_IMODE(output.parent.stat().st_mode)}) + '\\n')\n"
            "output.write_text('#!/bin/sh\\necho ' + repr(json.dumps({'ran': kind})) + ' >> \"$ARTWORK_LOG\"\\n')\n"
            "output.chmod(0o700)\n"
            "raise SystemExit(23 if os.environ['ARTWORK_FAIL'] == kind else 0)\n",
            encoding="utf-8",
        )
        compiler.chmod(0o700)
        for name in ("sips", "ictool"):
            command = command_dir / name
            command.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            command.chmod(0o700)
        env = os.environ.copy()
        env.update(
            PATH=str(command_dir) + os.pathsep + env.get("PATH", ""),
            TMPDIR=str(temporary_builds),
            ARTWORK_LOG=str(log),
            ARTWORK_FAIL=fail_compiler,
        )
        result = subprocess.run(
            ["sh", "-c", recipe],
            cwd=fixture,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=10,
        )
        records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
        return result, records, temporary_builds

    def test_compiler_failure_never_runs_stale_output(self):
        for failed_stage in ("render", "finish"):
            with self.subTest(stage=failed_stage), tempfile.TemporaryDirectory() as tmp:
                result, records, builds = self.run_recipe(Path(tmp).resolve(), failed_stage)

                self.assertNotEqual(result.returncode, 0, result.stderr)
                self.assertNotIn({"ran": failed_stage}, records)
                self.assertEqual(list(builds.iterdir()), [])

    def test_success_uses_private_temporary_binaries_and_cleans_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, records, builds = self.run_recipe(Path(tmp).resolve())

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn({"ran": "render"}, records)
            self.assertIn({"ran": "finish"}, records)
            compiled = [record for record in records if "compiled" in record]
            self.assertEqual(len(compiled), 2)
            directories = {Path(record["compiled"]).parent for record in compiled}
            self.assertEqual(len(directories), 1)
            for record in compiled:
                self.assertEqual(record["mode"], stat.S_IRWXU)
                self.assertEqual(Path(record["compiled"]).parent.parent, builds)
                self.assertFalse(Path(record["compiled"]).parent.exists())


if __name__ == "__main__":
    unittest.main()
