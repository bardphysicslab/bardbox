# Claude handoff: DEVICE-SETTINGS-COMPARE-1 + FEATURED-ONCE-1 shared documentation

- **Event:** `DEVICE-SETTINGS-FEATURED-ONCE-DOCS`, October 21, 2026. **Status:** the two wording findings from Codex's review of `c46155a` are applied; ready for Codex exact-head review. Documentation only.
- **Branch:** `claude/device-settings-docs` from clean `main` `86a8b69`. The PR, exact head and status are recorded in [#64](https://github.com/bardphysicslab/bardbox/issues/64). Not merged; Claude does not self-merge. The branch was checked before every commit and push; there are no `main` writes.
- **Acceptance:** [bardbox#31 comment 6326655979](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6326655979), the combined scope, identical to [Reference#9 comment 6326655675](https://github.com/bardphysicslab/BardBox-Reference/issues/9#issuecomment-6326655675). Pinned to engineering-standards `91a2d7c` and bardbox `86a8b69`.
- **App:** [BardBox-Reference#24](https://github.com/bardphysicslab/BardBox-Reference/pull/24), merged at `2fd900e` after independent review (review-only `d97c36a`, 10 checks green).
- **Previous handoff** (EDIT-SAVE-FEEDBACK-1-DOCS, PR #67): archived at [archive/CLAUDE-HANDOFF-EDIT-SAVE-FEEDBACK-1-DOCS.md](CLAUDE-HANDOFF-EDIT-SAVE-FEEDBACK-1-DOCS.md). Only one relative link path was changed (to the sibling archive file).
- **Kept as is:** the historical `codex/registry-identity-docs@28d97a3` ref and PR52's records.

## Corrections after review (wording only)

Findings: [bardbox#31 comment 6326865323](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6326865323).
1. **Web UI standard, first-pass section set:** the future-Featured sentence no longer says "shown above the sections, still also inside their section". Placement is now decided: a featured field is shown above the sections and omitted from its section, while still belonging to that section's logical group (Name and Location to Identity), so featuring moves it rather than duplicating it. Only the selection itself remains future.
2. **Architecture map, Dashboard card:** the unframed / amber / green / no-visible-buttons sentences are now explicitly scoped to the **dashboard card's inline editing**. The Device settings table's explicit Edit, Review, Confirm, Back and Cancel labels are stated as accepted for that table only.

**Checks:** the focused link/anchor check and `git diff --check` were re-run (see #64). No runtime or Mermaid change.

## Changes

- **`docs/web-ui-standard.md`:**
  - **Card top:** a featured field appears only in the featured area, so Name and Location are no longer shown in Identity. This supersedes the featured-and-in-Identity rule.
  - **Edit rule:** Name and Location are edited only at the featured position; Owner and coordinates are edited in Identity.
  - **New "Device settings comparison page" bullet:**
    - the Registry table layout with in-row Edit → Review → Confirm / Back / Cancel;
    - UID first and read-only, and visible while editing (sticky on narrow screens);
    - no Add, Register or Archive;
    - explicit labels on this table page only, with dashboard editing kept for comparison on the same Registry values;
    - no Alarm settings, preferences or access control.
- **`docs/architecture-map.md`** (Dashboard card) and **`ARCHITECTURE.md`** (UI flow): featured once, and the Device settings page.
- **`docs/testing-guide.md`:** checks for featured once and for the settings table.
- **`docs/DECISIONS.md`:** a new combined row. It notes what it supersedes (the featured-and-in-Identity placement), that the paused FEATURED-ONCE-1 entry is resumed, and PR24 merged.
- **`docs/firmware-api-continuation.md`:** a new **latest** entry. The previous entry is labelled history, and its handoff link is repointed to the archive.

Superseded decisions are kept as history. No Mermaid block changed, and there is no runtime change.

## Checks

- **Local link and anchor check** over the changed docs, this handoff and all `coordination/archive/` files: see #64.
- **`git diff --check`:** clean.

## State

- **Canonical checkout:** restored to `main` after the push.
- **No Reference writes.**
- **My Reference scratch server on 8780:** stopped after this handoff; its DB is kept. Port 8781 was not touched.

## Next step

Codex reviews the exact head, then merges and does the local sync.
