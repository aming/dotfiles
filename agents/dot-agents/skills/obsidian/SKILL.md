---
name: obsidian
version: "1.3.1"
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
triggers:
  - "obsidian"
  - "vault"
  - "daily note"
  - "obsidian cli"
  - "note"
  - "append to"
  - "prepend to"
  - "search my vault"
  - "create a note"
  - "read note"
  - "move note"
  - "rename note"
  - "delete note"
  - "tasks in obsidian"
  - "open tasks"
  - "backlinks"
  - "orphaned notes"
  - "broken links"
  - "frontmatter"
  - "properties"
  - "sync history"
  - "obsidian bases"
  - "file history"
---

# Obsidian CLI

The official Obsidian CLI (released in v1.12, February 2026) lets you control every aspect of Obsidian from the terminal. It communicates with a running Obsidian desktop instance via IPC.

> Read `references/command-reference.md` when you need specific flags, output formats, or
> subcommands for any command group. It covers all 130+ commands with full parameter tables
> and has a table of contents at the top.

## Executable Selection

Always run the CLI as `obsidian-cli`.

Do not call `obsidian`, and do not fall back to `obsidian`. On macOS, `obsidian` can resolve to the GUI executable inside `/Applications/Obsidian.app/Contents/MacOS/`, especially on case-insensitive filesystems, and may exit with `-1` and no useful output. The real terminal CLI in the app bundle is `obsidian-cli`.

If `obsidian-cli` is unavailable, report that the Obsidian CLI is not correctly registered and use the safest direct file operation only if the task can tolerate bypassing Obsidian-aware behavior. Do not try to repair PATH, create symlinks, or launch the GUI unless the user explicitly asks.

## Prerequisites

| Requirement | Details |
|---|---|
| Obsidian Desktop | **v1.12.0+** |
| CLI enabled | Settings → Command line interface → Toggle ON |
| Obsidian running | The desktop app **must be running** for CLI to work (IPC) |

### Platform Notes

