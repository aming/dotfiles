## [ERR-20260413-001] skill-tool-discovery-mismatch

**Logged**: 2026-04-13T00:00:00-07:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
The skill tool could not load `systematic-debugging` even though it appeared in session-provided available skills metadata.

### Error
```text
Skill or command "systematic-debugging" not found. Available: github-kb, pdf, self-improvement, skill-creator, web-search-advanced, playwright, frontend-ui-ux, git-master, dev-browser, review-work, ai-slop-remover, /init-deep, /ralph-loop, /ulw-loop, /cancel-ralph, /refactor, /start-work, /stop-continuation, /remove-ai-slops, /handoff
```

### Context
- Operation attempted: load the `systematic-debugging` skill before troubleshooting a Neovim Treesitter error
- Environment: OpenCode session in `/home/aming/dotfiles`
- Inputs: `skill(name="systematic-debugging", user_message="Investigate and troubleshoot a Neovim Treesitter error...")`

### Suggested Fix
Investigate why session skill metadata and the runtime skill registry diverge, or expose unavailable skills consistently so orchestration can make reliable decisions.

### Metadata
- Reproducible: yes
- Related Files: agents/dot-agents/skills/self-improvement/SKILL.md
