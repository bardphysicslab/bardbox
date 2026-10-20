# Repository layout and configuration filenames

This is the one maintained guide to where things live in a BardBox project
repository: the repository roots, the server application's modules, and where
each module keeps its code, configuration and saved data. Other documents link
here instead of keeping their own tree.

**Status.** Accepted reference layout for new BardBox projects
([BB-004](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271296848),
with the composition [owner supplement](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271666389), which named the module "Application" before the
[naming refinement](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271757925) renamed it Composition,
and the [pre-write critique dispositions](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271384280)).
It is a *proposed map*, not an inventory of existing CESH or RKC files, not
generated scaffolding and not evidence that any module is implemented or
enabled. Existing projects are not migrated by this guide. Paths below are
proposed; example code filenames are illustrative, not frozen APIs.

**Scope.** The application tree describes the *server application's* source
layout ([science-location clarification](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271713054)). It is not a requirement to run every calculation on the server:
firmware keeps its own layout and code under `software/firmware/`, and this guide
moves no logic between firmware and server modules and no existing CESH logic.
A project chooses where a scientific calculation runs. For example, a future
CESH node indicator might compute an index locally in firmware while another
instance computes it server-side in Processing. Methods such as AQI, and where
they execute, remain future project design; keeping scientific definitions
consistent across implementations is desirable, but no algorithm or central
calculation library is selected.

## Repository roots

```text
<project>/
  hardware/
    ecad/            KiCad schematics, boards, libraries and fabrication exports (when the project has hardware)
    mcad/            enclosure and mechanical source and exports (when the project has hardware)
  software/
    app/             the server application: one folder per module (next section)
    firmware/        BardBox firmware; one PlatformIO project directly here, or
                     firmware/<project>/ when there is more than one
  tests/             automatic application tests
    <module>/        tests for one application module
    integration/     cross-module scenarios
  scripts/           occasional operational utilities that call module interfaces
  deploy/            installation, service, endpoint, update and rollback configuration and helpers
  docs/              project documentation
```

There is **no top-level `data/` folder** in the reference layout. Saved state
belongs to the module that owns it, inside that module's `data/` folder.
Software-only tools and standards repositories need no artificial `hardware/`
folders. Shared libraries may have their own documented source location; link
them rather than copying them into a module folder.

## Application modules (`software/app`)

Every application module has its own folder and its own `config/` folder, even
when it is small, a no-op, or an optional capability the project has not
enabled. A module has a `data/` folder only when it actually keeps saved state.

```text
software/app/
  main.py                     thin entry point: calls the Composition module, nothing else
  composition/                which modules are included and enabled; startup wiring
    composition.py
    config/
  registry/                   node definitions, monitored entities, names, locations
    registry.py
    config/
    data/                     registered definitions and identity bindings
  communications/             receives and fetches data from nodes and sources
    config/
    http/
      push_receiver.py        HTTP push receiver
    serial/
      serial_adapter.py       serial adapter (optional)
    drivers/
      <source>_driver.py      one source driver per source type: parse and normalize
  ingestion/                  validates incoming observations (no owned saved state)
    validate.py
    config/
  latest_readings/            newest accepted value per entity and channel
    latest_store.py
    config/
    data/                     only if the latest view must survive a restart
  archive/                    durable measurement history and acceptance bookkeeping
    archive.py
    config/
    data/
      measurements/<stable-entity-id>/   one entity's history, possibly several rotated files
      receipts/                          acceptance, deduplication and tombstone bookkeeping
  health/                     freshness, contact and delivery status
    health.py
    config/
    data/                     only if health projections must survive a restart
  processing/                 project calculations, derived results, conversions
    calculations.py
    units.py
    config/
  alarm/                      alarm rules, thresholds and alarm state (optional)
    alarm.py
    config/
    data/                     active alarm state and history
  escalation/                 contacts, acknowledgement, next action (optional)
    escalation.py
    config/
    data/                     escalation and acknowledgement state
    notification_adapters/
      <provider>_adapter.py   SMS, email or other delivery provider
  queries/                    read interfaces used by rendering and the partner API
    queries.py
    config/
  controls/                   authorized edit requests routed to the owning module
    controls.py
    config/
  rendering/                  dashboards, cards and charts
    pages.py
    config/
    templates/
    static/                   the only public static asset root
  authentication/             operator, device and partner-consumer authentication
    authentication.py
    config/
    data/                     credential verification material and sessions, never in Git
  time/                       clocks, deadlines and scheduling mechanisms
    clock.py
    config/
  diagnostics/                the central application error log
    error_log.py
    config/
    data/
      errors.log              the one application error log
  backup/                     optional Drive backup (included, OFF by default)
    backup.py
    config/
    data/                     manifest, deferrals, lock and checkpoint state
  partner_api/                optional read-only pull API for external consumers
    partner_api.py
    config/
```

