# Claude handoff: annotated application layout

- **Milestone ID:** `OCT19-LAYOUT-1`
- **Task:** [bardbox#31](https://github.com/bardphysicslab/bardbox/issues/31),
  [BB-004](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271296848),
  [critique dispositions](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271384280),
  composition [owner supplement](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271666389) (first named Application),
  [naming refinement](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271757925) (module renamed Composition, folder `composition/`),
  [science-location clarification](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271713054).
- **Shared guidance:** bardphysicslab/engineering-standards@aa8454649fc2e8bb5ad50a5829f8d0cbda736442
- **BardBox standards:** bardphysicslab/bardbox@41fb97e7b0d7b80738ba44cb3942c795ecb3eaca
- **Branch:** `codex/annotated-application-layout` from that baseline in the
  canonical BardBox checkout. The exact head and pull request are recorded in
  the pull request and the #31 checkpoint; this file does not embed its own hash.
- **Roles:** Claude implements (sole writer); Codex independently reviews the
  exact head; the maintainer decides merge. engineering-standards is unchanged.
- **Previous milestone records:** [OCT19-DOCS-1 handoff](archive/CLAUDE-HANDOFF-OCT19-DOCS-1.md)
  and [review](archive/CODEX-REVIEW-OCT19-DOCS-1.md), archived unchanged.

## Changes

- [docs/repository-layout.md](../docs/repository-layout.md) is the one annotated
  general tree: repository roots (no top-level `data/`); 18 application modules,
  each with `config/` and `data/` only where state applies; map-label mapping;
  per-module table; locators; configuration files; state-survival caveats; the
  central error log; Archive entity histories and receipts; tests, scripts and
  deploy; the named nesting deviation; existing-project and adoption neutrality;
  open engineering detail. Illustrative code files sit in every module. The tree
  is explicitly the server application's layout; firmware keeps its own, and
  calculation location (for example AQI) stays project design.
- Pointers: README, ARCHITECTURE, Architecture Map (Composition owner row and
  physical-folder pointer), config/report workflow, service operations, Pi
  runtime; DECISIONS BB-004.

## Evidence

Link, anchor, fence, table and whitespace checks over all tracked Markdown and
`git diff --check`; results at the exact head are in the pull request. No
Mermaid drawing changed, and none was rendered. No scaffold, runtime, pilot,
deployment or infrastructure change.

## Open (unchanged by this milestone)

Entity ID grammar and effective-time bindings; filing of unassigned or
unknown-time records and corrections; storage formats and rotation; multi-file
configuration sync; persistent-storage mechanism and permissions; consistent
snapshots; hot reconfiguration and enable/disable transitions; log rotation and
retention; owners for remaining project-wide settings; reconciling CESH-first
adoption with the RKC next-demo discussion.

## Consumer impact

The project template and pilots are not changed. When the template adopts this
layout, its own documentation should link this guide rather than copy the tree.

**Next action:** Codex reviews the exact head; maintainer decides merge.
