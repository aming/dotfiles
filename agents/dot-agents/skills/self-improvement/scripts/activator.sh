#!/bin/bash
# Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind the agent about learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

# Output reminder as system context
cat << 'EOF'
<self-improvement-reminder>
After completing this task, evaluate if extractable knowledge emerged:
- Non-obvious solution discovered through investigation?
- Workaround for unexpected behavior?
- Project-specific pattern learned?
- Error required debugging to resolve?

If yes: Log to the canonical learning directory selected by applicable AGENTS.md rules
(default .agents/learnings/ under the git root; agents/learnings/ here). Record
the chosen absolute path after `git rev-parse --show-toplevel`; never use a subdirectory cwd as a root fallback using the self-improvement skill format.
If high-value (recurring, broadly applicable): Consider skill extraction.
</self-improvement-reminder>
EOF
