---
name: obsidian
description: >
  Use this skill when the user wants direct operations on an Obsidian vault: read
  or edit notes and daily notes, search vault contents, count or list notes,
  manage tasks, move or rename files, find orphaned notes or broken links,
  inspect frontmatter/properties, manage sync or file history, query Bases,
  manage bookmarks, script the CLI, or run JavaScript against the Obsidian API.
  Trigger when the request implies "go into my vault and do X"; the user wants
  action on vault data, not an explanation. Skip pure conceptual or GUI-help
  questions such as settings navigation, theme/plugin installation, sync
  troubleshooting, Dataview syntax, keyboard shortcuts, or parsing vault files
  with unrelated external scripts.
metadata:
  version: "1.3.1"
  triggers: ["obsidian", "vault", "daily note", "obsidian cli", "note", "append to", "prepend to", "search my vault", "create a note", "read note", "move note", "rename note", "delete note", "tasks in obsidian", "open tasks", "backlinks", "orphaned notes", "broken links", "frontmatter", "properties", "sync history", "obsidian bases", "file history"]
---

# Obsidian CLI

The official Obsidian CLI (released in v1.12, February 2026) lets you control every aspect of Obsidian from the terminal. It communicates with a running Obsidian desktop instance via IPC.

> Read `references/command-reference.md` when you need specific flags, output formats, or
> subcommands for any command group. It covers all 130+ commands with full parameter tables
> and has a table of contents at the top.

## Executable Selection

Use `obsidian` by default: the official CLI registers that command on macOS and Linux. Check `obsidian version` and `obsidian help` before vault operations. If a deployment actually provides `obsidian-cli` (for example, a local wrapper or bundled variant), verify it with `version` and `help`, then substitute that executable consistently in the examples. Absence of `obsidian-cli` alone is not a registration failure. If neither verified command works, report the exact failure; do not repair PATH or create symlinks during a note task.

