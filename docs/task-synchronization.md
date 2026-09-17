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

BardBox Tools supplies the offline audit, bounded live-read adapters, reviewed
identity policy, durable operation journal and opt-in Trello/GitHub senders.
Both senders are disabled by default. They require fresh source checks, a durable
single-attempt claim and read-back confirmation; ambiguous outcomes remain pending.
Their explicit best-effort race policy does not make remote writes atomic. GitHub
label replacement can overwrite a concurrent label edit after the source read.

These are building blocks for reviewed actions. The tooling includes durable
revision-pair guards, reviewed card-link and initial-baseline adoption, two-sided
direction planning and version-checked local policy storage. Coordinating policy,
journal and adoption during a complete run, proved-not-applied recovery and live
deployment validation remain unfinished. No status labels, Blocked lists,
schedules, credentials or bulk migration are installed automatically.

Deployment requires reviewed board/list mappings, classifications and credentials,
plus a live smoke test and an explicit operational choice about remaining remote
races. Template/project instructions should link this policy; do not copy mappings
or synchronization code into firmware or dashboards. The existing BardBox change
skill covers tracking and propagation; no rewrite is needed.