- **macOS / Linux**: Use `obsidian-cli`. If PATH registration is missing, the macOS app-bundled binary is usually `/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`.
- **Windows**: Requires an `Obsidian.com` redirector file placed alongside `Obsidian.exe`. **Must run with normal user privileges** — admin terminals produce silent failures.
  - If colon subcommands (`property:set`, `daily:append`, etc.) with parameters return exit 127, check that `Obsidian.com` exists alongside `Obsidian.exe`. If missing, you have an outdated installer — download the latest from [obsidian.md/download](https://obsidian.md/download) and reinstall.
  - **Git Bash / MSYS2 users**: use a wrapper named `obsidian-cli` that invokes `Obsidian.com`; do not use `obsidian`, because Bash can resolve it to `Obsidian.exe` (GUI).
- **Headless Linux**: Use the `.deb` package (not snap). Run under `xvfb`. Prefix commands with `DISPLAY=:5` (or your xvfb display number). Ensure `PrivateTmp=false` if running as a service.

## Syntax

All parameters use **`key=value`** syntax. Quote values containing spaces.

```bash
obsidian-cli <command> [subcommand] [key=value ...] [flags]
```

### Multi-Vault

Target a specific vault with `vault=<name>`:

```bash
obsidian-cli vault="My Vault" daily:read
obsidian-cli vault="Work Notes" search query="meeting"
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

```bash
obsidian-cli read path="folder/note.md"
obsidian-cli create path="folder/note" content="# New Note"
obsidian-cli create path="folder/note" template="meeting-notes"
obsidian-cli append path="folder/note.md" content="New paragraph"
obsidian-cli prepend path="folder/note.md" content="Top content"
obsidian-cli move path="old/note.md" to="new/note.md"
obsidian-cli rename path="folder/old-name.md" name="new-name"
obsidian-cli delete path="folder/note.md"
obsidian-cli delete path="folder/note.md" permanent
```

### Moving & Renaming Notes

Prefer first-class file subcommands over low-level API calls because they are easier to audit, align with documented CLI behavior, and preserve Obsidian's link-aware handling.

```bash
# Move and/or rename in one operation; target includes .md
obsidian-cli move path="old/folder/Old Name.md" to="new/folder/New Name.md"

# Rename within the same folder; name omits .md
obsidian-cli rename path="folder/Old Name.md" name="New Name"
```

Use `eval` for file moves or renames only when no suitable documented subcommand exists.

There is no reliable Obsidian CLI folder-rename workflow to depend on. For folder renames, default to this safer workflow instead:

1. Create the destination folder.
2. Move each note from the old folder into the new folder with `obsidian-cli move`.
3. Remove the old folder only after it is empty.

This keeps note moves link-aware without depending on unsupported folder-level rename behavior.

### Daily Notes

```bash
obsidian-cli daily                          # Open today's daily note
obsidian-cli daily:read                     # Print content of today's note
obsidian-cli daily:append content="- [ ] New task"
obsidian-cli daily:prepend content="## Morning Notes"
```

### Search

```bash
obsidian-cli search query="project alpha"
obsidian-cli search query="TODO" path="projects" limit=10
obsidian-cli search query="meeting" format=json   # Returns JSON array of file paths
obsidian-cli search query="urgent" case
```

### Properties & Tags

```bash
obsidian-cli properties path="note.md"
obsidian-cli property:set path="note.md" name="status" value="active"
obsidian-cli property:read path="note.md" name="status"
obsidian-cli property:remove path="note.md" name="draft"
obsidian-cli tags counts sort=count
obsidian-cli tag name="project/alpha"
```

Use `property:set` for scalar properties such as `status`, `summary`, and `created`. It serializes `value=` as a scalar string/date and can turn wikilink/list properties into strings, for example `in: "[[Maps]]"`. For array/list properties such as `up`, `related`, `in`, `tags`, and `aliases`, preserve the vault's existing YAML list shape unless the user explicitly wants scalar values:

```yaml
up:
  - "[[Sources]]"
created: 2020-06-01
in:
  - "[[Maps]]"
```

After every property write, verify by reading the exact note. If `property:set` prints only the outdated-installer warning or exits successfully without changing the file, report that limitation before using another approach. If `property:set` damages list-valued properties, repair them to the vault's established list format.

When the task is specifically about Obsidian properties, do a second verification pass with `obsidian-cli property:read` for each property you changed. Prefer the explicit file form the user asked for when it works in the environment:

```bash
obsidian-cli property:read file="note.md" name="status"
obsidian-cli property:read file="note.md" name="tags"
```

If the environment or docs use `path=` instead of `file=`, treat them as equivalent command shapes and use the one that actually works, but still verify the property values through `property:read` rather than only inspecting raw YAML.

### Tasks

```bash
obsidian-cli tasks                          # All tasks (done + todo) — same as tasks all in v1.12
obsidian-cli tasks all                      # All tasks (done + todo)
obsidian-cli tasks done                     # Completed only
obsidian-cli tasks daily                    # Tasks in today's daily note
obsidian-cli task path="note.md" line=12 toggle
obsidian-cli tasks | grep "\[ \]"           # Workaround: filter to incomplete only
```

### Developer & Automation

```bash
obsidian-cli eval code="app.vault.getFiles().length"
obsidian-cli dev:screenshot path="folder/screenshot.png"  # Path must be vault-relative
obsidian-cli dev:debug on                                 # Required before dev:console
obsidian-cli dev:console limit=20
obsidian-cli dev:errors
```

## No-Argument Invocation

Do not run `obsidian-cli` with no command. Always provide an explicit command such as `vault`, `read`, `search`, or `daily:read`. If you need an interactive Obsidian UI action, ask the user instead of trying to launch the GUI from this skill.

## Common Agent Patterns

### Daily Journal Automation

```bash
# Append a timestamped entry
obsidian-cli daily:append content="## $(date '+%H:%M') — Status Update
- Completed: feature branch merge
- Next: code review for PR #42
- Blocked: waiting on API credentials"
```

### Create Note from Template with Metadata

```bash
obsidian-cli create path="projects/new-feature" template="project-template"
obsidian-cli property:set path="projects/new-feature.md" name="status" value="planning"
obsidian-cli property:set path="projects/new-feature.md" name="created" value="$(date -I)"
obsidian-cli daily:append content="- Started [[projects/new-feature|New Feature]]"
```

### Vault Analytics Script

```bash
obsidian-cli files total                    # Total file count
obsidian-cli tags counts sort=count         # Most used tags
obsidian-cli tasks | grep "\[ \]"          # Incomplete tasks across vault
obsidian-cli orphans                        # Notes needing integration
obsidian-cli unresolved                     # Broken links to fix
```

### Search and Extract for AI Processing

```bash
obsidian-cli search query="meeting notes" format=json | jq '.[]'
obsidian-cli read path="meetings/standup.md" | grep "Action item"
```

### Sync Management

```bash
obsidian-cli sync:status                    # Check sync health
obsidian-cli sync:history path="important.md"  # Version history
obsidian-cli sync:restore path="important.md" version=3  # Rollback
```

### Execute Obsidian Commands

```bash
# Find a command ID, then execute it
obsidian-cli commands | grep "graph"
obsidian-cli command id="graph:open"

# Open settings, trigger a plugin action
obsidian-cli command id="app:open-settings"
obsidian-cli command id="dataview:dataview-force-refresh-views"
```

## Tips

1. **Paths are vault-relative** — use `folder/note.md`, not absolute filesystem paths.
2. **`create` paths omit `.md`** — the extension is added automatically.
3. **`move` requires full target path** including `.md` extension.
4. **Pipe-friendly** — plain text output works with `grep`, `awk`, `sed`, `jq`.
5. **JSON output** — use `format=json` on `search` for a JSON array of file paths. The `files` command does not support JSON output.
6. **Stderr noise** — GPU/Electron warnings on headless are harmless; filter with `2>/dev/null`.
7. **`daily:prepend`** inserts content after frontmatter, not at byte 0.
8. **Use first-class subcommands before `eval`** — for example, use `obsidian-cli move` or `obsidian-cli rename` for file moves/renames. Reserve `eval` for cases where no suitable documented CLI subcommand exists or direct Obsidian API access is truly needed.
9. **There is no dependable folder-rename command** — create the new folder, move each note with `obsidian-cli move`, then remove the empty source folder.
10. **`template:insert`** inserts into the currently active file in the Obsidian UI — it does not accept a `path=` parameter. If no file is open, it returns `Error: No active editor. Open a file first.` To create a file from a template via CLI, use `obsidian-cli create path="..." template="..."` instead.
11. **`property:set` stores list values as strings** — `value="tag1, tag2"` writes a literal comma-separated string, not a YAML array. For proper array fields, edit the note's frontmatter directly (e.g. via `read` → modify → `create --force`) or use `eval` to call the Obsidian API.
12. **`eval` requires single-line JavaScript** — multiline JS passed inline fails with a token error. Write the script to a temp file instead:
    ```bash
    cat > /tmp/obs.js << 'JS'
    var files = app.vault.getMarkdownFiles();
    files.length;
    JS
    obsidian-cli eval code="$(cat /tmp/obs.js)"
    ```
13. **Multi-vault targeting should use `vault=<name>`** — do not use positional vault syntax. If `vault=<name>` fails, omit the vault option and switch vaults manually in the Obsidian UI.
14. **When colon subcommands are unavailable** (e.g. Windows Git Bash without wrapper), prefer non-colon alternatives: use `properties` instead of `property:read`, and `obsidian-cli daily:path` + `append` instead of `daily:append`.

## Gotchas

- `property:set` is safe for scalar values such as `status`, `summary`, and `created`, but it can serialize list-shaped properties as plain strings. Treat `tags`, `aliases`, `up`, `in`, and similar multi-value properties as YAML you must preserve.
- When the user asks to add or fix Obsidian properties, remember that those properties live in YAML frontmatter. The real success condition is not "a property command ran"; it is "the note now has valid frontmatter in the expected shape."
- After any property write, read the exact note back and verify both the frontmatter shape and the body content. Do not assume a success exit code means the note changed correctly.
- For property tasks, do not stop after `obsidian-cli read`. Also verify each changed property with `obsidian-cli property:read name="..." file="..."` or the working `path=` form in that environment. The skill should prove the properties are readable through the dedicated property command.
- If the note already has frontmatter, preserve unrelated keys and keep the body intact.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Empty output / hangs | Obsidian not running, or admin terminal (Windows) | Start Obsidian; use normal-privilege terminal |
| `obsidian-cli` command not found | CLI not registered in PATH | Re-enable CLI in Settings; restart terminal; on macOS, use `/Applications/Obsidian.app/Contents/MacOS/obsidian-cli` if present |
| Unicode errors | Fixed in v1.12.2+ | Update Obsidian |
| Wrong vault targeted | Multi-vault ambiguity | Pass vault name as first arg |
| IPC socket not found (Linux) | `PrivateTmp=true` in systemd | Set `PrivateTmp=false` |
| Snap confinement issues | Snap restricts IPC | Use `.deb` package instead |
| Multi-vault targeting fails | Vault name matching issue | Prefer `vault=<name>`; otherwise omit vault name and target the active vault |
| `property:set` list value is a string | CLI stores value as-is | Edit frontmatter directly or use `eval` |
| Colon+params exit 127 (missing `.com`) | Outdated installer — `Obsidian.com` absent | Reinstall from [obsidian.md/download](https://obsidian.md/download) |
| `obsidian` exits `-1` with no output | `obsidian` resolved to GUI executable instead of CLI | Do not use `obsidian`; use `obsidian-cli` only |
| Colon+params exit 127 (Git Bash / MSYS2) | Shell wrapper invokes `.exe` instead of `.com` | Create a wrapper named `obsidian-cli` that calls `/c/path/to/Obsidian.com "$@"` |