Verified against the [official CLI command reference](https://help.obsidian.md/cli) on 2026-10-27 (Obsidian 1.12+). Recheck local `help <command>` when behavior differs.

## Prerequisites

| Requirement | Details |
|---|---|
| Obsidian Desktop | App **v1.12.0+** with installer **v1.12.7+** |
| CLI enabled | Settings → Command line interface → Toggle ON |
| Obsidian running | The desktop app is required for IPC; a CLI command may launch it if stopped |

### Platform Notes

- **macOS / Linux**: Register `obsidian` through Settings → General → Command line interface; follow the executable checks above. A verified local wrapper may have a different name.
- **Windows**: Requires an `Obsidian.com` redirector file placed alongside `Obsidian.exe`. **Must run with normal user privileges** — admin terminals produce silent failures.
  - If colon subcommands (`property:set`, `daily:append`, etc.) with parameters return exit 127, check that `Obsidian.com` exists alongside `Obsidian.exe`. If missing, you have an outdated installer — download the latest from [obsidian.md/download](https://obsidian.md/download) and reinstall.
  - **Git Bash / MSYS2 users**: verify which executable resolves; a local wrapper invoking `Obsidian.com` can avoid resolving to the GUI `Obsidian.exe`.
- **Headless Linux**: Use the `.deb` package (not snap). Run under `xvfb`. Prefix commands with `DISPLAY=:5` (or your xvfb display number). Ensure `PrivateTmp=false` if running as a service.

## Syntax

All parameters use **`key=value`** syntax. Quote values containing spaces.

```bash
obsidian <command> [subcommand] [key=value ...] [flags]
```

### File Targets

`file=<name>` uses Obsidian wikilink-style name resolution; it can omit the folder and extension and may be ambiguous when names repeat. `path=<path>` requires the exact vault-relative path, including the extension for existing notes. Use `path=` for precise edits and verification; the two forms are equivalent only when name resolution selects the same file.

### Multi-Vault

Target a specific vault with `vault=<name>`:

```bash
obsidian vault="My Vault" daily:read
obsidian vault="Work Notes" search query="meeting"
```

If omitted, the CLI targets the most recently active vault.

## Command Overview

The CLI provides **130+ commands** across these groups:

| Group | Key Commands | Purpose |
|---|---|---|
| **files** | `read`, `create`, `append`, `prepend`, `move`, `rename`, `delete`, `files`, `folders`, `folder`, `file`, `open`, `random` | Note CRUD, opening files, and file discovery |
| **daily** | `daily`, `daily:read`, `daily:append`, `daily:prepend`, `daily:path` | Daily note operations |
| **search** | `search`, `search:context`, `search:open` | Full-text search; `search:context` returns matching lines |
| **properties** | `properties`, `property:read`, `property:set`, `property:remove`, `aliases` | Frontmatter/metadata management |
| **tags** | `tags`, `tag` | Tag listing, counts, and filtering |
| **tasks** | `tasks`, `task` | Task querying, filtering, and toggling |
| **links** | `backlinks`, `links`, `unresolved`, `orphans`, `deadends` | Graph and link analysis |
| **bookmarks** | `bookmarks`, `bookmark` | List and add bookmarks |
| **templates** | `templates`, `template:read`, `template:insert` | Template listing, rendering, insertion |
| **plugins** | `plugins`, `plugins:enabled`, `plugin`, `plugin:enable`, `plugin:disable`, `plugin:install`, `plugin:uninstall`, `plugin:reload`, `plugins:restrict` | Plugin management |
| **publish** | `publish:site`, `publish:list`, `publish:status`, `publish:add`, `publish:remove`, `publish:open` | Obsidian Publish operations |
| **sync** | `sync`, `sync:status`, `sync:history`, `sync:read`, `sync:restore`, `sync:open`, `sync:deleted` | Obsidian Sync operations |
| **themes** | `themes`, `theme`, `theme:set`, `theme:install`, `theme:uninstall` | Theme management |
| **snippets** | `snippets`, `snippets:enabled`, `snippet:enable`, `snippet:disable` | CSS snippet management |
| **commands** | `commands`, `command`, `hotkeys`, `hotkey` | Execute Obsidian commands by ID; inspect hotkeys |
| **bases** | `bases`, `base:query`, `base:views`, `base:create` | Obsidian Bases (v1.12+ database feature) |
| **history** | `history`, `history:list`, `history:read`, `history:restore`, `history:open` | File version recovery (File Recovery plugin) |
| **workspace** | `workspace`, `workspaces`, `workspace:save`, `workspace:load`, `workspace:delete`, `tabs`, `tab:open`, `recents` | Workspace layout and tab management |
| **diff** | `diff` | Compare local vs sync file versions |
| **dev** | `eval`, `dev:screenshot`, `dev:debug`, `dev:console`, `dev:errors`, `dev:css`, `dev:dom`, `devtools` | Developer/debugging tools |
| **vault** | `vault`, `vaults`, `vault:open`, `version`, `help`, `reload`, `restart` | Vault info and app control |
| **other** | `outline`, `wordcount`, `unique`, `web` | Utility commands |

## Quick Reference — Most Common Commands

### Reading & Writing Notes

Before moves or renames, check **Automatically update internal links** in vault settings; automatic link preservation depends on it. If disabled, explicitly update and verify affected links.

```bash
obsidian read path="folder/note.md"
obsidian create path="folder/note" content="# New Note"
obsidian create path="folder/note" template="meeting-notes"
obsidian append path="folder/note.md" content="New paragraph"
obsidian prepend path="folder/note.md" content="Top content"
obsidian move path="old/note.md" to="new/note.md"
obsidian rename path="folder/old-name.md" name="new-name"
obsidian delete path="folder/note.md"
obsidian delete path="folder/note.md" permanent
```

### Moving & Renaming Notes

Prefer first-class file subcommands over low-level API calls because they are easier to audit and align with documented CLI behavior.

Automatic internal-link updates require the vault setting **Automatically update internal links** to be enabled. Check that setting before moving or renaming notes, including per-note moves during folder renames; if disabled, plan explicit link updates and verification rather than promising automatic preservation. Verify the destination and affected links after each operation.

```bash
# Move and/or rename in one operation; target includes .md
obsidian move path="old/folder/Old Name.md" to="new/folder/New Name.md"

# Rename within the same folder; name omits .md
obsidian rename path="folder/Old Name.md" name="New Name"
```

Use `eval` for file moves or renames only when no suitable documented subcommand exists.

There is no reliable Obsidian CLI folder-rename workflow to depend on. For folder renames, default to this safer workflow instead:

1. Create the destination folder.
2. Move each note from the old folder into the new folder with `obsidian move`.
3. Remove the old folder only after it is empty.

For this workflow, automatic link updates require the vault setting above; verify affected links after the moves.

### Daily Notes

```bash
obsidian daily                          # Open today's daily note
obsidian daily:read                     # Print content of today's note
obsidian daily:append content="- [ ] New task"
obsidian daily:prepend content="## Morning Notes"
```

### Search

```bash
obsidian search query="project alpha"
obsidian search query="TODO" path="projects" limit=10
obsidian search query="meeting" format=json   # Returns JSON array of file paths
obsidian search query="urgent" case
```

### Properties & Tags

```bash
obsidian properties path="note.md"
obsidian property:set path="note.md" name="status" value="active"
obsidian property:read path="note.md" name="status"
obsidian property:remove path="note.md" name="draft"
obsidian tags counts sort=count
obsidian tag name="project/alpha"
```

Use typed `property:set` writes: `type=text|list|number|checkbox|date|datetime`. For list properties, specify `type=list` and preserve the existing YAML list shape. For example:

```bash
obsidian property:set path="note.md" name="status" value="active" type=text
obsidian property:set path="note.md" name="created" value="2026-05-01" type=date
obsidian property:set path="note.md" name="tags" value="project/atlas,draft" type=list
obsidian property:set path="note.md" name="in" value="[[Maps]]" type=list
obsidian property:read path="note.md" name="tags"
```

Verify both the exact note and every changed property using `property:read path=... name=...`. Confirm list items, unrelated frontmatter, and body content remain correct. If a local version ignores typed writes, report the observed limitation and use the Obsidian API only when needed, then verify again.

### Tasks

```bash
obsidian tasks                          # All tasks (done + todo)
obsidian tasks todo                     # Incomplete tasks only
obsidian tasks done                     # Completed only
obsidian tasks daily                    # Tasks in today's daily note
obsidian task path="note.md" line=12 toggle
obsidian tasks todo                     # Incomplete tasks only
```

### Developer & Automation

```bash
obsidian eval code="app.vault.getFiles().length"
obsidian dev:screenshot path="folder/screenshot.png"  # Path must be vault-relative
obsidian dev:debug on                                 # Required before dev:console
obsidian dev:console limit=20
obsidian dev:errors
```

## No-Argument Invocation

Do not run `obsidian` with no command. Always provide an explicit command such as `vault`, `read`, `search`, or `daily:read`. If you need an interactive Obsidian UI action, ask the user instead of trying to launch the GUI from this skill.

## Common Agent Patterns

### Daily Journal Automation

```bash
# Append a timestamped entry
obsidian daily:append content="## $(date '+%H:%M') — Status Update
- Completed: feature branch merge
- Next: code review for PR #42
- Blocked: waiting on API credentials"
```

### Create Note from Template with Metadata

```bash
obsidian create path="projects/new-feature" template="project-template"
obsidian property:set path="projects/new-feature.md" name="status" value="planning"
obsidian property:set path="projects/new-feature.md" name="created" value="$(date -I)"
obsidian daily:append content="- Started [[projects/new-feature|New Feature]]"
```

### Vault Analytics Script

```bash
obsidian files total                    # Total file count
obsidian tags counts sort=count         # Most used tags
obsidian tasks todo                     # Incomplete tasks across vault
obsidian orphans                        # Notes needing integration
obsidian unresolved                     # Broken links to fix
```

### Search and Extract for AI Processing

```bash
obsidian search query="meeting notes" format=json | jq '.[]'
obsidian read path="meetings/standup.md" | grep "Action item"
```

### Sync Management

```bash
obsidian sync:status                    # Check sync health
obsidian sync:history path="important.md"  # Version history
obsidian sync:restore path="important.md" version=3  # Rollback
```

### Execute Obsidian Commands

```bash
# Find a command ID, then execute it
obsidian commands | grep "graph"
obsidian command id="graph:open"

# Open settings, trigger a plugin action
obsidian command id="app:open-settings"
obsidian command id="dataview:dataview-force-refresh-views"
```

## Tips

1. **Paths are vault-relative** — use `folder/note.md`, not absolute filesystem paths.
2. **`create` paths omit `.md`** — the extension is added automatically.
3. **`move to=` accepts a folder or path** — use a full destination path including `.md` when precision matters.
4. **Pipe-friendly** — plain text output works with `grep`, `awk`, `sed`, `jq`.
5. **JSON output** — use `format=json` on `search` for a JSON array of file paths. The `files` command does not support JSON output.
6. **Stderr noise** — GPU/Electron warnings on headless are harmless; filter with `2>/dev/null`.
7. **`daily:prepend`** inserts content after frontmatter, not at byte 0.
8. **Use first-class subcommands before `eval`** — for example, use `obsidian move` or `obsidian rename` for file moves/renames. Reserve `eval` for cases where no suitable documented CLI subcommand exists or direct Obsidian API access is truly needed.
9. **Folder rename workflow** — create the new folder, move each note with `obsidian move`, then remove the empty source folder. Automatic link updates require **Automatically update internal links** to be enabled; otherwise update and verify links explicitly.
10. **`template:insert`** inserts into the currently active file in the Obsidian UI — it does not accept a `path=` parameter. If no file is open, it returns `Error: No active editor. Open a file first.` To create a file from a template via CLI, use `obsidian create path="..." template="..."` instead.
11. **Use typed properties** — use `property:set type=list` for lists and `type=date` for dates; verify both note content and dedicated property reads. When replacing a full note, the documented create flag is `overwrite`, for example `obsidian create path="note.md" content="..." overwrite`; read and preserve the complete body and unrelated frontmatter first.
12. **If inline multiline JavaScript fails locally**, pass a genuinely single-line program. For a short script, write it on one line:
    ```bash
    obsidian eval code="var files = app.vault.getMarkdownFiles(); files.length;"
    ```
    For complex scripts, use a JavaScript-aware bundler/minifier to emit one line before passing it; do not pass `$(cat multiline.js)` or blindly strip newlines (which can break comments and string literals).
13. **Multi-vault targeting should use `vault=<name>`** — do not use positional vault syntax. If `vault=<name>` fails, omit the vault option and switch vaults manually in the Obsidian UI.
14. **When colon subcommands are unavailable** (e.g. Windows Git Bash without wrapper), prefer non-colon alternatives: use `properties` instead of `property:read`, and `obsidian daily:path` + `append` instead of `daily:append`.

## Gotchas

- `The CLI is unable to find Obsidian` does not prove the app is closed. On macOS, a Codex sandbox can block IPC to a running Obsidian app. Check the main process if possible (process inspection may also be restricted), then retry one needed read-only CLI command such as `obsidian version` outside the sandbox with scoped approval. If it succeeds, use narrowly scoped access for the task's CLI operations, respecting write authorization; never approve a broad CLI prefix because it includes mutating commands. If it still fails, check that the CLI is enabled and a vault is open. Use minimal direct file operations only when safe, and read back affected notes.
- Use `property:set type=list` for `tags`, `aliases`, `up`, `in`, and similar list properties; verify the resulting YAML list and dedicated property reads.
- When the user asks to add or fix Obsidian properties, remember that those properties live in YAML frontmatter. The real success condition is not "a property command ran"; it is "the note now has valid frontmatter in the expected shape."
- After any property write, read the exact note back and verify both the frontmatter shape and the body content. Do not assume a success exit code means the note changed correctly.
- For property tasks, do not stop after `obsidian read`. Also verify each changed property with `obsidian property:read name="..." file="..."` or `path=` with the exact vault-relative path (preferred for precise targeting). The skill should prove the properties are readable through the dedicated property command.
- If the note already has frontmatter, preserve unrelated keys and keep the body intact.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Empty output / hangs | Obsidian not running, or admin terminal (Windows) | Start Obsidian; use normal-privilege terminal |
| `The CLI is unable to find Obsidian` | App not running, CLI disabled, or sandboxed IPC | See **Gotchas** before concluding the app is closed |
| `obsidian` command not found | Standard command unavailable | Check registration in Settings → General → Command line interface; verify any documented local variant with `version` and `help` |
| Unicode errors | Fixed in v1.12.2+ | Update Obsidian |
| Wrong vault targeted | Multi-vault ambiguity | Pass `vault=<name>` before the command |
| IPC socket not found (Linux) | `PrivateTmp=true` in systemd | Set `PrivateTmp=false` |
| Snap confinement issues | Snap restricts IPC | Use `.deb` package instead |
| Multi-vault targeting fails | Vault name matching issue | Prefer `vault=<name>`; otherwise omit vault name and target the active vault |
| `property:set` list value is a string | Missing type or local version behavior | Use `type=list`; verify exact content and property reads |
| Colon+params exit 127 (missing `.com`) | Outdated installer — `Obsidian.com` absent | Reinstall from [obsidian.md/download](https://obsidian.md/download) |
| `obsidian` exits `-1` with no output | `obsidian` resolved to GUI executable instead of CLI | Use the CLI executable (on Windows `Obsidian.com`, not the GUI `Obsidian.exe`); verify with `obsidian version` |
| Colon+params exit 127 (Git Bash / MSYS2) | Shell wrapper invokes `.exe` instead of `.com` | Create a wrapper named `obsidian` that calls `/c/path/to/Obsidian.com "$@"` |

## Evaluation Fixtures

For repeatable evaluations without a personal vault, read `evals/SETUP.md` and initialize a fresh disposable vault with `python3 evals/init_vault.py --destination /tmp/obsidian-eval-vault`. The initializer refuses an existing destination; CLI evaluations require opening this disposable vault in Obsidian first.
