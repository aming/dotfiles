import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REFERENCE = ROOT / "skills" / "skill-creator" / "references" / "openai_yaml.md"
SCRIPT_RESOURCES = ROOT / "skills" / "skill-creator" / "references" / "script-resources.md"


class OpenAIYamlReferenceTest(unittest.TestCase):
    def test_openai_yaml_reference_documents_required_fields(self) -> None:
        self.assertTrue(REFERENCE.exists())
        content = REFERENCE.read_text()
        required = [
            "agents/openai.yaml",
            "display_name",
            "short_description",
            "default_prompt",
            "$skill-name",
            "helper-role markdown",
        ]
        missing = [item for item in required if item not in content]

        self.assertEqual(missing, [])

    def test_script_resources_lists_runtime_categories(self) -> None:
        content = SCRIPT_RESOURCES.read_text()
        required = [
            "Dependency-light scripts",
            "Model-dependent scripts",
            "quick_validate.py",
            "generate_openai_yaml.py",
            "init_skill.py",
            "run_eval.py",
            "run_loop.py",
            "improve_description.py",
        ]
        missing = [item for item in required if item not in content]

        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
