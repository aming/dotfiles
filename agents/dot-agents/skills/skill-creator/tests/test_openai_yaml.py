import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GENERATOR = ROOT / "skills" / "skill-creator" / "scripts" / "generate_openai_yaml.py"
TARGET_METADATA = ROOT / "skills" / "skill-creator" / "agents" / "openai.yaml"


def write_skill(skill_dir: Path, name: str = "metadata-skill") -> None:
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Create metadata fixtures.\n---\n\n# Metadata Skill\n"
    )


def field_value(content: str, field_name: str) -> str:
    prefix = f"  {field_name}: "
    for line in content.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip().strip('"')
    raise AssertionError(f"Missing field: {field_name}")


class OpenAIYamlTest(unittest.TestCase):
    def run_generator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GENERATOR), *args],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_generator_writes_required_interface_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "metadata-skill"
            skill_dir.mkdir()
            write_skill(skill_dir)

            result = self.run_generator(
                str(skill_dir),
                "--interface",
                "default_prompt=Use $metadata-skill to create a focused skill.",
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            content = (skill_dir / "agents" / "openai.yaml").read_text()
            self.assertIn("interface:", content)
            self.assertEqual(field_value(content, "display_name"), "Metadata Skill")
            short_description = field_value(content, "short_description")
            self.assertGreaterEqual(len(short_description), 25)
            self.assertLessEqual(len(short_description), 64)
            self.assertEqual(
                field_value(content, "default_prompt"),
                "Use $metadata-skill to create a focused skill.",
            )

    def test_generator_rejects_unknown_interface_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "metadata-skill"
            skill_dir.mkdir()
            write_skill(skill_dir)

            result = self.run_generator(
                str(skill_dir),
                "--interface",
                "unsupported=value",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unknown interface field", result.stdout + result.stderr)

    def test_target_skill_has_openai_metadata(self) -> None:
        self.assertTrue(TARGET_METADATA.exists())
        content = TARGET_METADATA.read_text()
        self.assertIn("interface:", content)
        self.assertEqual(field_value(content, "display_name"), "Skill Creator")
        short_description = field_value(content, "short_description")
        self.assertGreaterEqual(len(short_description), 25)
        self.assertLessEqual(len(short_description), 64)
        self.assertIn("$skill-creator", field_value(content, "default_prompt"))


if __name__ == "__main__":
    unittest.main()
