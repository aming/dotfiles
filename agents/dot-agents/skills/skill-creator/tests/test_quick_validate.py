import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "skills" / "skill-creator" / "scripts" / "quick_validate.py"


def write_skill(skill_dir: Path, frontmatter: str, body: str | None = None) -> None:
    content = f"---\n{frontmatter}---\n\n{body or '# Test Skill\\n'}"
    (skill_dir / "SKILL.md").write_text(content)


class QuickValidateTest(unittest.TestCase):
    def run_validator(self, skill_dir: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(skill_dir)],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_valid_skill_with_compatibility_without_pyyaml_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "metadata-skill"
            skill_dir.mkdir()
            write_skill(
                skill_dir,
                "name: metadata-skill\n"
                "description: Create metadata fixtures.\n"
                "compatibility: Requires Python 3.11.\n",
            )

            result = self.run_validator(skill_dir)

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("Skill is valid!", result.stdout)

    def test_unknown_frontmatter_key_fails_with_actionable_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "bad-skill"
            skill_dir.mkdir()
            write_skill(
                skill_dir,
                "name: bad-skill\n"
                "description: Bad fixture.\n"
                "foo: bar\n",
            )

            result = self.run_validator(skill_dir)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unexpected key(s)", result.stdout)
            self.assertIn("foo", result.stdout)

    def test_multiline_description_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "multiline-skill"
            skill_dir.mkdir()
            write_skill(
                skill_dir,
                "name: multiline-skill\n"
                "description: |\n"
                "  Create and update skills.\n"
                "  Use when skill metadata is involved.\n",
            )

            result = self.run_validator(skill_dir)

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
