# Shared engineering guidance

This directory is the single maintained copy of the engineering guidance
shared by Bard Physics Lab repositories. Other repositories reference it from
their root `AGENTS.md`; they do not copy it.

This repository is public. Do not add private hostnames, paths, account names,
credentials or personal contact details here.

## What to read

Agent tools do not load these files automatically, and a Markdown link loads
nothing. Open and read each file that applies:

| File | When |
| --- | --- |
| `development-workflow.md` | Always, before planning or delegating work |
| `agent-practice.md` | Before any change |
| `checkouts-and-worktrees.md` | Before choosing, creating or ending a checkout |

Then read the repository's own root `AGENTS.md` and `ARCHITECTURE.md`, and the
documents they require. BardBox device and platform projects also read this
repository's root `AGENTS.md` and `ARCHITECTURE.md`.

## Version: one SHA per task

At the start of each task, resolve `main` of `bardphysicslab/bardbox` to one
commit SHA. Read every shared file at that SHA, never from a working tree,
which may hold unpublished edits.

- **Local clone:** run `git -C <clone> fetch origin main`, then
  `git -C <clone> rev-parse origin/main`. Read files with
  `git -C <clone> show <sha>:docs/engineering/<file>`.
- **No local clone:** get the SHA with
  `gh api repos/bardphysicslab/bardbox/commits/main --jq .sha`. Read files with
  `gh api "repos/bardphysicslab/bardbox/contents/docs/engineering/<file>?ref=<sha>" -H "Accept: application/vnd.github.raw"`.

Record `Shared guidance: bardphysicslab/bardbox@<sha>` once, in the task's
durable evidence: the handoff, pull request, commit message or the
repository's dated evidence record. Keep using that SHA for the rest of the
task.

Copies are not authoritative. That includes chat project sources, desktop
files, agent memory and earlier conversations.

## If the guidance cannot be read

- **The fetch fails but a local `origin/main` exists:** resolve the SHA from
  it. Record that SHA and say it may be stale.
- **No shared file can be read at a resolved SHA:** read-only investigation
  and reporting may continue. Do not implement, commit, push, deploy or end
  checkouts until the guidance has been read, or until the maintainer
  explicitly says to proceed without it. Report which file could not be read.

## Precedence

Both supported agent tools combine instruction files into one context. They do
not resolve conflicts themselves, so these rules decide:

1. The maintainer's explicit instructions for the current task set its scope.
   Authorization covers only the actions it names.
2. For safety, data integrity, approvals, environment isolation and sources
   of truth, the most restrictive applicable rule wins, wherever it is written.
3. Otherwise, a topic-specific standard governs its topic over a general
   summary. A repository's root files govern its local facts: paths, commands,
   owners and architecture.
4. A repository may deviate from a shared rule only by naming that rule and
   giving the reason. Any other conflict means stop and ask.

## Changing this guidance

Change it here, by pull request. In the pull request, list the repositories
affected and any effect on how the tools load instructions. Keep an unchanged
move of existing text separate from a change in what the text requires. When
moving a file or section, leave a pointer at the old location.
