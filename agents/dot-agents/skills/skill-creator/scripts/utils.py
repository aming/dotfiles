"""Shared utilities for skill-creator scripts."""

from pathlib import Path
from typing import TypeAlias


FrontmatterValue: TypeAlias = str | dict[str, str] | list[str] | None


class FrontmatterParseError(Exception):
    pass


def _strip_scalar_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _parse_block(lines: list[str], start: int, folded: bool) -> tuple[str, int]:
    values: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if line.startswith((" ", "\t")):
            values.append(line.strip())
            index += 1
            continue
        break
    separator = " " if folded else "\n"
    return separator.join(values), index


def _parse_nested_mapping(lines: list[str], start: int) -> tuple[dict[str, str], int]:
    values: dict[str, str] = {}
    index = start
    while index < len(lines):
        line = lines[index]
        if not line.startswith((" ", "\t")):
            break
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if ":" not in stripped:
            raise FrontmatterParseError(f"Invalid nested frontmatter line: {stripped}")
        key, raw_value = stripped.split(":", 1)
        values[key.strip()] = _strip_scalar_quotes(raw_value.strip())
        index += 1
    return values, index


def parse_frontmatter_text(frontmatter_text: str) -> dict[str, FrontmatterValue]:
    frontmatter: dict[str, FrontmatterValue] = {}
    lines = frontmatter_text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            index += 1
            continue
        if line.startswith((" ", "\t")):
            raise FrontmatterParseError(f"Unexpected indented frontmatter line: {stripped}")
        if ":" not in line:
            raise FrontmatterParseError(f"Invalid frontmatter line: {line}")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            raise FrontmatterParseError("Frontmatter key cannot be empty")

        match value:
            case "|" | "|-":
                parsed_value, index = _parse_block(lines, index + 1, folded=False)
                frontmatter[key] = parsed_value
            case ">" | ">-":
                parsed_value, index = _parse_block(lines, index + 1, folded=True)
                frontmatter[key] = parsed_value
            case "":
                nested_value, next_index = _parse_nested_mapping(lines, index + 1)
                frontmatter[key] = nested_value if nested_value else ""
                index = next_index
            case _:
                if value.startswith("[") and value.endswith("]"):
                    items = [
                        _strip_scalar_quotes(item.strip())
                        for item in value[1:-1].split(",")
                        if item.strip()
                    ]
                    frontmatter[key] = items
                else:
                    frontmatter[key] = _strip_scalar_quotes(value)
                index += 1
    return frontmatter


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse a SKILL.md file, returning (name, description, full_content)."""
    content = (skill_path / "SKILL.md").read_text()
    lines = content.split("\n")

    if lines[0].strip() != "---":
        raise ValueError("SKILL.md missing frontmatter (no opening ---)")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise ValueError("SKILL.md missing frontmatter (no closing ---)")

    frontmatter_text = "\n".join(lines[1:end_idx])
    frontmatter = parse_frontmatter_text(frontmatter_text)
    name_value = frontmatter.get("name", "")
    description_value = frontmatter.get("description", "")
    name = name_value if isinstance(name_value, str) else ""
    description = description_value if isinstance(description_value, str) else ""

    return name, description, content
