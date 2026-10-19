# Historical GoLab refactor prompts (archived, non-operative)

These five files are agent task prompts written for the GoLab monitor GT-521S
refactor (spring 2026). They were moved here unchanged from `refactor/` on
October 19, 2026 (OCT19-DOCS-1, [bardbox#31](https://github.com/bardphysicslab/bardbox/issues/31)).

They are **provenance only**:

- Do not execute their commands or follow their instructions ("commit and
  push", Pi restarts, repository paths). They predate the current workflow and
  name documents that no longer exist (`capabilities-schema.md`,
  `pi-app-instructions.md`).
- They are not BardBox standards. Current rules live in the root
  [AGENTS.md](../../../AGENTS.md), [ARCHITECTURE.md](../../../ARCHITECTURE.md)
  and the standards they index.
- Workstation-specific paths inside them are historical and must not be copied
  into active documents.

| File | Original purpose |
| --- | --- |
| [refactor-instructions.md](refactor-instructions.md) | Audit and phased refactor plan for the GoLab dashboard |
| [fix-gt521s-driver-refactor.md](fix-gt521s-driver-refactor.md) | Consolidate GT-521S protocol logic into the driver |
| [fix-gt521s-start.md](fix-gt521s-start.md) | Start/data-flow repair after the refactor |
| [fix-gt521s-wake-logic.md](fix-gt521s-wake-logic.md) | Wake logic matching observed device behavior |
| [pr10-review-checklist.md](pr10-review-checklist.md) | Review checklist for that refactor PR |

The legacy driver they produced is described in
[drivers/gt521s_driver/README.md](../../../drivers/gt521s_driver/README.md);
its known drift is tracked in [bardbox#49](https://github.com/bardphysicslab/bardbox/issues/49).
