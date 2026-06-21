import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILL_MD = ROOT / "skills" / "skill-creator" / "SKILL.md"


class SkillMarkdownStructureTest(unittest.TestCase):
    def test_skill_md_has_path_map_gotchas_and_reference_triggers(self) -> None:
        content = SKILL_MD.read_text()
        checks = [
            "create a new skill",
            "update an existing skill",
            "evaluate skill outputs",
            "optimize trigger description",
            "## Gotchas",
            "references/schemas.md",
            "references/script-resources.md",
            "references/openai_yaml.md",
        ]
        missing = [check for check in checks if check not in content]

        self.assertEqual(missing, [])
        self.assertLessEqual(len(content.splitlines()), 500)


if __name__ == "__main__":
    unittest.main()
