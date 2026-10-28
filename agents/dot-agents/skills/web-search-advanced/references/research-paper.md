# Web Search Advanced - Research Paper Category

## Capability and compatibility

Prefer `web_search_advanced_exa` with the category described below.
Read `api-compatibility.md` before choosing fields. Follow the parent SKILL.md's
capability discovery, permitted-delegation/direct-search fallback, GitHub routing,
and Results / Sources / Notes answer structure. The examples below require the
advertised connector schema; use supported fields only and disclose lost controls.

## When to Use

Use `category: "publication"` when you need:
- Academic papers from arXiv, OpenReview, PubMed, etc.
- Scientific research on specific topics
- Literature reviews with date filtering
- Papers containing specific methodologies or terms

## Examples

Recent papers on a topic:
```
web_search_advanced_exa {
  "query": "transformer attention mechanisms efficiency",
  "category": "publication",
  "startPublishedDate": "2024-01-01T00:00:00Z",
  "numResults": 15,
  "type": "auto"
}
```

Papers from specific venues:
```
web_search_advanced_exa {
  "query": "large language model agents",
  "category": "publication",
  "includeDomains": ["arxiv.org", "openreview.net"],
  "numResults": 20,
  "type": "deep"
}
```

## Output Format

Use the parent Results / Sources / Notes structure with these category details:

1) Results (structured list with title, authors, date, abstract summary)
2) Sources (URLs with publication venue)
3) Notes (methodology differences, conflicting findings)
