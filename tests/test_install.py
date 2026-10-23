import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('toolkit_install', ROOT / 'install.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        # Preserve fixtures for inspection; tests never recursively delete paths.
        self.sandbox = Path(tempfile.mkdtemp(prefix='agent-skills-toolkit-test-')).resolve()
        self.destination = self.sandbox / 'skills'

    def command(self, action='install', success=True):
        result = subprocess.run([sys.executable, str(ROOT / 'install.py'), action,
                                 '--destination', str(self.destination)], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def test_install_verify_backup_preserves_unrelated_skill(self):
        other = self.destination / 'unrelated-skill'
        other.mkdir(parents=True)
        (other / 'keep.txt').write_text('preserve me')
        self.command()
        self.command('verify')
        self.command('backup')
        self.assertEqual((other / 'keep.txt').read_text(), 'preserve me')
        backups = list((self.sandbox / 'skill-backups').iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual(sorted(p.name for p in backups[0].iterdir()), sorted(module.NAMES))
        self.assertFalse(any((self.destination / name).exists() for name in module.NAMES))

    def test_collision_stops_before_any_other_skill_is_copied(self):
        existing = self.destination / module.NAMES[-1]
        existing.mkdir(parents=True)
        (existing / 'keep.txt').write_text('do not overwrite')
        self.command(success=False)
        self.assertEqual(list(self.destination.iterdir()), [existing])
        self.assertEqual((existing / 'keep.txt').read_text(), 'do not overwrite')

    def test_modified_install_is_never_moved_by_backup(self):
        self.command()
        file = self.destination / module.NAMES[0] / 'SKILL.md'
        file.write_text(file.read_text(encoding='utf-8') + '\nlocal edit\n', encoding='utf-8')
        self.command('verify', success=False)
        self.command('backup', success=False)
        self.assertTrue(all((self.destination / name).is_dir() for name in module.NAMES))
        self.assertFalse((self.sandbox / 'skill-backups').exists())

    def test_tampered_source_is_detected(self):
        manifest = json.loads((ROOT / 'manifest.json').read_text())
        self.assertEqual(list(module.NAMES), manifest['skills'])
        expected = module.payload()
        for name in module.NAMES:
            self.assertEqual(module.inventory(ROOT / 'skills' / name), expected[name])
            skill = (ROOT / 'skills' / name / 'SKILL.md').read_text(encoding='utf-8')
            self.assertTrue(skill.startswith('---\nname: ' + name + '\n'))
            self.assertIn('\ndescription: ', skill)
        original = module.inventory
        try:
            module.inventory = lambda folder: {'unexpected.txt': 'changed'}
            with self.assertRaisesRegex(ValueError, 'checksum/inventory mismatch'):
                module.payload()
        finally:
            module.inventory = original


if __name__ == '__main__':
    unittest.main()
