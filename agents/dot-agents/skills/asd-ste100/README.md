# ASD-STE100 Assisted Review Skill

Rewrite technical English and review it against ASD-STE100 Issue 9. The skill accounts for all 53 writing rules, the official dictionary, and approved technical nouns and verbs.

**This is an assisted workflow, not an automatic compliance certificate.** The Python script checks supported patterns and local vocabulary. The skill and a qualified reviewer address meaning, grammatical function, document structure, terminology approval, and safety.

## Modes

| Mode | Use | Acceptance |
|---|---|---|
| STE review | Explicit STE rewrites and compliance reviews | All applicable rules, dictionary uses, and technical terminology need review. |
| Clarity | General simplification and agent-output rewrites | No STE compliance claim. Preserves necessary vocabulary, modality, and verb forms. |

Explicit STE requests select STE review in `SKILL.md`. The script defaults to clarity for ordinary lint use; select `--mode ste` for the assisted workflow.

## Install

Copy the complete `asd-ste100/` directory to your host's skill location. Keep `scripts/`, `references/`, and `examples/` together. The linter uses Python 3 and the standard library, including its sibling `scripts/ste_vocabulary.py`.

The skill includes [`references/issue9-dictionary.json`](references/issue9-dictionary.json), a factual vocabulary index with approvals, part-of-speech labels, printed forms, and source-entry references. Original definitions, help, and examples remain in the [official Issue 9 PDF](https://zenodo.org/records/23666006), linked from [ASD](https://www.asd-ste100.org/about_STE.html). Keep private terminology and restricted source-text exports local. Consult the standard's copyright notice and [official usage notice](https://www.asd-ste100.org/STE_downloads.html) before redistributing source text.

## Run

From the skill directory:

```bash
python3 scripts/ste-lint.py --mode ste --text-type procedure \
  --dictionary references/issue9-dictionary.json \
  --terminology /path/to/project-terms.json instructions.md

python3 scripts/ste-lint.py --mode ste --text-type description \
  --dictionary references/issue9-dictionary.json --json description.md
python3 scripts/ste-lint.py --mode clarity description.md
python3 scripts/ste-lint.py --list-rules --json
```

The second command uses the bundled dictionary but intentionally omits project terminology. Its report retains that approval gap. Omitting `--dictionary` also leaves vocabulary membership unchecked.

Use `--text-type procedure` for the 20-word limit and `--text-type description` for the 25-word limit. Lint mixed documents in separate sections; notes are descriptive text.

For vocabulary schemas, explicit inflections, canonical aliases, and counting units, read [`references/vocabulary-format.md`](references/vocabulary-format.md). Use the bundled index for surface checks and follow its `meaning_ref` values to review the actual dictionary entries. The script accepts JSON, not a PDF. A custom export can replace the bundled index, but loading it does not authenticate it or prove it is complete. Noun plurals require review of countability and source restrictions; the bundled index does not invent unprinted forms.

## Coverage

[`references/rule-coverage.json`](references/rule-coverage.json) is the 53-rule inventory. Each record identifies an official rule, related automatic checks, applicable text types, and remaining review criteria. `--list-rules` shows this inventory without reading stdin.

STE mode adds:

- Dictionary surface-form lookup and explicit inflections from local data.
- Approved technical nouns/verbs and noncanonical-alias detection.
- Contraction and descriptive-paragraph-length checks.
- Possible progressive constructions, alongside possible passive and perfect constructions.
- STE-oriented sentence counting: parentheses, explicit quoted text, hyphens, and configured names, labels, quantities, and other counting units.
- Official rule references on mapped findings, missing-source reporting, and a review-required result.

Selected phrasal verbs, nominalizations, sentence lengths, and semicolons are also checked. Grammar detection remains heuristic. Marketing adjectives, arbitrary synonym-group rotation, and the project-specific dangling-conjunction check belong to clarity mode, not formal STE coverage.

The dictionary lookup does **not** validate contextual meaning or part of speech. Technical terms do not become valid in every context merely by appearing in a glossary. Parenthetical text is checked separately, while also counting as one outer word. Unmarked names/titles/labels, unconfigured units, formulas, complex lists, noun-phrase structure, and grammatical ambiguity still need review. Inline and fenced code are excluded from prose checks; Markdown support is partial.

The JSON report retains `violations`, `count`, `hard_count`, `baseline`, `words`, and `per_100_words`, and adds `mode`, `status`, and `compliance`. STE reports include `coverage` with all 53 rules, vocabulary-source gaps, and applicable `review_required` criteria. `compliance` is always `not-verified`.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clarity checks within baseline, or a successful rule-list/self-test command. |
| 1 | Hard findings exceed baseline. |
| 2 | Invalid input or configuration. |
| 3 | STE scan found no hard findings; review remains required. |

STE review never returns an acceptance code. Correct hard findings, inspect heuristic advisories, then complete the remaining review against the official standard. Nonzero `--baseline` and `--disable` are rejected in STE mode. They remain available for selective clarity lint.

## Skill output

General rewrites return the revised text. An STE request with incomplete sources or review also gets a concise `Review required:` line. Request an analysis to get rule IDs, original wording, revisions, and remaining review.

The examples in [`examples/before-after.md`](examples/before-after.md) illustrate clarity and rule principles. They are not verified compliant documents. [`examples/linter-edge-cases.md`](examples/linter-edge-cases.md) intentionally contains invalid list endings for the clarity checker.

## Verify the implementation

```bash
python3 scripts/ste-lint.py --selftest
python3 -m unittest discover -s scripts -p 'test_ste_*.py'
```

The self-test covers existing clarity/Markdown behavior. The additional tests exercise local vocabulary and assisted-review behavior. Passing implementation tests does not certify a document or the checker.

## Sources

- [Official Issue 9 record and PDF](https://zenodo.org/records/23666006)
- [ASD: rules, dictionary, and terminology](https://www.asd-ste100.org/about_STE.html)
- [ASD: usage notice and human oversight](https://www.asd-ste100.org/STE_downloads.html)
- [Rule interpretation and source map](references/writing-rules.md)
