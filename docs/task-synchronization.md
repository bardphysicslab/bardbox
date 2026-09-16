# GitHub and Trello task synchronization

GitHub owns technical specifications and issue identity. Trello owns human
priority, ownership and scheduling. Every actionable GitHub issue must have one
linked card on the configured project board. Pull requests are implementation
links, not automatically separate tasks.

## Deterministic status contract

Use one GitHub issue label for an open task:

| GitHub label/state | Trello destination |
| --- | --- |
| `bardbox:status:backlog` | Backlog |
| `bardbox:status:up-next` | Up Next |
| `bardbox:status:in-progress` | In Progress |
| `bardbox:status:blocked` | Blocked |
| Closed issue | Done (an already archived card is acceptable) |

An open/reopened issue without exactly one recognized status label needs a
human status decision; do not silently guess Backlog or retain Done. Closing an
issue takes precedence over old status labels. Work starting requires In Progress;
blocked work requires an exact blocker and unblock condition in the task.

A planning change originating in Trello must update the designated GitHub status
label as part of the same reviewed operation. If both sides changed since the
last synchronized revision, report a conflict instead of overwriting either.
This initial audit plans GitHub-to-Trello status differences only; it does not
infer which of concurrent edits represents the user's latest intent.

## Identity and duplicate prevention

Map repositories explicitly to boards and exact list IDs. Match a card using a
canonical `https://github.com/owner/repo/issues/number` link, never its title.
Adopt existing links before creating cards; include archived cards in discovery.
Multiple matches or ambiguous/missing destination lists are conflicts. Do not
create another card or silently move ownership across boards. A repository
transfer/rename or issue transfer requires explicit mapping migration.

## Audit and future automation

BardBox Tools `python -m bardbox_tools.task_sync snapshot.json` produces an offline,
read-only plan. Complete pagination and include archived cards before marking a
snapshot complete. It returns desired moves/creations with issue/card revisions,
or conflicts. Exit 0 means no differences among the explicitly inventoried
issues; 1 means actions/conflicts; 2 means invalid inventory. This is not proof
that an incomplete or manually misclassified source export has no missing tasks.

A future writer must re-read both sides and verify stored revisions immediately
before a mutation. Re-check duplicate identity before creation and after uncertain
responses; never blindly retry a create. Preserve human descriptions, members,
labels, due dates and checklist content. Record a durable identity/revision map
and operation result, and suppress its own event echoes. Conflicting source
changes, partial pagination, access failures and rate limits halt the affected
operation. Do not treat missing read access as deleted tasks.

This change supplies policy and a tested offline audit only. It does not install
labels, create missing Blocked lists, schedule network synchronization, or perform
bulk changes. Live connector collection, concurrency-safe writes and existing-card
migration remain follow-up work. Deployment requires reviewed board/list mappings
and credentials. Template/project instructions should link this canonical policy;
do not maintain independent mappings in firmware or dashboards. The existing
BardBox change skill already covers tracking and propagation; no rewrite needed.
