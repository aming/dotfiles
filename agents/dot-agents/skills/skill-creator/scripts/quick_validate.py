#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import sys
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    return True, "Skill is valid!"


def lint_skill(skill_path):
    """Best-practices lint checks (warning-only)."""
    skill_path = Path(skill_path)
    skill_md = skill_path / 'SKILL.md'
    warnings = []

    content = skill_md.read_text()
    lines = content.splitlines()

    if len(lines) > 500:
        warnings.append(
            f"SKILL.md has {len(lines)} lines (>500). Consider progressive disclosure and moving details to references/."
        )

    if not re.search(r'^\s*##\s+Gotchas\b', content, re.MULTILINE):
        warnings.append("Missing '## Gotchas' section. Add recurring pitfalls discovered during real usage.")

    references_dir = skill_path / "references"
    mentions_references = "references/" in content or references_dir.exists()
    has_conditional_reference = bool(
        re.search(r'\bif\b.{0,160}references\/[A-Za-z0-9._/-]+', content, re.IGNORECASE | re.DOTALL)
    )
    if mentions_references and not has_conditional_reference:
        warnings.append(
            "References are present but no condition-based loading trigger was found. "
            "Use patterns like: 'If X happens, read references/<file>.md'."
        )

    generic_phrases = [
        "best practices",
        "as needed",
        "when appropriate",
        "leverage",
    ]
    for phrase in generic_phrases:
        if content.lower().count(phrase) >= 4:
            warnings.append(
                f"Phrase '{phrase}' appears frequently; check for generic filler and replace with concrete procedures."
            )
            break

    return warnings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    if valid:
        warnings = lint_skill(sys.argv[1])
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"- {warning}")
    sys.exit(0 if valid else 1)
