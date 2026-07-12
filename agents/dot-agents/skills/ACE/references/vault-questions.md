# ACE Vault Questions

Read this file when the user is asking questions against the vault rather than asking you to process a single note.

Examples:

- "What ACE notes do I already have about sleep?"
- "Do I already have a map for this topic?"
- "How is my Calendar organized right now?"
- "Where would this belong in my vault?"

## Purpose

The goal is to answer from evidence in the vault, not from generic ACE theory.

When the user asks a vault question, inspect the relevant folders and notes first. Prefer grounded answers based on actual paths, note titles, wikilinks, and frontmatter over abstract advice.

## Workflow

1. Identify the question type: structure, placement, existing notes, relationships, or gaps.
2. Search the most likely ACE areas first instead of the whole vault by default:
   - `+` for raw captures.
   - `Atlas/Maps` and `Atlas/Dots` for understanding.
   - `Calendar/` for time-based notes.
   - `Efforts/` for active work.
3. Use targeted `Glob` to find likely filenames and `Grep` to search note contents.
4. Read only the strongest candidate notes needed to answer.
5. Summarize what you found and what it means in ACE terms.
6. If the user's real goal is action, transition from answering to note processing.

## Search Patterns

Use the lightest search that can answer the question.

- For "Do I already have a note/map on X?" search `Atlas/Maps` and `Atlas/Dots` first.
- For "Where should this go?" inspect both the note itself and nearby destination folders.
- For "How is this area organized?" read the relevant folder tree and 1-3 representative notes.
- For "What related notes already exist?" search titles first, then content, then verify by reading candidate notes.

## Answering Style

When helpful, use this structure:

```text
What I found:
- <note or folder>
- <note or folder>

ACE reading:
- <what this suggests about placement, structure, or topic coverage>

Next move:
- <optional action, such as create a map, leave in Inbox, move note, or link related notes>
```

Always call out uncertainty when the vault is sparse, inconsistent, or only loosely ACE-shaped.

## Placement Questions

If the user asks where a note belongs, answer from both:

1. The note's primary intent.
2. The vault's current structure and existing neighboring notes.

If those conflict, explain the tradeoff and prefer the vault's consistent ACE pattern unless the user is actively changing the pattern.

## MOC Questions

When the user asks whether a map already exists:

1. Search `Atlas/Maps` first.
2. Check whether a broader existing MOC can absorb the topic.
3. Prefer updating an existing map over creating a duplicate.
4. Only recommend a new MOC when there is a real cluster or navigation need.

## Boundaries

- Do not answer broad vault questions from memory when the vault can be inspected directly.
- Do not over-read the whole vault for a narrow question.
- Do not create or move notes unless the user is really asking for action or explicitly approves edits.
- Do not confuse "what exists" with "what should exist"; separate current state from your recommendation.
