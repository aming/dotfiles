---
name: para
description: Use this skill whenever the user asks to organize, classify, audit, create, move, rename, or clean up notes, files, folders, tasks, projects, or a knowledge base using PARA, Projects/Areas/Resources/Archive, Second Brain organization, actionability-based filing, inbox triage, or knowledge routing. For ACE vaults, defer routing and meeting-note placement to the ACE skill. PARA covers non-ACE PKM. This skill is especially important for non-ACE Obsidian vaults, personal knowledge management systems, workspace folder structures, project dashboards, and note migrations, even when the user does not explicitly say "PARA" but asks where something should live or how to keep information organized.
---

# PARA Organization

Organize information by actionability so the user can find the material needed for current work without maintaining a fussy taxonomy. PARA is a routing system, not a decorative folder scheme: each destination should make the next action, responsibility, reference use, or inactive state clearer.

## Activation Precedence

For an ACE vault (local rules identify ACE, or the established `+`, `Atlas`, `Calendar`, `Efforts` layout does), use the **ACE skill** for PKM routing and organization. PARA covers non-ACE PKM and ordinary PARA workspaces; do not impose Projects/Areas/Resources/Archives on an ACE vault. Meeting-note routing also defers to the ACE skill inside ACE vaults, including its Calendar/Meetings conventions and links to relevant Efforts. If the user explicitly requests a migration from ACE to PARA, treat that as a migration task and establish the target mapping first.


## Source Basis

This skill follows the PARA method's core idea: organize information around current projects and goals rather than broad school-style subjects. Use local workspace rules first, then apply the general PARA decision model.

If the task involves a large audit, migration, ambiguous Area-vs-Resource decisions, or more than 10 items, read `references/routing-decision-guide.md` before deciding routes.

## Default Workflow

1. Identify the surface and scope.
   - Determine whether the user wants an explanation, a routing recommendation, a concrete note/file move, a folder structure, an audit, or a migration.
   - For a vault, repository, drive, or folder system, read local operating rules first: `AGENTS.md`, `README.md`, existing top-level folders, and relevant index notes.
   - For Obsidian note operations, use the Obsidian skill or an Obsidian-aware workflow before raw filesystem moves.

2. Classify by current actionability.
   - Ask what the item helps the user do next, maintain, reuse, or preserve.
   - Prefer current actionability over topic. A note about "career" can be a Project, Area, Resource, or Archive depending on its role today.
   - If the route is unclear, place the item in an inbox or return a routing question rather than forcing a false category.

3. Apply the PARA decision ladder.
   - `Projects`: finite active outcomes with a clear desired result. These should usually have next actions, deadlines, deliverables, owners, or success criteria.
   - `Areas`: ongoing responsibilities or standards to maintain. These have no fixed endpoint and need periodic review.
   - `Resources`: reusable reference material, examples, templates, research, or interests that may support future work but are not active responsibilities.
   - `Archives`: inactive, completed, paused, obsolete, or no-longer-relevant items preserved for lookup.
   - `Inbox`: raw capture or uncertain routing. Include what is unknown and what would decide the final location.

4. Respect local overlays.
   - If the workspace defines support layers such as daily notes, system folders, templates, attachments, administration, or automation guidance, keep those layers intact.
   - Do not force operating rules into `Resources` when the workspace has a dedicated system or administration location.
   - Use daily notes for chronological traceability; do not make them the canonical home for durable knowledge.

5. Execute safely when action is requested.
   - For a single clear item, route or move it directly and verify the result.
   - For bulk changes, produce a move plan first unless the user already approved the exact mapping.
   - In Obsidian, automatic internal-link updates require the vault setting **Automatically update internal links** to be enabled; otherwise plan explicit link updates and verification.
   - Prefer reversible, link-aware moves. Preserve backlinks, aliases, frontmatter, source context, and indexes.
   - Update related overview or index notes when that is the local convention.

6. Verify and report.
   - Read back changed files or changed sections.
   - Check links, backlinks, unresolved references, or indexes when moves could affect navigation.
   - Report what changed, what remains, what is blocked, and any items left in inbox because classification was uncertain.

## Routing Tests

