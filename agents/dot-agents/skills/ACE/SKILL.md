---
name: ACE
description: Process and reason about the user's Obsidian vault using the Nick ACE framework. Use this skill whenever the user asks to ACE a note, classify or move notes, clean up `+`, set up or lint an ACE vault, check whether the vault follows the ACE folder contract, decide where something belongs in Atlas/Calendar/Efforts, or ask ACE-specific questions against the vault such as how notes are organized, what related notes already exist, or how a topic is represented in the vault. Use it even when the user does not explicitly say "ACE" if the real task is organizing, validating, navigating, or understanding an ACE-style Obsidian vault.
compatibility: Obsidian CLI, Python 3
---

# ACE Vault Router

Use this skill to operate on an Obsidian vault in the ACE way.

Do not frame ACE as capture-only. This skill supports three kinds of work:

1. Validate the vault structure so ACE decisions are grounded in the actual folder contract.
2. Answer questions against the vault so the user can understand what already exists and how things connect.
3. Process, connect, and move notes using Add, Boats, Develop, MOCs, Communicate, and the ACE destination rules.

The default ACE arc is still:

```text
Capture in `+` -> Process with `Add` -> Move to Atlas / Calendar / Efforts -> Relate later
```

But note processing is only one branch of the skill, not the whole identity.

## Load Rules

- If the user asks whether the vault follows ACE, wants to set up ACE folders, asks for a lint/check command, or you are unsure whether a placement rule is essential versus optional, read `references/folder-structure.md` first.
- If the user asks an ACE question about what already exists in the vault, how a topic is represented, whether a map already exists, or where something fits based on current vault contents, read `references/vault-questions.md` first.
- If the user wants edits, moves, links, development, MOC work, or processing of specific notes, read `references/note-processing.md` first.
- If more than one condition applies, start with structure, then inspect the vault, then process notes.

## Available Resources

- `references/folder-structure.md` - Full ACE contract, lint workflow, required versus recommended folders, and example layouts.
- `references/vault-questions.md` - How to inspect the vault and answer ACE questions from evidence.
- `references/note-processing.md` - Add, Boats, Develop, MOC, Communicate, destination rules, and note-editing guidance.
- `scripts/lint_ace_structure.py` - Validates whether a vault matches the ACE folder contract.

## First Principles

ACE is organized by intent, not by arbitrary category.

- `Atlas` is for understanding: knowledge, concepts, frameworks, people, sources, maps.
- `Calendar` is for focusing through time: daily notes, logs, meetings, reflections, time-based capture.
- `Efforts` is for acting: active projects, priorities, commitments, outcomes.
- Links provide relatedness. Do not duplicate the same note across ACE folders.
- `+` is the capture and cooling-pad space. Raw notes start there when their final intent is unclear.

When explaining decisions to the user, use this framing: "What is this note trying to help Future You do? Understand, remember a moment, or act?"

## Compact Structure Contract

Treat these top-level folders as the essential ACE contract:

```text
+/
Atlas/
Calendar/
Efforts/
```

Treat these as the recommended working subfolders for this skill:

```text
Atlas/
├── Maps/
└── Dots/
    ├── Things/
    ├── Statements/
    ├── People/
    └── Sources/

Calendar/
├── Journals/
├── Reviews/
└── Meetings/

Efforts/
├── On/
├── Ongoing/
├── Simmering/
├── Sleeping/
└── Notes/
```

Use `x/` as a support area for templates, attachments, and utilities. It is useful but not part of the core ACE headspaces.

Required versus recommended:

- `+`, `Atlas`, `Calendar`, and `Efforts` are the essential contract.
- The listed subfolders are the recommended target layout for this skill.
- Vault-specific support areas such as `x/` are optional unless the user wants the richer Ideaverse-style layout.

For the full decision table, detailed folder meanings, or lint interpretation, read `references/folder-structure.md`.

## Obsidian-Safe Operations

ACE work happens inside an Obsidian vault, so use the `obsidian` CLI for vault operations instead of raw filesystem edits. Obsidian-aware commands preserve links, metadata, and app state better than moving files with filesystem tools.

- For reading a note, use `obsidian read path="vault-relative/path.md"`.
- For note creation or edits, prefer `obsidian create`, `obsidian append`, `obsidian prepend`, `obsidian property:set`, or `obsidian eval` when needed.
- For every rename or folder move, prefer `obsidian move path="old/path.md" to="new/path.md"` with vault-relative paths.
- For folder renames, prefer creating the new folder, moving each note into it with `obsidian move`, then removing the empty old folder.
- Do not emulate a move by creating a new file and deleting the old one.
- Do not use raw `mv`, `cp`, `rm`, or `apply_patch` add/delete pairs for Obsidian note moves.
- If the Obsidian CLI is unavailable or fails, stop and report the blocker instead of falling back to raw filesystem moves.

## Mode Selection

Choose the lightest mode that fits the user's request:

1. `Lint / setup` for questions about whether the vault is ACE-compliant, what folders are missing, or how to fix the structure.
2. `Vault question` for questions about what the vault already contains, how a topic is organized, what related notes exist, or where a note should go.
3. `Note processing` for editing, moving, linking, renaming, or developing notes.

Default to checking structure first when the user asks broad ACE questions and the answer may depend on whether the vault follows the ACE contract.

## Gotchas

- Do not confuse the essential ACE contract with the richer example layout. `x/` is a support area, not one of the four ACE headspaces.
- Use the lint script for structure questions instead of re-deriving the ACE contract from memory each time.
- `Calendar` uses the `Journals/`, `Reviews/`, and `Meetings/` structure in this skill.
- `Efforts/Sleeping` is the ACE cold-storage bucket. Do not invent a parallel `Archive` folder under Efforts unless the user explicitly wants that deviation.
- This local Obsidian CLI can report success for `property:set` while making no file changes. Verify the note after every property edit.
- Do not answer broad vault questions from ACE theory alone when the vault can be inspected directly.

## Default Workflow

1. Decide which mode fits the request.
2. If the request depends on ACE structure, load `references/folder-structure.md` and validate or inspect the structure first.
3. If the request is a vault question, load `references/vault-questions.md` and answer from what is actually in the vault.
4. If the request is note processing, load `references/note-processing.md` and do the smallest correct edit or move.
5. Preserve the user's intent and existing vault style unless the user asks for a broader reorganization.
