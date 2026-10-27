# PARA Routing Decision Guide

Use this guide for large audits, migrations, or ambiguous routing decisions.

## Activation Precedence

See **Activation Precedence** in `SKILL.md`: ACE vaults defer PKM routing and meeting-note placement to the ACE skill; PARA covers non-ACE PKM and ordinary PARA workspaces, and a requested ACE-to-PARA conversion is a migration that establishes the target mapping first.


## Decision Tree

1. Is the item active right now?
   - If no, consider `Archives` unless it is reusable reference.
   - If yes, continue.

2. Does the item have a finish line?
   - Deliverable, event, launch, incident, ticket, filing, decision, proposal, trip, application, migration, report, or review cycle: `Projects`.
   - No fixed end: continue.

3. Does the user have an ongoing responsibility to maintain it?
   - Health, finances, career, home maintenance, relationships, review cadence, standards, recurring checklists, and active operating procedures: `Areas`.
   - No maintenance responsibility: continue.

4. Is it reusable reference?
   - Articles, research, templates, examples, snippets, general how-tos, learning notes, external references: `Resources`.
   - No clear future use: consider `Archives`.

5. Is the evidence insufficient?
   - Use `Inbox` or a named holding bucket. Add a note explaining the missing context.

## Evidence To Inspect

For each item, look for:

- Dates: due date, completion date, last touched date.
- Verbs: launch, submit, fix, decide, migrate, review, maintain, monitor, learn.
- Owners: user-owned, delegated, external reference only.
- Artifacts: checklist, decision log, template, meeting notes, research clipping, reference guide.
- Links: backlinks from active projects, daily notes, tasks, tickets, calendars, or issue trackers.
- Status words: active, blocked, waiting, done, paused, superseded, archived.

## Migration Safety

Before moving many notes or files:

1. Inventory current paths.
2. Build a proposed mapping table.
3. Mark low-confidence items for confirmation.
4. Choose the safest move tool for the surface. In Obsidian, automatic internal-link updates require **Automatically update internal links** to be enabled; otherwise plan explicit updates and verify affected links.
5. Preserve metadata, frontmatter, aliases, backlinks, and source context.
6. Update indexes, overviews, dashboards, and daily-note pointers if the workspace uses them.
7. Verify a sample first for large migrations.
8. Read back moved files and check unresolved links.

## Naming Defaults

Use existing conventions first. If the workspace has no convention, prefer:

- `01-Projects/<outcome-name>/`
- `02-Areas/<responsibility-name>/`
- `03-Resources/<topic-name>/`
- `04-Archives/<year-or-domain>/`
- `00-Inbox/`

Some vaults use singular names such as `02-Area` or numbered prefixes such as `04-Archive`. Match the local tree exactly.

## Review Cadence

Recommend cadence only when useful:

- Weekly: active Projects and next actions.
- Monthly: Areas and standards that need maintenance.
- Quarterly: Resources for pruning and consolidation.
- On completion: move Project material to Archive, or summarize durable operational knowledge into an Area.

## Common Edge Cases

- A project support note can live inside the Project while active, then become a Resource or Archive later.
- A completed project can leave behind a reusable template; archive the project and extract the template to Resources.
- An incident note is a Project during response, then Archive or postmortem after closure.
- A procedure is an Area artifact if it governs an active responsibility; it is a Resource only if it is generic advice or a reusable template.
- Meeting notes usually belong with the Project or Area they support. If that is unclear, use Inbox with a short routing note.
- Operating rules should follow local system or administration folders when present rather than being forced into Resources.
