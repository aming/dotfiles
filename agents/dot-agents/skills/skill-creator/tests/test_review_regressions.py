import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))
from aggregate_benchmark import generate_benchmark, generate_markdown
from quick_validate import validate_skill

spec = importlib.util.spec_from_file_location('review_generator', SKILL / 'eval-viewer/generate_review.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class ReviewRegressionTests(unittest.TestCase):
    def test_missing_measurements_stay_missing_and_real_tokens_are_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for config in ('old_skill', 'with_skill'):
                run = root / 'eval-0-improvement' / config / 'run-1'
                run.mkdir(parents=True)
                (run / 'grading.json').write_text(json.dumps({
                    'summary': {'pass_rate': 1 if config == 'with_skill' else 0},
                    'execution_metrics': {'output_chars': 5000},
                    'timing': {'total_duration_seconds': 4} if config == 'with_skill' else {},
                }))
                if config == 'with_skill':
                    (run / 'timing.json').write_text(json.dumps({'total_tokens': 123}))
            result = generate_benchmark(root)
            old, new = result['runs']
            self.assertIsNone(old['result']['tokens'])
            self.assertIsNone(old['result']['time_seconds'])
            self.assertEqual(new['result']['tokens'], 123)
            self.assertEqual(new['result']['time_seconds'], 4)
            self.assertEqual(result['run_summary']['delta']['pass_rate'], '+1.00')
            self.assertIsNone(result['run_summary']['delta']['time_seconds'])
            self.assertIsNone(result['metadata']['executor_model'])
            self.assertIn('—', generate_markdown(result))

    def test_metadata_ancestor_and_nested_outputs_are_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case = root / 'eval-3-test'
            outputs = case / 'with_skill/run-1/outputs/draft-skill/agents'
            outputs.mkdir(parents=True)
            (case / 'eval_metadata.json').write_text(json.dumps({'eval_id': 3, 'prompt': 'Review this draft'}))
            (outputs / 'grader.md').write_text('Nested artifact')
            run, = review.find_runs(root)
            self.assertEqual(run['prompt'], 'Review this draft')
            self.assertEqual(run['eval_id'], 3)
            self.assertEqual(run['outputs'][0]['name'], 'draft-skill/agents/grader.md')

    def test_invalid_or_empty_scalars_and_name_mismatch_fail(self):
        cases = [
            'name: ""\ndescription: valid',
            'name: draft\ndescription: ""',
            'name: draft\ndescription: "unterminated',
            "name: draft\ndescription: 'unterminated",
            'name: draft\ndescription: bad: scalar',
            'name: draft\ndescription: # comment only',
            'name: draft\ndescription: - invalid scalar',
            'name: mismatch\ndescription: valid',
        ]
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'draft'
            folder.mkdir()
            for frontmatter in cases:
                with self.subTest(frontmatter=frontmatter):
                    (folder / 'SKILL.md').write_text(f'---\n{frontmatter}\n---\n')
                    self.assertFalse(validate_skill(folder)[0])
            description = json.dumps('escaped "quote"')
            (folder / 'SKILL.md').write_text(f'---\nname: draft\ndescription: {description}\n---\n')
            self.assertTrue(validate_skill(folder)[0])

    def test_eval_inputs_exist_and_no_machine_paths_remain(self):
        path = SKILL / 'evals/evals.json'
        data = json.loads(path.read_text())
        self.assertNotIn('/Users/', path.read_text())
        self.assertNotIn('<CONFIG>', path.read_text())
        for case in data['evals']:
            for file in case['files']:
                self.assertTrue((SKILL / file).exists(), file)
