import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SEARCH=ROOT/'skills/ui-ux-pro-max/scripts/search.py'


class AdditionTests(unittest.TestCase):
    def setUp(self):
        self.work=Path(tempfile.mkdtemp(prefix='toolkit-additions-test-')).resolve()

    def run_search(self,*args):
        result=subprocess.run([sys.executable,'-B',str(SEARCH),*args,'--json'],cwd=self.work,capture_output=True,encoding='utf-8',timeout=20)
        self.assertEqual(result.returncode,0,result.stderr)
        return json.loads(result.stdout)

    def test_domain_and_stack_search_without_persistence(self):
        result=self.run_search('keyboard focus modal','--domain','ux')
        self.assertGreater(result['count'],0)
        result=self.run_search('streaming suspense','--stack','nextjs')
        self.assertGreater(result['count'],0)
        self.assertEqual(list(self.work.iterdir()),[])

    def test_design_system_and_explicit_persistence_never_overwrite_by_default(self):
        result=self.run_search('community library accessible calm','--design-system','-p','Synthetic Library')
        self.assertIsNone(result['persistence'])
        self.assertEqual(list(self.work.iterdir()),[])
        result=self.run_search('community library accessible calm','--design-system','-p','Synthetic Library','--persist','--output-dir',str(self.work))
        master=Path(result['persistence']['master_file'])
        self.assertTrue(master.resolve().is_relative_to(self.work))
        master.write_text('Keep this edited synthetic design decision',encoding='utf-8')
        second=self.run_search('different synthetic query','--design-system','-p','Synthetic Library','--persist','--output-dir',str(self.work))
        self.assertEqual(second['persistence']['status'],'skipped_exists')
        self.assertEqual(master.read_text(), 'Keep this edited synthetic design decision')

    def test_add_missing_keeps_existing_unchanged(self):
        destination=self.work/'skills'
        first=destination/'spec-driven-development'
        import shutil
        shutil.copytree(ROOT/'skills/spec-driven-development',first)
        before=hashlib.sha256((first/'SKILL.md').read_bytes()).hexdigest()
        result=subprocess.run([sys.executable,str(ROOT/'install.py'),'install','--add-missing','--destination',str(destination)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(before,hashlib.sha256((first/'SKILL.md').read_bytes()).hexdigest())
        self.assertEqual(len(list(destination.iterdir())),10)

    def test_add_missing_modified_collision_copies_nothing(self):
        destination=self.work/'skills'
        first=destination/'spec-driven-development'
        first.mkdir(parents=True)
        (first/'SKILL.md').write_text('user edits')
        result=subprocess.run([sys.executable,str(ROOT/'install.py'),'install','--add-missing','--destination',str(destination)],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(list(destination.iterdir()),[first])


if __name__=='__main__':unittest.main()
