from pathlib import Path
import unittest

SKILL_MD = Path(__file__).resolve().parents[1] / "SKILL.md"

class TestSkillStoragePath(unittest.TestCase):
    def test_local_rules_override_default_and_choose_existing_sink(self):
        content = SKILL_MD.read_text()
        self.assertIn("Repository-local instructions", content)
        self.assertIn("agents/AGENTS.md", content)
        self.assertIn("LEARNING_REL=agents/learnings", content)
        self.assertIn('LEARNINGS_DIR="$ROOT/$LEARNING_REL"', content)
        self.assertIn("chosen absolute", content)

    def test_no_cwd_fallback_or_automatic_log_deletion(self):
        content = SKILL_MD.read_text()
        self.assertIn("git rev-parse --show-toplevel", content)
        self.assertNotIn("|| pwd", content)
        self.assertIn("require an explicitly identified project root", content)
        self.assertIn("Do not merge, delete, or relocate", content)
