# BardBox Cross-Repo Platform and Tooling Audit — 2026-09-08

## Purpose

This audit reviews BardBox projects as a portfolio rather than treating any one deployment as the reference for everything. The goal is to identify proven patterns across repositories, classify what is platform-wide versus project-specific, and define the next consolidation work for standards, shared tooling, the project template, and reproducible development environments.

The governing rule is:

> Promote the best proven BardBox behavior from across the ecosystem into one canonical standard or shared implementation. Do not preserve duplication merely because a pattern first appeared in a production repository.

## Repositories reviewed

Primary platform/control repositories:

- `bardphysicslab/bardbox`
- `bardphysicslab/bardbox-tools` including the active `codex/bardbox-tools` restructuring branch
- `bardphysicslab/bardbox-project-template`

Production/project implementations reviewed for reusable patterns:

- `bardphysicslab/cesh-air-monitor`
- `bardphysicslab/rkc-monitor`
- `bardphysicslab/solar-monitor`
- `bardphysicslab/btex-air-sensor`
- `bardphysicslab/bardbox-labcheck`

CESH Noise does not currently appear as a separate repository and should be evaluated within whichever repository owns its implementation when that code is promoted or split.

## Executive findings

1. **BardBox already has the right architectural direction, but the implementation is between copied helpers and shared tooling.** The roadmap, agent instructions, and `bardbox-tools` direction all call for one deterministic implementation exposed through CLI and MCP. Existing project repositories still contain duplicated helper scripts.

2. **Operational resilience is mature enough to standardize now.** RKC and CESH both implement side-effect-free `/health`, systemd process recovery, and an independent watchdog. The project template also carries the pattern.

3. **Verified archival backup is mature enough to standardize now, but Solar still has a conflicting backup model.** CESH's non-destructive copy + verification manifest + exact-version retention model is safer for an archive. Solar's snapshot approach has a useful application-lock/snapshot idea, but its documented `rclone sync` behavior conflicts with the archive invariant that remote history must not be deleted by source disappearance.

4. **Configuration synchronization is clearly platform-wide code.** CESH and Solar carry the same `sync_app_config.py` implementation; RKC carries a close variant. The project template carries another canonical copy. This is now duplicated shared infrastructure and should move behind `bardbox-tools`.

5. **Local engineering helpers are also platform functionality.** Git status, config comparison, audit reports, environment checks, data query/retrieval, and MCP exposure belong in `bardbox-tools`, with CLI and MCP sharing deterministic core logic.

6. **`bardbox.toml` is the right machine-readable project boundary but is not yet universal.** LabCheck already uses it and `bardbox-tools` already consumes it for `doctor`, `audit`, config checks, tests, and Git checks. Existing monitor repos should adopt manifests incrementally.

7. **RKC contributes several strong application-architecture patterns that should be promoted as principles or reusable interfaces, not copied as freezer-specific code.** These include policy separation from Twilio, explicit acknowledgement/escalation state, audit logging independent of periodic sensor logging, safe simulation/live-test separation, and preserving alarm-condition visibility when notifications are disabled.

8. **Solar contributes an important concurrency pattern.** Independent acquisition loops prevent slow Wi-Fi polling from delaying fresh SPN1 serial acquisition. The platform principle is broader: unrelated acquisition sources should not block one another when they have different timing/failure characteristics.

9. **LabCheck validates the project-manifest, deterministic-runner, capability-interface, evidence-preservation, and safe-state direction.** Those ideas should feed BardBox architecture and shared driver contracts while LabCheck-specific test suites remain local.

10. **Docker/Dev Containers should begin now for contributor and CI reproducibility, but not as a blanket production-runtime rule.** Containerization solves Python/tool/dependency drift; shared versioned packages solve cross-repo code drift. Both are needed. Docker alone cannot keep copied code synchronized.

## Classification model

Every reusable finding should land in exactly one primary bucket.

### 1. Canonical BardBox standard

A documented behavior or contract applicable to every relevant project.

Examples:

- normalized reading/status semantics;
- service restart and watchdog rules;
- config/example separation and migration behavior;
- backup archive invariants;
- project manifest schema;
- driver/capability boundaries;
- source-of-truth and deployment rules;
- safe AI/automation permission boundaries.

### 2. Shared BardBox implementation

Executable logic that should exist once and be versioned centrally.

Primary home: `bardbox-tools` for Python/local/CLI/MCP engineering tooling. Separate shared runtime/firmware packages may be justified later where deployment dependencies require them.

