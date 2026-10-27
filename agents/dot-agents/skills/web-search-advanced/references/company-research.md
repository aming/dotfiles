# Company Research

## Capability and compatibility

Prefer `web_search_advanced_exa` with the category described below.
Read `api-compatibility.md` before choosing fields. Follow the parent SKILL.md's
capability discovery, permitted-delegation/direct-search fallback, GitHub routing,
and Results / Sources / Notes answer structure. The examples below require the
advertised connector schema; use supported fields only and disclose lost controls.

## Dynamic Tuning

No hardcoded numResults. Tune to user intent:
- User says "a few" → 10-20
- User says "comprehensive" → 50-100
- User specifies number → match it
- Ambiguous? Ask: "How many companies would you like?"

## Query Variation

Exa returns different results for different phrasings. For coverage:
- Generate 2-3 query variations
- Run in parallel
- Merge and deduplicate

## Categories

Use appropriate Exa `category` depending on what you need:
- `company` → homepages, rich metadata (headcount, location, funding, revenue)
- `news` → press coverage, announcements
- Social search → public commentary; follow `tweet.md` for category discovery
- `people` → LinkedIn profiles (public data)
- No category (`type: "auto"`) → general web results, deep dives, broader context

Start with `category: "company"` for discovery, then use other categories or no category with `maxAgeHours` where exposed (see `api-compatibility.md`) for deeper research.

### Filters

Apply `api-compatibility.md`; inspect the connector schema rather than assuming
historical category restrictions. Publication-date windows are unavailable for
company and people discovery. For dated coverage, use news or general search
and verify dates in the retrieved sources.

## LinkedIn

Public LinkedIn via Exa: `category: "people"`, no other filters.
Auth-required LinkedIn → explain limitation and ask for alternative sources.

## Examples

### Discovery: find companies in a space
```
web_search_advanced_exa {
  "query": "AI infrastructure startups San Francisco",
  "category": "company",
  "numResults": 20,
  "type": "auto"
}
```

### Deep dive: research a specific company
```
web_search_advanced_exa {
  "query": "Anthropic funding rounds valuation 2024",
  "type": "deep",
  "maxAgeHours": 24,
  "numResults": 10,
  "includeDomains": ["techcrunch.com", "crunchbase.com", "bloomberg.com"]
}
```

### News coverage
```
web_search_advanced_exa {
  "query": "Anthropic AI safety",
  "category": "news",
  "numResults": 15,
  "startPublishedDate": "2024-01-01T00:00:00Z"
}
```

### LinkedIn profiles
```
web_search_advanced_exa {
  "query": "VP Engineering AI infrastructure",
  "category": "people",
  "numResults": 20
}
```

## Output Format

Use the parent Results / Sources / Notes structure with these category details:

1) Results (structured list; one company per row)
2) Sources (URLs; 1-line relevance each)
3) Notes (uncertainty/conflicts)
