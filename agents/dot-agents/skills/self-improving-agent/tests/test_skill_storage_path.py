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
            "<repo-root>/.agents/learnings/",
            'mkdir -p "$ROOT/.agents/learnings"',
            "$ROOT/.agents/learnings/LEARNINGS.md",
            "$ROOT/.agents/learnings/ERRORS.md",
            "$ROOT/.agents/learnings/FEATURE_REQUESTS.md",
            'grep -n "keyword" "$ROOT/.agents/learnings/"*.md',
            'grep -n "Pattern-Key: <pattern_key>" "$ROOT/.agents/learnings/LEARNINGS.md"',
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

    def test_skill_anchors_storage_to_git_repository_root(self) -> None:
        # Given: agents may run with a nested cwd (a stack, a subproject).
        content = SKILL_MD.read_text(encoding="utf-8")

        # Then: the skill resolves the git root and forbids nested or symlinked copies.
        for expected_rule in (
            "git rev-parse --show-toplevel",
            "never to the current working directory",
            "Never add a symlink and never keep two copies",
        ):
            with self.subTest(expected_rule=expected_rule):
                self.assertIn(
                    expected_rule,
                    content,
                    f"repository-root rule should be present: {expected_rule}",
                )


if __name__ == "__main__":
    unittest.main()
