# ADR-001: BardBox Tools as the Shared Deterministic Tooling Layer

- **Status:** Accepted
- **Date:** 2026-09-03

## Context

BardBox projects need common engineering operations such as configuration comparison, repository inspection, protocol/compliance checks, test orchestration, deployment/status inspection, data queries, report generation, and eventually archive synchronization.

Some of this functionality has previously lived in individual project repositories or in `bardbox-mcp`. Copying these utilities between projects creates drift and makes it difficult to know which implementation is authoritative. Putting engineering logic directly into an AI or MCP interface would also make verification dependent on the interface being used.

BardBox needs one deterministic implementation that can be used by humans, CI, AI agents, and other automation.

## Decision

Create and evolve **`bardbox-tools`** as the shared deterministic engineering-tooling layer for BardBox.

The core implementation must be ordinary, testable Python code. User and agent interfaces must call that shared implementation rather than reimplementing the same behavior.

Conceptually:

```text
bardbox-tools/
├── core/
│   ├── config_compare.py
│   ├── git.py
│   ├── audit.py
│   ├── drive.py
│   └── data_query.py
├── cli/
└── mcp/
    └── server.py
```

The exact package layout may evolve without changing this decision.

### Interfaces

The command-line interface should expose high-level operations such as:

```text
bardbox doctor
bardbox config-check
bardbox git-status
bardbox audit
bardbox query
```

The MCP interface should remain small and purpose-built, exposing high-level capabilities such as project status, audits, diffs, protocol status, and data queries rather than arbitrary shell access or a large collection of tiny tools.

### Deterministic evidence first

Checks such as configuration comparison, Git state, protocol compliance, dependency state, and test results must be determined by code wherever practical. AI may interpret that evidence and recommend actions, but AI reasoning is not a replacement for deterministic validation.

### Safety

Inspection capabilities should be read-only by default. Consequential operations such as production deployment, destructive Git operations, production configuration changes, service restarts, data deletion, or broad migrations require explicit authorization and should be separated from ordinary inspection interfaces.

### Relationship to `bardbox-mcp`

The existing `bardbox-mcp` work should evolve toward or become part of `bardbox-tools`. MCP is an interface to BardBox tooling, not an independent implementation layer. Existing executable names may be retained temporarily for compatibility during migration.

## Consequences

### Positive

- One canonical implementation of common BardBox engineering checks.
- CLI, CI, MCP, and AI workflows can produce consistent results.
- Project repositories no longer need copied utility implementations.
- Deterministic evidence can be archived and inspected independently of an AI conversation.
- New agent interfaces can be added without duplicating engineering logic.

### Costs and constraints

- Existing copied utilities will need gradual migration.
- `bardbox-mcp` naming/package structure may require compatibility handling during transition.
- Shared tooling becomes infrastructure and therefore requires tests, versioning, and careful backwards compatibility.
- Hardware- or deployment-specific checks may still require project adapters rather than forcing all behavior into a generic core.

## Alternatives considered

### Keep utilities in each project repository

Rejected because copied implementations drift and make platform-wide compliance difficult to verify.

### Put the logic primarily in MCP tools

Rejected because CLI, CI, and non-MCP agents would then need duplicate implementations or depend on an AI-facing protocol to perform deterministic engineering work.

### Let AI agents perform the checks themselves

Rejected because results would depend on model behavior, available context, and prompting rather than reproducible validation.

## Follow-up

Initial implementation should establish the `bardbox-tools` package and shared core, then add the project manifest, configuration comparator, Git inspection, `bardbox audit`, `bardbox doctor`, and the small MCP interface in the roadmap order.
