---
name: asd-ste100
description: "Rewrite or review English using ASD-STE100 Simplified Technical English. Use for explicit STE100, STE-100, ASD-STE100, or STE compliance requests, and to clarify technical instructions, tool descriptions, error messages, and agent output. Default to 80%: all structural rules at full strength with document-consistency vocabulary. Use STE review (strict) for explicit STE requests; review all 53 Issue 9 rules, the official dictionary, and approved project terminology. Preserve meaning, uncertainty, and requirement strength. Do not apply to creative or marketing copy unless requested."
compatibility: Python 3 for the optional stdlib-only linter; authoritative Issue 9 and approved project terminology for a complete assisted review.
---

# Simplified Technical English

## Choose the contract

**80% (default)**: Use for general simplification, agent output, READMEs, PR descriptions, error messages, tool descriptions, status reports, and inter-agent instructions. Apply every structural rule at full strength: sentence limits, one instruction per sentence, active voice, no semicolons, paragraph limits, lists for sequences, and simple tenses except where a compound form carries information the simple form cannot. Treat lexical rules as document-consistency rules, not dictionary checks: one term per concept, verb over nominalization, no synonym rotation. Keep identifiers, numbers, conditions, exceptions, and hedges exactly as the source states them. Do not compress content to hit a style target. Describe the result as an 80% rewrite, not verified STE.

"80%" is a scope, not a fuzzy score. The countable rules stay at 100%; vocabulary and the one-word-one-meaning lockdown relax. A per-sentence "80% compliant" target is uncheckable, and it tempts a writer to delete the qualifiers that carry the meaning.

**STE review (Strict)**: Use when the user requests ASD-STE100, STE compliance, or a rewrite in STE, or when the text is a safety-critical procedure. Apply the actual Issue 9 rules and vocabulary. The script supplies partial checks, not a compliance certificate. Meaning, grammatical function, terminology qualifications, and safety need review.

An aircraft procedure and an agent instruction can have different subject matter. Both still need the correct STE rules when the user requests STE. Do not invent an exception because the text concerns software.

Both contracts preserve meaning first. The difference is how far they push word choice, not how much content they may drop.

## Why 80% is the default

Strict STE prompting reliably shortens sentences and cuts passive voice, but the available prompt-level tests did not show better model comprehension, and one informal test measured 46.8% of scored facts lost in Claude's code explanations under strict STE, against 8.5% under a loose plain-English instruction. The human studies that justify STE found gains on difficult procedures, especially for non-native readers, and no gain on easy text. The 80% scope keeps the checkable structural rules and avoids the fact loss that strict prompting showed. It is a defensible default, not a proven optimum: no study compares 80% and 100% head to head. Read `references/mode-evidence.md` when the user asks why 80% is the default or disputes the mode choice.

## Authoritative sources

Issue 9, January 2025, has 53 writing rules in nine sections and a controlled dictionary. Technical nouns and technical verbs extend the dictionary only under the standard's terminology rules. These sources apply to STE review; 80% tasks use the structural rules and document consistency instead.

For every STE review task, read `references/rule-coverage.json`. It accounts for each official rule ID, the script's related checks, and the judgment still required. When interpreting a rule or a dictionary entry, consult the actual [official Issue 9 PDF](https://zenodo.org/records/23666006/files/ASD-STE100_ISSUE9.pdf?download=1), linked from the [ASD website](https://www.asd-ste100.org/about_STE.html). Use `references/writing-rules.md` for the source map and important exceptions, not as a substitute for the standard.

Use the dictionary's actual approved meanings, parts of speech, and forms. A common English word is not automatically approved. A word that appears in the dictionary is not necessarily approved for every grammatical use or meaning.

Use the bundled vocabulary facts in `references/issue9-dictionary.json`: headword approvals, part-of-speech labels, explicitly printed forms, and authoritative entry references. Definition text, help, and examples remain in the official PDF. Keep private project terminology local. Consult the edition's copyright notice and the [official usage notice](https://www.asd-ste100.org/STE_downloads.html) before redistributing source text. Neither ASD nor STEMG certifies this skill or its output.

