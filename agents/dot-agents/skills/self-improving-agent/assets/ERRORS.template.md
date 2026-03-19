# Errors

Template for `agents/learnings/ERRORS.md` in an OpenCode project.

Unexpected command, tool, and API failures worth remembering.

**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted

## Entry Format

```markdown
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
```

## Recommended Project Layout

```text
agents/
  learnings/
    LEARNINGS.md
    ERRORS.md
    FEATURE_REQUESTS.md
```
