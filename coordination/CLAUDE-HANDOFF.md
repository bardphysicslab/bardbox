# Claude handoff: shared adoption principle, CONFIG-CARD-GROUPS-1 and BNG room examples

- **Event:** `CARD-GROUPS-DOCS`, October 22, 2026. **Status:** complete, ready for Codex independent exact-head review. Documentation only.
- **Content head:** `2672804584f068008def2db2c7e01b1e9543b592` on `claude/card-groups-docs`, from clean `main` `764473c`. This handoff is the next commit on the same branch, and the PR head is that commit, pushed. The only change after `2672804` is this file. The branch was checked before every commit and push; there are no `main` writes.
- **PR:** [bardbox#70](https://github.com/bardphysicslab/bardbox/pull/70). Not merged; Claude does not self-merge.
- **Accepted sources:** [bardbox#31 comment 6340809622](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6340809622) (shared-module adoption principle), [comment 6340776600](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6340776600) (BNG-ROOM-DASH-1 + SHARED-CARD-RULES-1, identical to Reference#9 comment 6340774553), [comment 6340973552](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6340973552) (CONFIG-CARD-GROUPS-1, identical to Reference#9 comment 6340974766).
- **App:** [BardBox-Reference#26](https://github.com/bardphysicslab/BardBox-Reference/pull/26), merged at `ee5477c` after independent review. No Reference writes in this pass.
- **Previous handoff** (CARD-LAYOUT-DOCS, PR #69): archived at [archive/CLAUDE-HANDOFF-CARD-LAYOUT-DOCS.md](archive/CLAUDE-HANDOFF-CARD-LAYOUT-DOCS.md). Only its one relative link path changed (to the sibling archive file).
- **Kept as is:** the historical `codex/registry-identity-docs@28d97a3` ref and PR52's records.

## What changed

1. **`ARCHITECTURE.md`:**
   - New section "Shared modules, safe adoption" directly after the introduction. It states the rule (improve once, adopt easily, preserve each instance's configuration, data and project behaviour), keeps project differences separate from shared code (example: Reference's Rendering layout versus its BNG example provider), and requires stable interfaces with explicit, tested migrations for incompatible changes. It says easy adoption is not automatic rollout, deployment, broad refactoring or forced upgrades.
   - The platform-direction bullet now describes the refined card order and the BNG examples.
2. **`docs/web-ui-standard.md`:**
   - **Card order** rewritten as a numbered cross-project rule: Name, Location, featured measurements in configured order with one measurement/range pair per row, full-width switches, automatic group folders. Featuring moves a field; a fully featured folder stays present and empty. It refines the earlier "two fields per row" wording.
   - **New "Groups, featuring and display configuration":** module-declared logical groups; Rendering builds the folders; presentation configuration (visibility, featuring, explicitly ordered) separate from domain settings and data, never changing ownership, save paths or identity. It also states current behaviour: all ten folders, featuring set in code, no engine or selection page, Name stays the heading label. A small YAML example is labelled **PROPOSED, not implemented** and is read by no runtime.
   - **New "Reference example: simulated BNG rooms":** registered synthetic devices, a separate persisted provider keyed to the stable device key, unavailable rather than default values, shared range/Alerts between the card and Device settings, SIMULATED/ALARM status with truthful Health, no delivery or production Alarm, freezer page removed, push-button Edit/Save/Cancel, Registry identity review unchanged, Archive unresolved.
   - **Device settings bullet:** push-button appearance; the example range/Alerts columns with validate-before-write and truthful partial saves, explicitly example settings and not Alarm settings.
3. **`docs/architecture-map.md`:** Device settings also edits the example provider's range and Alerts for the simulated rooms.
4. **`docs/testing-guide.md`:** the card-order check is updated to measurement/range rows and moved fields; a new check covers example or project-specific providers (round trip, validate before write, truthful partial save, unavailable storage, real devices never reinterpreted).
5. **`docs/firmware-api-continuation.md`:** a new latest entry for this pass; the previous entry becomes history and records its merge (`764473c`, bardbox#69) and its refinement.
6. **`docs/DECISIONS.md`:** one new row after CARD-LAYOUT-DEMO-1 linking all three accepted comments; earlier entries kept.

**Unchanged:** runtime code, Mermaid diagrams, firmware, hardware, deployment, RKC/CESH runtimes, auth, the production Alarm design, Registry identity review and Archive placement.

## Checks

- Local link and anchor check over the six changed docs and all archived handoffs: 145 relative links, all resolving once this handoff exists (the continuation entry links it).
- `git diff --check` passes. No private workstation, database or session details were added.

## Workspace

- Canonical checkout, branch `claude/card-groups-docs`. No other checkout or worktree was created.
- Claude's own Reference scratch server (port 8780) is stopped; its synthetic databases are kept in Claude's session scratch area. The user preview was not touched; its update is Codex's.

## Next step

Codex reviews bardbox#70 at the exact head and merges after green checks.