Code filenames such as `registry.py` or `<source>_driver.py` are illustrative: they
show that each module's code sits beside its `config/` and `data/`, not a required
file list, API or scaffold. A module may have several code files or subfolders.

The 18 modules match the [Architecture Map](architecture-map.md#project-server-template).
Where the map uses a combined or older label, the folders are:

| Map label | Folder(s) |
| --- | --- |
| Latest-reading store / "Latest/Health 07" | `latest_readings/` and `health/` |
| Clock / scheduling utilities, "Clock/startup 03" | `time/` (mechanisms) and `composition/` with `main.py` (startup wiring) |
| Persistent configuration owner, capability selection | `composition/` owns which modules are included and enabled; each module owns its own settings |
| Notification adapters | `escalation/notification_adapters/` |
| Analysis / sensor QA, "Science 11" | `processing/` |
| Optional partner export / read API | `partner_api/` |

### What each module keeps

| Module | Plain-language job | `config/` holds | `data/` holds |
| --- | --- | --- | --- |
| `composition` | Decides which modules this instance includes and enables, and wires them together at startup | Included/enabled module list and wiring choices (not scientific formulas, cutoffs or other modules' settings) | None |
| `registry` | Knows every node, the entity it monitors, and its display name and location | Validation rules and defaults; where the project measurement contract is declared (its format is open) | Registered nodes, entities, bindings and descriptive metadata |
| `communications` | Accepts pushed records, reads serial sources, fetches remote sources | Endpoints, size/rate limits, adapter settings | None in the reference layout |
| `ingestion` | Checks each observation against the registry and contracts | Validation options | None (no owned saved state) |
| `latest_readings` | Holds the newest valid value per entity and channel | Retention of the current view | Only if the current view must survive restart |
| `archive` | Stores measurement history per entity and records what was accepted | Storage allowance, rotation and retention policy | `measurements/<stable-entity-id>/`, `receipts/` |
| `health` | Works out freshness, contact and delivery status | Stale and offline thresholds | Only if projections must survive restart |
| `processing` | Calculates server-side derived results and unit conversions where the project runs them on the server | Calculation definitions and parameters | None in the reference layout; project-specific state only if later designed (derived-value storage is open, map D1) |
| `alarm` | Evaluates alarm conditions and owns the enable/disable state | Thresholds, delays, allowed ranges, control declarations | Active alarm state and history |
| `escalation` | Tracks who is contacted, acknowledgements and next actions | Contacts, order, availability, opt-outs, templates, provider settings | Escalation and acknowledgement state |
| `queries` | Serves read requests through other modules' read interfaces | Query bounds | None (no owned saved state) |
| `controls` | Passes authorized edits to the owning module, then re-reads them | Which edits are offered and to whom | None |
| `rendering` | Draws dashboards and cards | Display selections, display units, timezone presentation | None |
| `authentication` | Verifies operators, devices and partner consumers | Authentication methods and policies (no secret values) | Credential verification material and, where used, sessions |
| `time` | Supplies clocks, deadlines and schedulers | Clock sources | None (no owned saved state) |
| `diagnostics` | Collects, writes and rotates the central error log | Redaction, rotation and size bounds | `errors.log` |
| `backup` | Copies and verifies Archive snapshots to Drive when enabled | Enabled flag, schedule, destination reference | Manifest, deferrals, lock, checkpoint |
| `partner_api` | Answers read-only external pull requests | Field mapping and request bounds (keys are verified by `authentication`) | None |

In the reference layout Ingestion, Processing, Time, Queries and Controls own no
saved state, and none should be invented for them. That describes their
reference needs, not a ban: a project may later design explicit state for one of
them (for example stored derived science values, whose storage owner is open as
map D1) through the normal design and review path. Queries and clock reads still
read live data and time; "no owned saved state" is not a claim that they are
mathematically pure. Latest readings and Health keep state only when a
project needs it to survive a restart. Communications keeps none in the
reference layout. A disabled module's `config/` may hold only tracked defaults or
an example.

### Including, enabling and empty folders

- **Folder presence never enables anything.** The Composition module's
  configuration decides which modules are included and enabled. A disabled module
  needs no live configuration and no saved data; nothing is fabricated for it.
- **Composition is not a catch-all.** It owns instance composition only. Alarm
  still owns thresholds, Escalation still owns contacts, and every other module
  keeps its own settings and state. Settings that have no named owner yet stay
  explicitly open; they are not moved into Composition by default. (Composition
  was first named "Application"; only the name changed, to avoid confusion with
  the overall `software/app` application.)
- **Hot changes are open.** Reload, runtime enable/disable transitions and
  restart semantics are not decided by this layout.
- **Named deviation from the shared nesting guidance.** The shared guidance
  ([engineering-standards agent practice, module organization](https://github.com/bardphysicslab/engineering-standards/blob/main/agent-practice.md#module-organization);
  [ENG-003](https://github.com/bardphysicslab/engineering-standards/issues/17#issuecomment-6269649466))
  and BB-003 say to avoid empty nesting for trivial code. BardBox deliberately
  deviates at the application-module level: every module keeps its own folder and
  `config/` even when small or disabled, so readers always find a capability in
  the same place (BB-004). Inside a module, avoid gratuitous nesting, and never
  copy a shared implementation only to fill a folder. A folder does not prove a
  dependency boundary.
- An empty module folder needs at most a short marker file, not its own guide.

## Finding things

| You are looking for | Look in |
| --- | --- |
| Application errors | `software/app/diagnostics/data/errors.log` |
| One entity's measurements (for example a freezer) | `software/app/archive/data/measurements/<stable-entity-id>/` |
| Whether a record was accepted or is a duplicate | `software/app/archive/data/receipts/` (through Archive, never by editing files) |
| A module's settings | `software/app/<module>/config/` |
| Which modules are enabled | `software/app/composition/config/` |
| A module's code | `software/app/<module>/` |
| A module's tests | `tests/<module>/`; cross-module scenarios in `tests/integration/` |
| Service, update and rollback setup | `deploy/` |
| Firmware source and its build/test layout | `software/firmware/` |

## Configuration files

- **Classify configuration by content, not by whether it holds real instance
  values** ([configuration-tracking correction](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271790738)). Non-secret settings may be tracked in Git, including an
  instance's actual choices; for example, Composition's module selection should
  be tracked for history and reproducibility. Credentials, genuinely private
  deployment configuration and runtime state are never tracked.
- Where a module needs both, its `config/` keeps the tracked non-secret settings
  (or safe examples and defaults) separate from **private overrides** that stay
  out of Git. The override mechanism, file names, formats and schemas are open;
  this guide does not choose them. Never replace private values with an example,
  and never commit secrets.
- Each owning module validates, persists and applies its own settings
  ([configuration ownership](architecture-map.md#configuration-ownership)).
- **Existing projects** use one `app_config.json` (for example
  `software/app/config/app_config.json`, or `raspi/config/` in older ones) and the
  single-file `scripts/sync_app_config.py`
  ([config/report workflow](config-report-workflow.md)). That remains their
  current, supported tooling. Their live file holds secrets and stays ignored and
  protected; nothing here migrates it. Synchronizing many module files is open
  work; this guide does not change existing deployments.

## Saved state that must survive updates

Module `config/` and `data/` locations are **logical**. Private configuration
(credentials and genuinely private deployment values) and module runtime data are
kept out of Git and must survive code updates, redeploys, image rebuilds and
moving the application to another server. Tracked non-secret settings travel
with the repository revision.

- **Keep state on persistent storage.** A deployment keeps each module's live
  configuration and data on storage that is not replaced when the code is
  updated (a persistent mount or equivalent), while tracked non-secret settings,
  defaults and examples still come from the release. The exact mechanism is open and nothing here
  implements it or claims that current deployments are protected.
- **Avoid commands that destroy ignored files** in a deployed tree, such as
  `git clean -fdx`, `git reset --hard` followed by clean-up, `rsync --delete`
  onto the application folder, or replacing the folder with a fresh clone.
- **One process is not isolation.** Folder boundaries are not operating-system
  security boundaries: modules in one process can read each other's files. Use
  least-privilege file ownership for the service user and keep secrets out of
  logs and reports.
- **`rendering/static/` is the only public static asset root.** It is the only
  application folder mounted or exposed as a public static file root; no other
  application directory becomes a static or public file root, and private
  `config/` or `data/` folders are never exposed wholesale. Rendered pages from
  `rendering/templates/` and owner-mediated, authorized data responses remain
  permitted, including selected historical files returned by the canonical
  authenticated [Data API](service-operations-standard.md#read-only-historical-data-api).
- **Data access is narrow.** Only approved measurement data or snapshots from
  `archive/data/measurements/` may be offered through the authenticated read-only
  [Data API boundary](data-api-mcp-boundary.md); `archive/data` as a whole is not
  a clean readings root, because it contains receipts.
- **Backup is not a copy of the tree.** Backup reads through Archive's (and other
  owners') snapshot interfaces and must restore Registry bindings, Archive
  measurements and receipts consistently
  ([ingestion contract](ingestion-contract.md#envelope-rejection-and-durable-acceptance)).
  A Git ignore or a portable source copy is not a backup. Drive backup stays OFF by
  default ([service operations](service-operations-standard.md)).

## Central error log

`software/app/diagnostics/data/errors.log` is the one application error log
(written `app/diagnostics/data/errors.log` relative to `software/`). There is no
second application log root.

- Following [BB-002](DECISIONS.md), operational modules report the failures they detect through
  the shared logging interface. Pure modules such as Ingestion perform no log
  writes: they return structured faults, and their calling module logs them.
  Diagnostics owns collection, redaction, writing and rotation. The rotation
  schedule and retention are not chosen here.
- It is **not** Archive's acceptance or rejection bookkeeping, not the record of
  inbound requests or messages that may contain personal data (their retention is
  open, map D9), and not the operating system's service output (for example the
  systemd journal), which remains separate.
- This chooses a location, not a running logging implementation.

## Archive: entity histories and receipts

- Measurement history is grouped by **stable entity**:
  `archive/data/measurements/<stable-entity-id>/`. Every record keeps its original
  node, device and sensor attribution, so replacing hardware neither splits nor
  rewrites an entity's history. One history may span several rotated files; file
  format and rotation are open.
- `<stable-entity-id>` is a placeholder. Entity ID grammar is open; display
  names and locations never appear in the path.
- `receipts/` holds acceptance, deduplication and tombstone bookkeeping. The two
  path groups are a logical organization, not a decision to use two independent
  physical stores: acceptance stays one Archive-owned atomic or recoverably
  journaled operation across measurements and receipts, all workers, retries and
  restore. A receipt file alone is not an acknowledgement authority. Existing
  record identity, deduplication key, tombstone and restore rules are unchanged
  ([ingestion contract](ingestion-contract.md#envelope-rejection-and-durable-acceptance)).
- Grouping by entity does not change per-node saturation anchors or backup
  policy, and does not change receipt identities.
- **Open before dependent Archive work:** how records are filed for unassigned
  nodes or unknown measurement time, how historical entity bindings take effect,
  and how corrections are handled. No unassigned-record folder, automatic
  reassignment or rejection policy is chosen here.

## Tests, scripts and deploy

| Folder | Job | Not its job |
| --- | --- | --- |
| `tests/` | Automatic tests that assert behavior: `tests/<module>/` per application module and `tests/integration/` for cross-module scenarios, with synthetic data only | Live data, deployment actions |
| `scripts/` | Occasional operational utilities that call module interfaces (for example, checking installed Registry definitions through Registry validation) | Duplicating validation or runtime logic, or a second deployment implementation |
| `deploy/` | Installation, service units, endpoints, updates, rollback, and their helpers | Application behavior |

Existing exceptions stay labelled as current implementations until deliberately
reconciled: the single-file config synchronizer, and backup scripts such as
CESH's that contain backup logic (target: the logic belongs in `backup/`, its
timer in `deploy/`). Firmware keeps its own build and host-test layout under
`software/firmware/`.

## Existing projects and adoption

CESH and RKC predate this layout and differ from it (for example RKC's mixed
`data/logs/`, top-level `data/`, and single-file configuration). Their current
paths remain valid for them, and nothing here claims they conform or must move.
Earlier versions of this guide said BardBox repositories use the RKC layout;
this general layout replaces that statement.

This guide does not choose an adoption or demonstration order. The accepted
roadmap puts CESH first in a development instance of the template; a later
discussion prefers a minimal RKC/freezer reference for the next demonstration
on a proposed lab test host. Those must be reconciled on
[bardbox#31](https://github.com/bardphysicslab/bardbox/issues/31) and the
template roadmap before any rollout claims either order. No hosting change is
authorized.

## Hardware folders

ECAD contains KiCad schematics, boards, libraries and revisioned fabrication
exports. MCAD contains enclosure/mechanical source and exports. Do not treat an
empty folder or README as proof that drawings exist or an assembly is validated.

## Firmware configuration

Use tracked `include/config.example.h` for safe placeholder configuration and
ignored `include/config.h` for the local deployment values (placement accepted
October 20, 2026 on [#31](https://github.com/bardphysicslab/bardbox/issues/31),
replacing the earlier `src/` placement; existing projects that keep these
headers in `src/`, such as CESH, have not been migrated and are not changed by
this rule). The example header is not activated or compiled automatically: C++
uses a header only through an explicit `#include`, and `main.cpp` includes
`config.h` only when its variant uses configuration. A `**/config.h` ignore
covers either location independently of the include. Configuration includes pins,
sampling choices and identity as well as credentials; `secrets.h` is therefore
not the preferred filename. Existing private `secrets.h` must be locally renamed,
not overwritten with example defaults. Keep both private names ignored during
migration. Never commit real credentials. Firmware version and hardware revision
remain independent; a header rename alone does not change deployed behavior.

## Migration checks

Update imports, relative data/config paths, scripts, service entry points, tests,
CI, documentation and ignores together. Compare firmware bytes across pure moves
and run path-sensitive tests/builds. Inventory untracked private config and runtime
data before deploying; repository moves must not overwrite or strand them. Prepare
service rollback to the old commit/entry point and verify real data roots after
migration. Source layout adoption does not itself authorize production migration.

The user is the sign-off owner for consequential merges. Branding and part-number
allocation remain with the user; a future initial-flashing app may assign instance
identifiers after that policy is defined. Do not allocate or rename deployed IDs
as part of repository reorganization.

## Open engineering detail

These stay open before any work that depends on them: entity ID grammar and
effective-time bindings; filing of unassigned or unknown-time records and
corrections; storage formats and rotation; multi-file configuration
synchronization; the persistent-storage mechanism and permissions; consistent
snapshot mechanics; hot reconfiguration, reload and enable/disable transitions;
log rotation and retention.
