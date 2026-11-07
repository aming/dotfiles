# ASD-STE100 Skill — Simplified Technical English for Agent Output

An agent skill that rewrites dense, ambiguous English using rules inspired by [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/) (STE) — the controlled-language standard the aerospace and defense industry built so aircraft maintenance instructions cannot be misread.

This skill repurposes that same discipline for a different reader: an **AI agent** parsing another agent's output, a tool description, an error message, or an inter-agent instruction, with no human in the loop to resolve ambiguity.

## Why STE, and Why for Agents

STE exists because a misread instruction on an aircraft can kill people, and the intended readers were often not native English speakers with no author to call for clarification. The standard's fix: one meaning per word, active voice, simple tenses, one instruction per sentence, short sentences, no dropped words.

An LLM agent parsing another agent's output is in a strikingly similar position — no back-channel, no way to ask "did you mean X or Y?" The same rules that keep a mechanic from misreading a torque spec keep a downstream agent from misreading a tool description or an inter-agent message.

## Before / After

| Before | After |
|---|---|
| "This tool will attempt to synchronize state across the various backends that have been configured, and if a conflict is detected it may resolve it automatically depending on the strategy that has been set, or otherwise it will surface the conflict for manual review." | "The tool will try to synchronize state across the configured backends. If it detects a conflict, it may resolve the conflict automatically, depending on the configured strategy. Otherwise, it will report the conflict for manual review." |
| "An error may have occurred while processing your request due to a possible mismatch in the expected data format, which could be caused by an outdated client version." | "An error may have occurred while processing your request. A mismatch with the expected data format may have caused the error. An outdated client version could have caused this mismatch." |

More examples, including illustrations of the official STE rules themselves, in [`examples/before-after.md`](examples/before-after.md).

## What This Skill Does

1. Picks a mode. **Strict** covers procedures, error messages, and tool descriptions. **STE-flavored** covers READMEs, PR descriptions, and explanatory prose. STE-flavored keeps the sentence discipline but not the fixed-vocabulary lockdown.
2. Reads the input English text for meaning.
3. Flags every rule violation sentence-by-sentence: ambiguous word choice, present-perfect/complex tense, passive voice with an unclear actor, multi-instruction sentences, oversized noun clusters, dropped words, sentences over length, phrasal verbs, nominalized actions, semicolons, hedge stacks, and marketing adjectives.
4. Rewrites each flagged sentence — without dropping any fact, condition, or scope qualifier from the original. If a shorter phrasing would lose required precision, it keeps the longer phrasing and flags the trade-off instead of silently simplifying.
5. Outputs the rewritten text on its own — no preamble, no mode announcement, no change summary — plus a one-line `Kept as-is:` note when it deliberately left something unsimplified.

Ask for the reasoning ("show the diff", "which rules did it break") and it outputs a before/after table naming each rule instead.

The structural rules it checks are mechanical — you can point at the word or punctuation mark that breaks each one. The rules that depend on ASD's dictionary are flagged as advisory rather than enforced, and the rules that need taste are left to you.

The linter checks structural patterns only. It does not compare an original text with a rewrite, verify that requirement strength stayed the same, or prove that the rewrite preserved meaning. A zero-violation result means that the configured structural checks found no problems.

The deterministic linter checks semicolons, a short list of soft phrasal verbs (spin up, reach out, dive into, kick off, circle back, touch base), nominalizations, marketing adjectives, passive voice, present-perfect forms (including irregular participles such as "has run"), long sentences, synonym rotation, and dangling conjunctions in supported list items. It does not check noun-cluster length (that needs part-of-speech tagging) and it does not know phrasal verbs outside its list, so "take off the panel" passes. It never flags hedges or modality.

Use `--text-type procedure` for the 20-word instruction limit. The default `--text-type description` uses the 25-word description limit. For mixed documents, lint procedure sections separately.

For the sentence-length check, a word is a whitespace-separated token with at least one letter or digit. Inline code in single backticks, list markers, blockquote markers, and bare punctuation such as a spaced em dash are not words.

The repo's own prose does not lint clean: the rule tables quote the patterns they forbid, and some sentences run long. Lint it with `python scripts/ste-lint.py --baseline 36 SKILL.md` and read the findings as examples, not defects.

