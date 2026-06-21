# OpenAI Skill Metadata

`agents/openai.yaml` is machine/UI metadata for skill lists and chips. It is separate from helper-role markdown such as `agents/grader.md`, `agents/analyzer.md`, and `agents/comparator.md`; those helper files are instructions an agent may read, not metadata.

## Required Interface Fields

```yaml
interface:
  display_name: "Skill Creator"
  short_description: "Create and improve Codex skills"
  default_prompt: "Use $skill-name to ..."
```

- `display_name`: Human-facing skill name.
- `short_description`: Human-facing scan text, 25-64 characters.
- `default_prompt`: A short starter prompt. It must mention `$skill-name`, replacing `skill-name` with the actual skill frontmatter name.

## Optional Interface Fields

Only include optional fields when the user provides a real value.

- `icon_small`: Relative path to a small icon under `assets/`.
- `icon_large`: Relative path to a large icon under `assets/`.
- `brand_color`: Hex color for UI accents.

## Generation

Use `scripts/generate_openai_yaml.py` from the skill directory or from the repository root:

```bash
python3 skills/skill-creator/scripts/generate_openai_yaml.py <skill-dir> \
  --interface default_prompt="Use $skill-name to create a focused skill."
```

The generator rejects unknown interface keys and validates `short_description` length and `default_prompt` skill mention.
