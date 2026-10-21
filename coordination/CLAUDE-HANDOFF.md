# Claude handoff: EDITABLE-FRAMES-OWNER-1 shared documentation

- **Event:** `EDITABLE-FRAMES-OWNER-1-DOCS`, October 21, 2026. **Status:** complete, ready for Codex independent exact-head review. Documentation only.
- **Branch:** `claude/editable-frames-owner-docs` from clean `main` `d93491c`. The PR, exact head and status are recorded in [#64](https://github.com/bardphysicslab/bardbox/issues/64). Not merged; Claude does not self-merge. The branch was checked before every commit and push; there are no `main` writes.
- **Acceptance:** [bardbox#31 comment 6323356438](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6323356438) and [bardbox#10 comment 6323356061](https://github.com/bardphysicslab/bardbox/issues/10#issuecomment-6323356061), identical to [Reference#9 comment 6323355685](https://github.com/bardphysicslab/BardBox-Reference/issues/9#issuecomment-6323355685). Pinned to engineering-standards `91a2d7c` and bardbox `d93491c`.
- **App:** [BardBox-Reference#22](https://github.com/bardphysicslab/BardBox-Reference/pull/22), merged at `59b6b7e`.
- **Previous handoff** (DOCS-RECONCILE, PR #65): archived at [archive/CLAUDE-HANDOFF-DOCS-RECONCILE.md](archive/CLAUDE-HANDOFF-DOCS-RECONCILE.md). Only one relative link path was changed (its OCT19-LAYOUT-1 link now points to the sibling file); the prose is unchanged.

## Changes

- **`docs/web-ui-standard.md`:**
  - **Generic rule:** missing *read-only* values show `—`, unframed. *Editable* values are framed, and an unassigned one is an empty frame with its label visible.
  - **Card top:** an unassigned Name or Location is an empty frame, superseding the labelled-dash wording.
  - **Edit rule:**
    - a new "Editable values are framed" bullet (a keyboard-accessible affordance; read-only UID, MAC, status, measurements and unavailable capabilities keep `—`);
    - Registry owns the optional owner;
    - Owner is editable in Identity, and is descriptive, not an account, permission or identity;
    - Name, Owner and hardware identity are independent;
    - UID/MAC are read-only on the card with no inline Registry link, and the top-navigation Registry list is their editor.
- **`docs/architecture-map.md`:**
  - **Registry list:** new registrations have no owner assigned, superseding the once-per-project CESH/RKC default. Existing explicit owners are kept.
  - **Dashboard card:** Owner is added to the in-place fields, with the same validation, revision and history, and empty clears it. Values are framed, and there is no inline UID link.
- **`ARCHITECTURE.md`:** the UI-flow summary says no assumed owner, with Owner editable in frames.
- **`docs/DECISIONS.md`:** a new EDITABLE-FRAMES-OWNER-1 row. It notes what it supersedes (the REG-UI-FLOW-1 owner default and the editable labelled dash), keeps the earlier rows, and records PR22 merged at `59b6b7e`.
- **`docs/testing-guide.md`:** the dashboard check now separates read-only dashes from empty editable frames.
- **`docs/firmware-api-continuation.md`:** a new **latest** entry with PR22's merge proof. The previous entry is labelled history, and its handoff link is repointed to the archive.

**Historical checkpoint prose is kept.** For example, the October 21 identity checkpoint still says "owner default", as history. No Mermaid block changed, so no render was needed. No runtime change.

## Checks

- **Local link and anchor check** over the changed docs, this handoff and all `coordination/archive/` files: see #64 for the result at the exact head.
- **`git diff --check`:** clean.

## State

- **Canonical checkout:** restored to `main` (`d93491c`) after the push.
- **Kept as is:** the historical `codex/registry-identity-docs@28d97a3` ref and PR52's records.
- **No Reference writes.**
- **My Reference scratch server on 8780 (PID 45848):** stopped after this handoff; its DB is kept. Port 8781 was not touched.

## Next step

Codex reviews the exact head. Merge after review; then the local sync.
