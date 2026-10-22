# Claude handoff: CARD-LAYOUT-DEMO-1 + SETTINGS-DIRECT-SAVE-1 shared documentation

- **Event:** `CARD-LAYOUT-DOCS`, October 22, 2026. **Status:** complete, ready for Codex independent exact-head review. Documentation only.
- **Branch:** `claude/card-layout-docs` from clean `main` `e090034`. The PR, exact head and status are recorded in [#64](https://github.com/bardphysicslab/bardbox/issues/64); the scope was recorded there before any edit ([comment 6340332935](https://github.com/bardphysicslab/bardbox/issues/64#issuecomment-6340332935)). Not merged; Claude does not self-merge. The branch was checked before every commit and push; there are no `main` writes.
- **Acceptance:** [bardbox#31 comment 6339948902](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6339948902), identical to [Reference#9 comment 6339948462](https://github.com/bardphysicslab/BardBox-Reference/issues/9#issuecomment-6339948462). Pinned to engineering-standards `91a2d7c` and bardbox `e090034`.
- **App:** [BardBox-Reference#25](https://github.com/bardphysicslab/BardBox-Reference/pull/25), merged at `c4f044a` after independent exact-head review.
- **Previous handoff** (DEVICE-SETTINGS-FEATURED-ONCE-DOCS, PR #68): archived at [archive/CLAUDE-HANDOFF-DEVICE-SETTINGS-FEATURED-ONCE-DOCS.md](archive/CLAUDE-HANDOFF-DEVICE-SETTINGS-FEATURED-ONCE-DOCS.md). Only one relative link path was changed (to the sibling archive file).
- **Kept as is:** the historical `codex/registry-identity-docs@28d97a3` ref and PR52's records.

## Changes

- **`docs/web-ui-standard.md`** (authoritative):
  - **Colour meanings:** ordinary values neutral; labels and units muted; amber for warning or disabled protection; red for active alarm or fault; green for enabled or positive; the editing feedback colours kept separate; every colour has a state label.
  - **Minimal content:** labels, values and controls only, with no invented explanations or tooltips; validation errors stay beside the editor.
  - **Card order:** the header with status at the right; featured values before controls, two per row, a value beside its range, numbers with units; each featured switch a full-width row; folders below; featured once. It is marked as platform direction, shown in Reference only as a simulated example, with no RKC/CESH adoption.
  - **Alarm state and switch (card top item 2, the Alarm control bullet, the frequent-control exception, the Alarm switch placement):** a featured alarm switch is a full-width card row labelled with its state; a switch that is not featured stays in the Alarm section, with the read-only indicator on the card. The older in-section-only placement is explicitly **superseded for featured controls**, with the records kept. Alarm keeps evaluation, delivery, meaning, permission and save. Not an implemented Alarm capability.
  - **Alarm reminder (reconciled with minimal content, from Codex's diff check):** the disabled state label stays and there is no automatic reminder text. The earlier mandatory on-card reminder ("Within range — alarm disabled. Re-enable when ready.") is marked superseded, with the switch-amendment link kept. The fresh/valid-evidence constraint is kept and now applies to any within-range indication. Delivery-not-evaluation, manual re-enable and the active-condition outline are unchanged. Architecture, map, testing guide and decision index were checked: none carries the reminder.
  - **Device settings:** Edit → Save/Cancel. Save persists directly; the Review/Confirm/Back step and arrows are superseded (record kept); old forms never save through Review or Back; the Registry identity review is unchanged.
- **`docs/architecture-map.md`:** the Dashboard card (settings Save/Cancel) and the Alarm ownership row (featured-switch supersession; Alarm keeps ownership).
- **`ARCHITECTURE.md`:** the UI-flow summary.
- **`docs/testing-guide.md`:** checks for settings Save, card order, minimal content and colours.
- **`docs/DECISIONS.md`:** a new CARD-LAYOUT-DEMO-1 + SETTINGS-DIRECT-SAVE-1 row (what it supersedes; Archive unresolved; no runtime adoption).
- **`docs/firmware-api-continuation.md`:** a new **latest** entry. The previous entry is labelled history, and its handoff link is repointed to the archive.

**Excluded:** Archive placement, which is unresolved. No Mermaid block changed, there is no runtime change, and no private paths or session details are published.

## Checks

- **Local link and anchor check** over the changed docs, this handoff and all `coordination/archive/` files: see #64.
- **`git diff --check`:** clean.

## State

- **Canonical checkout:** restored to `main` after the push.
- **No Reference writes.**
- **My Reference scratch server:** stopped after this handoff; its DB is kept. The user preview is updated separately by Codex.

## Next step

Codex reviews the exact head, then merges and does the local sync.
