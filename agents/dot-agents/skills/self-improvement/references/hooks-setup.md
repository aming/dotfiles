# OpenCode-first reminder hooks

OpenCode users should start with the manual capture workflow in `SKILL.md`.
The fallback storage path is `.agents/learnings/` under the git root.
Hooks are optional reminders; they never select a storage directory or write logs.
Always resolve the git root and apply local AGENTS.md storage rules first.

## OpenCode adapter

The [official OpenCode plugin guide](https://opencode.ai/docs/plugins/) documents
project plugins in `.opencode/plugins/` and the `tool.execute.after` event.
Use an OpenCode plugin's `tool.execute.after` callback to invoke the detector.
The adapter supplies raw tool output in `TOOL_OUTPUT`; this is an explicit adapter
contract, not a built-in environment variable supplied by OpenCode.
Resolve `skillDir` to the installed self-improvement directory before enabling:

```javascript
import { execFileSync } from "node:child_process";

export const LearningReminder = async () => ({
  "tool.execute.after": async (_input, output) => {
    const skillDir = "/absolute/path/to/skills/self-improvement";
    const reminder = execFileSync("bash", [`${skillDir}/scripts/error-detector.sh`], {
      env: { ...process.env, TOOL_OUTPUT: String(output.output ?? "") },
      encoding: "utf8",
    }).trim();
    if (reminder) output.output += `\n${reminder}`;
  },
});
```

Install the adapter using the plugin mechanism supported by your OpenCode version;
verify the callback fires before relying on it. No Claude settings file is involved.
If plugin hooks are unavailable, call the scripts directly from the skill directory:

```bash
bash scripts/activator.sh
TOOL_OUTPUT='error: example failure' bash scripts/error-detector.sh
printf '%s\n' 'fatal: example failure' | bash scripts/error-detector.sh
bash scripts/extract-skill.sh test-skill --dry-run
```

Expected detector output contains `<error-detected>` for those failure samples and
is empty for `TOOL_OUTPUT='success'`. The scripts accept plain text, not host-specific
JSON; parse structured tool results in the host adapter before invoking them.

## Other agents (secondary)

For Claude Code, a PostToolUse command wrapper must decode its documented stdin
JSON and pass the tool result text as `TOOL_OUTPUT`, or pipe raw text to the script.
`CLAUDE_TOOL_OUTPUT` remains a compatibility fallback for wrappers that set it;
it is not assumed to exist. A prompt hook can invoke `scripts/activator.sh` using
an absolute installed skill path.

For Codex and Copilot, use the manual workflow unless the installed host documents
a supported hook interface. Do not assume `.codex/settings.json` accepts Claude's
hook schema. If adapters are unavailable, reminders can be called directly with
`bash /absolute/path/to/skills/self-improvement/scripts/activator.sh`.

## Troubleshooting

Run scripts explicitly with `bash`; executable bits are unnecessary for this route.
Check the installed skill path, pass a known failure sample, and inspect adapter
stderr. Avoid logging secrets from tool output and keep reminders brief.
