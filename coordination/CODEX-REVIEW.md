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
