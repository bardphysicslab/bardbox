# Codex review: OCT19-DOCS-1

Review date: October 19, 2026. Reviewer: Codex, independently of Claude's
implementation. Result: **no remaining blocking findings for the documentation
scope**. This review does not authorize merge, deployment or implementation.

## Exact reviewed implementation heads

| Repository / PR | Reviewed head | Base |
| --- | --- | --- |
| [BardBox PR 50](https://github.com/bardphysicslab/bardbox/pull/50) | `ed4b93ad577bc946280b619670b22a5d8613dbef` | `31100b88958299560b672d88030bc8e11585d2dd` |
| [Engineering standards PR 18](https://github.com/bardphysicslab/engineering-standards/pull/18) | `0fb5062b7665009b4e30318d573977d839a0946b` | `2cb958318b5b603b2b250c351425212e10a64fed` |

Review-record commits contain only reviewer-authored evidence; their exact
published heads are recorded on the PR and owning issue. The initial review
covers the heads above, including the final card-contract amendment and its
state-versus-configuration correction. Later amendments are reviewed below.

## Scope and conclusions

- The accepted decisions and later accepted UI amendments are linked from the
  decision index and owning issue. Main-status vocabulary, exact field choices,
  descriptor format and a future AQI/color light remain open or deferred.
- Required Registry and Processing, module-owned configuration, units/time,
  stable monitored entities, serial recording, bounded storage, backup defaults,
  read-only partner access and the CESH-first development sequence are recorded
  as target direction rather than implemented or deployed behavior.
- The three diagrams retain one maintained home. Redundant guides redirect to
  maintained owners; dated continuation and old prompts remain provenance.
- Finite-storage loss does not become delivery acknowledgement. Ordinary
  verified-backup cleanup, rolling history and saturation eviction are distinct;
  protected deduplication metadata still fails closed. Unknown device time is
  preserved rather than fabricated.
- Card sections come from included modules. Modules declare displayable values
  and controls without exposing complete configuration or secrets. Alarm owns
  its control meaning and permissions; Rendering uses the authorized owner
  path. Alerts-off semantics are explicitly target behavior. Escalation
  acknowledgements and next action are operational state, not editable settings.
- Runtime code, firmware, drivers, tests, fixtures, scripts, policy pages and PDF
  are unchanged. The public README change corrects a sample redirect only.
  Unpublished template hardware remains untouched under its separate follow-up.

## Review corrections verified

The implementation now preserves mobile GPS observation compatibility, narrows
legacy ACK/retention/time-gate wording, removes stale proposal/layout claims,
distinguishes target vendor separation from current CESH coupling, binds the
sample backend to loopback, fixes the consent recipe, and separates Escalation
state from configuration. The issue summary retains the earlier text as history.

## Verification and limits

- Independently inspected the changed-file scope and documentary diffs,
  including follow-up commits and all changed contract boundaries.
- Independently checked conventional relative Markdown links, heading anchors
  and balanced fences over 65 BardBox and 12 engineering Markdown files at the
  first published heads; checked subsequent changed files and anchors. No
  unresolved link/fence finding. Final whitespace checks pass in both repos.
- Engineering workflow checker passes; its two existing unit tests pass at the
  reviewed engineering head. Its GitHub scaffold check also reports success.
- Archive moves were committed unchanged before labels and relative-link fixes.
- Mermaid source was structurally inspected; **rendering was not verified**.
  The diagrams must not be described as renderer-tested. No runtime, device,
  service, backup/restore or deployment acceptance is claimed by this review.
- Open engineering contracts remain in the map and continuation; documentation
  acceptance does not resolve them or authorize their implementation.

Shared guidance: bardphysicslab/engineering-standards@2cb958318b5b603b2b250c351425212e10a64fed

Next owner/action: maintainer reviews the two PRs and decides merge. Existing
feature checkouts remain available; no cleanup or host synchronization occurs.

## Active-alarm outline amendment review

Reviewed implementation: `2bd65624b98989378936063ade5727a7baba3e71`, based on
the previously published `d555edc294f2d13ef8f06aa6447f8a37e5770b91`. Accepted
[owning-issue amendment](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270510607).
Result: **no blocking findings** in the four-file documentation amendment.

- Active Alarm state alone triggers a slow red card-outline pulse with persistent
  textual ALARM indication; reduced motion uses a static red outline and text.
- Connection, freshness and AQI/category colors are separate and cannot trigger
  that pulse. No AQI method or threshold is standardized.
- The Web UI rule, decision index, disposition A20 and handoff agree. No runtime,
  pilot, mockup, escalation or merge change. Engineering PR 18 is unchanged.
- Independently inspected the exact diff and read back the accepted issue entry.
  All 66 BardBox Markdown files pass conventional relative-link, heading-anchor
  and balanced-fence checks at this implementation head; whitespace checks pass.
  No new diagram change; the earlier Mermaid-rendering limitation remains.

This review-record update changes evidence only. The final published head is
recorded on PR 50 and issue 31; merge remains the maintainer's decision.

## Alarm switch and disabled-state amendment review

Reviewed implementation: `1b20d76b4429ee4c77838ca8758f020198464c4a`, following
`7a29bb4` and the relevant-condition precision fix `9663e48`; base publication
`7524c653c92ac07a97a3a6c73e01a68f3fe8dd78`.
[Accepted owning decision](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270769043).
Result: **no remaining blocking findings** in this five-file documentation delta.

Claude's critique is incorporated into the maintained draft: switch placement,
the explicit notification/escalation-only meaning of disabled, disabled plus
active-condition visibility, truthful recovery reminders, and combined
Identity/Health ownership. The prominent sliding switch sits below the heading
and above readings when Alarm is included; detailed settings remain expandable.
Acquisition and evaluation continue while disabled, and re-enable is manual.

Codex corrections preserve per-channel validity and the existing explicit
live-observation freshness exception. An unrelated channel fault does not erase
valid condition evidence; unknown device measurement time does not invalidate
an otherwise allowed, explicitly labelled live-observation freshness basis.
Neither replay receipt time nor an unsupported freshness claim can make the
reminder say currently within range. No new aggregate status policy is selected.

Multiple-rule switch scope, escalation restart/resume after re-enable, audit
specifics, exact wording and detailed reminder gating remain open. A CESH service
alarm is illustrative with no selected inactivity timeout or detection rule;
RKC's existing alarm requirement is preserved. PurpleAir Flex correction,
averaging and AQI work is future research, with no chosen algorithm. Local
mockup values and HTML are not adopted.

Independent verification: inspected the exact delta and its condition/time
compatibility against the ingestion contract; all 66 tracked Markdown files
pass conventional relative-link, heading-anchor and balanced-fence checks;
whitespace checks pass. No diagrams changed, so the earlier Mermaid rendering
limitation remains. Engineering PR 18 is unchanged. No runtime, pilot, demo,
merge or deployment acceptance is claimed. The following reviewer-record update
changes evidence only; the final published head is recorded on PR 50 and issue 31.
