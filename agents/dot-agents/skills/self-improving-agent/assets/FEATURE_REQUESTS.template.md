# Feature Requests

Template for `agents/learnings/FEATURE_REQUESTS.md` in an OpenCode project.

Requested capabilities that the current workflow or tooling does not support yet.

**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted_to_skill

## Entry Format

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

## Recommended Project Layout

```text
agents/
  learnings/
    LEARNINGS.md
    ERRORS.md
    FEATURE_REQUESTS.md
```
