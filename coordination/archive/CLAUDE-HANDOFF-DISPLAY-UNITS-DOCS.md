# Claude handoff: display units and the PROPOSED JSON display configuration

- **Event:** `DISPLAY-UNITS-DOCS` (DISPLAY-UNITS-1 + DISPLAY-JSON-REVIEW-1), October 22, 2026. **Status:** complete, ready for Codex independent exact-head review. Documentation only.
- **Content head:** `2820a6dba5eaeaa7a364fd301cdf413fae356f52` on `claude/display-units-docs`, from clean `main` `936fc73` (verified before branching). This handoff is the next commit on the same branch; the PR head is that commit, pushed. The only change after `2820a6d` is this file. The branch was checked before every commit and push; there are no `main` writes.
- **PR:** [bardbox#72](https://github.com/bardphysicslab/bardbox/pull/72). Not merged; Claude does not self-merge.
- **Accepted scope:** [bardbox#31 comment 6342348125](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6342348125), identical to [Reference#9 comment 6342346009](https://github.com/bardphysicslab/BardBox-Reference/issues/9#issuecomment-6342346009). Reviewed contract and lifecycle: [Rendering #71](https://github.com/bardphysicslab/bardbox/issues/71); Registry module tracker [#10](https://github.com/bardphysicslab/bardbox/issues/10).
- **App:** [BardBox-Reference#27](https://github.com/bardphysicslab/BardBox-Reference/pull/27), merged at `85cc96c` after independent review. No Reference writes in this pass.
- **Previous handoff** (CARD-GROUPS-DOCS, PR #70): archived at [archive/CLAUDE-HANDOFF-CARD-GROUPS-DOCS.md](CLAUDE-HANDOFF-CARD-GROUPS-DOCS.md). Only its one relative link path changed (to the sibling archive file).
- **Kept as is:** the historical `codex/registry-identity-docs@28d97a3` ref and PR52's records.

## What changed

1. **`docs/web-ui-standard.md`**
   - **New "Display units" section**, a cross-project rule:
     - **Switches:** neutral Metric/Imperial and Celsius/Fahrenheit switches above the Dashboard cards and Device settings rows; one saved application-wide preference, not per user; metric/Celsius default; a choice shown only after a confirmed save.
     - **Display:** one displayed decimal, units explicit; stored values, domain settings, history and evaluation keep canonical units and full precision.
     - **Edits:** captured edit units; untouched limits kept exactly; only edited values converted before the owner's unchanged validation; a Units change never reinterprets or discards a draft.
     - **Supported quantities:** temperature follows its explicit choice, and other or unknown quantities keep their declared units, so Metric/Imperial currently changes nothing visible.
     - **Ownership:** Processing does pure conversion; Rendering owns the versioned JSON preference and its I/O, separate from the pure HTML functions; shipped defaults are separate from the installation file; saves are revision-checked, atomic and read back; bad or newer files are kept, warned about and not written; the Controls hook is unchanged with no roles added.
     - **Detail:** links #71 and Reference PR27 instead of copying the contract.
   - **Layout configuration:** the YAML sketch is replaced by a **PROPOSED** JSON illustration. Only its `units` part is implemented today; the `card` part is loaded by nothing. Design notes cover owner-qualified field IDs, owner-declared ranges, ordered lists and visibility, defaults versus installation, and version handling. Applicability, unknown fields, hide/feature conflicts and any always-visible group are listed as **still open**, with no precedence rule or mandatory group decided. The engine and display-selection page stay future.
   - **Cross-links:** the Device settings bullet and the BNG example now link the Display units section.
   - **Unchanged:** the card order, ten folders, featured-once, colours, Alarm ownership and freezer page removal.
2. **`docs/architecture-map.md`:** the display-selections ownership row, the "Processing, units and time" paragraph and the configuration inventory row each note the Reference Units implementation; open items (field selection, timezone persistence) stay open.
3. **`ARCHITECTURE.md`:** the platform-direction bullet mentions the Units section and links the Rendering #71 and Registry #10 trackers.
4. **`docs/testing-guide.md`:** a new display-units check list.
5. **`docs/DECISIONS.md`:** one new row linking the accepted comments, contract, refinement and trackers; earlier entries kept.
6. **`docs/firmware-api-continuation.md`:** a new latest entry; the previous entry becomes history and records its merge (`936fc73`, bardbox#70).

**Unchanged:** runtime code, Mermaid diagrams, firmware, hardware, deployment, auth roles, Archive placement, RKC/CESH runtimes and production Alarm design.

## Checks

- Local link and anchor check, run after this handoff was written, over the six changed docs, this handoff and all archived handoffs: 154 relative links, 0 broken.
- `git diff --check` passes. No private workstation, database or session details were added.

## Workspace

Canonical bardbox checkout, branch `claude/display-units-docs`; no other checkout or worktree created. Claude's Reference scratch server is stopped; its synthetic data is kept privately. The user preview was not touched.

## Next step

Codex reviews bardbox#72 at the exact head and merges after green checks.
