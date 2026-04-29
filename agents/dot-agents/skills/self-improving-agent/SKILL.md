---
name: self-improvement
description: "Captures corrections, failures, missing capabilities, and reusable discoveries in agent so future work improves. Use this skill whenever a command, tool, or API fails unexpectedly; the user corrects the agent; the agent realizes its knowledge is outdated or wrong; a missing capability is exposed; or a better recurring approach is discovered. Record the result under .agent/learnings/, review related entries before major tasks, and promote durable workflow rules into AGENTS.md when they should change future behavior."
---

# Self-Improvement Skill

Use this skill in Agent hardness to turn mistakes, surprises, and reusable discoveries into durable project memory.

Default storage location:

```
<project-root>/.agent/learnings/
  LEARNINGS.md
  ERRORS.md
  FEATURE_REQUESTS.md
```

Keep the workflow lightweight: log the important thing, link it to the right files, and promote it when it becomes a durable rule.

## Quick Triage

| Situation | Action |
|-----------|--------|
| Command, tool, or API fails unexpectedly | Append an entry to `.agent/learnings/ERRORS.md` |
| User corrects the agent or supplies missing facts | Append an entry to `.agent/learnings/LEARNINGS.md` with category `correction` or `knowledge_gap` |
| Agent discovers a clearly better recurring approach | Append an entry to `.agent/learnings/LEARNINGS.md` with category `best_practice` |
| User asks for a capability the workflow does not support | Append an entry to `.agent/learnings/FEATURE_REQUESTS.md` |
| Similar issue already exists | Link it with `See Also`, update recurrence metadata, and consider a higher priority |
| Learning should change future agent behavior | Promote a concise rule into `AGENTS.md` |

## OpenCode Workflow

1. Capture the learning immediately in `.agent/learnings/` while the context is still fresh.
2. Search for related entries before creating a new one.
3. Record the concrete fix, correction, or missing capability in a format another agent can reuse quickly.
4. Promote the learning into `AGENTS.md` when it should change future behavior across tasks.
5. Revisit the logs before major work or when entering an area with prior mistakes.

## Project Layout

Create the learning directory inside the project:

```bash
mkdir -p .agent/learnings
```

Recommended files:

- `.agent/learnings/LEARNINGS.md` - corrections, knowledge gaps, best practices
- `.agent/learnings/ERRORS.md` - command failures, tool failures, API errors
- `.agent/learnings/FEATURE_REQUESTS.md` - user-requested capabilities that do not exist yet

## Logging Format

### Learning Entry

Append to `.agent/learnings/LEARNINGS.md`:

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

Append to `.agent/learnings/ERRORS.md`:

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

Append to `.agent/learnings/FEATURE_REQUESTS.md`:

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

When a new issue feels familiar, search the project logs first:

```bash
grep -n "keyword" .agent/learnings/*.md
grep -n "Pattern-Key: <pattern_key>" .agent/learnings/LEARNINGS.md
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
.agent/learnings/
```

## Skill Extraction

When a learning becomes broadly reusable outside the current project, turn it into a standalone skill:

```bash
./skills/self-improving-agent/scripts/extract-skill.sh skill-name --dry-run
./skills/self-improving-agent/scripts/extract-skill.sh skill-name
```

## Reference Files

- `references/examples.md` - complete example entries
- `references/hooks-setup.md` - optional hook setup notes for OpenCode-compatible hook setups
- `assets/LEARNINGS.template.md` - reusable template for `.agent/learnings/LEARNINGS.md`
- `assets/ERRORS.template.md` - reusable template for `.agent/learnings/ERRORS.md`
- `assets/FEATURE_REQUESTS.template.md` - reusable template for `.agent/learnings/FEATURE_REQUESTS.md`
- `assets/SKILL.template.md` - template for extracted skills

## Original Notes

The text you pasted reflects the pre-cleanup version of this skill. It was centered on OpenClaw, `.learnings/`, and several non-OpenCode integrations. This skill now intentionally uses an OpenCode-first workflow with `.agent/learnings/` and a smaller, more focused instruction set.

Key changes from the older version:

- storage moved from `.learnings/` to `.agent/learnings/`
- OpenClaw-specific setup and hook docs were removed
- promotion guidance was narrowed to `AGENTS.md`
- cross-agent boilerplate was removed so the skill stays focused on OpenCode behavior
