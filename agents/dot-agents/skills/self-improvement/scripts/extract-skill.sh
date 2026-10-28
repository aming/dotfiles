#!/bin/bash
# Create a sibling skill using the bundled template, independent of caller cwd.
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
SKILL_DIR=$(dirname -- "$SCRIPT_DIR")
SKILLS_DIR=$(dirname -- "$SKILL_DIR")
SKILL_NAME=""
DRY_RUN=false
usage() {
    echo "Usage: $0 <skill-name> [--dry-run] [--output-dir ABSOLUTE_DIRECTORY]"
    echo "Default output: sibling of $SKILL_DIR (independent of cwd)."
}
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --output-dir)
            [[ $# -ge 2 && "$2" = /* ]] || { echo '--output-dir requires an absolute directory' >&2; exit 1; }
            SKILLS_DIR=$2; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        -*) usage >&2; exit 1 ;;
        *) [[ -z "$SKILL_NAME" ]] || { usage >&2; exit 1; }; SKILL_NAME=$1; shift ;;
    esac
done
[[ "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || { echo 'Skill name must be lowercase kebab-case' >&2; exit 1; }
SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"
[[ ! -e "$SKILL_PATH" ]] || { echo "Skill already exists: $SKILL_PATH" >&2; exit 1; }
# The first fenced markdown block is the authoritative bundled scaffold.
render_template() {
    awk -v name="$SKILL_NAME" '
        /^```markdown$/ && !started { started=1; next }
        /^```$/ && started { exit }
        started { gsub(/skill-name-here/, name); print }
    ' "$SKILL_DIR/assets/SKILL.template.md"
}
if "$DRY_RUN"; then
    echo "Would create: $SKILL_PATH/SKILL.md"
    render_template
else
    mkdir -p -- "$SKILLS_DIR"
    mkdir -- "$SKILL_PATH"
    render_template > "$SKILL_PATH/SKILL.md"
    echo "Created: $SKILL_PATH/SKILL.md"
    echo 'Fill the TODOs and record the actual Skill-Path in the source learning.'
fi
