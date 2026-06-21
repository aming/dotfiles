import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INITIALIZER = ROOT / "skills" / "skill-creator" / "scripts" / "init_skill.py"


class InitSkillTest(unittest.TestCase):
    def run_initializer(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INITIALIZER), *args],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_initializes_normalized_skill_with_metadata_and_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_initializer(
                "Metadata Skill",
                "--path",
                tmp,
                "--resources",
                "scripts,references",
                "--interface",
                "default_prompt=Use $metadata-skill to create a focused skill.",
            )

            skill_dir = Path(tmp) / "metadata-skill"
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue((skill_dir / "SKILL.md").exists())
            self.assertTrue((skill_dir / "agents" / "openai.yaml").exists())
            self.assertTrue((skill_dir / "scripts").is_dir())
            self.assertTrue((skill_dir / "references").is_dir())
            self.assertFalse((skill_dir / "assets").exists())
            self.assertIn("Normalized skill name", result.stdout)

    def test_refuses_existing_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "metadata-skill"
            skill_dir.mkdir()

            result = self.run_initializer("metadata-skill", "--path", tmp)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stdout)

    def test_examples_require_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_initializer("metadata-skill", "--path", tmp, "--examples")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--examples requires --resources", result.stdout)


if __name__ == "__main__":
    unittest.main()
