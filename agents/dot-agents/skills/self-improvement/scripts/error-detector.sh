#!/bin/bash
# Self-Improvement Error Detector Hook
# Run from an OpenCode tool.execute.after adapter or another host wrapper.
# Accepts TOOL_OUTPUT, legacy CLAUDE_TOOL_OUTPUT, or raw tool output on stdin.

set -e

OUTPUT="${TOOL_OUTPUT:-${CLAUDE_TOOL_OUTPUT:-}}"
if [ -z "$OUTPUT" ] && [ ! -t 0 ]; then
    OUTPUT=$(cat)
fi

# Patterns indicating errors (case-insensitive matching)
ERROR_PATTERNS=(
    "error:"
    "Error:"
    "ERROR:"
    "failed"
    "FAILED"
    "command not found"
    "No such file"
    "Permission denied"
    "fatal:"
    "Exception"
    "Traceback"
    "npm ERR!"
    "ModuleNotFoundError"
    "SyntaxError"
    "TypeError"
    "exit code"
    "non-zero"
)

# Check if output contains any error pattern
contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

# Only output reminder if error detected
if [ "$contains_error" = true ]; then
    cat << 'EOF'
<error-detected>
A command error was detected. Consider logging this to the canonical ERRORS.md chosen from applicable AGENTS.md storage rules if:
- The error was unexpected or non-obvious
- It required investigation to resolve
- It might recur in similar contexts
- The solution could benefit future sessions

Use the self-improvement skill format: [ERR-YYYYMMDD-XXX]
</error-detected>
EOF
fi
