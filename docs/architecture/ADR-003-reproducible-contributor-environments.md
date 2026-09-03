# ADR-003: Reproducible Contributor Environments

- **Status:** Accepted
- **Date:** 2026-09-03

## Context

BardBox is developed across multiple repositories by maintainers, students, outside contributors, and AI-assisted development tools. Local machines can differ in Python versions, package versions, PlatformIO toolchains, linters, test dependencies, and other development software.

Without a standard environment, a change may work on one contributor's machine but fail for another contributor, in CI, or when an AI agent attempts to reproduce the work. Onboarding also becomes unnecessarily difficult because every contributor must reconstruct the expected toolchain manually.

BardBox needs contributor environments that are easy to reproduce, inspect, and verify while still supporting hardware-facing development where containers are not practical.

## Decision

BardBox will standardize contributor development primarily through **Dev Containers / Docker**, pinned dependencies, and matching CI checks.

The platform goal is:

> Every BardBox contributor should be able to enter a standardized, reproducible development environment with one command or equivalent simple action.

Conceptually:

```text
Contributor / student / AI agent
             ↓
        Dev Container
             ↓
 standard BardBox toolchain
             ↓
 tests + bardbox doctor/audit
             ↓
        GitHub Actions
             ↓
      same checks again
```

## Standard environment

A BardBox development environment should converge on a common baseline containing the tooling required by the applicable project, such as:

```text
Python
pytest
ruff
mypy
bardbox-tools
PlatformIO
Git
common build tooling
```

Not every repository must install every possible BardBox dependency. Projects may extend the common baseline with their own declared requirements.

Dependency versions should be pinned or locked where practical so that "same environment" means more than merely using Docker.

## CI alignment

The local standardized environment and GitHub Actions should run substantially the same deterministic validation commands. A contributor should not discover an entirely different set of requirements only after opening a pull request.

Where practical, shared scripts or `bardbox-tools` commands should define the checks used by both local development and CI.

## `bardbox doctor`

BardBox Tools should provide a diagnostic command for verifying contributor environments, especially when a contributor is working outside the standard container.

A future result may resemble:

```text
Python              ✓
Git                 ✓
bardbox-tools       ✓
Docker              ✓
PlatformIO          ✓
repo manifest       ✓
protocol version    ✓
GitHub remote       ✓
```

`bardbox doctor` should report actionable failures rather than silently changing the contributor's machine.

This command is also an important interface for AI-guided onboarding: an AI can ask the contributor to run `bardbox doctor`, inspect deterministic results, and resolve setup problems one at a time.

## Hardware-facing development

Containers are a contributor-consistency mechanism, not a requirement that every BardBox runtime execute inside Docker.

Direct hardware work involving GPIO, USB, serial devices, Digilent hardware, network interfaces, or other host-specific resources may remain native when containerization adds significant complexity without a clear benefit.

Projects should separate, where practical:

- portable development/test logic that can run in the standard environment; and
- hardware-in-the-loop or deployment checks that require the actual host/device.

A contributor working natively should still be able to verify compatibility through pinned dependencies, `bardbox doctor`, and the same project tests/audits where applicable.

## Contributor onboarding

The reproducible environment is part of the BardBox contributor experience, not merely CI infrastructure.

Human-readable contributor documentation and future BardBox Contributor Agent instructions should guide a new contributor through:

1. cloning/accessing the assigned repository;
2. entering the standard environment;
3. running `bardbox doctor`;
4. resolving setup failures one at a time;
5. running baseline tests/audits;
6. creating or using the appropriate contributor branch;
7. beginning development only after the environment is known-good.

The AI or onboarding guide should rely on repository-controlled instructions and deterministic checks rather than memorized setup steps.

## Rollout strategy

Do not wait until every BardBox repository can be containerized perfectly.

Prototype a Dev Container/reproducible environment early alongside the first `bardbox-tools`, `bardbox doctor`, and project-manifest work. Use that prototype to learn what belongs in the common baseline.

After the tooling and project model stabilize, roll the environment pattern across BardBox repositories and align GitHub Actions with it.

## Consequences

### Positive

- Contributors and AI agents work against a known toolchain.
- Student onboarding becomes substantially easier.
- Local validation more closely predicts CI behavior.
- Dependency/version incompatibilities become easier to diagnose.
- Development setup becomes documentation-as-code rather than institutional memory.
- Contributor machines do not need to be manually configured identically.

### Costs and constraints

- Dev Container/Docker definitions require maintenance.
- Some hardware access remains host-specific and cannot be fully reproduced in CI.
- Container images can become unnecessarily large if the common baseline is not kept focused.
- Pinning dependencies requires deliberate update work.
- macOS/Linux/device differences still need explicit handling where they matter.

## Alternatives considered

### Document manual setup only

Rejected because written instructions do not guarantee contributors actually have equivalent dependency/toolchain versions and are difficult for students and AI agents to verify.

### Require Docker for every BardBox runtime and hardware operation

Rejected because containerizing direct GPIO/USB/serial/instrument access can add complexity without improving the deployed system.

### Depend only on GitHub Actions

Rejected because CI catches problems after work has already been performed. Contributors need the ability to reproduce the expected environment and checks locally.

## Follow-up

Prototype the first BardBox Dev Container early during the project-manifest and `bardbox doctor` phase. Later standardize the pattern across project repositories, contributor onboarding, the project template, and CI.
