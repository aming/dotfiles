---
name: github-kb
description: Answer questions about GitHub repositories, issues, pull requests, releases, or README/docs using the gh CLI to find and cite sources. Only trigger this skill when the user explicitly mentions GitHub; when they do, use it even if they don’t provide a full repo link. Prefer public repositories; if a repo is ambiguous, ask a quick clarifying question or propose the most likely repo and confirm.
---

# GitHub-KB

You help users answer questions about GitHub projects. Only use this skill when the user explicitly mentions GitHub. Use the gh CLI to locate relevant repos, issues, pull requests, release notes, and README content. Provide a concise answer with citations. If the user asks for more detail, produce a structured report.

## Compatibility

- Tooling: gh CLI (authenticated if needed)
- Scope: public repositories by default

## Core workflow

1) Confirm GitHub mention and identify the target repo(s)
- If the user did not mention GitHub explicitly, do not use this skill.
- If the user gives a URL or owner/repo, use it.
- If not, search GitHub and pick the best match:
  - Use: gh search repos "<keywords>" --limit 5
  - Choose the most relevant repo and confirm if ambiguous.
- If the question spans multiple repos, list them and ask which to focus on.

2) Gather evidence
- Prefer primary sources: issues, pull requests, releases, README, docs in the repo.
- Use targeted searches:
  - Issues/PRs: gh search issues "<query> repo:owner/repo" --include-prs --limit 10
  - PRs only: gh search prs "<query> repo:owner/repo" --limit 10
  - Releases: gh release list -R owner/repo
  - README content in the terminal: gh repo view owner/repo
- Search and list output locate sources; read their bodies before drawing conclusions or citing them:
  - Issue body: gh issue view <number> -R owner/repo
  - PR body: gh pr view <number> -R owner/repo
  - Add --comments to either view command when discussion is relevant.
  - Release notes: gh release view <tag> -R owner/repo
  - Latest release notes: gh release view -R owner/repo
- Read linked repository docs relevant to the claim as well. A browser launch is not retrieved evidence; verify the actual content and cite its source URL.
- Keep discussion, merged changes, and released behavior distinct; absence in a limited search does not prove a feature is unsupported.

3) Answer concisely with citations
- Provide a short answer first.
- Include 2-5 citations (issue/PR/release/README URLs) that back the answer.
- If evidence is weak or mixed, say so and explain what you checked.

4) Offer details on request
- If the user asks for more detail, provide the structured report below.

## Short answer format

Honor any output format explicitly requested by the user. Otherwise use this template for a short answer (the detailed report below replaces it when requested):

Short answer: <1-4 sentences>
Citations: <bullet list of URLs>

## Detailed report format

Use this when the user asks for details or a report.

# [Title]
## Summary
## Evidence (with links)
## Steps to reproduce or validate (if applicable)
## Recommendations / Next steps

## Guidance and edge cases

- If the user request is vague, ask one clarifying question after you identify the most likely repo.
- If there is no good evidence, state that clearly and suggest what to check next.
- If the user asks to search private repos, explain that you need access and how to provide it.

## Gotchas

- Use --include-prs for a combined issue/PR search; issues-only search omits PRs.
- Search titles and snippets locate evidence; they do not replace reading source bodies.
- For explicit GitHub questions, this workflow owns the final response format. If broader web research is also needed, use web-search-advanced for that portion and integrate its verified sources here.

## Examples

These examples are schematic, not researched answers. All bracketed claims and
OWNER/repo, number, and vX.Y.Z citation placeholders must be replaced with verified
content and real URLs from sources read in the current task. Never emit these
placeholder citations or illustrative claims as factual evidence.

**Example 1:**
Input: "Does the issuespl project on GitHub support webhooks?"
Output (schematic):
Short answer: [Conclusion supported by the README and issue/PR bodies actually read, with any uncertainty.]

Citations:
- [Relevant issue](https://github.com/OWNER/issuespl/issues/123)
- [Relevant PR](https://github.com/OWNER/issuespl/pull/456)

**Example 2:**
Input: "Give me a detailed report on the latest GitHub release of vercel/next.js."
Output (schematic):

# Latest GitHub release of vercel/next.js
## Summary
[Verified tag, release date, and principal changes from the release body.]
## Evidence (with links)
- [Release notes](https://github.com/vercel/next.js/releases/tag/vX.Y.Z): [Verified changes and caveats.]
## Steps to reproduce or validate (if applicable)
[Documented validation steps for the verified version, or explain why not applicable.]
## Recommendations / Next steps
[Actions justified by the release notes and the user's situation.]
