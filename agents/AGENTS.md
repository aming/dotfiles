# AGENTS

## OVERVIEW
First-party OpenCode skill library, helper scripts, and durable learnings.

## STRUCTURE
```text
agents/
├── dot-agents/
│   ├── .opencode/   # local package dependency for agent tooling
│   ├── memsearch/   # repo-scoped memory assets
│   └── skills/      # skill definitions, refs, scripts, eval helpers
└── learnings/       # environment-specific errors and corrections
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Add or edit a skill | `agents/dot-agents/skills/<skill>/SKILL.md` | primary source of behavior |
| Adjust skill automation | `agents/dot-agents/skills/<skill>/scripts/` | Python and shell helpers |
| Review system skills | `agents/dot-agents/skills/.system/` | curated skills mirrored into repo |
| Check package dependency | `agents/dot-agents/.opencode/package.json` | currently only plugin dependency |
| Capture prior failures | `agents/learnings/{ERRORS.md,LEARNINGS.md}` | repo-specific environment traps |

## CONVENTIONS
- Skill roots are documentation-first: `SKILL.md` defines behavior; scripts and references support it.
- Keep skill-specific assets inside the skill directory instead of inventing shared global folders.
- Prefer adding durable environment lessons to `agents/learnings/` when the issue is repo-specific, not transient.
- Utility scripts here are first-party; do not mix them with vendored plugin scripts elsewhere in the repo.

## ANTI-PATTERNS
- Do not treat `.system/` skill content as generic repo docs; it is executable guidance with supporting assets.
- Do not scatter learning notes across random markdown files when `agents/learnings/` is the intended sink.
- Do not infer unsupported subagent types; `agents/learnings/ERRORS.md` records prior failures from that assumption.

## COMMANDS
```bash
python3 agents/dot-agents/skills/skill-creator/scripts/quick_validate.py <skill-path>
python3 agents/dot-agents/skills/skill-creator/scripts/run_eval.py ...
```

## NOTES
- This tree is one of the main first-party code surfaces in the repo.
- If child AGENTS files are ever added below `skills/`, keep them skill-family specific and avoid repeating root repo bootstrap guidance.
