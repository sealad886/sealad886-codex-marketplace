"""Exercise release allocation/freshness contracts at their external command boundary."""
import contextlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import textwrap
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
AUTO = ROOT / '.github/workflows/plugin-release-marketplace.yml'
MANUAL = ROOT / '.github/workflows/marketplace-release.yml'


def heredocs():
    return [textwrap.dedent(s) for s in re.findall(
        r"python3 - <<'PY'\n(.*?)^          PY$", AUTO.read_text(), re.M | re.S)]


def allocator():
    return next(s for s in heredocs() if 'git' in s and 'fetch' in s)


class MarketplaceReleaseTests(unittest.TestCase):
    def allocate(self, tags):
        # Git tags exist independently of GitHub Releases; values are peeled SHA/annotation.
        def run(args, **kwargs):
            if args[:2] == ['git', 'fetch']:
                output = ''
            elif args[:3] == ['git', 'tag', '--list']:
                output = '\n'.join(tags)
            elif args == ['git', 'rev-parse', 'HEAD']:
                output = 'current-sha'
            elif args[:2] == ['git', 'rev-parse']:
                output = tags[args[-1][:-3]][0]
            elif args[:2] == ['git', 'for-each-ref']:
                output = tags[args[-1].removeprefix('refs/tags/')][1]
            else:
                raise AssertionError(args)
            return subprocess.CompletedProcess(args, 0, stdout=output)
        output = io.StringIO()
        with patch('subprocess.run', side_effect=run), patch.dict(os.environ, PLUGIN_RELEASE_TAG='plugin-v1.0.0'), contextlib.redirect_stdout(output):
            exec(compile(allocator(), str(AUTO), 'exec'), {})
        return output.getvalue().strip()

    def test_first_snapshot(self):
        self.assertEqual(self.allocate({}), '0.1.0')

    def test_tag_without_release_reserves_version(self):
        self.assertEqual(self.allocate({'marketplace-v2.3.4': ('old-sha', 'manual')}), '2.3.5')

    def test_partial_publication_reuses_owned_tag(self):
        self.assertEqual(self.allocate({'marketplace-v0.1.0': ('current-sha', 'Marketplace snapshot after plugin-v1.0.0')}), '0.1.0')

    def test_same_source_with_other_owner_is_not_reused(self):
        self.assertEqual(self.allocate({'marketplace-v0.1.0': ('current-sha', 'manual')}), '0.1.1')

    def test_same_owner_with_other_source_is_not_reused(self):
        self.assertEqual(self.allocate({'marketplace-v0.1.0': ('old-sha', 'Marketplace snapshot after plugin-v1.0.0')}), '0.1.1')

    def test_older_recovery_does_not_downgrade_latest(self):
        for workflow, variable in [(AUTO, 'MARKETPLACE_TAG'), (MANUAL, 'RELEASE_TAG')]:
            code = textwrap.dedent(re.search(r"python3 -c '\n(.*?)^          '", workflow.read_text(), re.M | re.S).group(1))
            for tag, expected in [('marketplace-v1.0.0', 'false'), ('marketplace-v2.0.0', 'true')]:
                with self.subTest(workflow=workflow.name, tag=tag):
                    output = io.StringIO()
                    with patch.dict(os.environ, {variable: tag}), patch('sys.stdin', io.StringIO(json.dumps([[{'tag_name': 'plugin-v99.0.0', 'draft': False}], [{'tag_name': 'marketplace-v2.0.0', 'draft': False}]]))), contextlib.redirect_stdout(output):
                        exec(compile(code, str(workflow), 'exec'), {})
                    self.assertEqual(output.getvalue().strip(), expected)

    def publish(self, workflow, already_exists=False):
        runs = re.findall(r"^        run: \|\n((?:^          .*\n|^\n)+)", workflow.read_text(), re.M)
        script = next(textwrap.dedent(run) for run in runs if 'gh release create' in run)
        fake_gh = r"""
        gh() {
          [[ " $* " == *" --repo $GITHUB_REPOSITORY "* || " $* " == *" repos/$GITHUB_REPOSITORY/"* ]] || return 42
          case "$1 $2" in
            "api --paginate")
              echo '[[{"tag_name":"plugin-v9.0.0","draft":false}],[{"tag_name":"marketplace-v2.0.0","draft":false}]]' ;;
            "release view") [[ "$ALREADY_EXISTS" == true ]] ;;
            "release create") printf '%s\n' "$@" ;;
            *) return 43 ;;
          esac
        }
        """
        env = dict(os.environ, GITHUB_REPOSITORY='owner/repo', RELEASE_TAG='marketplace-v1.0.0',
                   MARKETPLACE_TAG='marketplace-v1.0.0', PLUGIN_RELEASE_TAG='plugin-v1.0.0',
                   ALREADY_EXISTS=str(already_exists).lower())
        return subprocess.run(['bash', '-c', textwrap.dedent(fake_gh) + script], env=env,
                              check=True, capture_output=True, text=True).stdout

    def test_publish_without_checkout_uses_explicit_repository(self):
        for workflow in (AUTO, MANUAL):
            with self.subTest(workflow=workflow.name):
                self.assertIn('--latest=false', self.publish(workflow))

    def test_existing_release_retry_skips_creation(self):
        for workflow in (AUTO, MANUAL):
            with self.subTest(workflow=workflow.name):
                output = self.publish(workflow, already_exists=True)
                self.assertNotIn('--verify-tag', output)
                self.assertIn('already exists', output)

    def test_manual_tag_must_be_annotated_and_match_validated_sha(self):
        runs = re.findall(r"^        run: \|\n((?:^          .*\n|^\n)+)", MANUAL.read_text(), re.M)
        script = next(textwrap.dedent(run) for run in runs if 'requires an annotated tag' in run)
        fake_gh = r"""
        gh() {
          if [[ "$2" == */git/ref/tags/* ]]; then
            printf '%s\n' "$TAG_OBJECT"
          else
            printf '%s\n' "$TAG_SOURCE"
          fi
        }
        """
        for tag_object, source, success in [('tag-object', 'event-sha', True), ('', 'event-sha', False), ('tag-object', 'moved-sha', False)]:
            with self.subTest(annotated=bool(tag_object), source=source):
                env = dict(os.environ, GITHUB_REPOSITORY='owner/repo', RELEASE_TAG='marketplace-v1.0.0',
                           RELEASE_SHA='event-sha', TAG_OBJECT=tag_object, TAG_SOURCE=source)
                result = subprocess.run(['bash', '-c', textwrap.dedent(fake_gh) + script], env=env,
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode == 0, success)


if __name__ == '__main__':
    unittest.main()
