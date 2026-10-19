# Claude handoff: editable-field UI rule

- **Milestone ID:** `EDIT-UI-1`
- **Task:** [accepted editable-field UI rule](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6274318475)
  (BB-003 supplement) on [bardbox#31](https://github.com/bardphysicslab/bardbox/issues/31).
- **Pull request:** [bardbox#52](https://github.com/bardphysicslab/bardbox/pull/52), branch
  `codex/editable-field-ui-rule` from task baseline `main` `34b8ae6` in the
  canonical BardBox checkout. The exact head is recorded in the pull request;
  this file does not embed its own hash.
- **Shared guidance:** bardphysicslab/engineering-standards@aa8454649fc2e8bb5ad50a5829f8d0cbda736442
- **BardBox standards:** bardphysicslab/bardbox@34b8ae6e7a9ee3340093b6091df7acfd97578b83
- **Roles:** Claude implemented (sole writer); Codex independently reviewed the
  exact head; the maintainer decides merge.
- **Previous milestone record:** [OCT19-LAYOUT-1 handoff](archive/CLAUDE-HANDOFF-OCT19-LAYOUT-1.md).

## Changes (documentation only)

- [Web UI standard, "Where editing controls live"](../docs/web-ui-standard.md#where-editing-controls-live):
  edit each setting in its owning module's UI section; in the card UI, name and
  location change only through Identity's Edit name and location button (other
  authorized owner interfaces are not ruled out); owners declare editable fields
  and permission; save through Controls, then read back; drafts survive refresh;
  honest failure and uncertain-outcome handling; no automatic exposure of
  configuration or secrets; a frequent operational control can sit on the main
  card only by an explicit accepted decision.
- Alarm-control placement (final, [accepted decision](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6274413539),
  superseding only the earlier prominent-slider placement): the enable/disable
  switch is inside the expandable Alarm section; the main card always shows a
  read-only "Alarm enabled"/"Alarm disabled" indicator (text plus color), not a
  toggle and distinct from the active `ALARM` condition and red outline. Disable
  semantics, manual re-enable, the truthful in-range reminder and the outline
  while disabled are unchanged. Reconciled in the card top area, module
  sections, editing-rule exception and alarm section; map row and DECISIONS
  link updated.
- [DECISIONS](../docs/DECISIONS.md) BB-003 link and the ARCHITECTURE presentation
  summary point to it.

## Open

Unchanged alarm open items: switch scope with several alarm rules, escalation
restart or resume on re-enable, toggle audit, exact wording and reminder gating.
No confirmation, hold or authentication workflow is selected.

## State

Documentation committed and pushed; reviewed with no blocking findings; not
merged; no runtime, Alarm, Escalation, authentication, firmware, pilot or
deployment change. The BardBox-Reference repository and its local demo were not
touched.

**Next action:** Codex records the final review; maintainer decides merge.
