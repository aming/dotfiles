# Bundled and Local Vocabulary Files

Use `--dictionary references/issue9-dictionary.json` from the skill directory. This bundled index contains vocabulary approval facts, part-of-speech labels, explicitly printed forms, and references to the authoritative entries. It does not reproduce original definitions, help, or examples. The assisted checker accepts UTF-8 JSON via `--dictionary` and `--terminology` in `--mode ste`; it does not parse the PDF or download vocabulary at runtime. Keep private project terminology and restricted source-text exports local.

A supplied file is not proof that its contents are authoritative or complete. Check its provenance, edition, definitions, forms, and coverage before relying on its findings. Missing files are configuration errors. Omitted flags are reported as missing-source gaps. No unknown-word findings are produced without a dictionary; this is an unchecked area, not approval.

## Dictionary

Top-level fields:

- `issue`: integer `9`.
- `source`: nonempty provenance string identifying the source and export/review revision.
- `entries`: nonempty array, including at least one approved entry.

Each entry:

| Field | Meaning |
|---|---|
| `word` | Headword or multi-word entry. Matching is case-insensitive. |
| `pos` | `n`, `v`, `adj`, `adv`, `pron`, `art`, `prep`, or `conj`. The bundled source also uses `phrase` for unlabeled phrases and `prefix` for the source's prefix entry; these are not inferred grammatical approvals. |
| `approved` | JSON boolean, not a string or number. |
| `meaning` | Nonempty approved meaning, required for an approved entry unless `meaning_ref` is supplied. |
| `meaning_ref` | Nonempty locator for the authoritative entry. Use it instead of reproducing the definition; follow it for contextual meaning and restrictions. |
| `forms` | Optional array of explicitly permitted surface forms. The headword is already included. |
| `alternatives` | Optional array of suggested alternatives for a non-approved entry. These are suggestions, not automatic replacements. |
| `restricted_uses` | Optional array of locators for approved uses that carry restrictions. Preserved as metadata; the checker does not enforce the restrictions, so review them in the source. |

The following is a **schema excerpt**, not a complete deployable dictionary:

```json
{
  "issue": 9,
  "source": "Issue 9, locally reviewed export; incomplete schema illustration",
  "entries": [
    {
      "word": "aid",
      "pos": "n",
      "approved": true,
      "meaning": "Help provided.",
      "forms": []
    }
  ]
}
```

The bundled index records printed headwords and verb/adjective forms. It also preserves page references, source-PDF identity, and restricted-use references where one spelling has both approved and non-approved uses. Its word/part-of-speech record count is not the introductory count of words in the standard. Noun plurals can be permitted without separate printed entries; review countability and help restrictions before adding those forms to a custom export. The checker never guesses plural, conjugated, comparative, or superlative forms. Neither `meaning` nor `meaning_ref` performs semantic validation.

The same spelling can have multiple entries with different parts of speech. The scanner accepts a surface form if at least one applicable entry marks it approved; establishing which part of speech is actually used remains a review task. Conflicting approval records for the same surface—headword or explicitly listed form—and part of speech are rejected.

## Project terminology

Top-level `issue` and `source` have the same requirements. `entries` can be empty if the project explicitly has no additional terms.

Each entry:

| Field | Meaning |
|---|---|
| `term` | Canonical approved technical noun or verb. |
| `pos` | `n` for a technical noun, `v` for a technical verb. |
| `definition` | Nonempty subject-field definition. |
| `category` | Integer category from Rule 1.5 (`n`: 1–22) or 1.12 (`v`: 1–4). |
| `forms` | Optional explicit approved forms. |
| `aliases` | Optional noncanonical spellings/designations for the same concept; findings suggest the canonical term. |
| `count_as_one` | Optional boolean, default false. Only for noun entries that qualify for a one-word counting provision. |

Illustrative project data, to be approved by the actual project owner:

```json
{
  "issue": 9,
  "source": "Project terminology review, revision 1",
  "entries": [
    {
      "term": "cache shard",
      "pos": "n",
      "definition": "One partition of the project cache.",
      "category": 19,
      "forms": ["cache shards"],
      "aliases": ["cache partition"],
      "count_as_one": false
    },
    {
      "term": "degrees Celsius",
      "pos": "n",
      "definition": "The temperature unit used by the project.",
      "category": 9,
      "count_as_one": true
    }
  ]
}
```

A normal technical noun does not become one counted word merely because it is in the glossary. Use `count_as_one` only for a qualifying name, identifier, title, label, abbreviation, quoted text, or unit under 8.6. For a category-9 counting entry, the scanner also groups an immediately preceding unsigned integer or decimal quantity with the unit: `10 degrees Celsius` counts as one. The quantity and unit must have one ASCII space between them. Signed quantities, thousands separators, and other formats remain review tasks. Review that the category-9 entry actually represents the intended measurement unit.

Aliases are not approved synonyms. The terminology owner has declared them noncanonical names for the same concept. A listed approved inflection belongs in `forms`, not `aliases`. Ambiguous aliases and conflicting terminology records are configuration errors.

## Matching and limitations

- Longest whole-token matches take precedence. A longer approved technical noun can include words that are not independently approved.
- Qualified project terminology can override a dictionary's non-approved headword, but only for the qualified technical use; the script cannot establish that use from grammar. A term, form, or alias that equals an approved dictionary surface is a configuration error.
- Soft-wrapped prose is joined for lookup. Sentence punctuation and masked code prevent accidental multi-word approval across unrelated text. Extra whitespace can therefore require review rather than matching a phrase.
- Unknown alphabetic words need correction, a qualifying approved technical term, or review of a legitimate exemption. Pure numbers do not need dictionary entries. Alphanumeric identifiers are not automatically approved just because they contain a digit.
- Punctuation and hyphenation are significant. The scanner does not turn `fuel-pump` into `fuel pump` or approve an unlisted variant. A non-alphanumeric prefix or suffix must end at a non-alphanumeric boundary, so `C++` does not approve `C++17`.
- Parts of speech, meanings, noun/verb category qualifications, American spelling exceptions, label/quotation exemptions, and contextual form restrictions remain review tasks.

STE mode always reports `compliance: not-verified`. No vocabulary file removes the need to review the applicable Issue 9 rules.