Candidates identified in this audit:

- config comparison and config migration/synchronization;
- Git repository inspection;
- project discovery and manifest loading;
- project audit and machine-readable reports;
- contributor `doctor` checks;
- production-vs-Git audit report generation/parsing;
- service/deployment inspection;
- standard health/watchdog verification;
- backup verification/manifest logic;
- standard archive-retention verification;
- data file discovery/retrieval/query packaging;
- shared CSV naming/path helpers;
- protocol compliance checks;
- shared driver capability contracts;
- MCP wrappers over the same deterministic functions used by the CLI.

### 3. Project-template material

Scaffolding and examples that teach a new project how to consume current BardBox standards and shared packages.

The template should increasingly contain configuration and integration examples rather than canonical copies of reusable implementations.

### 4. Project-specific behavior

Logic that should remain in the deployment repository.

Examples:

- RKC freezer thresholds, phone-chain policy, freezer UI content, and incident semantics;
- CESH PurpleAir/QuantAQ-specific ingestion and analysis helpers;
- Solar SPN1/solar-panel-specific acquisition and presentation;
- LabCheck test-suite sequences and DUT-specific procedures;
- project-specific deployment identities, credentials, endpoints, and hardware inventory.

## Cross-repo comparison

| Concern | Strongest current evidence | Platform decision |
| --- | --- | --- |
| Process crash recovery | RKC, CESH, project template | Standardize `Restart=always`, `RestartSec=5` for long-running FastAPI/Uvicorn services. |
| Hung-web-app recovery | RKC, CESH, project template | Standardize side-effect-free `/health` plus independent watchdog timer. |
| Rich application health | RKC | Keep separate from `/health`; useful project/application endpoint but must not burden the liveness probe. |
| Config example/live separation | CESH, RKC, Solar, template | Required where `app_config` is used. |
| Config synchronization | CESH/Solar identical helper; RKC variant; template copy | Move canonical merge/check logic to `bardbox-tools`; retain thin compatibility wrappers only during migration. |
| Git/config/project audit | `bardbox-tools` | Canonical shared implementation; expand rather than recreating shell reports per repo. |
| Human + AI interfaces | `bardbox-tools` | CLI and MCP must call the same deterministic core functions. |
| Project manifest | LabCheck + `bardbox-tools` | Promote `bardbox.toml` to the standard machine-readable project descriptor and roll out incrementally. |
| Historical archive + retention | CESH | Promote verified copy + manifest + exact-version retention invariants. |
| Snapshot before network backup | Solar | Useful optional technique for applications whose writers need a stable snapshot; does not override archive safety invariants. |
| `rclone sync` to archive | Solar | Do not promote. Replace for archival destinations because deletion propagation conflicts with BardBox archive semantics. |
| Active daily CSV handling | CESH | Promote: may upload active files, but verify/retention only after stable/closed. |
| Data filename identity | CESH and newer RKC exports | Prefer UID in filename for new per-node datasets; keep legacy readers during migration. File cadence may remain project-specific when justified. |
| Incident/event logging | RKC | Promote principle: operational events should be durable independently of periodic sensor samples when events matter operationally. |
| Notification provider boundary | RKC architecture | Promote provider-neutral notification interface; Twilio remains an implementation. |
| Safe live-vs-simulation testing | RKC | Promote pattern for consequential external actions: isolated simulation plus explicit live-test enablement and unmistakable test labeling. |
| Independent acquisition loops | Solar | Promote concurrency principle when sources have different timing/failure behavior. |
| Deterministic runner / safe state | LabCheck | Promote architecture principle; application-specific procedures remain local. |
| Capability-oriented drivers | LabCheck/BardBox driver direction | Continue toward shared capability contracts instead of device-shaped application APIs. |
| Local data API | CESH/template | Keep generic read-only data access behind narrow authenticated API where the data root is safe to expose. |
| Local Python helper scripts | all monitor repos | Audit each helper; platform-generic helpers move to shared tools, project-specific helpers stay local. |
| Setup/restart/health shell scripts | CESH/RKC/Solar/template | Replace duplicated logic over time with manifest-driven `bardbox` commands or generated deployment assets. |
| Dev environment | platform roadmap | Start Dev Container prototype now; align with CI. |
| Hardware production runtime | RKC/Solar/LabCheck | Native runtime remains acceptable when direct GPIO/USB/serial/device access is simpler and safer. |

