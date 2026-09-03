# ADR-004: MCP Permissions and AI Safety Model

- **Status:** Accepted
- **Date:** 2026-09-03

## Context

BardBox will expose project status, audits, diffs, protocol state, and data queries to AI agents through MCP and other interfaces. Those capabilities are useful because they let an agent inspect BardBox directly instead of relying on copied terminal output or stale context.

The same interface could become dangerous if it also provided unrestricted shell access, arbitrary filesystem access, deployment commands, production configuration writes, service restarts, destructive Git operations, or data deletion.

BardBox therefore needs a clear permission model that supports useful AI-assisted engineering while keeping consequential operations under explicit human control.

## Decision

BardBox AI/MCP access will be **read-only by default**, purpose-built, and separated from consequential write operations.

The primary design principle is:

> AI should be able to inspect broadly, reason from deterministic evidence, and propose changes; consequential actions should require an explicit authorization boundary.

## Read-only inspection surface

The standard MCP interface may expose high-level inspection operations such as:

```text
list_projects()
get_project_status(project)
audit_project(project)
get_project_diff(project)
query_data(...)
get_audit_details(project, section)
get_protocol_status(...)
```

These tools should return structured summaries first, with raw evidence available on demand where useful.

The interface should not expose arbitrary shell execution merely because an AI agent could use it to reproduce the same information.

## Deterministic evidence first

MCP should call `bardbox-tools` deterministic core functions rather than implementing checks inside the MCP server.

Conceptually:

```text
AI
 ↓
MCP interface
 ↓
bardbox-tools
 ↓
deterministic evidence
```

AI reasoning may explain a mismatch, recommend a migration, or identify likely causes, but deterministic checks remain independently inspectable.

## Consequential actions

The following classes of actions require explicit human authorization unless a narrower capability has been deliberately pre-authorized:

- modifying production configuration;
- deploying firmware or software to production systems;
- restarting or stopping production services;
- pushing or merging consequential Git changes;
- rebasing, resetting, force-pushing, or other destructive Git operations;
- deleting or moving production/archive data;
- changing device or network settings;
- broad multi-repository migrations;
- changing protocol/governance rules with platform-wide consequences.

Read and write capabilities should be separate interfaces wherever practical. A future write-capable tool should make the requested action explicit rather than hiding it behind a generic command executor.

## No arbitrary shell as the normal AI interface

BardBox MCP should not provide unrestricted shell access as its standard engineering interface.

High-level purpose-built tools are preferred because they:

- constrain the blast radius;
- provide stable machine-readable results;
- make permissions understandable;
- are easier to test;
- reduce accidental access to secrets;
- create a clearer audit trail.

A human or explicitly authorized development agent may still use normal development tools in a controlled local environment. That is separate from granting a general remote AI interface arbitrary command execution.

## Secrets

Secrets should remain outside repositories and normal MCP responses. Tools should retrieve credentials only through the appropriate local/runtime secret mechanism and should avoid returning secret values to the AI.

Where an operation can be completed without exposing a token, password, client secret, or private key to the agent, it should be designed that way.

## Git model

AI should normally be allowed to inspect repository state, diffs, branches, commits, tests, and pull requests.

When changes are requested, the preferred workflow is:

```text
AI prepares/scopes change
        ↓
feature branch / pull request
        ↓
CI + BardBox compliance checks
        ↓
human review where required
        ↓
merge
```

Direct mutation of protected production branches is not the normal AI workflow.

This policy complements repository branch protections, CODEOWNERS/review rules, and CI. MCP permissions do not replace GitHub enforcement.

## Data access

AI may inspect BardBox operational and scientific data through purpose-built data-query interfaces. Raw data should remain preserved and queryable.

Google Drive or other archive storage may be used for backup, historical files, and generated reports, but archive storage should not become a substitute for a controlled BardBox data/API interface.

If report-writing capability is added, it should be restricted to designated report/output locations rather than arbitrary file overwrite/delete access.

## Auditability

Consequential agent-assisted actions should be attributable and reviewable through normal system records such as Git commits/PRs, deployment logs, audit reports, or explicit action logs.

Agents should not claim an operation succeeded unless the operation or deterministic verification actually ran and returned evidence of success.

## Capability evolution

Read-only-by-default does not mean BardBox can never automate writes.

New write capabilities may be added when they have:

1. a clearly defined purpose;
2. narrow inputs and outputs;
3. deterministic preconditions where practical;
4. an explicit authorization model;
5. appropriate logging/auditability;
6. a safe failure mode;
7. human approval where the consequence warrants it.

A narrowly scoped operation such as creating a report file or opening a pull request is preferable to a generic "run anything" capability.

## Consequences

### Positive

- AI can inspect BardBox deeply without receiving broad destructive authority.
- Permissions are easier for maintainers and contributors to understand.
- Deterministic BardBox checks remain reusable outside AI workflows.
- Secrets and production systems have a smaller exposure surface.
- High-risk actions naturally pass through human review and existing Git/deployment controls.
- Future automation can be introduced incrementally rather than granting unrestricted access up front.

### Costs and constraints

- Some agent workflows require an extra approval step.
- Purpose-built tools require more design effort than exposing a shell.
- Write automation must be implemented capability by capability.
- Permission boundaries need tests and maintenance as BardBox grows.

## Alternatives considered

### Give the AI unrestricted shell/SSH access

Rejected as the default architecture because the permission surface is too broad, secrets are harder to isolate, and consequential actions are difficult to constrain or audit reliably.

### Make MCP permanently read-only

Rejected because carefully scoped future automation can be valuable. The system should permit explicit, narrow, reviewable write capabilities rather than forbidding them categorically.

### Rely on prompting the AI not to perform dangerous actions

Rejected because safety requirements should be enforced by capabilities, permissions, CI, repository rules, and human approval rather than prompt compliance alone.

## Follow-up

Implement the first BardBox MCP surface as read-only and high-level. Keep its tool count small. Add write capabilities only after the relevant deterministic tooling, permission boundary, review path, and audit trail exist.
