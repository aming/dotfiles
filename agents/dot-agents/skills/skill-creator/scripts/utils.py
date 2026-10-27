"""Shared utilities for skill-creator scripts."""

import json
import re
from pathlib import Path
from typing import TypeAlias


FrontmatterValue: TypeAlias = str | dict[str, str] | list[str] | None


class FrontmatterParseError(Exception):
    pass


def _parse_scalar(value: str):
    """Parse a conservative YAML scalar subset without a PyYAML dependency.

    Reject unsupported syntax rather than accepting malformed YAML as text.
    Use block scalars for multiline prose and JSON-compatible double quotes.
    """
    if value.startswith('"'):
        try:
            parsed, end = json.JSONDecoder().raw_decode(value)
        except ValueError as exc:
            raise FrontmatterParseError(f"Invalid quoted scalar: {exc}") from exc
        if value[end:].strip() and not re.fullmatch(r"\s+#.*", value[end:]):
            raise FrontmatterParseError("Unexpected text after quoted scalar")
        return parsed
    if value.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'(?:\s+#.*)?", value)
        if not match:
            raise FrontmatterParseError("Invalid single-quoted scalar")
        return match[1].replace("''", "'")
    if value.startswith("#"):
        return ""
    value = re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
    if value.startswith("["):
        try:
            items = json.loads(value)
        except ValueError as exc:
            raise FrontmatterParseError("Use JSON syntax for flow sequences") from exc
        if not isinstance(items, list):
            raise FrontmatterParseError("Expected a sequence")
        return items
    if (value.startswith(tuple("{}],&*!|>@`%")) or value in {"-", "?", ":"}
            or value.startswith(("- ", "? ", ": "))
            or re.search(r":(?:\s|$)", value)):
        raise FrontmatterParseError("Unsupported or invalid plain scalar; quote the value")
    if value.lower() in {"null", "~"}:
        return None
    if value.lower() in {"true", "false", "yes", "no", "on", "off"}:
        return value.lower() in {"true", "yes", "on"}
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", value):
        return float(value) if "." in value else int(value)
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
        values[key.strip()] = _parse_scalar(raw_value.strip())
        index += 1
    return values, index


def _parse_sequence(lines: list[str], start: int) -> tuple[list[FrontmatterValue], int]:
    values: list[FrontmatterValue] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if not line.startswith((" ", "\t")):
            break
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped == "-":
            values.append(None)
            index += 1
            continue
        if not stripped.startswith("- "):
            raise FrontmatterParseError(f"Invalid sequence line: {stripped}")
        values.append(_parse_scalar(stripped[2:].strip()))
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
        if key in frontmatter:
            raise FrontmatterParseError(f"Duplicate frontmatter key: {key}")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key):
            raise FrontmatterParseError(f"Invalid frontmatter key: {key}")
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
                probe = index + 1
                while probe < len(lines) and (
                        not lines[probe].strip() or lines[probe].strip().startswith("#")):
                    probe += 1
                probe_line = lines[probe] if probe < len(lines) else ""
                probe_stripped = probe_line.strip()
                if probe_line.startswith((" ", "\t")) and (
                        probe_stripped == "-" or probe_stripped.startswith("- ")):
                    frontmatter[key], index = _parse_sequence(lines, index + 1)
                else:
                    nested_value, next_index = _parse_nested_mapping(lines, index + 1)
                    frontmatter[key] = nested_value if nested_value else ""
                    index = next_index
            case _:
                frontmatter[key] = _parse_scalar(value)
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
