---
name: web-search-advanced
description: Advanced web research using Exa tools. Use this whenever the user needs external sources or up-to-date info: market/competitor scans, company or people research, academic papers, financial filings, tweet or social sentiment summaries, or authoritative code examples from docs/GitHub/StackOverflow. Trigger even if they do not say "search" explicitly whenever the task depends on web discovery, citations, or multiple third-party sources (e.g., “find 15 competitors,” “latest 10-K/10-Q,” “pull LinkedIn profiles,” “recent arXiv papers,” “tweet sentiment”). Avoid for tasks limited to local files, pasted data, reasoning-only questions, or when the user already provided the exact URLs and asks for summaries only.
---

# Web Search Advanced

Use Exa advanced tools to gather high-signal sources and return distilled results with citations. Prefer precision, deduplication, and compact outputs over dumping raw search results.

## Tool choices

Pick the narrowest tool/category that fits the task:

- **Code examples or API usage** → `get_code_context_exa`
- **Academic papers / arXiv / OpenReview / PubMed** → `web_search_advanced_exa` with `category: "research paper"`
- **SEC filings / earnings / annual reports** → `web_search_advanced_exa` with `category: "financial report"`
- **Tweets / X discussions** → `web_search_advanced_exa` with `category: "tweet"`
- **People / LinkedIn profiles / bios** → `web_search_advanced_exa` with `category: "people"`
- **Company discovery / competitors / funding** → `web_search_advanced_exa` with `category: "company"`
- **General web research** → `web_search_advanced_exa` with no category (`type: "auto"`)

If the user’s request spans multiple domains (e.g., company list + news + tweets), run separate targeted searches and merge results.

## Token isolation (critical)

Never run Exa searches in main context. Always spawn Task agents. Each agent should:

1. Run the Exa tool call(s).
2. Merge and deduplicate results.
3. Return only distilled output (brief markdown or compact JSON).

## Query strategy

- Generate **2–3 query variations** for coverage. Run them in parallel and dedupe.
- Tune `numResults` to user intent:
  - “a few” → 10–20
  - “comprehensive” → 50–100
  - explicit number → match it
  - ambiguous → ask “How many results should I return?”

## Category-specific restrictions (must follow)

- **Universal:** `includeText` and `excludeText` only allow **single-item arrays**. Multi-item arrays cause 400 errors.
- **company category:** do **not** use `includeDomains`, `excludeDomains`, or date filters.
- **people category:** no date filters, no `includeText`/`excludeText`, no `excludeDomains`, and `includeDomains` only for LinkedIn.
- **tweet category:** no `includeText`, `excludeText`, `includeDomains`, `excludeDomains`, or `moderation`.
- **financial report category:** `excludeText` is not supported.

If Exa returns insufficient results or content is auth-gated, say so and ask the user for alternative sources or access.

## Output format (default)

Return three sections:

1) Results (structured list, concise)
2) Sources (URLs with 1-line relevance each)
3) Notes (uncertainty, conflicts, or gaps)

## Category references

Read the relevant reference file before running searches:

- `references/get-code-context.md`
- `references/research-paper.md`
- `references/financial-report.md`
- `references/tweet.md`
- `references/people-research.md`
- `references/company-research.md`
