# Code Context (Exa)

## Capability and compatibility

Prefer `get_code_context_exa` for external code research.
Read `api-compatibility.md` before choosing fields. Follow the parent SKILL.md's
capability discovery, permitted-delegation/direct-search fallback, GitHub routing,
and Results / Sources / Notes answer structure. The examples below require the
advertised connector schema; use supported fields only and disclose lost controls.

## When to Use

Use this tool when programming work requires external discovery or current,
authoritative examples. Local code edits, supplied snippets, and reasoning-only
questions do not trigger this workflow. Explicit GitHub questions follow github-kb
first; consult this reference only for broader external code research such as:
- API usage and syntax
- SDK/library examples
- config and setup patterns
- framework "how to" questions
- debugging when you need authoritative snippets

## Inputs (Supported)

`get_code_context_exa` supports:
- `query` (string, required)
- `tokensNum` (number, optional; default ~5000; typical range 1000–50000)

## Query Writing Patterns (High Signal)

To reduce irrelevant results and cross-language noise:
- Always include the **programming language** in the query.
  - Example: use **"Go generics"** instead of just **"generics"**.
- When applicable, also include **framework + version** (e.g., "Next.js 14", "React 19", "Python 3.12").
- Include exact identifiers (function/class names, config keys, error messages) when you have them.

## Dynamic Tuning

Token strategy:
- Focused snippet needed → tokensNum 1000–3000
- Most tasks → tokensNum 5000
- Complex integration → tokensNum 10000–20000
- Only go larger when necessary (avoid dumping large context)

## Output Format

Follow the parent's Results / Sources / Notes structure:

1) Results: minimal working snippets with a brief explanation.
2) Sources: verified URLs supporting each approach; retrieve official documentation
   when returned context lacks a usable source. Never invent a source link.
3) Notes: versions, constraints, gotchas, and evidence gaps.

Before presenting, deduplicate similar results and keep the best representative
snippet per approach. GitHub-owned answers instead follow github-kb's template.
