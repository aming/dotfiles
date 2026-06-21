import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVALS_JSON = ROOT / "skills" / "skill-creator" / "evals" / "evals.json"


class EvalsJsonTest(unittest.TestCase):
    def test_eval_ids_are_unique_and_existing_cases_are_preserved(self) -> None:
        data = json.loads(EVALS_JSON.read_text())
        evals = data["evals"]
        ids = [item["id"] for item in evals]

        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(evals[0]["id"], 0)
        self.assertIn("outdated-skill", evals[0]["prompt"])
        self.assertEqual(evals[1]["id"], 1)
        self.assertIn("notes-cleanup", evals[1]["prompt"])

    def test_openai_derived_eval_cases_are_present(self) -> None:
        data = json.loads(EVALS_JSON.read_text())
        prompts = "\n".join(item["prompt"] for item in data["evals"])
        required = [
            "agents/openai.yaml",
            "init_skill.py",
            "PyYAML",
            "agents/grader.md",
        ]
        missing = [item for item in required if item not in prompts]

        self.assertEqual(missing, [])

    def test_evals_use_expectations_not_assertions(self) -> None:
        data = json.loads(EVALS_JSON.read_text())
        raw = EVALS_JSON.read_text()
        self.assertNotIn('"assertions"', raw)
        self.assertNotIn("assertion_results", raw)
        for item in data["evals"]:
            self.assertIn("prompt", item)
            self.assertIn("expected_output", item)
            self.assertIn("files", item)
            self.assertIn("expectations", item)
            self.assertNotEqual(item["expectations"], [])


if __name__ == "__main__":
    unittest.main()
