# ASD-STE100 Issue 9: Rule Sources and Review

The authoritative source is [ASD-STE100 Issue 9, January 2025](https://zenodo.org/records/23666006/files/ASD-STE100_ISSUE9.pdf?download=1). The [ASD website](https://www.asd-ste100.org/about_STE.html) links this official Zenodo record. The download-request form is not the only access route.

This skill paraphrases rule purposes and bundles vocabulary approval/form facts in `references/issue9-dictionary.json`. Original definitions, help, and examples remain in the linked standard; each approved index entry has a `meaning_ref` locator. Consult the edition's copyright notice and [ASD usage notice](https://www.asd-ste100.org/STE_downloads.html) before redistributing source text. The standard's availability is not tool certification.

## Complete rule inventory

Read `references/rule-coverage.json` for every STE task. It is the single maintained inventory of all 53 official writing-rule IDs, partial script checks, and remaining review criteria.

| Section | Subject | Rules |
|---|---|---|
| 1 | Words, forms, terminology, spelling | 1.1–1.14 |
| 2 | Multi-word nouns | 2.1–2.2 |
| 3 | Verbs | 3.1–3.7 |
| 4 | Sentences | 4.1–4.5 |
| 5 | Procedural writing | 5.1–5.5 |
| 6 | Descriptive writing | 6.1–6.6 |
| 7 | Safety instructions | 7.1–7.3 |
| 8 | Punctuation and word count | 8.1–8.7 |
| 9 | Writing practices | 9.1–9.4 |

Do not count the general recommendations in section 9 as additional writing rules. Issue 9 moved the former rule 2.3 to 4.5.

## Dictionary and terminology

Part 2, introduction page 2-0-3, identifies 875 approved words and 1274 non-approved words. These are edition-specific word counts, not a validation checksum for a JSON export. Entries specify part of speech, approved meanings or alternatives, and relevant forms/help.

Part 2, pages 2-0-5 through 2-0-8, explains noun plurals, permitted verb forms, auxiliary/modal restrictions, and adjective forms. For example, a noun plural can be permitted without being printed as its own entry. A local export must explicitly enumerate the surface forms accepted by this script; the script does not invent morphology.

Rules 1.5 and 1.12 allow qualifying technical nouns and verbs. There are 22 technical-noun categories and four technical-verb categories. Company terminology needs definitions, applicable categories, approved forms, and a consistent designation for each concept. It is not a blanket exemption for jargon or an arbitrary allowlist.

If using local vocabulary files, read `references/vocabulary-format.md`. Membership lookup cannot establish grammatical use, approved meaning, or technical-category qualification. These remain review tasks under 1.2, 1.3, 1.5–1.13, and 9.2 as applicable.

## Important exceptions and corrections

- **3.3/3.6:** A participial adjective can describe a condition after “be” without being passive voice. Passive voice is permitted in descriptive text only when the agent is unknown, not merely irrelevant. Source: pages 1-3-3 and 1-3-5.
- **3.2/3.4:** Perfect and other complex auxiliary constructions are not exempt merely because they preserve uncertainty or current relevance. Preserve meaning through an approved construction, or report the unresolved conflict. Source: pages 1-3-2 through 1-3-4.
- **5.2:** One instruction per sentence is the normal rule. Simultaneous actions can be combined. Establish timing before splitting a command. Source: page 1-5-2.
- **2.1/2.2:** Apply the three-word limit together with the provisions for full technical nouns, introduced shorter forms/abbreviations, and appropriate hyphens. A long official term is not automatically a defect. Source: pages 1-2-1 through 1-2-4.
- **4.2/4.5:** Do not shorten by omitting necessary words or using contractions. Article use has grammatical exceptions, including identified items such as an item followed by its identifier. Source: pages 1-4-3 and 1-4-8.
- **5.5:** Notes give information, not essential instructions, limits, or results. A reader must be able to perform the procedure correctly without the notes. Source: pages 1-5-5 through 1-5-7.
- **7.1–7.3:** Identify risk appropriately, start the safety instruction with a clear command/condition, and explain the risk or result. Correct language does not establish that the technical instruction is safe.
- **8.1:** Semicolons are not permitted. Other punctuation still needs correct use; this is not a blanket ban on em dashes.
- **8.4:** A colon introducing a vertical list ends the introductory counting unit. Each list item is counted separately.
- **8.5:** Parenthetical text counts as one outer word, but its inner text must also be checked separately.
- **8.6:** Numbers with units, abbreviations, identifiers, quoted text, specified titles/labels, and proper names have special one-word counting provisions. Work-step and paragraph numbers do not count.
- **8.7:** Hyphenated words count as one word. Spelling and appropriate hyphenation still require review.

The section 8 provisions are on pages 1-8-4 through 1-8-7. The script handles a documented subset, including explicitly configured counting units; it does not identify every semantic exemption.

## Interpreting a report

A mapped check establishes only the part it actually analyzes. A `partial` coverage entry still requires the record's `review` criterion. A `review-required` entry is not a passed rule. Applicability metadata guides review; classify mixed sections, notes, and safety text yourself.

STE mode returns exit 3 when no hard findings remain because automated acceptance is not supported. Complete all applicable rule reviews and verify the dictionary uses and technical terminology before making a document-level compliance claim.
