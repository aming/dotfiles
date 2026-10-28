import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SKILL_ROOT = Path(__file__).resolve().parents[1]

class TestScripts(unittest.TestCase):
    def run_script(self, name, *args, output=None, stdin="", cwd=None):
        env = os.environ.copy()
        env.pop("TOOL_OUTPUT", None)
        env.pop("CLAUDE_TOOL_OUTPUT", None)
        if output is not None:
            env["TOOL_OUTPUT"] = output
        return subprocess.run(["bash", str(SKILL_ROOT / "scripts" / name), *args],
                              input=stdin, env=env, cwd=cwd, capture_output=True, text=True)

    def test_detector_reads_documented_env_and_stdin(self):
        for kwargs in ({"output": "fatal: failure"}, {"stdin": "error: failure"}):
            with self.subTest(kwargs=kwargs):
                result = self.run_script("error-detector.sh", **kwargs)
                self.assertEqual(result.returncode, 0)
                self.assertIn("<error-detected>", result.stdout)
                self.assertIn("AGENTS.md", result.stdout)
        self.assertEqual(self.run_script("error-detector.sh", output="success").stdout, "")

    def test_extraction_is_cwd_independent_and_reuses_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            dry = self.run_script("extract-skill.sh", "qa-storage-path", "--dry-run", cwd=tmp)
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertIn(str(SKILL_ROOT.parent / "qa-storage-path"), dry.stdout)
            self.assertFalse((Path(tmp) / "skills").exists())
            actual = self.run_script("extract-skill.sh", "qa-storage-path", "--output-dir", tmp)
            self.assertEqual(actual.returncode, 0, actual.stderr)
            generated = (Path(tmp) / "qa-storage-path" / "SKILL.md").read_text()
            template = (SKILL_ROOT / "assets" / "SKILL.template.md").read_text().split("```markdown\n", 1)[1].split("\n```", 1)[0]
            self.assertEqual(generated, template.replace("skill-name-here", "qa-storage-path") + "\n")
            retry = self.run_script("extract-skill.sh", "qa-storage-path", "--output-dir", tmp)
            self.assertNotEqual(retry.returncode, 0)
