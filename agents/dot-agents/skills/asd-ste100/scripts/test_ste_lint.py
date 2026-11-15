"""Behavioral coverage for assisted STE lint, not a standard-conformance suite."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from ste_vocabulary import Vocabulary

SCRIPT = Path(__file__).with_name("ste-lint.py")
SPEC = importlib.util.spec_from_file_location("ste_lint", SCRIPT)
LINTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINTER)


class AssistedSteTests(unittest.TestCase):
    def cli(self, text, *flags):
        return subprocess.run([sys.executable, str(SCRIPT), *flags], input=text,
                              text=True, capture_output=True, check=False)

    def findings(self, text, **kwargs):
        return LINTER.lint(text, mode="ste", **kwargs)[0]

    def test_clean_scan_requires_review_and_reports_missing_sources(self):
        result = self.cli("Open the file.", "--mode", "ste", "--json")
        self.assertEqual(result.returncode, 3, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "review-required")
        self.assertEqual(report["compliance"], "not-verified")
        self.assertEqual(report["coverage"]["dictionary"], "missing")
        self.assertEqual(report["coverage"]["terminology"], "missing")
        self.assertTrue(report["coverage"]["gaps"])
        criteria = {rule["id"]: rule["review"] for rule in report["review_required"]}
        self.assertIn("1.3", criteria)  # Approved meanings remain unverified.
        self.assertIn("7.3", criteria)  # A clean scan cannot establish safety content.

    def test_hard_findings_point_to_official_rules(self):
        result = self.cli("Don't open the file; close it.", "--mode", "ste", "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        mapped = {finding["rule"]: finding["ste_rules"] for finding in report["violations"]}
        self.assertEqual(mapped["contraction"], ["4.2"])
        self.assertEqual(mapped["semicolon"], ["8.1"])

    def test_all_official_rules_are_exposed_for_review(self):
        result = self.cli("", "--list-rules", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        rules = json.loads(result.stdout)["rules"]
        expected = {f"{section}.{rule}"
                    for section, size in enumerate((14, 2, 7, 5, 5, 6, 3, 7, 4), 1)
                    for rule in range(1, size + 1)}
        self.assertEqual({rule["id"] for rule in rules}, expected)
        self.assertEqual(len(rules), len(expected))
        self.assertTrue(all(rule["review"].strip() for rule in rules))

    def test_ste_cannot_hide_findings_with_baselines_or_disabled_rules(self):
        for flags in (("--baseline", "2"), ("--disable", "semicolon")):
            with self.subTest(flags=flags):
                result = self.cli("Open the file; close it.", "--mode", "ste", *flags)
                self.assertEqual(result.returncode, 2)
                self.assertIn("does not permit", result.stderr)

    def test_modal_perfect_is_flagged_without_removing_uncertainty(self):
        text = "The request may\nhave failed."
        findings = self.findings(text)
        self.assertTrue(any(f["rule"] == "present-perfect" for f in findings))
        self.assertFalse(any(f["rule"] == "present-perfect" for f in LINTER.lint(text)[0]))

    def test_progressive_construction_across_a_soft_wrap_is_advisory(self):
        findings = self.findings("The door is\nopening.")
        progressive = [f for f in findings if f["rule"] == "ing-form"]
        self.assertEqual([(f["line"], f["col"], f["level"]) for f in progressive],
                         [(1, 10, "advisory")])

    def test_paragraph_limit_respects_blank_lines_and_text_type(self):
        sentences = ["The valve is open."] * 7
        findings = self.findings(" ".join(sentences))
        self.assertTrue(any(f["rule"] == "paragraph-length" for f in findings))
        self.assertFalse(any(f["rule"] == "paragraph-length"
                             for f in self.findings("\n\n".join(sentences))))
        self.assertFalse(any(f["rule"] == "paragraph-length"
                             for f in self.findings(" ".join(sentences), text_type="procedure")))

    def test_parenthetical_text_is_counted_separately_at_its_source_position(self):
        text = "Open the cover (" + " ".join(["word"] * 26) + ")."
        long = [f for f in self.findings(text) if f["rule"] == "long-sentence"]
        self.assertEqual([(f["line"], f["col"], f["match"]) for f in long], [(1, 17, "26 words")])
        counts = list(LINTER._ste_sentence_counts(
            "Make sure that the EMER pushbutton switch is released (the EMER legend is off)."))
        self.assertEqual([count for _, _, count in counts], [10, 5])

    def test_quoted_label_is_one_word_and_does_not_split_the_sentence(self):
        text = 'Touch the "Service. Overview" arrow to select the function page.'
        self.assertEqual([count for _, _, count in LINTER._ste_sentence_counts(text)], [9])
        text = " ".join(["word"] * 18) + ' "Service Overview" switch.'
        self.assertFalse(any(f["rule"] == "long-sentence"
                             for f in self.findings(text, text_type="procedure")))

    def test_identifier_parentheticals_do_not_add_sentences(self):
        text = ("The cover (1), valve (2), seal (3), plug (4), pin (5), "
                "and latch (6) are clean.")
        self.assertEqual(
            [count for _, _, count in LINTER._ste_sentence_counts(text)], [16])
        self.assertFalse(any(f["rule"] == "paragraph-length"
                             for f in self.findings(text)))

    def test_markdown_link_destination_is_not_a_parenthetical(self):
        text = "word " * 19 + "[word](url)."
        findings, words = LINTER.lint(text, mode="ste", text_type="procedure")
        self.assertEqual(words, 20)
        self.assertFalse(any(f["rule"] == "long-sentence" for f in findings))

    def test_reference_definition_is_not_prose(self):
        text = "See [word][ref] now.\n\n[ref]: https://example.com/page\n"
        with tempfile.TemporaryDirectory() as temporary:
            dictionary = Path(temporary) / "dictionary.json"
            dictionary.write_text(json.dumps({
                "issue": 9, "source": "Unit-test vocabulary", "entries": [
                    {"word": word, "pos": pos, "approved": True, "meaning": "Test"}
                    for word, pos in (("see", "v"), ("word", "n"),
                                      ("ref", "n"), ("now", "adv"))]}),
                encoding="utf-8")
            vocabulary = Vocabulary(dictionary_path=dictionary)
            findings = self.findings(text, vocabulary=vocabulary)
            self.assertEqual([finding for finding in findings
                              if finding["line"] == 3], [])

    def test_single_quoted_label_with_possessive_is_one_word(self):
        for label in ("‘Pilot’s Menu’", "'Pilot's Menu'"):
            with self.subTest(label=label):
                text = "word " * 18 + label + " switch."
                self.assertFalse(any(f["rule"] == "long-sentence"
                                     for f in self.findings(text, text_type="procedure")))

    def test_code_only_line_keeps_vocabulary_boundary(self):
        with tempfile.TemporaryDirectory() as temporary:
            dictionary = Path(temporary) / "dictionary.json"
            dictionary.write_text(json.dumps(
                {"issue": 9, "source": "Unit-test vocabulary", "entries": [
                    {"word": "in progress", "pos": "adv", "approved": True,
                     "meaning": "Ongoing"},
                    {"word": "progress", "pos": "n", "approved": False}]}),
                encoding="utf-8")
            vocabulary = Vocabulary(dictionary_path=dictionary)
            findings = self.findings("In\n`x`\nprogress.", vocabulary=vocabulary)
            self.assertIn("progress", [finding["match"] for finding in findings])

    def test_project_preferences_are_not_presented_as_official_violations(self):
        text = "Check the system. Verify the connections. A robust tool.\n\n- One and"
        self.assertFalse(any(f["rule"] in {"marketing-adjective", "synonym-rotation", "dangling-conjunction"}
                             for f in self.findings(text)))
        self.assertTrue(any(f["rule"] == "synonym-rotation" for f in LINTER.lint(text)[0]))

    def test_local_vocabulary_is_used_but_never_yields_automatic_acceptance(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dictionary = root / "dictionary.json"
            dictionary.write_text(json.dumps({"issue": 9, "source": "Unit-test vocabulary, not official data",
                "entries": [{"word": word, "pos": pos, "approved": True, "meaning": meaning}
                            for word, pos, meaning in (("open", "v", "Change to an open condition"),
                                                       ("the", "art", "Identifies a noun"))]}), encoding="utf-8")
            terminology = root / "terms.json"
            terminology.write_text(json.dumps({"issue": 9, "source": "Unit-test project glossary",
                "entries": [{"term": "cache shard", "pos": "n", "definition": "A cache partition",
                             "category": 19}]}), encoding="utf-8")
            flags = ("--mode", "ste", "--json", "--dictionary", str(dictionary),
                     "--terminology", str(terminology))
            result = self.cli("Open the cache\nshard.", *flags)
            self.assertEqual(result.returncode, 3, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["hard_count"], 0)
            self.assertEqual(report["coverage"]["dictionary"], "supplied")
            self.assertEqual(report["compliance"], "not-verified")
            result = self.cli("Open the mystery.", *flags)
            self.assertEqual(result.returncode, 1, result.stderr)
            unknown = [f for f in json.loads(result.stdout)["violations"] if f["rule"] == "dictionary-word"]
            self.assertEqual([(f["match"], f["line"], f["col"]) for f in unknown], [("mystery", 1, 10)])

    def test_approved_quantity_is_one_counted_word_but_ordinary_terms_are_not(self):
        with tempfile.TemporaryDirectory() as temporary:
            terms = Path(temporary) / "terms.json"
            terms.write_text(json.dumps({"issue": 9, "source": "Unit-test project glossary", "entries": [
                {"term": "degrees Celsius", "pos": "n", "category": 9,
                 "definition": "A temperature unit", "count_as_one": True},
                {"term": "cache shard", "pos": "n", "category": 19,
                 "definition": "A cache partition"}]}), encoding="utf-8")
            vocabulary = Vocabulary(terminology_path=terms)
            self.assertEqual(LINTER._ste_count_words("The temperature is 10 degrees Celsius.", vocabulary), 4)
            self.assertEqual(LINTER._ste_count_words("Open the cache shard.", vocabulary), 4)

    def test_code_and_markdown_are_not_unknown_prose(self):
        with tempfile.TemporaryDirectory() as temporary:
            dictionary = Path(temporary) / "dictionary.json"
            dictionary.write_text(json.dumps({"issue": 9, "source": "Unit-test vocabulary", "entries": [
                {"word": "open", "pos": "v", "approved": True, "meaning": "Open condition"},
                {"word": "the", "pos": "art", "approved": True, "meaning": "Identifies a noun"},
                {"word": "file", "pos": "n", "approved": True, "meaning": "A stored document"}]}), encoding="utf-8")
            vocabulary = Vocabulary(dictionary_path=dictionary)
            text = "- Open the `odd_identifier` file.\n\n```python\nunknown();\n```"
            self.assertFalse(any(f["rule"] == "dictionary-word"
                                 for f in self.findings(text, vocabulary=vocabulary)))

    def test_bundled_dictionary_works_from_the_documented_skill_directory(self):
        result = subprocess.run(
            [sys.executable, "scripts/ste-lint.py", "--mode", "ste", "--dictionary",
             "references/issue9-dictionary.json", "--json"],
            cwd=SCRIPT.parent.parent, input="Make sure that it is safe.", text=True,
            capture_output=True, check=False)
        self.assertEqual(result.returncode, 3, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["hard_count"], 0)
        self.assertEqual(report["coverage"]["dictionary"], "supplied")
        self.assertEqual(report["coverage"]["terminology"], "missing")
        vocabulary = Vocabulary(dictionary_path=SCRIPT.parent.parent / "references" / "issue9-dictionary.json")
        self.assertEqual(vocabulary.scan("give gives gave given"), [])
        rejected = vocabulary.scan("Utilize it.")
        self.assertEqual([finding["match"] for finding in rejected], ["Utilize"])

    def test_bad_vocabulary_and_bad_document_encoding_are_usage_errors(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bad = root / "bad.json"
            bad.write_text("{", encoding="utf-8")
            result = self.cli("Open the file.", "--mode", "ste", "--dictionary", str(bad))
            self.assertEqual(result.returncode, 2)
            self.assertIn(str(bad), result.stderr)
            document = root / "bad.md"
            document.write_bytes(b"\xff")
            result = self.cli("", "--mode", "ste", str(document))
            self.assertEqual(result.returncode, 2)
            self.assertIn(str(document), result.stderr)


if __name__ == "__main__":
    unittest.main()