## Shared-tooling consolidation target

The desired architecture is:

```text
Human / shell                         AI / MCP client
      |                                      |
      +---------------+  +-------------------+
                      v  v
                 bardbox-tools
             deterministic core logic
      config | git | audit | deploy | data | protocol
                      |
          +-----------+-----------+
          |                       |
     local repos             BardBox APIs
          |
    project manifests
```

Project repositories should describe themselves and carry project behavior. They should not maintain independent implementations of generic BardBox maintenance logic.

### Near-term CLI direction

The exact command surface can evolve, but the following is the intended class of functionality:

```text
bardbox doctor
bardbox audit
bardbox git-status
bardbox config check
bardbox config sync
bardbox deploy audit
bardbox service check
bardbox backup check
bardbox data query
```

These commands should consume `bardbox.toml` wherever possible rather than embedding RKC/CESH/Solar paths in shared code.

## `bardbox.toml` expansion

The existing LabCheck manifest proves the minimal concept. The next schema should support applicable fields such as:

```toml
project = "solar-monitor"
project_type = "monitor"
bardbox_protocol = "0.3"

[config]
example = "raspi/config/app_config.example.json"
runtime = "raspi/config/app_config.json"

[tests]
command = "pytest"

[service]
name = "solar-monitor"
health_url = "http://127.0.0.1:8000/health"

[data]
readings_root = "data/sensor_data"
filename_policy = "uid-daily"

[backup]
mode = "verified-archive"
```

Not every project needs every section. Hardware/instrumentation projects may declare different runtime and service fields.

## Helper-script migration policy

Do not mass-delete existing helpers immediately. Use a compatibility migration:

1. identify generic logic;
2. move/test it in `bardbox-tools`;
3. expose a stable CLI/API;
4. replace per-repo implementation with a thin wrapper only if compatibility is needed;
5. update template/examples to call the shared tool;
6. migrate active repositories;
7. delete obsolete copies only after the shared path is proven.

Project-specific scripts remain local. Examples include CESH's PurpleAir fetcher, RKC's freezer export, and Solar's SPN1 probe.

## Source-of-truth and production drift

GitHub/Git is the source of truth for code, deployment assets, schemas, and templates. Production hosts may contain deployment-local config, credentials, runtime state, data, and generated state, but should not accumulate unique source code or infrastructure behavior.

Production comparison should therefore become a standard read-only audit workflow:

```text
production host
    -> read-only manifest-driven inventory/report
    -> compare with repository declarations
    -> report drift
    -> fix source in Git
    -> deploy through reviewed Git update
```

The audit tool should prefer structured JSON plus a concise human view. It should not require an AI agent to have arbitrary root shell access merely to determine drift.

## Docker / Dev Container decision

### What Docker solves

- pinned Python/tool versions;
- reproducible dependencies;
- consistent local contributor setup;
- equivalent local/CI checks;
- a known environment for Codex/other coding agents;
- simpler onboarding.

### What Docker does not solve

- duplicated helper scripts across repositories;
- outdated code pinned inside different images;
- production config governance;
- protocol drift;
- Git branch/source-of-truth problems.

Those require shared versioned packages, manifests, deterministic audits, and governance.

### Decision

Begin one BardBox Dev Container prototype now, in parallel with `bardbox-tools` consolidation. Do not wait until every shared library is finished. The prototype should include:

- a pinned Python version;
- `bardbox-tools` installed from the intended development source/version;
- pytest and standard quality checks;
- enough tooling to run `bardbox doctor` and `bardbox audit`;
- no privileged hardware passthrough unless the selected prototype actually requires it;
- a matching GitHub Actions environment/check sequence where practical.

After the prototype is proven, roll it out to software-heavy BardBox repos. Decide production containerization separately per service. A VPS-hosted FastAPI service is a stronger production-container candidate than a Pi service whose primary job is direct GPIO/USB/serial hardware interaction.

## Repository-specific notes

### `bardbox`

- Architecture principles and promotion governance are already strong foundations.
- The roadmap branch correctly defines shared tools, MCP safety, manifests, Dev Containers, shared drivers, and template alignment.
- Standards currently need stronger wording that promotion comes from cross-repo comparison, not a single reference deployment.
- Some documentation still names the old `bardbox-mcp` local path and should be updated to the `bardbox-tools` direction.

### `bardbox-tools`

