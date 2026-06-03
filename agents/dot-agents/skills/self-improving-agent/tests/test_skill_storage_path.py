from pathlib import Path
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
LEGACY_AGENT_LEARNINGS = "." + "agent/learnings"
LEGACY_DOT_LEARNINGS_FILE = "." + "learnings/LEARNINGS.md"


class TestSkillStoragePath(unittest.TestCase):
    def test_skill_uses_agents_learning_path_when_describing_storage(self) -> None:
        # Given: the core skill instructions are the source of truth for storage.
        content = SKILL_MD.read_text(encoding="utf-8")

        # When: the storage contract is inspected.
        legacy_paths = (
            LEGACY_AGENT_LEARNINGS,
            f"<project-root>/{LEGACY_AGENT_LEARNINGS}/",
            LEGACY_DOT_LEARNINGS_FILE,
        )
        expected_paths = (
            "<project-root>/.agents/learnings/",
            "mkdir -p .agents/learnings",
            ".agents/learnings/LEARNINGS.md",
            ".agents/learnings/ERRORS.md",
            ".agents/learnings/FEATURE_REQUESTS.md",
            'grep -n "keyword" .agents/learnings/*.md',
            'grep -n "Pattern-Key: <pattern_key>" .agents/learnings/LEARNINGS.md',
            ".agents/learnings/",
        )

        # Then: only the new canonical path appears in read/write examples.
        for legacy_path in legacy_paths:
            with self.subTest(legacy_path=legacy_path):
                self.assertNotIn(
                    legacy_path,
                    content,
                    f"legacy storage path should be absent: {legacy_path}",
                )

        for expected_path in expected_paths:
            with self.subTest(expected_path=expected_path):
                self.assertIn(
                    expected_path,
                    content,
                    f"canonical storage path should be present: {expected_path}",
                )


if __name__ == "__main__":
    unittest.main()
