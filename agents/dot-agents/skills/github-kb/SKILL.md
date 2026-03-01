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
  - Issues/PRs: gh search issues "<query> repo:owner/repo" --limit 10
  - PRs only: gh search prs "<query> repo:owner/repo" --limit 10
  - Releases: gh release list -R owner/repo
  - README: gh repo view owner/repo --web or gh api repos/owner/repo/readme (if needed)

3) Answer concisely with citations
- Provide a short answer first.
- Include 2-5 citations (issue/PR/release/README URLs) that back the answer.
- If evidence is weak or mixed, say so and explain what you checked.

4) Offer details on request
- If the user asks for more detail, provide the structured report below.

## Short answer format

ALWAYS use this template:

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

## Examples

**Example 1:**
Input: "Does issuespl support webhooks?"
Output:
Short answer: It appears issuespl does not document webhook support yet; I only found open discussion and no merged implementation. If you want, I can dig into recent PRs for activity. 
Citations:
- https://github.com/OWNER/issuespl/issues/123
- https://github.com/OWNER/issuespl/pull/456

**Example 2:**
Input: "Give me details on the latest release of vercel/next.js"
Output:
Short answer: The latest release includes fixes for X and Y and a new feature Z; details are in the release notes. 
Citations:
- https://github.com/vercel/next.js/releases/tag/vX.Y.Z
