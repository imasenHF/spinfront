"""Verify builds publish daily pages without obsolete download artifacts."""
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build', ROOT / 'scripts/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class BuildOutputTests(unittest.TestCase):
    def test_fresh_and_repeated_builds_have_no_download_directory(self):
        with tempfile.TemporaryDirectory(prefix='.build-test-', dir=ROOT) as folder:
            output = Path(folder)

            def run_build():
                with patch('sys.argv', ['build.py', '--output', output.name]):
                    with contextlib.redirect_stdout(io.StringIO()):
                        build.main()

            run_build()
            self.assertFalse((output / 'downloads').exists())
            _, _, issues = build.load()
            for issue in issues:
                self.assertTrue((output / issue['report_date'] / 'index.html').is_file())
            for name in ['index.html', 'index.json', 'search-index.json']:
                self.assertTrue((output / name).is_file())

            legacy = output / 'downloads'
            legacy.mkdir()
            (legacy / 'old-issue.html').write_text('obsolete', encoding='utf-8')
            run_build()
            self.assertFalse(legacy.exists())
            self.assertTrue((output / issues[-1]['report_date'] / 'index.html').is_file())


if __name__ == '__main__':
    unittest.main()
