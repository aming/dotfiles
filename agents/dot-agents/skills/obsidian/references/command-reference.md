# Obsidian CLI — Full Command Reference

Complete reference for all official Obsidian CLI commands (v1.12+).

**Syntax**: `obsidian-cli <command> [subcommand] [key=value ...] [flags]`

Use `vault=<name>` when you need to target a specific vault.

All parameters use `key=value` syntax. Quote values containing spaces: `content="hello world"`.

---

## Table of Contents

1. [Files](#files)
2. [Daily Notes](#daily-notes)
3. [Search](#search)
4. [Properties](#properties)
5. [Tags](#tags)
6. [Tasks](#tasks)
7. [Links](#links)
8. [Bookmarks](#bookmarks)
9. [Templates](#templates)
10. [Plugins](#plugins)
11. [Publish](#publish)
12. [Sync](#sync)
13. [Themes](#themes)
14. [CSS Snippets](#css-snippets)
15. [Commands & Hotkeys](#commands--hotkeys)
16. [Obsidian Bases](#obsidian-bases)
17. [History](#history)
18. [Workspace & Tabs](#workspace--tabs)
19. [Diff](#diff)
20. [Developer](#developer)
21. [Unique Notes](#unique-notes)
22. [Web Viewer](#web-viewer)
23. [Vault & System](#vault--system)

---

## Files

File operations: read, write, create, move, delete, list.

### Reading Notes

```bash
obsidian-cli read path="folder/note.md"
```

Prints raw markdown content of a note to stdout. Path is vault-relative.

### Creating Notes

```bash
obsidian-cli create path="folder/note" content="# Title\n\nBody text"
obsidian-cli create path="folder/note" template="template-name"
```

- Path should **not** include `.md` — it is appended automatically.
- Use `template=` to create from a template file.
- Use `content=` to set initial content directly.

### Appending & Prepending

```bash
obsidian-cli append path="folder/note.md" content="Appended text"
obsidian-cli prepend path="folder/note.md" content="Prepended text"
```

- `append` adds content at the end of the file.
- `prepend` adds content after the frontmatter (not at byte 0).

### Moving & Renaming

```bash
obsidian-cli move path="old/path/note.md" to="new/path/note.md"
```

- `to=` is the full vault-relative target path including the `.md` extension.
- Can be used to move, rename, or both in a single command.

There is no documented folder-rename command. When the user wants to rename a folder, use this workflow instead:

1. Create the destination folder.
2. Move each note from the old folder into the new folder with `obsidian-cli move`.
3. Remove the old folder after it is empty.

This preserves Obsidian's link-aware note moves without relying on unsupported folder rename behavior.

### Deleting

```bash
obsidian-cli delete path="folder/note.md"           # Moves to trash
obsidian-cli delete path="folder/note.md" permanent  # Permanent deletion
```

### File Discovery

```bash
obsidian-cli files                       # List all files in vault
obsidian-cli files ext=md                # Filter by extension
obsidian-cli files folder="subfolder"    # Files in specific folder
obsidian-cli files total                 # Just the file count
obsidian-cli folders                     # List all folders
obsidian-cli folders folder="subfolder"  # Folders under a parent folder
obsidian-cli file path="folder/note.md"  # File info (size, created, modified dates)
obsidian-cli folder path="folder"        # Folder info
obsidian-cli folder path="folder" info=files    # File count/info only
obsidian-cli folder path="folder" info=folders  # Child folder count/info only
obsidian-cli folder path="folder" info=size     # Folder size only
obsidian-cli open path="folder/note.md"  # Open a file in Obsidian
obsidian-cli open file="Note Name" newtab # Open by Obsidian link resolution in a new tab
```

### Random Notes

```bash
obsidian-cli random           # Open a random note in Obsidian
obsidian-cli random:read      # Print content of a random note to stdout
```

### Renaming

```bash
obsidian-cli rename path="folder/note.md" name="new-name"
```

- `name=` is the new filename only (no path, no `.md` extension).
- Use `move` when you also want to change the folder.

---

## Daily Notes

Operations on the daily note (requires Daily Notes core plugin enabled).

```bash
obsidian-cli daily                           # Open today's daily note in Obsidian
obsidian-cli daily:read                      # Print today's daily note content to stdout
obsidian-cli daily:append content="text"     # Append content to today's note
obsidian-cli daily:prepend content="text"    # Prepend content (after frontmatter)
obsidian-cli daily:path                      # Print vault-relative path of today's note
```

**Notes:**
- `daily:prepend` inserts content after the frontmatter block, not at the very beginning.
- If today's note doesn't exist, `daily` will create it (using the configured template if set).
- Daily note format/folder are configured in Obsidian's Daily Notes plugin settings.

---

## Search

Full-text search across the vault.

```bash
obsidian-cli search query="search text"
obsidian-cli search query="text" path="folder"         # Scope to folder
obsidian-cli search query="text" limit=10               # Limit results
obsidian-cli search query="text" format=json            # JSON output (array of file paths)
obsidian-cli search query="text" matches                # Accepted but returns file paths only
obsidian-cli search query="text" case                   # Case-sensitive search
```

**Parameters:**
- `query=` — Search term (required)
- `path=` — Restrict search to a folder
- `limit=` — Maximum number of results
- `format=json` — Returns a JSON array of matching file paths: `["folder/note.md", ...]`
- `matches` — Flag accepted by the CLI but does not return match context/snippets in v1.12
- `case` — Enable case-sensitive matching

### Search with Context

```bash
obsidian-cli search:context query="search text"
obsidian-cli search:context query="text" path="folder" limit=10
obsidian-cli search:context query="text" case
obsidian-cli search:context query="text" format=json
```

Returns matching lines with surrounding context (not just file paths). Useful when you need to see the actual content that matched rather than just file paths.

### Open Search View

```bash
obsidian-cli search:open query="search text"
```

Opens the Obsidian search panel in the UI with the given query.

---

## Properties

Manage frontmatter (YAML metadata) on notes.

### Read All Properties

```bash
obsidian-cli properties path="note.md"
```

### Read Single Property

```bash
obsidian-cli property:read path="note.md" name="status"
```

### Set Property

```bash
obsidian-cli property:set path="note.md" name="status" value="active"
obsidian-cli property:set path="note.md" name="tags" value="[project, alpha]"
obsidian-cli property:set path="note.md" name="date" value="2026-02-27"
```

> **Note:** `property:set` is best for scalar properties. It stores `value=` as a scalar and can turn
> wikilink/list properties into strings. Passing `value="[project, alpha]"` writes the literal string
> `[project, alpha]`, not a YAML array. For true array-typed properties (e.g. `up`, `related`, `in`,
> `tags`, `aliases`), preserve the vault's existing YAML list shape or use `eval` with the Obsidian API.
> Always verify property writes by reading the exact note afterward; some outdated installers print a
> warning or exit successfully without applying the change.

### Remove Property

```bash
obsidian-cli property:remove path="note.md" name="draft"
```

### Aliases

```bash
obsidian-cli aliases path="note.md"
```

Lists all aliases defined in the note's frontmatter.

---

## Tags

Tag discovery and filtering.

```bash
obsidian-cli tags                          # List all tags in the vault
obsidian-cli tags counts                   # Tags with usage counts
obsidian-cli tags counts sort=count        # Sorted by frequency (most used first)
obsidian-cli tags path="note.md"           # Tags in a specific file
obsidian-cli tag name="project/alpha"      # List notes with a specific tag
```

**Notes:**
- Nested tags are supported (e.g., `project/alpha`).
- Tags from both frontmatter and inline `#tag` syntax are included.

---

## Tasks

Query and manage checkbox tasks across the vault.

### Querying Tasks

```bash
obsidian-cli tasks                         # All tasks (same as tasks all in v1.12)
obsidian-cli tasks all                     # All tasks (complete + incomplete)
obsidian-cli tasks done                    # Only completed tasks
obsidian-cli tasks path="note.md"          # Tasks in a specific file
obsidian-cli tasks daily                   # Tasks in today's daily note
```

> **Note:** In v1.12, `tasks` with no arguments returns all tasks (complete + incomplete), identical to `tasks all`. Filtering to incomplete-only is not currently supported without post-processing (e.g. pipe to `grep "\[ \]"`).

### Toggling Task Status

```bash
obsidian-cli task path="note.md" line=12 toggle
```

Toggles the checkbox on the specified line number between `- [ ]` and `- [x]`.

---

## Links

Graph analysis and link management.

```bash
obsidian-cli backlinks path="note.md"         # Notes linking TO this note
obsidian-cli backlinks path="note.md" counts  # With link counts per file
obsidian-cli links path="note.md"             # Outgoing links FROM this note
obsidian-cli unresolved                        # All unresolved [[wikilinks]]
obsidian-cli orphans                           # Notes with no incoming or outgoing links
obsidian-cli deadends                          # Notes with no outgoing links
```

---

## Bookmarks

Manage Obsidian bookmarks (requires Bookmarks core plugin).

```bash
obsidian-cli bookmarks                                      # List all bookmarks
obsidian-cli bookmark file="folder/note.md"                 # Bookmark a note
obsidian-cli bookmark file="folder/note.md" subpath="#Heading"  # Bookmark a heading
obsidian-cli bookmark folder="projects"                     # Bookmark a folder
obsidian-cli bookmark search="query text" title="My Search" # Bookmark a search
obsidian-cli bookmark url="https://example.com" title="Link" # Bookmark a URL
```

---

## Templates

Work with note templates (requires Templates or Templater plugin).

```bash
obsidian-cli templates                                      # List available templates
obsidian-cli template:read name="weekly-review"             # Read template content
obsidian-cli template:read name="weekly-review" resolve title="My Note"  # Render with variables
obsidian-cli template:insert name="weekly-review"           # Insert template into the active Obsidian UI file
```

**Parameters:**
- `name=` — Template name (without path prefix or extension)
- `resolve` — Process template variables (`{{date}}`, `{{title}}`, etc.)
- Title and other variables can be passed as `key=value` for template rendering.

> **Note:** `template:insert` inserts into whichever file is currently active in the Obsidian UI — it does not accept a `path=` parameter. If no file is open, it returns `Error: No active editor. Open a file first.` To create a new file from a template, use `obsidian-cli create path="..." template="..."` instead.

---

## Plugins

Manage community and core plugins.

```bash
obsidian-cli plugins                         # List all plugins (core + community)
obsidian-cli plugins:enabled                 # Only enabled plugins
obsidian-cli plugins versions                # Plugins with version numbers (community only)
obsidian-cli plugins:restrict                # Show restricted mode status
obsidian-cli plugins:restrict on             # Enable restricted mode (disables community plugins)
obsidian-cli plugins:restrict off            # Disable restricted mode
obsidian-cli plugin id="dataview"            # Get info about a specific plugin
obsidian-cli plugin:enable id="canvas"       # Enable a plugin
obsidian-cli plugin:disable id="canvas"      # Disable a plugin
obsidian-cli plugin:install id="dataview"    # Install from community plugins
obsidian-cli plugin:uninstall id="dataview"  # Uninstall a community plugin
obsidian-cli plugin:reload id="my-plugin"    # Reload a plugin (useful for dev)
```

> **Note:** `plugins versions` only shows version numbers for community plugins. Core (built-in) plugins share Obsidian's version and display blank version fields.

---

## Publish

Manage Obsidian Publish state (requires an Obsidian Publish site).

```bash
obsidian-cli publish:site                         # Show publish site slug and URL
obsidian-cli publish:list                         # List published files
obsidian-cli publish:list total                   # Count published files
obsidian-cli publish:status                       # List pending publish changes
obsidian-cli publish:status new                   # Show only new files
obsidian-cli publish:status changed               # Show only changed files
obsidian-cli publish:status deleted               # Show only deleted files
obsidian-cli publish:add path="folder/note.md"    # Publish a file
obsidian-cli publish:add changed                  # Publish all changed files
obsidian-cli publish:remove path="folder/note.md" # Unpublish a file
obsidian-cli publish:open path="folder/note.md"   # Open the published page in a browser
```

> **Note:** Publish commands operate on the Publish configuration in the running Obsidian app. They are not a replacement for direct file sync or Git publishing workflows.

---

## Sync

Manage Obsidian Sync (requires active Sync subscription).

```bash
obsidian-cli sync                                   # Show sync status summary
obsidian-cli sync on                                # Resume syncing
obsidian-cli sync off                               # Pause syncing
obsidian-cli sync:status                            # Detailed sync status
obsidian-cli sync:history path="note.md"            # Version history for a file
obsidian-cli sync:read path="note.md" version=3     # Read a specific version
obsidian-cli sync:restore path="note.md" version=3  # Restore a previous version
obsidian-cli sync:deleted                           # List files deleted via sync
obsidian-cli sync:open                              # Open the Sync history view in the UI
```

---

## Themes

Manage appearance themes.

```bash
obsidian-cli themes                            # List installed themes
obsidian-cli themes versions                   # List installed themes with version numbers
obsidian-cli theme                             # Show the currently active theme
obsidian-cli theme name="Minimal"              # Get details about a specific theme
obsidian-cli theme:set name="Minimal"          # Switch to a theme
obsidian-cli theme:set name=""                 # Switch back to default theme
obsidian-cli theme:install name="Minimal"      # Install a community theme
obsidian-cli theme:install name="Minimal" enable  # Install and activate immediately
obsidian-cli theme:uninstall name="Minimal"    # Uninstall a theme
```

---

## CSS Snippets

Manage custom CSS snippet files (snippets live in `.obsidian/snippets/`).

```bash
obsidian-cli snippets                          # List all installed CSS snippets
obsidian-cli snippets:enabled                  # List only enabled snippets
obsidian-cli snippet:enable name="my-style"    # Enable a snippet
obsidian-cli snippet:disable name="my-style"   # Disable a snippet
```

---

## Commands & Hotkeys

Execute any Obsidian command by its ID, and inspect hotkey bindings.

```bash
obsidian-cli commands                          # List all available command IDs
obsidian-cli command id="app:reload"           # Execute a command by ID
obsidian-cli command id="editor:toggle-bold"   # Example: toggle bold in active editor
obsidian-cli hotkeys                           # List all hotkeys (tab-separated: id \t keybinding)
obsidian-cli hotkey id="app:open-settings"     # Get hotkey for a specific command
obsidian-cli hotkey id="app:open-settings" verbose  # Show if custom or default
```

**Typical workflow — find and run a command:**

```bash
obsidian-cli commands | grep "canvas"          # Find canvas-related command IDs
obsidian-cli command id="canvas:new-file"      # Execute the matched command
```

**Getting plugin command IDs:**

```bash
obsidian-cli commands | grep "dataview"        # List all Dataview plugin commands
```

---

## Obsidian Bases

Obsidian Bases (v1.12+) is a built-in database feature. Base files (`.base`) store structured data and support multiple views.

```bash
obsidian-cli bases                                    # List all .base files in vault
obsidian-cli base:query file="tasks" format=json      # Query default view of a base
obsidian-cli base:query file="tasks" view="Kanban"    # Query a specific view
obsidian-cli base:query path="folder/tasks.base" format=csv  # Query by path
obsidian-cli base:views file="tasks"                  # List all views in a base file
obsidian-cli base:create file="tasks" title="Buy milk"  # Add an item to a base
```

**Supported output formats for `base:query`:** `json` (default), `csv`, `tsv`, `md`, `paths`

---

## History

File version history (built-in to Obsidian, separate from Sync). Requires the File Recovery core plugin.

```bash
obsidian-cli history:list                             # List all files that have history
obsidian-cli history path="folder/note.md"            # List versions of a specific file
obsidian-cli history:read path="folder/note.md"       # Read the latest saved version
obsidian-cli history:read path="folder/note.md" version=3  # Read a specific version
obsidian-cli history:restore path="folder/note.md" version=3  # Restore a version
obsidian-cli history:open path="folder/note.md"       # Open file recovery UI for a file
```

> **Note:** History is distinct from [Sync version history](#sync). History uses Obsidian's built-in File Recovery snapshots; Sync history uses Obsidian Sync cloud versions.

---

## Workspace & Tabs

Inspect and manage the Obsidian workspace layout and open tabs.

```bash
obsidian-cli workspace                                # Show the full workspace tree
obsidian-cli workspace ids                            # Include workspace item IDs
obsidian-cli workspaces                               # List saved workspaces
obsidian-cli workspaces total                         # Count saved workspaces
obsidian-cli workspace:save name="Research Layout"    # Save current layout
obsidian-cli workspace:load name="Research Layout"    # Load a saved layout
obsidian-cli workspace:delete name="Research Layout"  # Delete a saved layout
obsidian-cli tabs                                     # List all open tabs (flat list)
obsidian-cli tabs ids                                 # Include tab/group IDs
obsidian-cli tab:open file="folder/note.md"           # Open a file in a new tab
obsidian-cli tab:open view="graph"                    # Open a view type in a new tab
obsidian-cli recents                                  # List recently opened files
```

---

## Diff

Compare local and sync versions of a file.

```bash
obsidian-cli diff path="folder/note.md"               # List available versions (local + sync)
obsidian-cli diff path="folder/note.md" from=1 to=2   # Diff two specific versions
obsidian-cli diff path="folder/note.md" filter=local  # Show only local versions
obsidian-cli diff path="folder/note.md" filter=sync   # Show only sync versions
```

---

## Developer

Debugging and development tools.

### Screenshots

```bash
obsidian-cli dev:screenshot path="folder/screenshot.png"
```

Takes a screenshot of the Obsidian window and saves it. **Path must be vault-relative** — absolute filesystem paths are silently ignored.

### JavaScript Evaluation

```bash
obsidian-cli eval code="app.vault.getFiles().length"
obsidian-cli eval code="app.vault.getMarkdownFiles().map(f => f.path).join('\n')"
```

Executes arbitrary JavaScript in the Obsidian app context. Has access to the full Obsidian API (`app`, `app.vault`, `app.workspace`, `app.metadataCache`, etc.).

> **Multiline scripts:** Passing multiline JavaScript inline fails with "Invalid or unexpected token".
> Write the code to a temp file and use command substitution instead:
>
> ```bash
> cat > /tmp/obs.js << 'JS'
> var files = app.vault.getMarkdownFiles();
> files.map(f => f.path).join('\n');
> JS
> obsidian-cli eval code="$(cat /tmp/obs.js)"
> ```

### Console & Errors

```bash
obsidian-cli dev:debug on              # Start capturing console output (required before dev:console)
obsidian-cli dev:debug off             # Stop capturing console output
obsidian-cli dev:console limit=20     # Recent console output (requires dev:debug on first)
obsidian-cli dev:errors                # Recent error messages
```

> **Note:** `dev:console` will return an error unless `dev:debug on` has been run first in the current session.

### DOM Inspection

```bash
obsidian-cli dev:dom selector=".view-content"             # Get outerHTML of first match
obsidian-cli dev:dom selector=".view-content" all         # Get all matches
obsidian-cli dev:dom selector=".view-content" text        # Get text content
obsidian-cli dev:dom selector=".view-content" total       # Count matching elements
obsidian-cli dev:dom selector=".view-content" attr=class  # Get an attribute value
obsidian-cli dev:dom selector=".view-content" css=color   # Get a CSS property value
```

### CSS Inspection

```bash
obsidian-cli dev:css selector=".view-content"              # Inspect CSS with source locations
obsidian-cli dev:css selector=".view-content" prop=color   # Filter by CSS property name
```

### Chrome DevTools Protocol

```bash
obsidian-cli devtools                                      # Toggle Electron DevTools panel
obsidian-cli dev:cdp method="Runtime.evaluate" params='{"expression":"1+1"}'  # Run a CDP command
```

### Mobile Emulation

```bash
obsidian-cli dev:mobile on                                 # Enable mobile emulation
obsidian-cli dev:mobile off                                # Disable mobile emulation
```

---

## Unique Notes

Create notes through the Unique Note Creator core plugin.

```bash
obsidian-cli unique name="Idea" content="Initial text" # Create a unique note
obsidian-cli unique name="Idea" open                   # Create and open the note
obsidian-cli unique name="Idea" paneType=split         # Open in a split pane
```

The exact generated path follows the Unique Note Creator plugin settings in the running vault.

---

## Web Viewer

Open URLs in Obsidian's Web Viewer core plugin.

```bash
obsidian-cli web url="https://example.com"        # Open URL in Web Viewer
obsidian-cli web url="https://example.com" newtab # Open URL in a new tab
```

---

## Vault & System

### Vault Information

```bash
obsidian-cli vault                         # Current vault: name, path, file/folder counts
obsidian-cli vault info=path               # Return a specific vault field
obsidian-cli vaults                        # List all known vaults
obsidian-cli vaults total                  # Count known vaults
obsidian-cli vaults verbose                # Include vault paths
obsidian-cli vault:open name="Work"        # Switch vaults in the TUI only
```

> **Note:** `vault:open` is documented as TUI-only. For non-interactive automation, prefer running from the target vault directory or passing `vault=<name>` before the command when the local CLI supports it.

### Other Utilities

```bash
obsidian-cli help                          # Show all available commands
obsidian-cli help read                     # Show help for one command
obsidian-cli version                       # Obsidian version info
obsidian-cli outline path="note.md"        # Heading structure of a note
obsidian-cli wordcount path="note.md"      # Word and character count
obsidian-cli recents                       # Recently opened files
obsidian-cli reload                        # Reload the vault (re-index)
obsidian-cli restart                       # Restart the Obsidian app
```

---

## Output Formatting & Piping

The CLI outputs plain text by default, ideal for piping into Unix tools.

### Supported `format=` values

| Format | Description | Best for |
|---|---|---|
| `text` | Plain text (default) | Piping to grep/awk/sed |
| `json` | JSON array or object | Processing with jq, AI agents |
| `csv` | Comma-separated values | Spreadsheet import |
| `tsv` | Tab-separated values | Shell parsing with cut/awk |
| `yaml` | YAML output | Config-style processing |
| `md` | Markdown table | Embedding results in notes |
| `paths` | One path per line | Batch file operations |
| `tree` | Tree view | Visual hierarchy |

Not all formats are supported by every command. Use `text` or `json` when in doubt.

### Examples

```bash
# Count notes in a folder
obsidian-cli files folder="projects" | wc -l

# Find notes with a specific tag, then read them
obsidian-cli tag name="urgent" | while read -r note; do
  echo "=== $note ==="
  obsidian-cli read path="$note"
done

# Export search results as JSON and process with jq
# format=json returns an array of file path strings: ["folder/note.md", ...]
obsidian-cli search query="meeting" format=json | jq '.[]'

# Query a base as CSV
obsidian-cli base:query file="tasks" format=csv

# Filter console errors (requires dev:debug on first)
obsidian-cli dev:debug on
obsidian-cli dev:console limit=50 | grep -i error
```

---

## Multi-Vault Usage

When working with multiple vaults, pass the vault name with `vault=<name>`:

```bash
obsidian-cli vault="Personal" daily:read
obsidian-cli vault="Work" search query="standup"
obsidian-cli vault="Archive" files total
```

If the vault name contains spaces, quote it. The vault name must match what's shown in `obsidian-cli vaults`.

> **Compatibility note:** On some environments, `obsidian-cli vault="My Vault" command` returns
> `Error: Command "My Vault" not found`. If this occurs, omit the vault name — the CLI will target
> the most recently active vault. Switch vaults in the Obsidian UI before running CLI commands
> when targeting a specific vault.

---

## Headless / Server Setup (Linux)

For running Obsidian CLI on a headless Linux server (useful for AI agent integration):

1. Install the `.deb` package (not snap — snap confinement breaks IPC)
2. Install and start `xvfb`: `Xvfb :5 -screen 0 1920x1080x24 &`
3. Start the Obsidian desktop app under xvfb using the platform launcher for that environment.
4. Run CLI commands through `obsidian-cli`, for example: `DISPLAY=:5 obsidian-cli daily:read`

**Systemd note**: If running as a service, ensure `PrivateTmp=false` so the IPC socket is accessible.

**Stderr filtering**: Headless environments produce harmless GPU warnings. Filter with:

```bash
DISPLAY=:5 obsidian-cli search query="test" 2>/dev/null
```
