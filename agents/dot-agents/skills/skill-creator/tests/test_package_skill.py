import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKAGER = ROOT / "skills" / "skill-creator" / "scripts" / "package_skill.py"
SKILL_DIR = ROOT / "skills" / "skill-creator"


class PackageSkillTest(unittest.TestCase):
    def test_package_includes_metadata_and_excludes_development_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(PACKAGER), str(SKILL_DIR), tmp],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            package_path = Path(tmp) / "skill-creator.skill"
            self.assertTrue(package_path.exists())
            with zipfile.ZipFile(package_path) as archive:
                names = archive.namelist()

            self.assertIn("skill-creator/agents/openai.yaml", names)
            self.assertFalse(any(name.startswith("skill-creator/evals/") for name in names))
            self.assertFalse(any(name.startswith("skill-creator/tests/") for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertFalse(any(name.endswith(".pyc") for name in names))


if __name__ == "__main__":
    unittest.main()
