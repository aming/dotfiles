import os
from pathlib import Path
import subprocess
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = SKILL_ROOT.parents[1]
SCRIPT_ROOT = SKILL_ROOT / "scripts"
LEGACY_AGENT_LEARNINGS = "." + "agent/learnings"
LEGACY_DOT_LEARNINGS_FILE = "." + "learnings/LEARNINGS.md"


def run_bash_script(
    script_name: str,
    *args: str,
    env_updates: dict[str, str] | None = None,
) -> str:
    env = os.environ.copy()
    if env_updates:
        env.update(env_updates)

    result = subprocess.run(
        ("bash", str(SCRIPT_ROOT / script_name), *args),
        cwd=WORKSPACE_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


class TestScriptStoragePath(unittest.TestCase):
    def test_activator_uses_agents_learning_path_when_hook_runs(self) -> None:
        output = run_bash_script("activator.sh")

        self.assertIn("Log to .agents/learnings/", output)
        self.assertNotIn(LEGACY_AGENT_LEARNINGS, output)

    def test_error_detector_uses_agents_learning_path_when_failure_seen(self) -> None:
        output = run_bash_script(
            "error-detector.sh",
            env_updates={"CLAUDE_TOOL_OUTPUT": "fatal: test failure"},
        )

        self.assertIn(".agents/learnings/ERRORS.md", output)
        self.assertNotIn(LEGACY_AGENT_LEARNINGS, output)

    def test_extractor_uses_agents_learning_path_when_dry_run_scaffolds(self) -> None:
        output = run_bash_script("extract-skill.sh", "qa-storage-path", "--dry-run")

        self.assertIn("Original File: .agents/learnings/LEARNINGS.md", output)
        self.assertNotIn(LEGACY_DOT_LEARNINGS_FILE, output)


if __name__ == "__main__":
    unittest.main()