Use these questions in order:

1. Does this support a finite active outcome with an end state?
   - Yes: `Projects`.
2. Is the user responsible for keeping this healthy, current, reviewed, or operational?
   - Yes: `Areas`.
3. Is this mainly something to learn from, cite, reuse, or consult later?
   - Yes: `Resources`.
4. Is this completed, paused, obsolete, superseded, or retained only for history?
   - Yes: `Archives`.
5. Is important routing context missing?
   - Yes: `Inbox`, with a short note explaining the missing decision.

## Common Patterns

| Item | Default route | Reason |
|---|---|---|
| Launch plan, incident response, job application, tax filing for this year | `Projects` | Finite active outcome |
| Health, finances, household maintenance, career development, recurring reviews | `Areas` | Ongoing responsibility or standard |
| How-to guide, article notes, template, example, reusable research, checklist pattern | `Resources` | Reusable reference without maintenance obligation |
| Completed project, closed incident, old planning snapshot, superseded research | `Archives` | Inactive but worth preserving |
| Raw meeting note, unsorted clipped text, unclear download | `Inbox` | Needs triage before canonical placement |

## Area vs Resource

This is the most common mistake. Use responsibility as the tie-breaker.

- `Areas`: "I am responsible for keeping this true, healthy, current, or operational."
- `Resources`: "I may want to reuse or consult this later."

Examples:
- An active household maintenance checklist belongs in `Areas` when the user is responsible for keeping it current.
- A generic checklist template belongs in `Resources`.
- A monthly budget process the user maintains belongs in `Areas`.
- A saved article about budgeting belongs in `Resources`.

## Project vs Area

Projects should turn over. Areas persist.

- If it can be completed and celebrated, it is probably a Project.
- If it repeats indefinitely or defines a standard, it is probably an Area.
- If an Area is too broad, extract active Projects from it rather than filing everything under the Area.
- If a Project becomes a continuing responsibility, move or summarize it into the relevant Area after completion.

## Output Formats

For a routing recommendation, use:

```markdown
## PARA Routing

| Item | Destination | Confidence | Reason | Next action |
|---|---|---:|---|---|
| item name | `01-Projects/example` | High | Finite active outcome with due date | Move note and update project index |

## Assumptions
- ...

## Open Questions
- ...
```

For a migration plan, use:

```markdown
## Migration Plan

## Assumptions
## Proposed Mapping
## Moves Requiring Confirmation
## Index/Backlink Updates
## Verification
## Rollback Notes
```

For completed changes, use:

```markdown
Updated:
- `path/to/file.md` - what changed

Verification:
- Read back changed files.
- Checked relevant links or indexes.

Remaining:
- Items left in inbox or needing user confirmation.
```

## Gotchas

- Do not route by broad subject alone. Route by how the item is used now.
- Do not bury an active Project under an Area just because the topic matches.
- Do not make every interesting topic into an Area; Areas carry maintenance responsibility.
- Do not put active maintenance procedures into Resources when they govern an ongoing responsibility.
- Do not delete instead of archiving unless the user explicitly asks for deletion.
- Do not perform bulk moves without a clear mapping, link-aware method, and verification step.
- Do not create a second PARA root when the workspace already has one.
- Do not treat daily notes as canonical storage. They are chronological pointers.
- Do not ignore local workspace conventions. A local `AGENTS.md` or deeper rule can override generic PARA folder names.

## Examples

**Input:** "Where should I put notes for the Q3 promotion packet I need to submit?"
**Output:** Route to `Projects` because it is a finite active deliverable. Keep reusable career evidence in an Area or Resource only if it outlives the packet.

**Input:** "I have a folder called Home Renovation with contractor notes, a current kitchen remodel plan, paint color research, and old warranty PDFs."
**Output:** Split by actionability: the active remodel plan goes to `Projects`, recurring home maintenance notes go to `Areas`, reusable design research goes to `Resources`, and expired or superseded warranties go to `Archives`.

**Input:** "Clean up these imported notes but I am not sure what half of them are."
**Output:** Classify clear items, put uncertain imports in `Inbox` or a holding bucket, and record what evidence is needed before final routing.