The dangling-conjunction rule checks list markers at the start of a line with zero to three leading spaces and ASCII spaces after the marker. It supports unordered markers `-`, `*`, and `+`, and ordered numeric markers that end in `.` or `)`, such as `1.` or `1)`. It checks indented continuation lines up to the final meaningful line. It does not parse list syntax inside blockquotes, lazy continuation, or full nested-list semantics. A standalone line with four or more leading spaces is not treated as a list marker. Within an active list item, indentation at the computed content column is treated as continuation text. Fence detection follows CommonMark for blockquotes and for the fence itself. A fence opens on three or more backticks or tildes, also inside a blockquote. It closes on a run of the same character that is at least as long and has only spaces or tabs after it. A fence in a blockquote closes when the quote ends. In an HTML block, a `>` line is text and opens no fence. An HTML block starts on a block tag such as `<div>`, or on one complete tag alone on its line that does not continue a paragraph. Inline HTML such as `<span>` in a line of text starts no HTML block. In the main pass, no fence opens in an HTML block, at any quote depth. An HTML block can also sit in a blockquote, and it ends when its quote ends. The dangling-conjunction pass does not track HTML blocks, so it still opens a fence there. The linter does not track list items. So it accepts a fence at any indent. It also accepts a closing fence up to three columns deeper than the opening fence, also at the top level. A fence in a list item does not close when the item ends. A fence that starts on the line of a list marker is not detected. Its closing line then opens a fence, and the linter skips the text after it.

The intentionally invalid examples/linter-edge-cases.md file demonstrates incomplete Markdown list items. Run python scripts/ste-lint.py examples/linter-edge-cases.md to confirm that the linter reports the two expected findings. The file is a test fixture and should not be used as compliant STE prose.

It does **not** reproduce ASD's official ~900-word approved dictionary. The standard is free to obtain but not free to redistribute: Issue 9 permits reproduction only with ASD's written authority, or by eight listed categories of organisation that this project does not belong to. This skill applies the underlying *principle* (plainest available word, used the same way every time) rather than checking against a fixed word list. For certified STE-compliant documentation, use the real standard.

Full rule summary and citations: [`references/writing-rules.md`](references/writing-rules.md).

## Installation

This skill uses a `SKILL.md` file, Markdown references, and an optional Python linter. It does not require a particular model provider, agent API, or proprietary tool.

Copy the complete `asd-ste100/` directory into the skill directory supported by your agent. Use your host's documented project or user skill location. Keep `SKILL.md`, `references/`, `examples/`, and `scripts/` together so relative paths resolve. Reload the host's skill catalog if required.

Install this repository's copy to include its updated instructions and linter. An upstream installation can contain a different version.

If your host does not support skill discovery, load `SKILL.md` as task instructions and provide access to the sibling resources. Automatic invocation requires host support for skill discovery.

### Optional linter

The linter requires Python 3 and uses only the standard library. From the installed skill directory, run:

```bash
python3 scripts/ste-lint.py --text-type procedure instructions.md
python3 scripts/ste-lint.py --text-type description description.md
python3 scripts/ste-lint.py --selftest
```

If Python or command execution is unavailable, apply the rewrite instructions manually and report automated linting as not run when asked for verification.

## Usage

Trigger with a request to simplify or clarify English text:

```
Disambiguate this tool description
Rewrite this error message so an agent can't misparse it
Use ASD-STE100 to simplify this English: [paste text]
Apply ASD-STE100 to this instruction
```

Or paste text and ask your agent to "disambiguate this" / "apply STE100 to this" / "reduce ambiguity in this output."

You get the rewritten text back and nothing else. To see which rules were applied, add "show the diff" or "explain the changes" to the request.

## Scope

Built for: agent-to-agent messages, tool/function descriptions, error messages, system prompts, inter-agent instructions — any English text a machine or non-native reader has to parse without a human to ask.

For creative writing or marketing copy, use this skill only when the user explicitly requests an STE rewrite. STE is deliberately flat and literal.

One limit worth stating up front: this fixes the form of a text, not its substance. A paragraph with nothing to say comes out short, clean, and still empty.

## Other Languages

- **Hebrew:** [g4lb/asd-ste100-hebrew-skill](https://github.com/g4lb/asd-ste100-hebrew-skill) is a Hebrew port of this skill. It includes a Hebrew linter. ASD-STE100 defines English only, so the Hebrew rules are an adaptation, not an official standard.
- **Indonesian:** [jshsinaga/asd-ste100-indonesian-skill](https://github.com/jshsinaga/asd-ste100-indonesian-skill) adapts this skill for Indonesian technical text. Its Indonesian rules are an adaptation, not an official ASD-STE100 standard.

## Related Tools

- [meiluosi/rewrite-fidelity-skill](https://github.com/meiluosi/rewrite-fidelity-skill) compares the original text with the rewrite. It flags changes in meaning and modality. It uses pattern matching, so check each flag yourself.

## Sources

- [ASD-STE100 official site](https://www.asd-ste100.org/)
- [ASD-STE100 — About STE](https://www.asd-ste100.org/about_STE.html)
- [ASD Europe — Simplified Technical English](https://www.asd-europe.org/standards-specifications/simplified-technical-english/)
- [Simplified Technical English — Wikipedia](https://en.wikipedia.org/wiki/Simplified_Technical_English)
- [TechScribe — ASD-STE100 Simplified Technical English](https://www.techscribe.co.uk/techw/asd-simplified-technical-english.htm)