- This is the correct home for local Python/MCP/CLI engineering utilities.
- Current implementation already includes manifest loading, config comparison, Git inspection, `doctor`, `audit`, JSON audit output on the active restructuring branch, query tooling, and MCP/data access.
- Finish the package/module rename and remove documentation paths that still assume `~/Code/bardcollege/bardbox-mcp`.
- Next high-value additions are manifest-driven config sync and deployment/service audit.

### `bardbox-project-template`

- Correctly demonstrates service/watchdog/config/Data API patterns.
- Still carries canonical script copies. Over time these should become calls/wrappers around shared tooling rather than a second source of truth.
- Its backup reference already points at the safer verified archive model.
- Add `bardbox.toml` and Dev Container support after the manifest/tooling contract is stable enough.

### `cesh-air-monitor`

Promote/platform candidates:

- verified non-destructive archive backup;
- backup manifest and retention invariants;
- active daily file exclusion from verification;
- watchdog deployment pattern;
- config-sync semantics;
- UID-bearing daily filenames for new per-node data;
- generic read-only historical Data API pattern.

Keep local:

- PurpleAir/QuantAQ integration and project-specific analysis/ingestion.

### `rkc-monitor`

Promote/platform candidates:

- simple `/health` separated from richer app health;
- two-layer service recovery;
- provider-neutral alarm architecture;
- durable incident/event logging separate from periodic sampling;
- simulation/live external-action testing separation;
- explicit auditability of operational changes;
- configuration-driven deployment values;
- safe legacy compatibility during config/schema evolution.

Keep local:

- freezer alarm semantics and escalation policy;
- Twilio-specific provider implementation;
- freezer export transformation;
- RKC dashboard content.

### `solar-monitor`

Promote/platform candidates:

- independent acquisition loops for sources with different latency/failure characteristics;
- writer lock + stable snapshot concept where a backup job needs a coherent source view;
- configuration-driven backup interval with dry-run generation concept, if generalized through manifest-driven tooling.

Do not promote unchanged:

- archival `rclone sync` behavior;
- template-era service-name assumptions still present in helper scripts.

### `btex-air-sensor`

- Confirms config synchronization has already spread beyond the original monitor repos.
- Treat firmware/sensor behavior as a future source for shared ESP32/sensor libraries once the protocol/library boundaries are ready.

### `bardbox-labcheck`

Promote/platform candidates:

- `bardbox.toml` project identity;
- deterministic audit-first workflow;
- explicit distinction between platform-generic drivers/tools and project-specific procedures;
- deterministic runner/safe-state principles;
- capability-oriented driver boundary.

Keep local:

- test suite definitions;
- DUT procedures and pass/fail policy;
- LabCheck-specific station UI and result models.

## Immediate implementation order

1. Land this cross-repo audit and make cross-repo promotion the formal governance rule.
2. Finish the `bardbox-tools` package/module rename and merge the active audit/tooling work.
3. Define/expand the `bardbox.toml` schema for monitor/service projects.
4. Move config sync/check logic into `bardbox-tools` and leave temporary wrappers in projects.
5. Add manifest-driven `bardbox deploy audit` / `bardbox service check` read-only inspection.
6. Add a standard production-vs-Git drift report format.
7. Add `bardbox.toml` to one existing monitor and validate `doctor` + `audit` end to end.
8. Prototype the Dev Container and equivalent CI checks in one software-heavy repo.
9. Reconcile Solar backup behavior with the verified archive standard while preserving any useful snapshot/locking technique.
10. Audit RKC, CESH, Solar, BTEX, and LabCheck helper scripts one by one and migrate only genuinely generic logic to shared tooling.
11. Update `bardbox-project-template` to consume shared tooling and include the manifest/Dev Container contract.
12. Continue shared-driver and firmware-library extraction only after the tooling/manifests can report dependency versions and compliance.

## Definition of success

BardBox has completed this consolidation stage when:

- a project declares its BardBox identity and relevant paths in `bardbox.toml`;
- `bardbox doctor` and `bardbox audit` work without project-specific code in the tooling package;
- config/Git/service/deployment checks are implemented once in shared tooling;
- production drift can be inspected read-only and fixed through Git rather than by editing production first;
- new projects inherit the standard through the template;
- existing projects can migrate without breaking project-specific behavior;
- contributor/AI environments are reproducible through the Dev Container/CI baseline;
- copied generic helper scripts are steadily disappearing instead of multiplying.
