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


# Codex review: EDIT-UI-1

Reviewed author head: `bc2f0562bf1c37f49a7fd6ff60dfe0f03bc5f0c3` on `codex/editable-field-ui-rule`, baseline `34b8ae6e7a9ee3340093b6091df7acfd97578b83`. [PR #52](https://github.com/bardphysicslab/bardbox/pull/52). Result: **no remaining blocking documentation findings**. No merge authorized.

Shared guidance: bardphysicslab/engineering-standards@aa8454649fc2e8bb5ad50a5829f8d0cbda736442
BardBox standards: bardphysicslab/bardbox@34b8ae6e7a9ee3340093b6091df7acfd97578b83

Scope and acceptance: [owner-section edit rule](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6274318475) and the final [alarm-control placement](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6274413539). The latter supersedes only the former prominent-slider placement; the intermediate discussion remains history, not current uncertainty.

Independent exact-diff review verified:

- The maintained Web UI standard owns the rule, with concise architecture and BB-003 index links rather than a duplicate guide. Values may be shown where useful; dashboard edits live in the owner’s section. Name/location headings remain plain text with the Identity edit button; this does not prohibit other authorized owner interfaces.
- Owners explicitly declare editable fields and permissions, validate/persist/apply, and receive authorized requests through Controls. Rendering awaits save completion and re-reads saved values; no reverse owner-to-Rendering dependency. Draft/section preservation, stale-response protection, feedback/central diagnostics and honest uncertain-outcome handling are covered. Full configuration, secrets and internal/read-only settings are not automatically exposed.
- All four current placement passages agree: the alarm switch is inside expandable Alarm for deliberate action; the main card always shows a text-plus-color read-only Alarm enabled/Alarm disabled indicator. It is not a toggle and is distinct from the active ALARM condition and outline. No confirmation/hold/authentication workflow was added. The map row and decision index reflect this; old issue entries remain historical.
- The final alarm delta preserves delivery/escalation pausing while acquisition/evaluation continue, manual re-enable, condition-specific truthful in-range reminder and the active outline/text while disabled. No alarm precedence, threshold, multiple-rule switch scope, escalation restart/resume or audit policy was invented. The generic prominent-control exception no longer lists alarm toggling.

Verification: independent local-link/anchor checks at the reviewed head covered 99 links across all six changed Markdown files with zero findings; git diff --check passed. The author also reports all 69 tracked Markdown files checked for links/anchors/fences/tables/whitespace. The exact author head changes only documentation and handoff records; no executable tests are warranted for this prose-only change. This repository has no configured PR check runs for this branch. These checks supplement semantic review and do not prove runtime adoption.

Reference conformance is separate: [BardBox-Reference placement verification](https://github.com/bardphysicslab/BardBox-Reference/issues/1#issuecomment-6274298406) at reference PR #2 head d49f141 confirms one Edit name and location button inside Identity, plain card heading/location, and preserved open draft during polling. Existing independently checked save/Cancel/validation/restart evidence is unchanged. No reference code change was needed; no Alarm runtime exists in that demo. The local demo and user runtime edits were preserved.

Checkpoint: single canonical BardBox checkout, Claude sole documentation writer in the verified existing session; Codex independent reviewer. Author commits are preserved remotely on PR #52; this subsequent review-only commit changes no standard text. Prior handoff is retained under coordination/archive. Branch/PR are intentionally retained unmerged pending Kornelis’s decision; next action is maintainer review/merge authorization, before further implementation. Existing legacy worktrees remain untouched. No firmware, pilot, service, deployment or runtime capability change, and no skill/governance implementation change; template/consumer adoption remains separately scoped. No unresolved decision blocks this documentation milestone; the unrelated pre-existing alarm open items remain open.
