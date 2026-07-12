# ACE Folder Structure

Read this file when you need to:

- Decide whether a vault matches ACE structurally.
- Set up an ACE vault from scratch.
- Explain which ACE folders are essential vs optional.
- Run the ACE lint/check command.

## Core Idea

ACE is primarily a headspace model:

- `Atlas` = understand
- `Calendar` = focus through time
- `Efforts` = act

The folder structure should make that model easy to apply, but it should not be so strict that it only fits one starter vault.

## Portable ACE Contract

These are the essential folders this skill should assume for a general ACE vault:

```text
+/
Atlas/
Calendar/
Efforts/
```

### Required Substructure For This Skill

This skill's routing rules rely on these subfolders being present or being the intended target structure:

```text
Atlas/
├── Maps/
└── Dots/
    ├── Things/
    ├── Statements/
    ├── People/
    └── Sources/

Efforts/
├── On/
├── Ongoing/
├── Simmering/
├── Sleeping/
└── Notes/
```

Reasoning:

- `Atlas/Maps` vs `Atlas/Dots/*` lets the skill distinguish navigation pages from individual knowledge notes.
- `Things`, `Statements`, `People`, and `Sources` are the main routing buckets the skill uses for Atlas notes.
- The four Efforts intensity buckets are how the skill distinguishes current work, ongoing responsibilities, future possibilities, and cold storage.

## Recommended Calendar Structure

Calendar is organized by note type with year-based folders for scalability:

```text
Calendar/
├── Journals/              ← Daily notes, monthly notes, dated entries
│   ├── 2025/
│   │   ├── 2025-03-15.md
│   │   └── 2025-03.md
│   └── 2026/
│       └── 2026-04-30.md
├── Reviews/               ← Yearly reviews, periodic summaries
│   └── 2025.md
└── Meetings/              ← Meeting notes with titles
    └── 2025-03-15-Team Sync.md
```

### Folder Purposes

| Folder | Purpose |
|--------|---------|
| `Calendar/Journals/` | Year-based folders for daily notes, monthly summaries, and dated journal entries. Format: `YYYY/YYYY-MM-DD.md` or `YYYY/YYYY-MM.md` |
| `Calendar/Reviews/` | Periodic reviews and summaries. Format: `YYYY.md` for yearly reviews |
| `Calendar/Meetings/` | Meeting notes with descriptive titles. Format: `YYYY-MM-DD-<title>.md` |

### What Goes in Each Calendar Folder

**Journals/**:
- Daily Notes — journal entries, quick captures, daily reflections
- Monthly Notes — month-end reviews, summaries (e.g., `2025-03.md`)
- Dated Entries — any time-stamped personal notes

**Reviews/**:
- Yearly Reviews — annual reflections, goal reviews (e.g., `2025.md`)
- Quarterly Reviews — if you track quarters (e.g., `2025-Q1.md`)

**Meetings/**:
- Meeting Notes — conversations, 1:1s, team syncs
- Event Notes — conferences, workshops with specific dates

### Practical Tips

- Use year-based folders (`Journals/2025/`) to keep the view uncluttered as years accumulate
- Journal entries use `YYYY-MM-DD.md` format for automatic sorting
- Meeting notes include a descriptive title: `YYYY-MM-DD-<meeting name>.md`
- Link outward. Calendar notes can link to Atlas concepts and Efforts projects.

## Optional Support Areas

These are useful support areas, but they are not part of the minimal ACE contract:

```text
x/
x/Templates/
x/Images/
```

Use them for:

- templates
- images and attachments
- readmes / meta notes
- utility notes
- archived support material

Use `x/Templates/template-base.md` as the canonical base template for new notes. Point Note Composer at that file so new derived notes use the same ACE base structure. Avoid keeping multiple legacy base-template filenames around because that makes the vault's default note scaffolding ambiguous.

Do not treat missing `x/` as an ACE failure in the portable ACE profile.

## Reference Layout From This Vault

This vault's intended structure uses the Journals/Reviews/Meetings calendar layout plus a `x/` support area:

```text
+/
Atlas/
├── Maps/
└── Dots/
    ├── People/
    ├── Sources/
    ├── Statements/
    └── Things/
Calendar/
├── Journals/
│   └── 2025/
├── Reviews/
└── Meetings/
Efforts/
├── Notes/
├── On/
├── Ongoing/
├── Simmering/
└── Sleeping/
x/
├── Images/
└── Templates/
```

Use this as the example layout when teaching or scaffolding ACE unless the user wants something leaner.

## Lint Script

Available script:

- `scripts/lint_ace_structure.py` - Validates an ACE vault against either the portable `essential` profile or the richer `ideaverse` profile, including whether Obsidian config sends raw captures to `+`, creates daily notes in the current `Calendar/Journals/<Year>/` folder, and points Templates at `x/Templates`.

Run it from the ACE skill root:

```bash
python3 scripts/lint_ace_structure.py --vault "/path/to/vault" --format text
```

Useful variants:

```bash
python3 scripts/lint_ace_structure.py --vault "/path/to/vault" --profile essential --format json
python3 scripts/lint_ace_structure.py --vault "/path/to/vault" --profile ideaverse --format text
```

### Profile Meaning

- `essential`: checks the portable ACE contract and warns on richer-structure drift.
- `ideaverse`: checks the richer example layout from this vault more strictly.

### How To Interpret Results

- `error` = a required folder for the chosen profile is missing.
- `warning` = the vault is valid enough to use, but a convention is drifting or a recommended folder is missing.
- `info` = confirmation of an optional support area or a useful note about the structure.

The lint also checks Obsidian config files so the vault can verify that new raw captures default to `+`, daily notes land in the current `Calendar/Journals/<Year>/` folder, templates point at `x/Templates`, Note Composer uses `x/Templates/template-base.md`, the canonical base template exists at that path, and `.keepme` placeholders stay hidden from the file list. Treat config findings as setup drift, not as a structural ACE failure.

Empty required ACE folders should contain a `.keepme` placeholder so git can keep them checked in. Hide those placeholders from the file list with `userIgnoreFilters` in `.obsidian/app.json`.

### What To Do When The Lint Fails

1. Fix missing required ACE folders first.
2. Verify Calendar uses the Journals/Reviews/Meetings structure.
3. Add optional support folders only if they solve a real problem.
4. Re-run the lint after structural changes.
