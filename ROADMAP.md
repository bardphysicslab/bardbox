# BardBox Platform Roadmap

This roadmap is the source of truth for evolving BardBox from a collection of related monitoring projects into a maintained, reusable platform with shared standards, tooling, data access, AI integration, and contributor workflows.

The roadmap is intentionally ordered by dependency rather than by fixed dates. Concrete implementation work should be tracked in GitHub issues and project boards, while architecture decisions should be recorded separately in ADRs.

## Guiding Principles

- BardBox behavior should be deterministic, testable, and inspectable before AI reasoning is applied.
- Shared functionality should have one canonical implementation whenever practical.
- Project-specific repositories should declare how they use BardBox rather than redefine BardBox-wide behavior.
- Protocol and architectural changes should be explicit and reviewed rather than silently introduced by one project.
- Human approval should remain required for consequential changes such as production configuration changes, deployments, pushes, service restarts, firmware updates, and destructive operations.
- Local development, CI, and deployment environments should be reproducible where practical, while hardware-facing runtime components may remain native when containerization would add unnecessary complexity.
- AI integrations should be agent-agnostic through MCP wherever possible.

## Phase 1 — BardBox Tools Foundation

Goal: establish one shared automation/tooling package that can be used by humans through a CLI and by AI agents through MCP.

- [ ] Evolve `bardbox-mcp` into the broader `bardbox-tools` package/repository structure.
- [ ] Keep reusable deterministic Python logic separate from interfaces.
- [ ] Provide CLI entry points for human use.
- [ ] Provide MCP entry points for AI-agent use.
- [ ] Preserve existing BardBox query functionality during the transition.
- [ ] Move the config comparator into shared BardBox tooling.
- [ ] Add reusable Git inspection helpers.
- [ ] Add project discovery/registration.

Proposed structure:

```text
bardbox-tools/
├── core/
│   ├── config_compare.py
│   ├── git.py
│   ├── audit.py
│   ├── data_query.py
│   ├── drive.py
│   └── protocol.py
├── cli/
└── mcp/
```

## Phase 2 — Project Manifest and Standard Audit

Goal: make every BardBox project self-describing and machine-auditable.

- [ ] Define a small project manifest, tentatively `bardbox.toml`.
- [ ] Record project name, project type, protocol version, config locations, test commands, deployment/service metadata, and shared-library dependencies.
- [ ] Add `bardbox audit`.
- [ ] Make audits produce both human-readable output and machine-readable JSON.
- [ ] Check runtime config against example/schema.
- [ ] Check test status.
- [ ] Check Git working-tree state.
- [ ] Check current branch and upstream relationship.
- [ ] Check local HEAD against GitHub remote state.
- [ ] Check BardBox protocol compliance.
- [ ] Check deployment/service state where available.
- [ ] Add `bardbox doctor` for contributor environment checks.

Example audit areas:

```text
Protocol
Config
Tests
Git working tree
Local vs origin
Dependencies
Deployment
Data freshness
```

## Phase 3 — MCP and Safe Agent Access

Goal: expose BardBox capabilities to ChatGPT, Claude, Codex, Kimi, and other MCP-capable agents through a small, safe interface.

- [ ] Define a deliberately small MCP tool surface.
- [ ] Reuse the same Python implementation as the CLI.
- [ ] Start read-only by default.
- [ ] Expose project status, audits, diffs, protocol status, and data queries.
- [ ] Separate inspection permissions from consequential-write permissions.
- [ ] Require explicit human approval for consequential actions.
- [ ] Avoid arbitrary shell execution through MCP.

Candidate MCP tools:

```text
list_projects()
get_project_status(project)
audit_project(project)
get_project_diff(project)
get_protocol_status(project)
query_data(...)
get_audit_details(project, section)
```

## Phase 4 — Automatic Project Health Monitoring

Goal: continuously detect project drift without automatically overwriting contributor work.

- [ ] Add a lightweight scheduled BardBox audit process on development machines where useful.
- [ ] Track registered local BardBox repositories.
- [ ] Detect uncommitted changes.
- [ ] Detect local branches ahead of or behind GitHub.
- [ ] Detect stale dependencies.
- [ ] Detect failing tests or protocol checks.
- [ ] Produce status reports rather than automatically pulling/pushing by default.
- [ ] Expose these status reports through MCP.
- [ ] Add notifications or scheduled summaries later if useful.

The system should distinguish conditions such as:

```text
clean and in sync
clean but behind origin
clean but ahead of origin
modified working tree
branch diverged
protocol mismatch
test failure
```

## Phase 5 — BardBox Data and Report Layer

Goal: let humans and AI query, analyze, and report on BardBox data independent of where that data is physically stored.

- [ ] Create a unified BardBox data abstraction.
- [ ] Keep the BardBox API as the preferred interface for recent/live operational data.
- [ ] Add BardBox Drive/archive access for historical datasets and backups.
- [ ] Allow data queries through CLI and MCP.
- [ ] Preserve raw data access for analysis.
- [ ] Add report-generation workflows.
- [ ] Allow restricted report writes to approved report/archive locations.
- [ ] Archive generated reports to BardBox Drive where appropriate.
- [ ] Keep Drive as archive/storage rather than coupling the AI architecture directly to a personal Google account wherever possible.

Conceptual flow:

```text
AI Agent
   ↓ MCP
bardbox-tools
   ↓
BardBox data layer
   ├── BardBox API
   └── BardBox Drive/archive
```

## Phase 6 — Protocol Compliance and Governance Automation

Goal: make BardBox standards enforceable and ensure intentional deviations trigger architectural review rather than silent drift.

