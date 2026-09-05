# BardBox Architecture Principles

This is a living design document for BardBox developers and contributors. It records the reasoning principles we want to use while evolving the platform. These are design heuristics, not necessarily requirements for every existing project yet. Mature principles can later be promoted into formal BardBox standards.

## 1. Put knowledge in the right place

Good architecture is largely about deciding which component should know what.

For every component, ask both:

- What is the minimum this component needs to know to do its job?
- What should this component explicitly *not* know?

Keeping unnecessary knowledge out of a component reduces coupling and makes failures, testing, replacement, and maintenance easier to reason about.

## 2. Give components clear, narrow responsibilities

Sampling, communication, storage, alarm policy, notification delivery, UI rendering, and other concerns should not become one tangled responsibility.

Example: a sensor sampler should collect readings and make them available. It should not need to know whether Wi-Fi is connected, whether the server is healthy, or whether an SMS provider is available.

A communication component can independently decide whether a reading can be sent upstream or must be buffered. Thus sampling can continue even while communications are degraded.

This principle applies at several scales: functions, modules, drivers, services, and state machines.

## 3. Prefer independent state machines for independent concerns

Do not force unrelated concerns into one large state machine simply because they occur in the same product.

Example: sampling state and communications state can evolve independently. Loss of Wi-Fi should not imply that sampling has stopped.

Also distinguish **state** from **context/input**. For example, in a freezer alarm system, door-open status may be useful context explaining a temperature excursion without necessarily being an alarm state itself.

A simple temperature alarm model might be:

1. Normal — temperature is within bounds.
2. Pre-alarm — temperature is outside bounds and the grace timer is running.
3. Alarm — temperature has remained outside bounds longer than the configured interval.

Door state can accompany those states as context rather than unnecessarily multiplying the number of states.

## 4. Interfaces are contracts

Components should communicate through explicit, predictable interfaces. An interface states what a component promises to accept or provide without requiring its consumer to understand its internal implementation.

APIs and BardBox driver boundaries are examples of this principle.

External services should sit behind BardBox-owned interfaces where practical. For example, alarm policy should not be written in terms of Twilio. BardBox can define a notification/SMS interface and implement Twilio as one provider. Replacing Twilio should then require changing the provider implementation rather than the alarm system.

## 5. External providers execute; BardBox owns policy

Sensor nodes report facts. BardBox application logic interprets those facts and decides what actions are required. External providers execute narrowly defined actions.

For example:

- node: reports temperature and door state;
- application/alarm logic: determines whether an alarm condition exists and what notifications are required;
- notification provider: delivers an SMS or email.

An outage of one external provider should not unnecessarily stop data collection, storage, dashboards, backups, or unrelated notification channels. The system should expose a degraded condition rather than collapse as a whole.

## 6. Safety-critical behavior must not depend on the UI

The web UI should generally be a view/control surface, not the owner of operational safety.

For example, a LabCheck test runner should own the test sequence and safe-state behavior. A browser crash must not leave a power supply, load, or other instrument indefinitely in a potentially unsafe test condition.

Whether a test continues or aborts after UI loss is a test-policy decision, but either behavior must be implemented safely by the runner rather than accidentally determined by the browser's survival.

## 7. `main` should assemble and start, not become the brain

The program entry point should be intentionally boring. Its primary job is composition: load configuration, instantiate/select components, wire dependencies together, and start the application/runtime.

It should not accumulate device-specific logic, alarm policy, UI layout, or other business rules.

A useful warning sign is a `main` file filled with application-specific conditional logic.

The application layer may coordinate components, but `main` should normally call into that layer rather than *be* that layer.

## 8. Ask: can this be described instead of programmed?

If a difference between deployments can be expressed as data, strongly consider configuration rather than application-specific code.

Examples include device identity, sensor inventory, labels, locations, thresholds, ranges, and other deployment-specific choices.

This is a heuristic, not a rule that all behavior belongs in configuration. Configuration should describe the system; code should implement behavior and enforce contracts.

## 9. Shared UI belongs to BardBox; applications provide content

BardBox should move toward a shared UI/design system rather than each application independently recreating its dashboard.

Shared platform concerns can include:

- Bard branding and common header structure;
- typography and spacing;
- standard card sizing/layout rules;
- common identity, health, and hardware sections;
- common status/alarm presentation;
- reusable graph and card components.

Individual applications such as RKC or CESH should primarily provide their unique configuration, capabilities, data, and application-specific content.

Where practical, configuration should describe the monitored system and the shared UI framework should render standard structures from that description. A change to a shared BardBox component should then propagate consistently rather than require edits in every application.

## 10. Design for replacement and partial failure

A healthy architecture assumes components will change and fail.

Ask during design:

- If this provider disappears next year, what must change?
- If this component crashes, what should continue working?
- Can one subsystem enter a degraded state without taking unrelated subsystems down?
- Does the component responsible for an operation also own its cleanup/safe-state behavior?

The goal is not zero failure. The goal is understandable, bounded failure and straightforward replacement.

## 11. Promote proven ideas into standards deliberately

This document captures how we reason while developing BardBox. It is distinct from formal project requirements.

When a principle becomes sufficiently mature and specific, translate it into the appropriate BardBox standard, protocol, template requirement, tooling check, or implementation guide. This keeps exploratory architectural thinking separate from rules that every BardBox project is required to follow.
