# October 19, 2026 documentation review: findings and dispositions

Dated record for milestone OCT19-DOCS-1
([bardbox#31](https://github.com/bardphysicslab/bardbox/issues/31)). It maps
every finding from the October 19 reviews (Claude and Codex, all 69 tracked
files at `31100b88958299560b672d88030bc8e11585d2dd`) to a documentation change,
a justified unchanged boundary, or an explicit follow-up. It is evidence, not
guidance: the linked documents govern.

Governing decisions: [BB-003](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991),
[UI clarification](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269649488),
[buffer estimates](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269868018),
[UI amendment](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270151957),
[ENG-003](https://github.com/bardphysicslab/engineering-standards/issues/17#issuecomment-6269649466).
Exploratory status-label discussion after those entries is not a decision.

Disposition key: **Changed** (edited here), **Unchanged** (boundary kept, with
reason), **Open** (contract work stays explicitly open), **Follow-up** (tracked
elsewhere).

## Architecture review findings

| # | Finding | Disposition | Where |
| --- | --- | --- | --- |
| A1 | "Never remove before ACK" rules conflict with saturation eviction | Changed: narrow capacity-eviction exception, counted as loss, never an ACK; no protocol-version change; "never clear automatically to recover from upload failure" kept | [Web Node protocol](../web-node-protocol.md#persistent-buffering), [transport recovery](../transport-recovery-standard.md), [buffer API](../firmware-buffer-api.md), [map](../architecture-map.md#node-firmware-template) |
| A2 | Anchor plus a permanently rejected FIFO head | Open: blocked-head behavior stays the safe initial rule; no automatic skip; interaction is engineering detail | [map](../architecture-map.md#node-firmware-template), [buffer API](../firmware-buffer-api.md) |
| A3 | Firmware evictions must reach the central log | Changed: bounded durable loss count reported when communication permits; no first/last loss IDs or new UI mandated | [buffer API](../firmware-buffer-api.md), [map](../architecture-map.md#node-firmware-template) |
| A4 | Verified-backup-before-pruning versus backup OFF and saturation | Changed: history ON, backup OFF, rolling window, enabled-backup anchor distinct from verified retention; rows evict but tombstone metadata fails closed | [service operations](../service-operations-standard.md), [ingestion contract](../ingestion-contract.md#envelope-rejection-and-durable-acceptance), [map](../architecture-map.md#local-history-and-backup) |
| A5 | Minimal UID registry versus Registry-owned channel definitions | Changed: declared project measurement contract, resolved by Registry (also for a UID-only demo); several declarations may be views of one project-owned contract | [ingestion contract](../ingestion-contract.md), [channel names](../channel-names.md), [map row 10](../architecture-map.md#server-data-inventory-and-module-operations) |
| A6 | Partner pull versus internal-only networking | Changed: read-only pull direction; existing restrictions stay until an authorized access plan; consumers not redefined as internal | [network access](../network-access.md), [map](../architecture-map.md#project-server-template), [Data API boundary](../data-api-mcp-boundary.md#optional-partner-read-api) |
| A7 | UID meaning on hardware replacement | Changed and Open: identity layers separate node UID, monitored entity and App ID; replacement attribution and effective-time binding open; no UID grammar change | [node naming](../node-naming-standard.md#identity-layers) |
| A8 | Processing required | Changed: replaces Analysis/sensor QA in drawing, inventory and matrix; no-op allowed | [map](../architecture-map.md#processing-units-and-time) |
| A9 | Rendering, display units, local time, buffer indicator | Changed: D2 owner resolved; header requires current time; card top area | [Web UI standard](../web-ui-standard.md), [map](../architecture-map.md#health-status-and-presentation) |
| A10 | Firmware recording ON including serial | Changed; serial retrieval Open; low-flash feasibility note | [blueprint](../firmware-blueprint.md), [serial/base API](../firmware-base-and-serial-api.md), [buffer API](../firmware-buffer-api.md) |
| A11 | Configuration in module subtrees; sync tooling assumes one file and has drifted across repositories | Changed for new references; Open for multi-file sync tooling; pilots not migrated | [config/report workflow](../config-report-workflow.md), [map](../architecture-map.md#configuration-ownership) |
| A12 | Monitored entities | Changed | [node naming](../node-naming-standard.md#identity-layers), map rows 3 and 11, [ingestion contract](../ingestion-contract.md) |
| A13 | Roadmap re-sequencing | Follow-up on GitHub (template roadmap issues; see the pull request) | [template#31](https://github.com/bardphysicslab/bardbox-project-template/issues/31) |
| A14 | Checkout synchronization and clones | Changed in engineering-standards (ENG-003) | `checkouts-and-worktrees.md` on branch `codex/module-checkout-guidance` |
| A15 | Metric default | Changed; `count/ft3` kept as a documented compatibility exception | [channel names](../channel-names.md), [reading format](../reading-format.md#units-and-time) |
| A16 | Bard IT policy conditions | Unchanged: linked in its original conditional wording, no compliance claimed and no permission inferred from a proxy | [network access](../network-access.md) |
| A17 | Decision recording | Changed: BB-003 index row linking the dated entry | [DECISIONS](../DECISIONS.md) |
| A18 | Later accepted UI amendment (heading, sections, catching-up, latest value, location source) | Changed | [Web UI standard](../web-ui-standard.md#card-top-area), [node naming](../node-naming-standard.md#identity-layers), [map](../architecture-map.md#health-status-and-presentation) |

## Complete-repository coverage findings

| # | Finding | Disposition | Where |
| --- | --- | --- | --- |
| C1 | Stale "pending/absent PR #15/#16/#23" claims | Changed: merged-draft status without claiming adoption; dated history preserved | blueprint, buffer API, USB provisioning, USB device configuration, README, AGENTS, ARCHITECTURE |
| C2 | Recording-default conflicts in additional places | Changed | blueprint, continuation, serial/base API |
| C3 | Several claimed owners of schema/units | Changed (see A5) | |
| C4 | Display timezone source | Open: Rendering labels local time; site/user preference and persistence open | [time sync](../time-sync-standard.md), [map](../architecture-map.md#processing-units-and-time) |
| C5 | Conflicting UID semantics across documents | Changed (see A7); device-instructions points to identity layers | |
| C6 | ARCHITECTURE and transport-recovery "no silent discard" wording | Changed: loss is counted and logged, not silent | |
| C7 | Compact chunk granularity versus record anchor | Changed: preserve base chunk or copy/re-encode, no mandated approach | [compact storage](../compact-record-storage.md) |
| C8 | Restart policy, plain-HTTP example, DNS fallback, stale references in Pi docs | Changed: Pi setup aligned to `Restart=always` with legacy status notes; example values replaced in network access | [Pi setup](../pi-setup.md), [Pi runtime](../pi-runtime-instructions.md) |
| C9 | Internal addresses, device serial and workstation paths in a public repository | Changed in active text (network access placeholders). Unchanged: archived prompts and legacy device notes keep their historical text (no history rewrite); the driver's default port is code and is tracked in bardbox#49 | |
| C10 | Existing public web surface (static policy pages) | Changed: the README recipe now sends `/consent` to the tracked `consent.pdf` instead of a missing `consent.html`. Unchanged: policy pages, PDF and any deployed server configuration | [public README](../../public/README.md) |
| C11 | RKC SMS webhook signature gap versus the written rule | Unchanged here: dated evidence stays dated; RKC owns the fix | [evidence](../server-data-inventory-evidence.md) |
| C12 | Duplicate UI standards | Changed: monitor instructions consolidated into the Web UI standard | |
| C13 | UID registry placeholder link | Changed: redirect to naming standard and registry owners, no-reuse rule preserved | |
| C14 | `jst` site code | Changed: marked historical, not for new nodes | |
| C15 | Implementation guide (Pi-hub era, missing `capabilities-schema.md`) | Changed: unique content moved, redirect left; mobile GPS exception preserved | [ARCHITECTURE](../../ARCHITECTURE.md#starting-a-new-project), [node naming](../node-naming-standard.md#application-identity), [map](../architecture-map.md#location-metadata-and-observed-position) |
| C16 | Stale README CESH status and duplicate UI reference | Changed | [README](../../README.md) |
| C17 | Unindexed documents with ambiguous status | Changed: ARCHITECTURE index complete; legacy Pi documents labelled per section; repository layout and reproducible development kept as modern standards | |
| C18 | Docker Compose packaging versus native/systemd | Changed: packaging labelled a proposal that does not change the current production model | [map](../architecture-map.md#project-server-template) |
| C19 | Data API file shape | Changed: partner API reuses posture, not shape | |
| C20 | GoLab refactor prompts | Changed: archived unchanged as non-operative provenance, redirects left | [archive](../../archive/legacy/refactor/README.md) |
| C21 | Dated firmware continuation | Changed: body archived unchanged; short current entry | [continuation](../firmware-api-continuation.md) |
| C22 | Privacy policy states no retention period | Unchanged: operational policy pages are out of scope; map D9 stays open | |
| C23 | Driver, tests, fixtures, dependency manifest and CI drift | Follow-up: [bardbox#49](https://github.com/bardphysicslab/bardbox/issues/49); driver README labelled legacy and non-conforming | [driver README](../../drivers/gt521s_driver/README.md) |
| C24 | Unpublished PCB work in the template checkout | Follow-up: [template#33](https://github.com/bardphysicslab/bardbox-project-template/issues/33); untouched | |
| C25 | Legacy exact-version retention and time-gate wording contradicting accepted finite-storage and unknown-time policies (review) | Changed: scoped to their cases | [map](../architecture-map.md#local-history-and-backup), [service operations](../service-operations-standard.md), [time sync](../time-sync-standard.md) |
| C26 | Exact-head review of `cc0a99d`: blueprint still described device instructions as using the old root; Pi setup gave a copyable public `0.0.0.0` plain-HTTP bind; data-source drivers implied vendor collection was already extracted | Changed: current status stated; backend bound to loopback behind the canonical HTTPS proxy rules; target versus current CESH coupling separated | [blueprint](../firmware-blueprint.md), [Pi setup](../pi-setup.md), [data source drivers](../data-source-drivers.md) |

## Codex cautions (all accepted)

1. Reuse the read-only boundary's posture without file shape or a second authority: applied (A6, C19).
2. Display ownership needs recording: D2 recorded as resolved owner with open details.
3. A blocked anchor may stay an explicitly documented blocked state: applied (A2).
4. Smallest durable cumulative loss accounting; no first/last IDs; delayed reporting fine: applied (A3).
5. No extra working clone absent a concrete role (not a blanket ban): ENG-003.
6. Keep Bard PDF conditions literal and infer no exposure permission: applied (A16).
7. Merged drafts are not adopted; modern layout/reproducibility documents are not obsolete; one project-owned contract may have several views; compact anchors are not mandated one way; central-log-only means no new loss UI while the blocked-state contract stays; open design may be recorded as open: applied throughout.

## Unchanged boundaries kept deliberately

Driver, test, fixture, script and public policy content; server data inventory
evidence (dated); historical archives; the eight existing redirects
(`CLAUDE.md`, `docs/ai/bardbox-change-skill.md`, `docs/architecture-principles.md`,
`docs/gpt-instructions.md`, and the four `docs/engineering/` pointers); USB
hardware installation confirmation; flasher Processing (deferred to Firmware Tools).