- [ ] Treat the main `bardbox` repository as the authoritative specification/governance source.
- [ ] Convert important protocol requirements into machine-checkable schemas/tests where practical.
- [ ] Run protocol checks in CI.
- [ ] Fail deterministic checks when an implementation violates the current BardBox protocol.
- [ ] Distinguish an implementation bug from a legitimate proposed protocol change.
- [ ] When intentional incompatibility is detected, create a structured architecture discussion rather than silently changing either side.
- [ ] Record accepted architecture changes in ADRs.
- [ ] Update protocol documentation when approved.
- [ ] Update schemas/tests when approved.
- [ ] Update `bardbox-project-template` when the standard changes.
- [ ] Identify all affected BardBox repositories.
- [ ] Create migration/update work for affected repositories.

Expected decision path:

```text
implementation conflicts with BardBox protocol
                ↓
        deterministic failure
                ↓
            AI review
                ↓
    implementation bug?
          or
    protocol should evolve?
                ↓
         human decision
                ↓
 coordinated protocol/template/project updates
```

## Phase 7 — Shared Drivers and Node Libraries

Goal: eliminate duplicated reusable hardware and protocol code across projects.

- [ ] Define canonical shared Python driver libraries.
- [ ] Define canonical shared ESP32/PlatformIO libraries.
- [ ] Move reusable sensor/device drivers into shared packages where appropriate.
- [ ] Move reusable BardBox transport, buffering, protocol, configuration, and node behavior into shared libraries where appropriate.
- [ ] Version shared libraries.
- [ ] Pin project dependencies to known-good versions.
- [ ] Add dependency-update workflows.
- [ ] Ensure fixes can propagate through version upgrades rather than manual copy/paste.

Examples of reusable components include:

```text
PMS5003/PMS6003 drivers
BME drivers
MAX31865 driver
SPN1 driver
ET5406A driver
Web Node transport
persistent buffering
config/schema helpers
```

The project template should demonstrate how to consume shared libraries; it should not contain duplicated canonical copies of every driver.

## Phase 8 — Reproducible Contributor Environments

Goal: reduce environment drift and make collaboration predictable.

- [ ] Define a shared BardBox development environment.
- [ ] Add Dev Container support where useful.
- [ ] Pin Python versions and important dependencies.
- [ ] Pin/test PlatformIO and firmware tooling where practical.
- [ ] Align local development tooling with GitHub Actions CI.
- [ ] Include linters, formatters, type checks, tests, and `bardbox-tools` in the standard environment.
- [ ] Keep direct hardware runtime native where Docker/device mapping would create unnecessary complexity.
- [ ] Use `bardbox doctor` to verify contributors who work outside the container.

## Phase 9 — Project Template Alignment

Goal: make new BardBox projects start compliant rather than requiring cleanup later.

- [ ] Ensure `bardbox-project-template` consumes the current BardBox standards.
- [ ] Include a project manifest.
- [ ] Include standard tests and CI hooks.
- [ ] Include Dev Container configuration where appropriate.
- [ ] Include shared-library dependency examples rather than copied implementations.
- [ ] Automatically detect when the template becomes incompatible with current BardBox standards.
- [ ] Propose/update the template when accepted protocol changes require it.

## Phase 10 — AI-Aware Engineering Workflow

Goal: make AI contributors useful without making BardBox dependent on any one AI vendor or relying on conversational memory.

- [ ] Add concise `AGENTS.md` instructions to the BardBox control repository and relevant project repositories.
- [ ] Require agents to read the roadmap, applicable protocol documents, and relevant ADRs before architecture-affecting changes.
- [ ] Teach agents to prefer shared solutions over project-specific duplication.
- [ ] Require before/after audits for significant changes.
- [ ] Require protocol conflicts to be surfaced rather than silently resolved.
- [ ] Use MCP as the agent-agnostic interface to BardBox tooling.
- [ ] Keep GitHub issues/project boards as the live work tracker.
- [ ] Keep ADRs as the permanent record of architectural decisions.

## Tracking Model

The intended hierarchy is:

```text
BardBox protocol/specification
    "What must BardBox obey?"

Architecture Decision Records
    "Why did we design it this way?"

ROADMAP.md
    "Where are we going?"

GitHub Issues
    "What specifically needs doing?"

GitHub Project
    "What are we doing right now?"

AGENTS.md
    "How should humans and AI work here?"

bardbox audit
    "Does the implementation actually match all of the above?"
```

## Initial Implementation Order

Do not attempt the whole roadmap at once. Start with this sequence:

1. Establish this roadmap as the planning source of truth.
2. Add `AGENTS.md` and initial ADRs for the decisions already made.
3. Complete the `bardbox-tools` foundation.
4. Define the project manifest.
5. Move the config comparator into `bardbox-tools`.
6. Add Git/local-vs-GitHub audit support.
7. Implement `bardbox audit`.
8. Expose the audit through CLI and MCP.
9. Validate the workflow across `solar-monitor`, `rkc-monitor`, and `cesh-air-monitor`.
10. Add automatic project-health monitoring.
11. Add unified BardBox data/archive access and report generation.
12. Add protocol-governance automation.
13. Refactor reusable drivers and node code into shared versioned libraries.
14. Add reproducible contributor environments and align CI.
15. Bring `bardbox-project-template` fully under automated compliance checks.

## Near-Term Definition of Done

The first major milestone is complete when a contributor or AI agent can ask BardBox for the health of any registered project and receive a deterministic report covering at least:

- project identity and protocol version;
- config consistency;
- tests;
- Git working-tree status;
- local-vs-GitHub status;
- protocol compliance;
- relevant dependency state;
- enough structured output for an AI agent to explain problems without needing unrestricted shell access.

At that point, BardBox will have the foundation of a maintainable multi-repository platform rather than relying on individual contributors to remember conventions manually.
