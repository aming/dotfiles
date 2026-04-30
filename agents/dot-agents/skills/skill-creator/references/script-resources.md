# Script Resources

Use this reference when creating or improving a skill that includes bundled scripts, one-off tool commands, script dependencies, or script interface design.

## When To Use Scripts

Use `scripts/` when the skill has deterministic or repetitive work that future agents would otherwise reimplement: parsing, conversion, validation, grading, packaging, API normalization, report generation, or multi-flag commands that are easy to mistype.

Do not create scripts for one-off shell commands that are already short, stable, and clear. Reference those commands directly in `SKILL.md`.

## One-Off Commands

Prefer dependency-resolving runners and pin versions when possible:

```bash
uvx ruff@0.8.0 check .
npx eslint@9 .
deno run npm:create-vite@6
go run example.com/tool@v1.2.3
```

State prerequisites in `SKILL.md`. Use the `compatibility` frontmatter field for runtime-level requirements such as Node.js, uv, Deno, Go, or a platform-specific CLI.

Move a command into `scripts/` once it needs non-trivial quoting, repeated flags, retries, parsing, branching, output shaping, or any logic the agent might get wrong on the first try.

## Referencing Scripts

Use paths relative to the skill directory root, not absolute paths. List scripts explicitly so the agent knows they exist:

```markdown
## Available scripts

- `scripts/validate.py` - Validates input files and returns JSON diagnostics
- `scripts/render_report.py` - Builds the final HTML report from normalized data
```

Show the intended command shape in the workflow:

```bash
python3 scripts/validate.py --input data.csv --format json
```

If a support file under `references/` includes commands, keep the same convention: command paths are still relative to the skill directory root.

## Agent-Friendly Script Interfaces

- Avoid interactive prompts. Accept input through flags, environment variables, stdin, or files, and fail quickly with a useful message when required input is missing.
- Implement concise `--help` output with a short description, flags, defaults, examples, and documented exit codes when failures are meaningful.
- Send machine-readable results to stdout, preferably JSON/CSV/TSV, and send progress, warnings, and diagnostics to stderr.
- Make errors actionable: say what failed, what was expected, what was received, and what command or flag to try next.
- Make scripts idempotent where practical because agents may retry after errors.
- For destructive or stateful actions, support `--dry-run` and require explicit `--confirm` or `--force` flags when appropriate.
- Keep output bounded. Default to summaries or require `--output` for large results; add `--limit`, `--offset`, or similar flags when pagination is useful.
- Reject ambiguous input instead of guessing. Prefer enums or closed sets for modes and formats.

## Self-Contained Dependencies

Prefer scripts that can run with one command and declare their own dependencies when the language supports it.

For Python scripts with third-party packages, use PEP 723 inline metadata and run with `uv run scripts/name.py`. Pin dependencies with version ranges and add `requires-python` when needed. If reproducibility matters more than convenience, add the relevant `uv lock --script` output.

For Deno scripts, use pinned `npm:` or `jsr:` imports.

For Bun scripts, pin versions in imports when relying on Bun auto-install.

For Ruby scripts, use `bundler/inline` and pin gems.

## Script Review Checklist

- Does `SKILL.md` list each script and explain when to use it?
- Can the agent run each script from the skill root with a single documented command?
- Does every script have non-interactive inputs and useful `--help`?
- Are dependencies pinned or otherwise constrained?
- Are stdout and stderr separated so structured output stays parseable?
- Are destructive actions protected by dry-run or explicit confirmation flags?
- Is the output size predictable enough for agent tool limits?
