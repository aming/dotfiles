# People Research

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
- Ambiguous? Ask: "How many profiles would you like?"

## Query Variation

Exa returns different results for different phrasings. For coverage:
- Generate 2-3 query variations
- Run in parallel
- Merge and deduplicate

## Categories

Use appropriate Exa `category` depending on what you need:
- `people` → LinkedIn profiles, public bios (primary for discovery)
- `personal site` → personal blogs, portfolio sites, about pages
- `news` → press mentions, interviews, speaker bios
- No category (`type: "auto"`) → general web results, broader context

Start with `category: "people"` for profile discovery, then use other categories or no category with `maxAgeHours` where exposed (see `api-compatibility.md`) for deeper research on specific individuals.

### Filters

Apply `api-compatibility.md`; inspect the connector schema rather than assuming
historical category restrictions. Publication-date windows are unavailable for
company and people discovery. For dated coverage, use news or general search
and verify dates in the retrieved sources.

## LinkedIn

Public LinkedIn via Exa: `category: "people"`, no other filters.
Auth-required LinkedIn → explain limitation and ask for alternative sources.

## Examples

### Discovery: find people by role
```
web_search_advanced_exa {
  "query": "VP Engineering AI infrastructure",
  "category": "people",
  "numResults": 20,
  "type": "auto"
}
```

### With query variations
```
web_search_advanced_exa {
  "query": "machine learning engineer San Francisco",
  "category": "people",
  "additionalQueries": ["ML engineer SF", "AI engineer Bay Area"],
  "numResults": 25,
  "type": "deep"
}
```

### Deep dive: research a specific person
```
web_search_advanced_exa {
  "query": "Dario Amodei Anthropic CEO background",
  "type": "auto",
  "maxAgeHours": 24,
  "numResults": 15
}
```

### News mentions
```
web_search_advanced_exa {
  "query": "Dario Amodei interview",
  "category": "news",
  "numResults": 10,
  "startPublishedDate": "2024-01-01T00:00:00Z"
}
```

## Output Format

Use the parent Results / Sources / Notes structure with these category details:

1) Results (name, title, company, location if available)
2) Sources (Profile URLs)
3) Notes (profile completeness, verification status)
