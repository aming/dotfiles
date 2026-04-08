# OPENCODE

## OVERVIEW
Profile configs for OpenCode and OCX, including model routing, plugin loading, and profile-specific excludes.

## STRUCTURE
```text
opencode/
└── dot-config/opencode/profiles/
    ├── default/
    │   ├── AGENTS.md
    │   ├── ocx.jsonc
    │   └── opencode.jsonc
    └── omo/
        ├── ocx.jsonc
        ├── oh-my-openagent.jsonc
        └── opencode.jsonc
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Base profile behavior | `opencode/dot-config/opencode/profiles/default/` | default OCX/OpenCode settings |
| OMO model routing | `opencode/dot-config/opencode/profiles/omo/oh-my-openagent.jsonc` | agent/category model map |
| OMO profile plugin setup | `opencode/dot-config/opencode/profiles/omo/opencode.jsonc` | enables `oh-my-openagent` |
| Profile exclude rules | `opencode/dot-config/opencode/profiles/*/ocx.jsonc` | `CLAUDE.md`, `CONTEXT.md`, `.opencode`, profile configs |

## CONVENTIONS
- Keep profile-local behavior in the profile directory; do not invent extra global config layers here.
- `opencode.jsonc` owns model/plugin settings; `ocx.jsonc` owns inclusion, exclusion, and registry behavior.
- The `omo` profile is the opinionated, multi-agent setup; `default` should stay lightweight.

## ANTI-PATTERNS
- Do not let `ocx.jsonc` include profile config files that are intentionally excluded.
- Do not duplicate model-routing logic across multiple files when `oh-my-openagent.jsonc` is already the routing table.
- Do not leave placeholder AGENTS instructions in active profiles.
