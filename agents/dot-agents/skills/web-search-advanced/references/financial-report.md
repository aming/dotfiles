# Web Search Advanced - Financial Report Category

## Capability and compatibility

Prefer `web_search_advanced_exa` with the category described below.
Read `api-compatibility.md` before choosing fields. Follow the parent SKILL.md's
capability discovery, permitted-delegation/direct-search fallback, GitHub routing,
and Results / Sources / Notes answer structure. The examples below require the
advertised connector schema; use supported fields only and disclose lost controls.

## When to Use

Use `category: "financial report"` when you need:
- SEC filings (10-K, 10-Q, 8-K, S-1)
- Quarterly earnings reports
- Annual reports
- Investor presentations
- Financial statements

## Examples

SEC filings for a company:
```
web_search_advanced_exa {
  "query": "Anthropic SEC filing S-1",
  "category": "financial report",
  "numResults": 10,
  "type": "auto"
}
```

Recent earnings reports:
```
web_search_advanced_exa {
  "query": "Q4 2025 earnings report technology",
  "category": "financial report",
  "startPublishedDate": "2025-10-01T00:00:00Z",
  "numResults": 20,
  "type": "auto"
}
```

Specific filing type:
```
web_search_advanced_exa {
  "query": "10-K annual report AI companies",
  "category": "financial report",
  "includeDomains": ["sec.gov"],
  "startPublishedDate": "2025-01-01T00:00:00Z",
  "numResults": 15,
  "type": "deep"
}
```

Risk factors analysis:
```
web_search_advanced_exa {
  "query": "risk factors cybersecurity",
  "category": "financial report",
  "numResults": 10,
  "enableHighlights": true,
  "highlightsQuery": "What are the main cybersecurity risks?"
}
```
If the discovered schema exposes highlights only through a nested object, send
`contents: {highlights: {query: "What are the main cybersecurity risks?"}}` instead and
adapt the remaining fields to the schema (see `api-compatibility.md`).

## Output Format

Use the parent Results / Sources / Notes structure with these category details:

1) Results (company name, filing type, date, key figures/highlights)
2) Sources (Filing URLs)
3) Notes (reporting period, any restatements, auditor notes)
