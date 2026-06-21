#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from typing import Final

try:
    from scripts.utils import parse_skill_md
except ModuleNotFoundError:
    from utils import parse_skill_md


ACRONYMS: Final = {"API", "CI", "CLI", "GH", "LLM", "MCP", "PDF", "PR", "SQL", "UI", "URL"}
BRANDS: Final = {
    "datadog": "DataDog",
    "fastapi": "FastAPI",
    "github": "GitHub",
    "openai": "OpenAI",
    "openapi": "OpenAPI",
    "pagerduty": "PagerDuty",
    "sqlite": "SQLite",
}
SMALL_WORDS: Final = {"and", "or", "to", "up", "with"}
ALLOWED_INTERFACE_KEYS: Final = {
    "brand_color",
    "default_prompt",
    "display_name",
    "icon_large",
    "icon_small",
    "short_description",
}


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def format_display_name(skill_name: str) -> str:
    formatted: list[str] = []
    for index, word in enumerate(part for part in skill_name.split("-") if part):
        lower = word.lower()
        upper = word.upper()
        if upper in ACRONYMS:
            formatted.append(upper)
        elif lower in BRANDS:
            formatted.append(BRANDS[lower])
        elif index > 0 and lower in SMALL_WORDS:
            formatted.append(lower)
        else:
            formatted.append(word.capitalize())
    return " ".join(formatted)


def generate_short_description(display_name: str) -> str:
    candidates = [
        f"Help with {display_name} tasks and workflows",
        f"Help with {display_name} tasks with guidance",
        f"Help with {display_name} workflows",
        f"{display_name} helper workflows",
    ]
    for candidate in candidates:
        if 25 <= len(candidate) <= 64:
            return candidate
    suffix = " helper workflows"
    max_name_length = 64 - len(suffix)
    trimmed = display_name[:max_name_length].rstrip()
    return f"{trimmed}{suffix}"


def parse_interface_overrides(raw_overrides: list[str]) -> tuple[dict[str, str], list[str]] | None:
    overrides: dict[str, str] = {}
    optional_order: list[str] = []
    for item in raw_overrides:
        if "=" not in item:
            print(f"[ERROR] Invalid interface override '{item}'. Use key=value.")
            return None
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            print(f"[ERROR] Invalid interface override '{item}'. Key is empty.")
            return None
        if key not in ALLOWED_INTERFACE_KEYS:
            allowed = ", ".join(sorted(ALLOWED_INTERFACE_KEYS))
            print(f"[ERROR] Unknown interface field '{key}'. Allowed: {allowed}")
            return None
        overrides[key] = value
        if key not in {"display_name", "short_description", "default_prompt"} and key not in optional_order:
            optional_order.append(key)
    return overrides, optional_order


def write_openai_yaml(skill_dir: Path, skill_name: str, raw_overrides: list[str]) -> Path | None:
    parsed = parse_interface_overrides(raw_overrides)
    if parsed is None:
        return None
    overrides, optional_order = parsed

    display_name = overrides.get("display_name") or format_display_name(skill_name)
    short_description = overrides.get("short_description") or generate_short_description(display_name)
    default_prompt = overrides.get("default_prompt") or f"Use ${skill_name} to create or improve a Codex skill."

    if not (25 <= len(short_description) <= 64):
        print(f"[ERROR] short_description must be 25-64 characters (got {len(short_description)}).")
        return None
    if f"${skill_name}" not in default_prompt:
        print(f"[ERROR] default_prompt must mention ${skill_name}.")
        return None

    interface_lines = [
        "interface:",
        f"  display_name: {yaml_quote(display_name)}",
        f"  short_description: {yaml_quote(short_description)}",
        f"  default_prompt: {yaml_quote(default_prompt)}",
    ]
    for key in optional_order:
        interface_lines.append(f"  {key}: {yaml_quote(overrides[key])}")

    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    output_path = agents_dir / "openai.yaml"
    output_path.write_text("\n".join(interface_lines) + "\n")
    print("[OK] Created agents/openai.yaml")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create agents/openai.yaml for a skill directory.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("--name", help="Skill name override, defaulting to SKILL.md frontmatter")
    parser.add_argument("--interface", action="append", default=[], help="Interface override in key=value format")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists():
        print(f"[ERROR] Skill directory not found: {skill_dir}")
        return 1
    if not skill_dir.is_dir():
        print(f"[ERROR] Path is not a directory: {skill_dir}")
        return 1

    skill_name = args.name
    if not skill_name:
        skill_name, _, _ = parse_skill_md(skill_dir)
    if not skill_name:
        print("[ERROR] Frontmatter 'name' is missing or invalid.")
        return 1

    result = write_openai_yaml(skill_dir, skill_name, args.interface)
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
