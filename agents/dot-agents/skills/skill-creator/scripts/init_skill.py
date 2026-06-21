#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path
from typing import Final

try:
    from scripts.generate_openai_yaml import write_openai_yaml
except ModuleNotFoundError:
    from generate_openai_yaml import write_openai_yaml


MAX_SKILL_NAME_LENGTH: Final = 64
ALLOWED_RESOURCES: Final = {"assets", "references", "scripts"}
SKILL_TEMPLATE = (
    "---\n"
    "name: {skill_name}\n"
    "description: [TODO: Explain what this skill does and when Codex should use it.]\n"
    "---\n\n"
    "# {skill_title}\n\n"
    "## Overview\n\n"
    "[TODO: 1-2 sentences explaining what this skill enables.]\n\n"
    "## Workflow\n\n"
    "[TODO: Add the shortest useful workflow. Move long detail into references/.]\n\n"
    "## Gotchas\n\n"
    "- [TODO: Replace with recurring pitfalls, or delete this section only if none exist.]\n"
)
EXAMPLE_SCRIPT = (
    "#!/usr/bin/env python3\n\n"
    "def main() -> int:\n"
    '    print("Replace this helper or delete it.")\n'
    "    return 0\n\n\n"
    'if __name__ == "__main__":\n'
    "    raise SystemExit(main())\n"
)
EXAMPLE_REFERENCE = (
    "# Reference\n\n"
    "Replace this file with focused details that should be loaded only when needed.\n"
)
EXAMPLE_ASSET = "Replace this placeholder with a real asset or delete it.\n"


def normalize_skill_name(skill_name: str) -> str:
    normalized = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    return re.sub(r"-{2,}", "-", normalized)


def title_case_skill_name(skill_name: str) -> str:
    return " ".join(word.capitalize() for word in skill_name.split("-") if word)


def parse_resources(raw_resources: str) -> list[str] | None:
    if not raw_resources:
        return []
    resources = [item.strip() for item in raw_resources.split(",") if item.strip()]
    invalid = sorted({item for item in resources if item not in ALLOWED_RESOURCES})
    if invalid:
        print(f"[ERROR] Unknown resource type(s): {', '.join(invalid)}")
        print(f"Allowed: {', '.join(sorted(ALLOWED_RESOURCES))}")
        return None
    deduped: list[str] = []
    for resource in resources:
        if resource not in deduped:
            deduped.append(resource)
    return deduped


def create_resource_dirs(skill_dir: Path, resources: list[str], include_examples: bool) -> None:
    for resource in resources:
        resource_dir = skill_dir / resource
        resource_dir.mkdir()
        print(f"[OK] Created {resource}/")
        if not include_examples:
            continue
        if resource == "scripts":
            example_script = resource_dir / "example.py"
            example_script.write_text(EXAMPLE_SCRIPT)
            example_script.chmod(0o755)
            print("[OK] Created scripts/example.py")
        elif resource == "references":
            (resource_dir / "reference.md").write_text(EXAMPLE_REFERENCE)
            print("[OK] Created references/reference.md")
        elif resource == "assets":
            (resource_dir / "example_asset.txt").write_text(EXAMPLE_ASSET)
            print("[OK] Created assets/example_asset.txt")


def init_skill(
    skill_name: str,
    output_parent: Path,
    resources: list[str],
    include_examples: bool,
    interface_overrides: list[str],
) -> Path | None:
    skill_dir = output_parent.resolve() / skill_name
    if skill_dir.exists():
        print(f"[ERROR] Skill directory already exists: {skill_dir}")
        return None

    skill_dir.mkdir(parents=True)
    skill_title = title_case_skill_name(skill_name)
    (skill_dir / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)
    )
    print("[OK] Created SKILL.md")

    metadata_path = write_openai_yaml(skill_dir, skill_name, interface_overrides)
    if metadata_path is None:
        return None

    create_resource_dirs(skill_dir, resources, include_examples)
    print(f"[OK] Skill '{skill_name}' initialized successfully at {skill_dir}")
    return skill_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new skill directory with starter files.")
    parser.add_argument("skill_name", help="Skill name, normalized to hyphen-case")
    parser.add_argument("--path", required=True, help="Output directory for the skill")
    parser.add_argument("--resources", default="", help="Comma-separated list: scripts,references,assets")
    parser.add_argument("--examples", action="store_true", help="Create placeholder resource files")
    parser.add_argument("--interface", action="append", default=[], help="Interface override in key=value format")
    args = parser.parse_args()

    skill_name = normalize_skill_name(args.skill_name)
    if not skill_name:
        print("[ERROR] Skill name must include at least one letter or digit.")
        return 1
    if len(skill_name) > MAX_SKILL_NAME_LENGTH:
        print(f"[ERROR] Skill name '{skill_name}' is too long ({len(skill_name)} characters).")
        return 1
    if skill_name != args.skill_name:
        print(f"Normalized skill name from '{args.skill_name}' to '{skill_name}'.")

    resources = parse_resources(args.resources)
    if resources is None:
        return 1
    if args.examples and not resources:
        print("[ERROR] --examples requires --resources to be set.")
        return 1

    result = init_skill(
        skill_name=skill_name,
        output_parent=Path(args.path),
        resources=resources,
        include_examples=args.examples,
        interface_overrides=args.interface,
    )
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
