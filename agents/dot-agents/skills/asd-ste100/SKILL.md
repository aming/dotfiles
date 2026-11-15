---
name: asd-ste100
description: "Rewrite or review English using ASD-STE100 Simplified Technical English. Use for explicit STE100, STE-100, ASD-STE100, or STE compliance requests, and to clarify technical instructions, tool descriptions, error messages, and agent output. For STE requests, review all 53 Issue 9 rules, the official dictionary, and approved project terminology. Preserve meaning, uncertainty, and requirement strength. Use clarity mode for general simplification. Do not apply to creative or marketing copy unless requested."
compatibility: Python 3 for the optional stdlib-only linter; authoritative Issue 9 and approved project terminology for a complete assisted review.
---

# Simplified Technical English

## Choose the contract

**STE review**: Use when the user requests ASD-STE100, STE compliance, or a rewrite in STE. Apply the actual Issue 9 rules and vocabulary. The script supplies partial checks, not a compliance certificate. Meaning, grammatical function, terminology qualifications, and safety need review.

**Clarity**: Use for general simplification without an explicit STE requirement. Prefer short, clear sentences, active voice, direct verbs, and consistent terminology. Preserve necessary vocabulary and verb forms. Describe the result as a clarity rewrite, not verified STE.

An aircraft procedure and an agent instruction can have different subject matter. Both still need the correct STE rules when the user requests STE. Do not invent an exception because the text concerns software.

## Authoritative sources

Issue 9, January 2025, has 53 writing rules in nine sections and a controlled dictionary. Technical nouns and technical verbs extend the dictionary only under the standard's terminology rules.

For every STE task, read `references/rule-coverage.json`. It accounts for each official rule ID, the script's related checks, and the judgment still required. When interpreting a rule or a dictionary entry, consult the actual [official Issue 9 PDF](https://zenodo.org/records/23666006/files/ASD-STE100_ISSUE9.pdf?download=1), linked from the [ASD website](https://www.asd-ste100.org/about_STE.html). Use `references/writing-rules.md` for the source map and important exceptions, not as a substitute for the standard.

Use the dictionary's actual approved meanings, parts of speech, and forms. A common English word is not automatically approved. A word that appears in the dictionary is not necessarily approved for every grammatical use or meaning.

Use the bundled vocabulary facts in `references/issue9-dictionary.json`: headword approvals, part-of-speech labels, explicitly printed forms, and authoritative entry references. Definition text, help, and examples remain in the official PDF. Keep private project terminology local. Consult the edition's copyright notice and the [official usage notice](https://www.asd-ste100.org/STE_downloads.html) before redistributing source text. Neither ASD nor STEMG certifies this skill or its output.

## Workflow

1. **Read for meaning.** Identify the actions, actors, conditions, quantities, exceptions, recommendations, obligations, uncertainty, and frequency. Preserve all of them. Resolve genuine ambiguity with the author rather than supplying a fact.
2. **Classify the text.** Separate procedures from descriptions. Instructions use procedural rules and the 20-word sentence limit. Descriptions use the 25-word limit and paragraphs of at most six sentences. Notes within procedures are descriptive text. Review safety instructions under section 7. Lint different text types separately.
3. **Establish vocabulary sources for STE review.** Use `references/issue9-dictionary.json` and the project's approved technical nouns and verbs. If configuring vocabulary inputs, read `references/vocabulary-format.md`. Follow each relevant `meaning_ref` in the bundled data to review the actual approved meaning and restrictions in the official PDF. An empty, explicitly supplied terminology list means the project has no additional terms. A missing list means approval is unknown. If a necessary source is unavailable, continue only as a partial review and disclose the gap.
4. **Review every applicable rule.** Use all 53 records in `references/rule-coverage.json`. Record each rule internally as satisfied, revised, not applicable with a reason, or requiring review. An unmapped rule is a review task, not an automatic pass. Establish each word's approved meaning and grammatical function. Check that domain terms qualify under the technical-noun or technical-verb categories.
5. **Rewrite without changing the contract.** Use approved wording and a different sentence construction when a word-for-word replacement fails. Keep conditions before the related commands when necessary. Keep distinct concepts distinct. Do not change a recommendation into an obligation or a possibility into a fact.
6. **Run the appropriate checks on the resulting text.** Use the commands below when Python is available. Inspect advisory findings as well as hard findings. A supported pattern is evidence for review, not proof of grammatical function. If execution is unavailable, state that automated checks were not run when reporting verification.
7. **Finish the review, not just the pattern scan.** Check the remaining rule criteria against the source text and authoritative standard. Qualified subject-matter review is necessary for safety, technical correctness, and terminology approval. Report unresolved items rather than declaring compliance.

