from pathlib import Path
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
RESOURCE_FILES = (
    SKILL_ROOT / "references" / "hooks-setup.md",
    SKILL_ROOT / "references" / "examples.md",
    SKILL_ROOT / "assets" / "LEARNINGS.template.md",
    SKILL_ROOT / "assets" / "ERRORS.template.md",
    SKILL_ROOT / "assets" / "FEATURE_REQUESTS.template.md",
)
LEGACY_AGENT_LEARNINGS = "." + "agent/learnings"
LEGACY_DOT_LEARNINGS_FILE = "." + "learnings/LEARNINGS.md"


class TestResourceStoragePath(unittest.TestCase):
    def test_resources_use_agents_learning_path_when_loaded(self) -> None:
        legacy_paths = (
            LEGACY_AGENT_LEARNINGS,
            LEGACY_DOT_LEARNINGS_FILE,
        )

        for resource_file in RESOURCE_FILES:
            content = resource_file.read_text(encoding="utf-8")

            with self.subTest(resource_file=resource_file.name):
                self.assertIn(
                    ".agents/learnings",
                    content,
                    f"resource should mention canonical path: {resource_file}",
                )

            for legacy_path in legacy_paths:
                with self.subTest(
                    resource_file=resource_file.name,
                    legacy_path=legacy_path,
                ):
                    self.assertNotIn(
                        legacy_path,
                        content,
                        f"resource should not mention legacy path: {resource_file}",
                    )


if __name__ == "__main__":
    unittest.main()
