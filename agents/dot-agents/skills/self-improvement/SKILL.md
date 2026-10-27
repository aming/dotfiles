---
name: self-improvement
description: "Captures corrections, failures, missing capabilities, and reusable discoveries in agent so future work improves. Use this skill whenever a command, tool, or API fails unexpectedly; the user corrects the agent; the agent realizes its knowledge is outdated or wrong; a missing capability is exposed; or a better recurring approach is discovered. Record the result in the canonical learning directory selected by applicable repository AGENTS.md instructions, defaulting to .agents/learnings/ under the git root (never the current working directory), review related entries before major tasks, and promote durable workflow rules into AGENTS.md when they should change future behavior."
---

# Self-Improvement Skill

Use this skill during agent work to turn mistakes, surprises, and reusable discoveries into durable project memory.

## Storage Location

Resolve the git repository root, then read its `AGENTS.md` and every applicable
nested `AGENTS.md` before choosing a log directory. Repository-local instructions
win over this skill's default `.agents/learnings/`; use the most specific applicable
rule when rules conflict. Inspect existing directories and log the chosen absolute
canonical path and the rule that selected it in your task report before appending.
Keep exactly one canonical log location; do not create a second default directory.

In this dotfiles repository, root `AGENTS.md` mentions `.agent/learnings/`, but the
more specific `agents/AGENTS.md` selects `agents/learnings/`, which exists. For work
under `agents/`, the canonical sink is therefore `<repo-root>/agents/learnings/`.
Neither `<repo-root>/.agent/learnings/` nor `<repo-root>/.agents/learnings/` exists
at the time of this reconciliation. Recheck local rules in other repositories.

```bash
ROOT=$(git rev-parse --show-toplevel) || { echo "No git root; identify the project root explicitly" >&2; exit 1; }
# After inspecting applicable AGENTS.md files, choose ONE repository-relative path.
LEARNING_REL=agents/learnings  # This repository's agents/ rule; default elsewhere: .agents/learnings
LEARNINGS_DIR="$ROOT/$LEARNING_REL"
printf 'Canonical learning path: %s (agents/AGENTS.md)\n' "$LEARNINGS_DIR"
mkdir -p "$LEARNINGS_DIR"
```

Outside git, require an explicitly identified project root; never fall back to `pwd`.
Do not merge, delete, or relocate existing learning logs without authorization.
Read the canonical log before appending and link related entries instead of duplicating.

## Quick Triage

| Situation | Action |
|-----------|--------|
| Command, tool, or API fails unexpectedly | Append an entry to `$LEARNINGS_DIR/ERRORS.md` |
| User corrects the agent or supplies missing facts | Append an entry to `$LEARNINGS_DIR/LEARNINGS.md` with category `correction` or `knowledge_gap` |
| Agent discovers a clearly better recurring approach | Append an entry to `$LEARNINGS_DIR/LEARNINGS.md` with category `best_practice` |
| User asks for a capability the workflow does not support | Append an entry to `$LEARNINGS_DIR/FEATURE_REQUESTS.md` |
| Similar issue already exists | Link it with `See Also`, update recurrence metadata, and consider a higher priority |
| Learning should change future agent behavior | Promote a concise rule into `AGENTS.md` |

## OpenCode Workflow

1. Capture the learning immediately in the canonical `$LEARNINGS_DIR` while the context is still fresh (resolve `$ROOT` first, even when working in a subdirectory).
2. Search for related entries before creating a new one.
3. Record the concrete fix, correction, or missing capability in a format another agent can reuse quickly.
4. Promote the learning into `AGENTS.md` when it should change future behavior across tasks.
5. Revisit the logs before major work or when entering an area with prior mistakes.

## Project Layout

Use the canonical path selected above for `LEARNINGS.md`, `ERRORS.md`, and
`FEATURE_REQUESTS.md`. Create only files needed for the current learning.

## Logging Format

### Learning Entry

Append to `$LEARNINGS_DIR/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what is correct now

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: conversation | error | user_feedback | tool_failure
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related)
- Pattern-Key: simplify.dead_code | harden.input_validation (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)
```

### Error Entry

Append to `$LEARNINGS_DIR/ERRORS.md`:

````markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description of what failed

### Error
```
Actual error message or output
```

### Context
- Command or operation attempted
- Inputs or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (if recurring)
````

### Feature Request Entry

Append to `$LEARNINGS_DIR/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the user wanted to do

### User Context
Why they needed it, what problem they were solving

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built, what it might extend

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name
```

## Promotion to `AGENTS.md`

Promote a learning when it should reliably change future OpenCode behavior for this project.

Good candidates:

- Build or test commands the agent should consistently use
- Required follow-up steps after common changes
- Project conventions that are easy to miss
- Repeated failure-prevention rules
- Tool usage patterns that save time or avoid breakage

## Recurring Pattern Detection

When a new issue feels familiar, search the repository-root log first:

```bash
# Reuse ROOT and LEARNINGS_DIR selected under Storage Location.
rg -n "keyword|Pattern-Key: <pattern_key>" "$LEARNINGS_DIR"
```

## Detection Triggers

Use this skill when you notice any of these:

- user corrections
- unexpected command or tool failures
- missing capabilities
- better recurring approaches
- outdated assumptions or missing project knowledge

## Version Control

Example `.gitignore` if you want the log local only:

```gitignore
# Replace with the canonical repository-relative path
agents/learnings/
```

## Skill Extraction

When a learning becomes broadly reusable outside the current project, turn it into a standalone skill. Run these commands from the self-improvement skill directory; output defaults to a sibling skill directory regardless of the caller's cwd:

```bash
bash scripts/extract-skill.sh skill-name --dry-run
bash scripts/extract-skill.sh skill-name
```

## Reference Files

- `references/examples.md` - complete example entries
- `references/hooks-setup.md` - optional hook setup notes for OpenCode-compatible hook setups
- `assets/LEARNINGS.template.md` - reusable template for `$LEARNINGS_DIR/LEARNINGS.md`
- `assets/ERRORS.template.md` - reusable template for `$LEARNINGS_DIR/ERRORS.md`
- `assets/FEATURE_REQUESTS.template.md` - reusable template for `$LEARNINGS_DIR/FEATURE_REQUESTS.md`
- `assets/SKILL.template.md` - template for extracted skills

## Gotchas

- Local AGENTS.md storage instructions override the default; record the chosen path.
- Resolve the project root explicitly; a nested cwd is never a root fallback.
- If enabling optional reminders, read `references/hooks-setup.md` before configuration.
- Promote durable project behavior only into `AGENTS.md`; skill extraction is a separate reuse workflow.
