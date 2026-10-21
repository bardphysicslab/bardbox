# Codex review: OCT19-LAYOUT-1

Reviewed implementation: `71c3c7348c9ba99bd90b0950863d763fc31f077f` on
`codex/annotated-application-layout`, base
`41fb97e7b0d7b80738ba44cb3942c795ecb3eaca`.
[PR 51](https://github.com/bardphysicslab/bardbox/pull/51).
Result: **no remaining blocking documentation findings**. No merge is authorized.

Claude provided the requested blind-spot critique before any documentation edit.
The maintainer then settled the missing owner as Composition, with the naming
and content-based configuration decisions preserved in the owning issue.
Codex inspected the exact documentary diff and follow-up corrections independently.

## Acceptance and boundary review

- The existing [repository layout](../docs/repository-layout.md) is the one
  annotated guide. README and architecture entry points visibly link it; no
  second application tree or executable scaffold was created.
- All 18 named application-server modules have their own folder, illustrative
  code and `config/`; optional folders do not enable capabilities. State folders
  are conditional on owned saved state rather than invented for stateless code.
- Composition owns module selection and startup wiring. It does not own Alarm
  thresholds, Escalation contacts or project scientific formulas. `main.py`
  delegates composition; runtime reload and transition semantics remain open.
- Nonsecret settings, including actual Composition selections, can be tracked;
  private configuration, credentials and runtime state remain excluded. No
  filename, configuration schema or override mechanism is selected.
- Module-local data and private configuration must survive redeploy and server
  migration. Mounts, permissions, defaults and snapshot consistency are assessed
  as requirements, not implemented infrastructure or verified pilot protection.
- Diagnostics owns the single error-log home; pure validators return faults for
  callers to log, preserving BB-002. Archive owns entity histories and separate
  receipt bookkeeping under one atomic/recoverably journaled acceptance. Existing
  attribution, deduplication, tombstone, per-node retention and restore invariants
  remain; unresolved filing/correction mechanisms are not guessed.
- Public static roots are separate from owner-mediated authorized historical
  data responses. Private application directories are not published wholesale.
- Tests, thin operational scripts and deployment helpers have distinct homes.
  Existing single-file/legacy layouts remain explicitly labelled, not migrated.
- The guide is a server-application map. Firmware and project scientific
  execution stay flexible; AQI method/location and demo/adoption ordering are
  not selected by folder documentation.

## Findings corrected before this review

Added representative code files and test subfolders; preserved the distinction
between stateless reference needs and later project science design; clarified
static asset roots without banning the authenticated Data API; applied the
Composition name consistently; corrected blanket private-config classification;
and preserved pure Ingestion's caller-owned logging path.

## Verification and limitations

- All 67 tracked Markdown files at the reviewed implementation head pass
  independent conventional relative-link, heading-anchor and balanced-fence
  checks. The annotated tree includes the exact 18 module names, each with
  `config/` and representative code. Whitespace checks pass.
- Changed-file inspection confirms documentation only. No runtime tests, build,
  device, live data, host, migration, deployment or DNS operation was performed.
- No Mermaid drawing changed; the earlier unverified rendering limitation is
  unchanged. No new diagram-rendering claim.
- Prior milestone records were moved unchanged before labels/link repairs.
  They remain historical evidence, not the current milestone's review.

This following reviewer-record commit changes evidence only; its exact published
head is recorded on the PR and owning issue. The feature is preserved off-machine
on the PR branch. Next: maintainer reviews PR 51 and decides merge; any later
implementation needs its own bounded scope and prerequisite open decisions.

Shared guidance: bardphysicslab/engineering-standards@aa8454649fc2e8bb5ad50a5829f8d0cbda736442

BardBox standards: bardphysicslab/bardbox@41fb97e7b0d7b80738ba44cb3942c795ecb3eaca

# Codex review — EDITABLE-FRAMES-OWNER-1-DOCS — October21,2026

PASS at author6d501dda100510ebca1904fa60dc922cfcf7f711, baseline d93491c7fd94c31bc702ae51d30e0c59de190792, PR66. Shared engineering91a2d7c0d4afd3eac55ec612be9866f46fb3a11d; BardBoxd93491c govern. User acceptance#31comment6323356438/#10comment6323356061; requested GitHub and local documentation publication, prior authorized checks-gated merge/sync. Claude implements, Codex independently reviews; this added review changes no standard text/runtime.

All8 changed Markdown files read: architecture, map, Web UI standard, testing guide, index, continuation, current handoff and archived prior handoff. Current rules consistently distinguish framed editable values (empty when unassigned with labels) from missing read-only dash/unframed and populated read-only actual values. Optional Owner edited in Identity through Registry validation/revision/history; new registration has no assumed owner, existing assignments preserved. Name/Owner/hardware identity remain independent. Inline UID Registry link removed, top navigation retained. Earlier owner default/editable-dash decisions linked as superseded, historical checkpoint prose preserved.

Two wording findings resolved at final author head. Independent local link/anchor/fence check128 links across all changed docs, zero findings; whitespace PASS. Archived DOCS-RECONCILE prose independently compared: unchanged except one corrected sibling relative path. Maintained Mermaid blocks unchanged; no render repetition warranted. No configured PR CI. No runtime tests repeated for prose. Separate app PR22 merged59b6b7e with19 independently passing focused tests, desktop/375px Owner save/clear/Cancel/long-value checks and all10 final CI green. Same-DB user preview restarted; current9devices/33history exactly preserved, including user's Name edit during the task. No hardware/deployment claim.

No remaining blocking findings. Merge and synchronize canonical local main, retain historical28dref and PR52 unique process records; clean only confirmed merged new task branch under shared rule10. Existing Reference#9 stays open/Backlog for future feedback/display preferences/feeds/promotion. Current completion evidence belongs#9 and shared#10/#31/#64; no further coding in this milestone.
