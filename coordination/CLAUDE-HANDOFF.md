# Claude handoff: Registry and rendering documentation reconciliation

- **Event:** `DOCS-RECONCILE` (TRUE-INPLACE-EDIT-1, part 2), October 21, 2026. **Status:** complete, ready for Codex independent exact-head review. Documentation only.
- **PR:** [bardbox#65](https://github.com/bardphysicslab/bardbox/pull/65), branch `claude/registry-rendering-docs`. The exact head is the commit containing this file; it is recorded in [#64](https://github.com/bardphysicslab/bardbox/issues/64). Not merged; Claude does not self-merge.
- **Authority:** the [accepted reconciliation](https://github.com/bardphysicslab/bardbox/issues/64#issuecomment-6322822102), which authorizes publishing, and the Codex-approved [preservation plan](https://github.com/bardphysicslab/bardbox/issues/64#issuecomment-6322957422). Pinned to engineering-standards `91a2d7c` and bardbox `641b5c0`.
- **App part:** [BardBox-Reference#20](https://github.com/bardphysicslab/BardBox-Reference/pull/20), merged at `cc8808f` ([delivery](https://github.com/bardphysicslab/BardBox-Reference/issues/9#issuecomment-6323058396)).
- **The previous handoff** (OCT19-LAYOUT-1) is archived unchanged at [archive/CLAUDE-HANDOFF-OCT19-LAYOUT-1.md](archive/CLAUDE-HANDOFF-OCT19-LAYOUT-1.md). This was done by cherry-picking PR52's own rename commit `798d267`.

## Preservation

- **The local checkpoint `codex/registry-identity-docs@28d97a3`:** its four commits (`8639017`, `a825ee6`, `45e3b43`, `28d97a3`) are unchanged ancestors of this branch. The ref itself is not pushed, amended or rebased.
- **[PR52](https://github.com/bardphysicslab/bardbox/pull/52):** its docs commits are carried by `cherry-pick -x`:
  - `a1e1dd0`→`8973856`, `b417319`→`cc37a2e`, `eaf2b50`→`fb4a487`;
  - the docs part of `bc2f056`→`dd5b9f0`;
  - its archive rename `798d267`.
- **PR52's own handoff and review records** (`51c2b2e`, `9a72c56`, and the coordination part of `bc2f056`) stay on its pushed branch. PR52 stays open.
- **After the cherry-picks,** `web-ui-standard.md` equalled PR52's head plus main's newer BB-010 text.

## Reconciliation (`94b1a4d`, `40f05c2`, and this commit)

- **Web UI standard:**
  - In-place editing, explicitly superseding the single edit-home / display-only heading rule for featured Name/Location; that rule is kept as dated history.
  - Name/Location featured and also in Identity, with the same values.
  - The first-pass ten sections with dashes; future display selection, Featured, auto-hide and preferences.
  - The future Alarm-outside preference.
  - Contact state versus `LIVE`.
- **Architecture map:** one consolidated current-versus-target Registry paragraph (inline Add row, in-row Edit/review, Archive, archived-reuse warning, transitional UID/MAC corrections, deferred permanence). The "one panel" wording is superseded.
- **ARCHITECTURE:** a linked summary instead of duplicated detail, and the Presentation bullet is amended.
- **Decision index:** rows for REG-INLINE-ADD-1, REG-ARCHIVED-REUSE-WARN-1, REG-INLINE-EDIT-1, RENDER-SECTIONS-1 and TRUE-INPLACE-EDIT-1; the REG-MANAGE-1 panel placement is marked superseded.
- **uid-registry and node naming:** current-versus-target notes; firmware-tools#41 is marked superseded history.
- **Continuation:** the latest dated entry, with the earlier checkpoint labelled history. In this commit, PR20 is updated from "in review" to merged proof.

## Evidence

- **Audit of all maintained Markdown** (outside `coordination/` and the archive/review history) for the old placement and management wording. What remains is intended supersession notes and archived history. Firmware/provisioning "registration" references are unrelated.
- **Local link and anchor check** for the changed docs: passes. `git diff --check` is clean.
- **Mermaid 10.9.1:** all 3 `architecture-map.md` diagrams, including the 2 changed by `28d97a3`, parse and render in a browser.
- No runtime, hardware or deployment change or claim.

## State

- **Canonical checkout** `/Users/kornelispoort/Code/bardcollege/bardbox`: restored to `codex/registry-identity-docs@28d97a3`, clean, after each step. Other worktrees untouched.
- **No worker or watcher started.**
- **Process slip (reported to the reviewer):** a Reference handoff-only commit `bd13a9a` was pushed directly to BardBox-Reference `main` after PR20 had merged. It is coordination-file only. It was not force-pushed or rewritten; the remedy is the maintainer's choice.

## Next step

Codex reviews the exact PR #65 head. Claude fixes any findings and re-hands off here.
