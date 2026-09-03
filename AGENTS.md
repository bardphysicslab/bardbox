# BardBox Agent Instructions

These instructions apply to AI agents and automated engineering tools working on the BardBox platform. The goal is to make AI-assisted work consistent with BardBox architecture rather than dependent on conversational memory.

## Before Making Changes

1. Read `ROADMAP.md` to understand the current platform direction and implementation order.
2. Read the protocol, standards, and implementation documentation relevant to the proposed change.
3. Read applicable Architecture Decision Records (ADRs) once they exist.
4. Inspect the current implementation and tests before proposing or making architecture-affecting changes.
5. Determine whether the requested change is project-specific or affects BardBox-wide behavior.

## Core Engineering Rules

- Prefer one canonical reusable implementation over copied implementations across repositories.
- Do not introduce a project-specific version of shared BardBox behavior without a documented reason.
- Treat the main `bardbox` repository as the authoritative source for BardBox-wide protocol and engineering standards.
- Project repositories should declare how they use BardBox rather than silently redefine BardBox-wide behavior.
- Keep deterministic validation, comparison, auditing, and data-access logic in shared tooling where practical.
- CLI and MCP interfaces should reuse the same underlying deterministic implementation rather than maintain separate logic.
- Keep AI integrations agent-agnostic where practical.
- Preserve raw data and machine-readable evidence when producing summaries or reports.

## Protocol and Architecture Conflicts

If a proposed or existing implementation conflicts with BardBox protocol or an accepted architecture decision:

1. Do not silently change the implementation to hide the conflict.
2. Do not silently change the BardBox protocol to accommodate the implementation.
3. Surface the conflict explicitly.
4. Determine whether the implementation is incorrect or whether the protocol genuinely needs to evolve.
5. Require human review for an intentional BardBox-wide protocol or architecture change.
6. Record accepted architecture changes in an ADR.
7. When a BardBox-wide standard changes, identify affected schemas, tests, shared libraries, the project template, and project repositories that may require coordinated updates.

## Verification

For significant changes, run the relevant deterministic checks before and after the change. As `bardbox-tools` matures, prefer the standard BardBox commands, including:

```text
bardbox doctor
bardbox audit
```

A normal audit should eventually cover at least:

- project identity and declared protocol version;
- configuration consistency;
- tests;
- Git working-tree status;
- local branch versus GitHub/upstream state;
- protocol compliance;
- shared dependency state;
- deployment/service state when applicable;
- data freshness when applicable.

Do not claim a check passed unless it was actually run or verified from trustworthy existing evidence.

## Git and Contributor Safety

- Inspect Git state before modifying a repository.
- Do not overwrite or discard another contributor's uncommitted work.
- Do not automatically pull, reset, rebase, merge, push, or otherwise rewrite contributor state merely to make a repository appear synchronized.
- Prefer reporting ahead/behind/diverged/dirty state and recommending the appropriate action.
- Keep changes scoped to the requested task.
- Use branches and reviewable changes for architecture or platform work.

## Consequential Actions

Human approval is required before consequential actions unless the user has explicitly authorized that specific action. Examples include:

- changing production configuration;
- deploying software or firmware;
- restarting production services;
- pushing or merging consequential changes;
- deleting or moving stored data;
- changing production device identity or network settings;
- destructive Git operations;
- broad automated migrations across repositories.

The ability to perform an action does not imply permission to perform it.

## Shared Components

Reusable drivers, protocol behavior, transport logic, buffering, configuration helpers, and other shared functionality should move toward canonical versioned libraries rather than being copied between projects.

The `bardbox-project-template` should demonstrate how to consume shared components and current standards. It should not become a second canonical copy of reusable implementations.

## Contributor Environment

BardBox should provide a reproducible contributor environment, primarily through Dev Containers/Docker plus pinned dependencies and matching CI checks.

The purpose of containerization is contributor and CI consistency. Hardware-facing runtime components may remain native where containerization would complicate GPIO, USB, serial, Digilent, networking, or other direct hardware access without a clear benefit.

Contributors working outside the standard container should eventually be able to use `bardbox doctor` to verify that their environment is compatible.

## AI and MCP Safety

- Prefer small, purpose-built MCP tools over arbitrary shell access.
- Start MCP capabilities read-only by default.
- Separate inspection capabilities from consequential-write capabilities.
- Retrieve structured summaries first and raw detail on demand to keep context focused.
- AI reasoning should interpret deterministic evidence; it should not replace deterministic validation.

## Planning and Tracking

Use the following hierarchy:

```text
BardBox protocol/specification  -> what BardBox must obey
ADRs                            -> why architectural decisions were made
ROADMAP.md                      -> where the platform is going
GitHub issues                   -> concrete implementation work
GitHub Project                  -> current work state
AGENTS.md                       -> how humans and AI should work
bardbox audit                   -> whether reality matches the above
```

When completing roadmap work, update the appropriate durable artifact rather than relying on a chat conversation to preserve the decision.