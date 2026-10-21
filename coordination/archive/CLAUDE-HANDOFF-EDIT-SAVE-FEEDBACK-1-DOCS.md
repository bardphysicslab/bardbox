# Claude handoff: EDIT-SAVE-FEEDBACK-1 shared documentation

- **Event:** `EDIT-SAVE-FEEDBACK-1-DOCS`, October 21, 2026. **Status:** complete, ready for Codex independent exact-head review. Documentation only.
- **Branch:** `claude/edit-save-feedback-docs` from clean `main` `5207bda`. The PR, exact head and status are recorded in [#64](https://github.com/bardphysicslab/bardbox/issues/64). Not merged; Claude does not self-merge. The branch was checked before every commit and push; there are no `main` writes.
- **Acceptance:** [bardbox#31 comment 6323916487](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6323916487), identical to [Reference#9 comment 6323915997](https://github.com/bardphysicslab/BardBox-Reference/issues/9#issuecomment-6323915997). Pinned to engineering-standards `91a2d7c` and bardbox `5207bda`.
- **App:** [BardBox-Reference#23](https://github.com/bardphysicslab/BardBox-Reference/pull/23), merged at `386271d` after independent review (review-only `233c867`, 10 checks green).
- **Previous handoff** (EDITABLE-FRAMES-OWNER-1-DOCS, PR #66): archived at [archive/CLAUDE-HANDOFF-EDITABLE-FRAMES-OWNER-1-DOCS.md](CLAUDE-HANDOFF-EDITABLE-FRAMES-OWNER-1-DOCS.md). Only one relative link path was changed (to the sibling archive file); the prose is unchanged.
- **Kept as is:** the historical `codex/registry-identity-docs@28d97a3` ref and PR52's records.

## Changes

- **`docs/web-ui-standard.md`:**
  - **Generic rule:** saved editable values are unframed at rest, with the frame on hover or focus; unassigned ones keep the subtle empty frame and label; missing read-only values keep `—`.
  - **Edit in place:** activating a value (click, tap or Enter) replaces it with its input; there are no adjacent Save/Cancel.
  - **New bullet, "No visible edit controls; server-confirmed feedback":**
    - an unchanged editor is neutral, and a changed draft is amber until confirmation;
    - Enter or Done submits, with related values together;
    - green appears only on a confirmed real change, then white with the frame gone, and a confirmed clear flashes the empty border;
    - green never comes from typing, optimistic state or a URL;
    - Escape restores without writing, an unchanged Enter is neutral, and nothing saves on blur;
    - a refusal keeps the amber draft with an error;
    - an uncertain outcome (no reply, an unreadable reply, or a storage error that may follow a commit) is re-read on every exit and never shown as saved;
    - no false cancel or double send, IME and keyboard support, and phone Done with leave/reload to abandon.
    - It explicitly supersedes the visible Save/Cancel (TRUE-INPLACE-EDIT-1) and the always-framed saved values (EDITABLE-FRAMES-OWNER-1); both records are kept. It links PR23.
  - **"Editable affordance" bullet:** replaces "Editable values are framed", which is superseded for saved values.
- **`docs/architecture-map.md`** (Dashboard card) and **`ARCHITECTURE.md`** (UI flow): describe server-confirmed feedback without visible buttons, with saved values unframed at rest.
- **`docs/testing-guide.md`:** dashboard checks for the unframed resting state and the amber → confirmed green → white sequence, the no-write exits, and refusal/uncertain behaviour.
- **`docs/DECISIONS.md`:** a new EDIT-SAVE-FEEDBACK-1 row, noting what it supersedes, with earlier rows kept and PR23 recorded as merged.
- **`docs/firmware-api-continuation.md`:** a new **latest** entry. The previous entry is labelled history, and its handoff link is repointed to the archive.

Historical decision prose is kept. No Mermaid block changed, and there is no runtime change.

## Checks

- **Local link and anchor check** over the changed docs, this handoff and all `coordination/archive/` files: see #64 for the result at the exact head.
- **`git diff --check`:** clean.

## State

- **Canonical checkout:** restored to `main` after the push.
- **No Reference writes.**
- **My Reference scratch server on 8780 (PID 50129):** stopped after this handoff; its DB is kept. Port 8781 was not touched.

## Next step

Codex reviews the exact head, then merges and does the local sync.