## Workflow

1. **Read for meaning.** Identify the actions, actors, conditions, quantities, exceptions, recommendations, obligations, uncertainty, and frequency. Preserve all of them. Keep genuine ambiguity as ambiguity: when `otherwise`, `or`, or `unless` can refer to two conditions, do not choose a reading. Do not invent an actor for a passive sentence. If a decision is required, ask the author or report the unresolved item.
2. **Choose the contract and classify the text.** Default to 80%. Use STE review (Strict) only for an explicit STE request or a safety-critical procedure. Separate procedures from descriptions. Instructions use procedural rules and the 20-word sentence limit. Descriptions use the 25-word limit and paragraphs of at most six sentences. Notes within procedures are descriptive text. Review safety instructions under section 7. Lint different text types separately.
3. **For STE review, establish vocabulary sources.** Use `references/issue9-dictionary.json` and the project's approved technical nouns and verbs. If configuring vocabulary inputs, read `references/vocabulary-format.md`. Follow each relevant `meaning_ref` in the bundled data to review the actual approved meaning and restrictions in the official PDF. An empty, explicitly supplied terminology list means the project has no additional terms. A missing list means approval is unknown. If a necessary source is unavailable, continue only as a partial review and disclose the gap. In 80% mode, skip the dictionary and use document consistency instead.
4. **Review every applicable rule.** For STE review, use all 53 records in `references/rule-coverage.json`. Record each rule internally as satisfied, revised, not applicable with a reason, or requiring review. An unmapped rule is a review task, not an automatic pass. Establish each word's approved meaning and grammatical function. Check that domain terms qualify under the technical-noun or technical-verb categories. For 80%, check the structural rules and term consistency only.
5. **Rewrite without changing the contract.** Use approved wording and a different sentence construction when a word-for-word replacement fails. Keep conditions before the related commands when necessary. Keep distinct concepts distinct. Do not change a recommendation into an obligation or a possibility into a fact. Do not delete a condition, identifier, number, or hedge to shorten a sentence.
6. **Run the appropriate checks on the resulting text.** Use the commands below when Python is available. Use `--mode ste` for STE review and `--mode 80` for the default contract. Inspect advisory findings as well as hard findings. A supported pattern is evidence for review, not proof of grammatical function. If execution is unavailable, state that automated checks were not run when reporting verification.
7. **Finish the review, not just the pattern scan.** For STE review, check the remaining rule criteria against the source text and authoritative standard. Qualified subject-matter review is necessary for safety, technical correctness, and terminology approval. For 80%, verify that no meaning was lost and that no compliance claim was made. Report unresolved items rather than declaring compliance.

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

# 80% default: structural checks, no dictionary claim.
python3 scripts/ste-lint.py --mode 80 --text-type description description.md

