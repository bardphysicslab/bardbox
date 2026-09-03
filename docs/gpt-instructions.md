# GPT Instructions for BardBox

This file is retained as a compatibility entry point for GPT-style assistants.
It is **not** a separate source of BardBox rules.

## Canonical Agent Instructions

Before helping with BardBox engineering work, read the repository-level
`AGENTS.md` and follow it as the authoritative agent/contributor instruction
entry point.

`AGENTS.md` defines how AI-assisted BardBox work should be performed, including:

- repository and platform authority;
- protocol and architecture conflict handling;
- deterministic verification expectations;
- Git and contributor safety;
- consequential-action approval requirements;
- shared-component policy;
- contributor environment expectations;
- MCP/AI safety;
- planning and tracking conventions.

## Detailed BardBox Standards

Do not duplicate detailed technical standards in this file. Read the relevant
canonical documentation under `docs/` for the work being performed. Examples
include:

- `device-instructions.md` for firmware/device behavior;
- `pi-driver-instructions.md` for Raspberry Pi driver contracts;
- `pi-runtime-instructions.md` for Pi runtime behavior;
- `monitor-instructions.md` for monitor/backend behavior;
- `node-naming-standard.md` for node identity;
- `channel-names.md` for normalized channel names;
- `reading-format.md` for reading/status representation;
- `service-operations-standard.md` for service operations;
- `promotion-governance.md` for promoting BardBox-wide behavior;
- applicable protocol documents, including the Web Node Protocol where relevant.

## Rule of Precedence

For AI-assisted work:

1. Follow `AGENTS.md` for engineering/contributor behavior.
2. Follow accepted ADRs for architecture decisions.
3. Follow the applicable BardBox protocol and detailed standards under `docs/`.
4. Follow project-specific instructions where they do not conflict with BardBox-wide standards.

If an implementation conflicts with BardBox standards, do not silently choose
one side. Follow the conflict-handling process in `AGENTS.md` and surface the
conflict for review.

This compatibility file should remain intentionally short so GPT-specific
instructions cannot drift into a second copy of BardBox policy.
