# Exa API compatibility

Baseline checked: 2026-10-27; official public OpenAPI version 2.0.0.

Read this before selecting request fields. Sources:
- [Search API](https://exa.ai/docs/reference/search)
- [Contents API](https://exa.ai/docs/reference/get-contents)
- [OpenAPI schema](https://exa.ai/docs/exa-spec.yaml)
- [MCP tools and configuration](https://exa.ai/docs/reference/exa-mcp)

## Filters

- `includeText` and `excludeText` are deprecated. Their current API limit is 50
  entries each, up to 4096 characters per entry, with approximate word matching.
  Prefer query terms and verification of retrieved content. Do not infer a
  universal single-item limit or exact phrase matching.
- `startCrawlDate` and `endCrawlDate` are deprecated and ignored, with an
  `IGNORED_FIELD` warning. Do not send them or claim they constrain results.
- Use `startPublishedDate` / `endPublishedDate` for publication windows, using
  ISO 8601 timestamps. These are unsupported for `company` and `people`;
  `people` also rejects `excludeDomains`.
- Use `category: "publication"` for scholarly papers, preprints, and journals.
  `research paper` and `tweet` are not current enumerated categories; other
  strings may be accepted as hints, without category-specific guarantees.
- Domain filters are documented generally; do not preserve historical blanket
  company-domain, LinkedIn-only, tweet-filter, or financial-text restrictions
  without evidence from the actual connector schema or response.

## Retrieval freshness

Use `maxAgeHours` where exposed: `0` requests fresh retrieval, `-1` uses cache,
and a positive value tolerates cached content of that age (current maximum 720).
When omitted, cached content may be used and uncached pages fetched live.
In the HTTP Search API this lives under `contents`; in Contents requests it is
at the top level. MCP may expose a top-level `maxAgeHours` field.

`livecrawl` is deprecated, cannot accompany `maxAgeHours`, and does not guarantee
fresh retrieval. Do not use it as a freshness promise. If an older connector only
exposes legacy options, omit them by default and disclose that freshness could
not be controlled; use a separate page-fetch capability if available.
A fresh fetch of an old article is still an old publication: use publication
filters for recent material and verify dates in source content. A fresh fetch
can also fail; inspect per-URL status and do not claim success without evidence.

## Connector boundary

The discovered tool's schema governs what can be submitted. API documentation
does not imply every MCP wrapper exposes every field, category, or search type.
Examples in the category files describe advanced MCP requests, conditional on
schema support; adapt them rather than passing unknown fields. Keep `type: "auto"`
as the default. The current `lite` mode does not support live-fetch freshness
controls; use a compatible mode or a separate Contents request if needed. Use `deep` and `additionalQueries` only when exposed; upstream
`additionalQueries` is for deep-search variants. Do not advertise every field as
universally supported. For HTTP requests use the documented nested `contents`
shape rather than flattened MCP extraction flags.

If the schema is older, record that compatibility limit and use supported query
terms plus source verification. On a validation error, inspect the specific
error, remove/adapt only the unsupported field, and report lost constraints.
Inspect response warnings/notices for ignored fields or relaxed restrictions.
Tool/delegation fallback and answer structure come from the parent SKILL.md.
