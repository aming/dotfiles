# Web Search Advanced - Tweet Category

## Capability and compatibility

Prefer `web_search_advanced_exa` with the category described below.
Read `api-compatibility.md` before choosing fields. Follow the parent SKILL.md's
capability discovery, permitted-delegation/direct-search fallback, GitHub routing,
and Results / Sources / Notes answer structure. The examples below require the
advertised connector schema; use supported fields only and disclose lost controls.

## When to Use

Use social-post search when you need:
- Social discussions on a topic
- Product announcements from company accounts
- Developer opinions and experiences
- Trending topics and community sentiment
- Expert takes and threads

## Category choice

Current Exa lists no dedicated `tweet` enum. If the connector advertises a
supported social category, use it; otherwise search generally with platform and
handle terms, optionally constraining domains when exposed. Verify each X/Twitter
URL and source date. An accepted `tweet` hint does not guarantee exhaustive posts.
Use publication filters for the requested time window and `maxAgeHours` for
retrieval freshness where supported; these are separate controls.

## Examples

Recent tweets on a topic:
```
web_search_advanced_exa {
  "query": "X Twitter Claude Code MCP experience",
  "startPublishedDate": "2025-01-01T00:00:00Z",
  "numResults": 20,
  "type": "auto",
  "maxAgeHours": 0
}
```

Search with specific keywords (put keywords in query, not includeText):
```
web_search_advanced_exa {
  "query": "X Twitter launching announcing new open source release",
  "startPublishedDate": "2025-12-01T00:00:00Z",
  "numResults": 15,
  "type": "auto"
}
```

Developer sentiment (use specific query terms instead of excludeText):
```
web_search_advanced_exa {
  "query": "X Twitter developer experience DX frustrating painful",
  "numResults": 20,
  "type": "deep",
  "maxAgeHours": 0
}
```

## Output Format

Use the parent Results / Sources / Notes structure with these category details:

1) Results (tweet content, author handle, date, engagement if visible)
2) Sources (Tweet URLs)
3) Notes (sentiment summary, notable accounts, threads vs single tweets)

Important: Be aware that tweet content can be informal, sarcastic, or context-dependent.