## Script

Run from the installed skill directory:

```bash
# Assisted STE review. Inputs remain local; nothing is uploaded.
python3 scripts/ste-lint.py --mode ste --text-type procedure \
  --dictionary references/issue9-dictionary.json \
  --terminology /path/to/project-terms.json instructions.md

# Dictionary lookup without project terminology still needs terminology review.
python3 scripts/ste-lint.py --mode ste --text-type description \
  --dictionary references/issue9-dictionary.json --json description.md

# General clarity, without a claim of STE compliance.
python3 scripts/ste-lint.py --mode clarity description.md

# Inspect the complete rule inventory.
python3 scripts/ste-lint.py --list-rules --json
```

The default script mode is `clarity`. Explicit STE requests require `--mode ste`.

In STE mode the script checks semicolons, sentence length, contractions, descriptive paragraph length, selected phrasal verbs and nominalizations, possible passive/progressive/perfect constructions, and supplied vocabulary. Local terminology can identify noncanonical aliases and explicitly configured counting units.

The grammar checks are heuristic. The dictionary check establishes surface-form membership only. It does not establish the meaning, part of speech, or permissible technical use in the sentence. Missing vocabulary sources remain coverage gaps.

The JSON report includes the 53-rule coverage inventory, source gaps, official rule IDs for findings, and applicable `review_required` criteria. Read it before making any compliance claim.

| Exit | Meaning |
|---|---|
| 0 | Clarity checks passed, or a rule-list/self-test command completed. Not an STE acceptance. |
| 1 | Hard findings exceed the allowed baseline. |
| 2 | Invalid input, flags, or vocabulary configuration. |
| 3 | Assisted STE scan completed with no hard findings; review is still required. |

STE mode permits neither nonzero baselines nor disabled checks. In clarity mode, `--baseline N` and `--disable rule1,rule2` support selective lint.

## Meaning-preserving STE review

- **Uncertainty is content.** In clarity mode, `may have failed` can remain unchanged. In STE mode, flag its complex verb construction under 3.2/3.4. Find a permitted construction with the same uncertainty, or report an unresolved conflict. The hedge does not make the construction STE-approved.
- **Requirement strength is content.** Preserve what `must`, `should`, `may`, and `can` mean in the source. If a word or sense is not approved, restructure the sentence or request a decision. Do not silently strengthen it.
- **Active voice has a specific exception.** Rule 3.6 permits passive voice in descriptions when the agent is unknown. An irrelevant but known agent is not the stated exception. A past participle describing a condition can be an adjective rather than passive voice.
- **Instruction count has an exception.** Rule 5.2 normally requires one instruction per sentence, but simultaneous actions can occur in one sentence. Establish the intended timing before splitting them.
- **Multi-word nouns have an exception.** Apply 2.1 together with 2.2. A long official technical noun can need its full form before a clear shorter form or permitted hyphenation.
- **Count with section 8.** Parenthetical text counts as one outer word and is checked separately. Quoted text, specified names/titles/labels, quantities with units, and hyphenated words have special counting rules. Whitespace counting alone is not an STE word count.
- **Terminology is not an arbitrary allowlist.** A term needs a subject-field definition, an applicable category, and project approval. Review noun/verb use and approved inflections. Similar words can refer to different things.

## Output

Default: return the rewritten text alone.

If an STE request still has missing sources, unresolved rules, or required subject-matter review, append one concise line:

`Review required: <specific missing source, unresolved rule, or subject-matter review>.`

If shortening would lose necessary information, preserve it and append:

`Kept as-is: <wording and the information it preserves>.`

For a requested analysis, use a table with **Rule ID**, **Original**, **Revision**, and **Remaining review**. Name the mode and the vocabulary sources used. Distinguish detected patterns from established violations. Describe an unverified result as partial or review-required, not compliant or certified.

## Gotchas

- A clean automated scan is not proof of STE compliance or meaning preservation.
- Dictionary membership does not establish approved meaning, part of speech, or inflection.
- Do not exempt compound tenses silently in STE mode to preserve modality. Report the conflict if a faithful permitted rewrite is unavailable.
- Do not unify words that describe different actions merely because a synonym heuristic flags them.
- Do not hide essential instructions, limits, results, or safety precautions in notes.
- Do not infer the correct safety sequence or invent a hazard, cause, frequency, or recovery step.
- Fenced and inline code are not reviewed as prose. Markup handling and rule coverage remain partial.

For illustrative rewrites, read `examples/before-after.md`. Those clarity examples are not independently verified STE-compliant documents.
