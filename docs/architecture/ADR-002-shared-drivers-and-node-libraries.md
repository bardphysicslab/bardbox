# ADR-002: Shared Drivers and Node Libraries

- **Status:** Accepted
- **Date:** 2026-09-03

## Context

BardBox projects increasingly use the same sensors, instruments, transports, and protocol behavior across multiple deployments. Examples include Plantower particulate sensors, BME environmental sensors, MAX31865 RTD interfaces, SPN1 instruments, programmable loads, serial/network transports, Web Node buffering, and common configuration/runtime behavior.

Historically, reusable code can easily be copied into individual project repositories. That is convenient initially but creates multiple implementations of what should be the same BardBox behavior. Fixes and protocol changes then need to be repeated across repositories, and deployed systems can silently diverge.

BardBox needs project-specific applications without project-specific copies of common drivers and node behavior.

## Decision

Reusable BardBox hardware drivers, protocol implementations, transport behavior, buffering logic, and other genuinely shared runtime components will move toward **canonical, versioned shared libraries**.

Project repositories should consume those libraries as explicit dependencies rather than copying their source code.

Conceptually:

```text
BardBox shared libraries
  ├── PMS5003 / PMS6003
  ├── BME280 / BME688
  ├── MAX31865
  ├── SPN1
  ├── ET54 / programmable-load support
  ├── transport helpers
  ├── Web Node protocol/buffering
  └── common config/runtime helpers
            ↓ versioned dependencies
  ┌─────────┼─────────┬─────────┐
solar     rkc       cesh      labcheck
```

The exact package/repository boundaries will be determined as implementations are extracted. This ADR establishes the ownership model, not a requirement that every component live in one monolithic package.

## Language and platform strategy

### Python / Raspberry Pi

Reusable Python drivers and runtime helpers should be proper importable packages with explicit versions and tests. Project applications own configuration and orchestration; shared packages own reusable device/protocol behavior.

### ESP32 / firmware

Reusable firmware behavior should be provided through versioned PlatformIO-compatible libraries or versioned Git/package dependencies. Shared Web Node transport, buffering, retry, acknowledgment, and protocol behavior should not be manually copied between firmware projects.

Hardware-specific application code may remain in the project when it is genuinely specific to that device or deployment.

## Dependency declaration

Each project should eventually declare the approved versions of shared BardBox dependencies through its project manifest and normal dependency/lock mechanisms.

`bardbox audit` should be able to compare:

```text
project-approved version
        ↕
repository dependency version
        ↕
deployed runtime version
```

A newer library existing upstream does not by itself make a deployment noncompliant. The important condition is whether the project is running the version approved/declared for that project.

## Source of truth

For each shared component there must be one canonical implementation location. The BardBox specification defines the required behavior; the shared library implements reusable behavior; project repositories configure and consume it.

The `bardbox-project-template` demonstrates how projects consume shared components. It must not contain a second canonical copy of shared driver or protocol implementations.

## Changes to shared behavior

A change to a shared library must be treated as potentially affecting multiple projects.

The expected workflow is:

1. Determine whether the change is an implementation fix or a BardBox-wide behavior/protocol change.
2. If BardBox-wide behavior changes, update the authoritative specification and record an ADR when appropriate.
3. Update the shared implementation and its tests.
4. Release/version the shared component.
5. Identify dependent BardBox projects.
6. Update projects deliberately through reviewed dependency changes rather than silently replacing deployed code.

Production systems should not automatically upgrade simply because a newer shared library exists.

## Consequences

### Positive

- Bug fixes can be made once and propagated deliberately.
- BardBox projects share consistent hardware and protocol behavior.
- Dependency versions become inspectable and auditable.
- Contributor and AI changes can target the canonical implementation rather than guessing which copy to modify.
- Protocol compliance and project health checks become practical across repositories.
- New projects can reuse proven components instead of starting with copied code.

### Costs and constraints

- Existing duplicated implementations will require gradual extraction and migration.
- Shared packages require versioning, tests, release discipline, and backwards-compatibility decisions.
- A shared-library change can have a larger blast radius, so CI and review become more important.
- Some hardware integrations are legitimately project-specific and should not be prematurely generalized.

## Alternatives considered

### Continue copying known-good drivers into new projects

Rejected because fixes and protocol changes diverge over time and there is no reliable canonical implementation.

### Put all drivers directly in the `bardbox` specification repository

Rejected as a blanket rule. The specification repository defines standards and may contain reference material, but reusable runtime implementations need appropriate package/version/release boundaries. Exact repository organization can evolve.

### Automatically keep every project on the newest shared library

Rejected because production hardware should run an explicitly approved dependency set. Newest is not equivalent to validated.

## Follow-up

Do not begin by extracting every existing driver at once. First establish `bardbox-tools`, project manifests, auditing, and dependency visibility. Then identify duplicated/high-value components and migrate them incrementally, with Web Node shared behavior and commonly reused hardware drivers as strong candidates.