# Inspect the complete rule inventory.
python3 scripts/ste-lint.py --list-rules --json
```

The default script mode is `80`. Explicit STE requests require `--mode ste`. The script's `clarity` profile implements the 80% checks, so `--mode clarity` is an accepted alias for `--mode 80`.

In STE review the script checks semicolons, sentence length, contractions, descriptive paragraph length, selected phrasal verbs and nominalizations, possible passive/progressive/perfect constructions, and supplied vocabulary. Local terminology can identify noncanonical aliases and explicitly configured counting units.

The grammar checks are heuristic. The dictionary check establishes surface-form membership only. It does not establish the meaning, part of speech, or permissible technical use in the sentence. Missing vocabulary sources remain coverage gaps.

The JSON report includes the 53-rule coverage inventory, source gaps, official rule IDs for findings, and applicable `review_required` criteria. Read it before making any compliance claim.

| Exit | Meaning |
|---|---|
| 0 | 80% checks passed, or a rule-list/self-test command completed. Not an STE acceptance. |
| 1 | Hard findings exceed the allowed baseline. |
| 2 | Invalid input, flags, or vocabulary configuration. |
| 3 | Assisted STE scan completed with no hard findings; review is still required. |

STE review permits neither nonzero baselines nor disabled checks. In 80% mode, `--baseline N` and `--disable rule1,rule2` support selective lint.

## Meaning-preserving review

- **Uncertainty is content.** In 80% mode, `may have failed` can remain unchanged. In STE review, flag its complex verb construction under 3.2/3.4. Find a permitted construction with the same uncertainty, or report an unresolved conflict. The hedge does not make the construction STE-approved.
- **Requirement strength is content.** Preserve what `must`, `should`, `may`, and `can` mean in the source. If a word or sense is not approved, restructure the sentence or request a decision. Do not silently strengthen it.
- **Ambiguity is content.** Keep `otherwise`, `or`, and `unless` when they can refer to two conditions. Choosing one reading is a meaning change, not a clarification. Name the ambiguity if the user asks for analysis.
- **Do not invent an actor.** A passive sentence may hide an actor the source does not identify. Keep the passive or use an impersonal subject; active voice is not worth a new fact.
- **80% is a scope, not a score.** Do not delete a condition, identifier, number, exception, or hedge to look closer to a percentage target.
- **Active voice has a specific exception.** Rule 3.6 permits passive voice in descriptions when the agent is unknown. An irrelevant but known agent is not the stated exception. A past participle describing a condition can be an adjective rather than passive voice.
- **Instruction count has an exception.** Rule 5.2 normally requires one instruction per sentence, but simultaneous actions can occur in one sentence. Establish the intended timing before splitting them.
- **Multi-word nouns have an exception.** Apply 2.1 together with 2.2. A long official technical noun can need its full form before a clear shorter form or permitted hyphenation.
- **Count with section 8.** Parenthetical text counts as one outer word and is checked separately. Quoted text, specified names/titles/labels, quantities with units, and hyphenated words have special counting rules. Whitespace counting alone is not an STE word count.
- **Terminology is not an arbitrary allowlist.** A term needs a subject-field definition, an applicable category, and project approval. Review noun/verb use and approved inflections. Similar words can refer to different things.

## Output

Default: return the rewritten text alone.

If the user asks which contract you used, answer in one line: `Mode: 80% (default).` or `Mode: STE review (Strict).` Do not defend the choice unless the user asks for the reason.

If an STE request still has missing sources, unresolved rules, or required subject-matter review, append one concise line:

`Review required: <specific missing source, unresolved rule, or subject-matter review>.`

If shortening would lose necessary information, preserve it and append:

`Kept as-is: <wording and the information it preserves>.`

For a requested analysis, use a table with **Rule ID**, **Original**, **Revision**, and **Remaining review**. Name the contract and the vocabulary sources used. Distinguish detected patterns from established violations. Describe an unverified result as partial or review-required, not compliant or certified.

## Gotchas

- A clean automated scan is not proof of STE compliance or meaning preservation.
- 80% is a scope, not permission to shorten. Relaxing vocabulary must not cut a condition, number, identifier, exception, or hedge.
- Do not claim STE review (Strict) or dictionary compliance when the dictionary and terminology sources are missing.
- Dictionary membership does not establish approved meaning, part of speech, or inflection.
- Do not exempt compound tenses silently in STE review to preserve modality. Report the conflict if a faithful permitted rewrite is unavailable.
- Do not unify words that describe different actions merely because a synonym heuristic flags them.
- Do not hide essential instructions, limits, results, or safety precautions in notes.
- Do not infer the correct safety sequence or invent a hazard, cause, frequency, or recovery step.
- Fenced and inline code are not reviewed as prose. Markup handling and rule coverage remain partial.

For illustrative rewrites, read `examples/before-after.md`. Those 80% examples are not independently verified STE-compliant documents.
