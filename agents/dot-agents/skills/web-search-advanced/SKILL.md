---
name: web-search-advanced
description: >
  Advanced web research using Exa tools. Use this whenever the user needs
  external sources or up-to-date info: market/competitor scans, company or
  people research, academic papers, financial filings, tweet or social
  sentiment summaries, or authoritative code examples from
  docs/GitHub/StackOverflow. Trigger even if they do not say "search"
  explicitly whenever the task depends on web discovery, citations, or
  multiple third-party sources (e.g., "find 15 competitors," "latest
  10-K/10-Q," "pull LinkedIn profiles," "recent arXiv papers," "tweet
  sentiment"). Avoid for tasks limited to local files, pasted data,
  reasoning-only questions, or when the user already provided the exact URLs
  and asks for summaries only. Explicit GitHub questions use github-kb first;
  use this skill only for any additional broader web research.
---

# Web Search Advanced

Use Exa advanced tools to gather high-signal sources and return distilled results with citations. Prefer precision, deduplication, and compact outputs over dumping raw search results.

## Routing and capability discovery

For explicit GitHub repository, issue, PR, release, or README questions, load
`../github-kb/SKILL.md` and follow its gh evidence workflow and output template.
Use this skill for additional web research beyond GitHub when the request needs it;
merge those findings into the GitHub answer. Do not replace gh evidence with Exa snippets.

Before searching, inspect the host's available tool inventory and input schemas.
Discover tools by capability, allowing provider-prefixed names; do not assume the
following names or every field in a reference are exposed:

- Code examples or API usage → prefer `get_code_context_exa`.
- Scholarly work → prefer `web_search_advanced_exa`, category `publication`.
- Filings → category `financial report`; people → `people`; companies → `company`.
- Social posts → use a supported social category/hint or general search with X URLs verified.
- General research → advanced search with no category, type `auto`.

If advanced search is absent, use available `web_search_exa` and a content-fetch
capability (such as `web_fetch_exa`) within their advertised schemas. If code
context is absent, search official documentation and retrieve the relevant pages.
If Exa is unavailable, use the host's available web search and page retrieval tools;
state that fallback and any unavailable filters or freshness guarantees. If no
search/retrieval tool is available, state the limitation and request source text
or an enabled capability. Never invent results, tool calls, or unsupported fields.
Advanced search may be opt-in. If enablement is needed, explain the official
[MCP setup](https://exa.ai/docs/reference/exa-mcp): a hosted connection can expose
it with `https://mcp.exa.ai/mcp?tools=web_search_exa,web_fetch_exa,web_search_advanced_exa`.
An explicit tools list replaces defaults; preserve any other tools the user needs.
After a user-authorized configuration change, reconnect/restart the client and
rediscover schemas. Do not assume this URL also enables code context or that an
omitted tool is globally removed. Do not change connector configuration or install
tools just to satisfy this skill; use the supported fallback meanwhile.

## Context management

Check whether Task/general-purpose delegation exists and is permitted by the host
and the current request. When available, prefer delegating substantial searches;
workers search, deduplicate, and return distilled findings with source URLs and
uncertainties. If delegation is absent or prohibited, search directly with small
result batches and bounded content, summarizing each batch before continuing.
Do not fail solely because Task is unavailable or invent a Task/subagent type.

## Query strategy

- Generate **2–3 query variations** for coverage. Run them in parallel and dedupe.
- Tune `numResults` to user intent:
  - “a few” → 10–20
  - “comprehensive” → 50–100
  - explicit number → match it
  - ambiguous → ask “How many results should I return?”

## API semantics and compatibility

If choosing filters or freshness options, read `references/api-compatibility.md` first.
It records the official API baseline checked on 2026-10-27, deprecations, and the
boundary between the API and MCP connector schemas. Pass only fields exposed by
the selected tool. Inspect warnings and notices; do not claim ignored filters
were enforced. Retrieve and read relevant source content before citing claims.

If results are insufficient or content is auth-gated, state the gap and use
available public sources; request alternative sources or access only if needed.

## Gotchas

- Publication time and retrieval freshness answer different questions.
- Deprecated crawl-date fields do not constrain results.
- An API field documented upstream may be missing or constrained in a connector.
- Apply the GitHub workflow's output template when it owns the question.

## Output format (default)

Honor any output format explicitly requested by the user. Otherwise, for web-research-only answers, return three sections. Category references refine the contents of these sections; they do not replace this structure:

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
