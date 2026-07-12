# ACE Note Processing

Read this file when the user wants to process, edit, move, link, or develop notes inside the vault.

## Defaults

- Keep edits small.
- Preserve the user's wording and multilingual voice.
- Light grammar cleanup is okay; do not rewrite the note into generic polished prose.
- Do not delete notes unless the user explicitly approves deletion.
- Ask one clarifying question only if moving the note would risk putting it in the wrong place.

## Content And Title Defaults

**Language style for Chinese content:** Default to 書面語 for note body text and other free-form note content unless the user asks for a different style.

**Title and summary language:** Use English for filenames, headings, MOC section headings, and `summary` frontmatter values unless the user explicitly asks otherwise.

Rename `Untitled` or `New note` immediately. Those are never meaningful titles.

## Core Workflow

1. Read the target note.
2. Identify the note's primary intent from the content, not just the title.
3. If the note is still raw and the user has not asked to process it now, leave it in `+`.
4. If the user asked to process it, do minimal processing only.
5. Preserve the existing title during Add unless the user explicitly asks for a rename or the title is truly unusable.
6. Add or complete frontmatter when it is missing or clearly incomplete, including a one-line `summary`.
7. Add useful `up` and `related` links when obvious from context.
8. Decide whether the note needs `note/boat`, `note/develop`, or no Relate tag.
9. If the note is a Boat, run the Boats process.
10. If the note should be developed, run the Develop process.
11. Consider whether a MOC exists or is needed only when a cluster of related notes is forming.
12. If the user wants to turn thinking into output, run the Communicate process.
13. Move the note to the best ACE destination using `obsidian move` unless a rename is explicitly needed.

## Frontmatter Guidance

Use the vault's existing YAML style for list-valued wikilink properties:

```yaml
up:
  - "[[Parent Note]]"
related:
  - "[[Related Note]]"
```

Use `summary` as a plain-language one-liner. It should answer: "What would Future Me need to know from this note at a glance?"

Verify note changes after `obsidian property:set`; this CLI can report success without changing the file.

## Add Process

The `Add` note is a cooling pad, not just an inbox.

When processing a note from `+`:

- Add a link.
- Preserve the current title unless it is unusable or the user asked to rename it.
- Add a one-line `summary`.
- Decide whether a Relate tag is useful.
- Add details only when they clarify the note.
- Move it to the best folder.
- Flag deletion candidates, but do not delete without approval.

Add answers two questions:

1. Where should this note live?
2. What does this note need next?

Add completes when the note is moved to the correct ACE folder. The `boat/develop/evergreen` Relate tags classify what the note needs **within** its destination folder — they do not block the move. A `note/boat` note still goes to Atlas/Efforts/Calendar after processing; the tag means "still needs tethering once there."

## Relate Tags

Use `note/boat` when the note is rough, short, newly formed, has few links, or mostly needs tethering.

Use `note/develop` when the note has clear value and should be developed with examples, critique, sources, or a stronger argument.

If the note is already clear enough for now, use no Relate tag.

Do not add both tags unless the user explicitly wants that workflow.

## Boats Process

A Boat is a note that is valuable but still floating alone. The goal is to tether it so Future You can find it again.

Workflow:

1. Extract 2-5 core terms, themes, or implied questions from the note.
2. Search the vault for candidate notes using titles, terms, synonyms, and parent concepts.
3. Prefer candidates in `Atlas/Maps` and `Atlas/Dots` before broad searching.
4. Suggest 2-5 tether notes.
5. Explain why each tether is useful in one line.
6. Add only the strongest obvious links automatically when the user asked you to process the note.

Three strong tethers are better than ten weak ones.

## Develop Process

Develop is for notes that already have a spark and deserve active growth. The goal is to help the user grow their own thinking, not replace it with polished AI prose.

Default to interactive coaching unless the user explicitly asks you to edit.

Useful lenses:

- own viewpoint
- example
- counterexample or limits
- source
- definition
- higher map

Workflow:

1. Identify the note's core claim or concept.
2. Check existing `up`, `related`, `summary`, and tags.
3. Search for obvious higher maps or related sources only when needed.
4. Ask 2-4 focused questions that help the user clarify their own view.
5. Offer 3-6 reference points the user can accept, reject, or modify.
6. If the user asked for edits, add only clearly useful sections.

Keep additions compact. Make the note more usable, not more generic.

## MOC Process

MOC means Map of Content. It is not a folder and not a mandatory next step for every note. It is a thinking surface for a cluster of related notes.

First principle:

```text
Add decides where a note lives.
Relate decides what it connects to.
MOC appears when connected notes need a thinking surface.
```

Create or update a MOC when:

- the user asks for a map
- related notes are getting scattered
- a cluster of roughly 3-5 related notes is forming
- the user wants to teach, summarize, or navigate a topic

Where MOCs live:

```text
Atlas/Maps/
```

Prefer updating an existing MOC over creating a duplicate. Keep new MOCs small and start with a simple gather structure.

## Communicate Process

Communicate turns thinking into output. A MOC is a map of the territory; output is a route through the territory for an audience.

Run this when the user wants to communicate, write, publish, teach, explain, or turn notes into something shareable.

Default workflow:

1. Ask who the output is for, what form it should take, and what source notes it should draw from unless the user already answered.
2. Create an outline first; do not draft the full final output unless the user asks.
3. Keep the source MOC as the map and let the output become the route.

Communicate outputs start as work, so place them in `Efforts/Notes/`.

## Quick Destination Rules

Use primary intent.

- Raw, uncertain, sparse capture -> `+`
- Concept, framework, reusable knowledge -> `Atlas/Dots/Things`
- Claim, insight, conclusion -> `Atlas/Dots/Statements`
- Person note -> `Atlas/Dots/People`
- External source -> `Atlas/Dots/Sources`
- MOC or navigation page -> `Atlas/Maps`
- Daily reflection or dated record -> `Calendar/Journals/<Year>/`
- Meeting note -> `Calendar/Meetings/`
- Review note -> `Calendar/Reviews/`
- Active work -> `Efforts/On` or another `Efforts/*` intensity bucket
- Supporting material for an effort -> `Efforts/Notes/`

If more than one destination seems plausible, choose by primary intent and connect the others with links.

If you are unsure between Calendar and Efforts, ask: am I recording this over time, or doing something about it?

## Title Rules

During Add, do not normally rename a recognizable title. Title refinement belongs later in Develop, when the note's meaning is clearer.

Rename during Add only when:

- the user explicitly asks for a rename
- the title is truly unusable such as `Untitled` or `New note`
- keeping the title would create an obvious collision that blocks the move

If a title is weak but still recognizable, keep it and optionally suggest a future rename.

## Final Response Pattern

When helpful, report the result like this:

```text
Processed: `<old path>` -> `<new path>`

Reason: <intent-based explanation>

Changed:
- <frontmatter/link/title/move/etc>

Unresolved: <only if there is a real question or risk>
```

If no move was made:

```text
Left in place: `<path>`

Reason: <why it should remain capture or why clarification is needed>
```

## Boundaries

- Do not force a sparse capture into Atlas just because it names a concept.
- Do not over-polish raw thinking.
- Do not split one note into multiple notes unless the user asks.
- Do not create a MOC unless there are enough related notes or the user asks.
- Do not invent unsupported facts or citations.
