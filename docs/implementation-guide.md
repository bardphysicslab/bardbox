# Bard Box Implementation Guide

## Purpose

This document explains the core architecture of Bard Box and how the pieces fit together.

For writing code, use the specific instruction documents:

* `device-instructions.md` — Arduino/ESP32 sensor nodes
* `pi-driver-instructions.md` — Raspberry Pi drivers
* `channel-names.md` — normalized channel reference

---

## Core Architecture

A Bard Box deployment has two essential parts:

### 1. Sensors / Devices

Sensors collect data. These may be:

* directly connected to the Raspberry Pi (I2C, SPI, USB, serial)
* connected via a microcontroller (Arduino, ESP32, etc.) when distance or isolation requires it

The connection method is implementation-specific and does not affect the system interface.

### 2. Raspberry Pi

The Pi is the hub. It:

* reads from sensors via drivers
* normalizes data
* serves an API
* powers dashboards or displays

All sensor communication goes through a standardized driver interface.
The rest of the system must not depend on hardware details.

---

## Core Rule

The Raspberry Pi is the normalization layer.

Devices and sensors may vary, but all data must be normalized before entering the system.

---

## Design Principles

1. **Interface-first** — define the contract before implementation
2. **Separation of concerns** — devices acquire data, Pi normalizes and serves it
3. **Data is the interface** — protocol output defines system behavior
4. **Protocol versioning** — validate versions and reject mismatches
5. **Hardware independence** — backend must not depend on sensors, wiring, or transport
6. **Reuse over rebuild** — extend existing code whenever possible
7. **Student-accessible** — understandable by a motivated undergraduate

---

## System Contract

Bard Box relies on three enforced interfaces:

* **Device → Pi:** Bard Box serial protocol (`HDR`, `DAT`, `INFO`)
* **Driver → Backend:** normalized driver interface (`get_info`, `get_capabilities`, `get_reading`)
* **Data model:** standardized channel names (`channel-names.md`)

Everything in the system depends on these contracts being strictly followed.

---

## Software Identity

Bard Box distinguishes between:

* **UID** → physical device identity (`bb-0001`)
* **App ID** → software/system identity (what the system does)

---

### App ID Format

```
bb-{app-name}
```

---

### What the App Name Represents

The app name should describe the **function of the system in terms of what it measures or provides**, not the specific hardware.

It should answer:

> “What information or capability does this system provide?”

Do NOT describe:

* specific sensors (`pms`, `bme`)
* wiring or transport
* internal implementation details

---

### Examples

Good:

* `bb-golab-air-quality`
* `bb-cleanroom-air-quality`
* `bb-gallery-environment`

Avoid:

* `bb-monitor` ❌ too vague
* `bb-pms-bme-arduino` ❌ hardware-focused
* `bb-particle-temp-sensor` ❌ component-focused

---

### Rules

* lowercase
* hyphen-separated
* human-readable
* stable across deployments
* describe **what is measured or delivered**, not how
* be specific enough to distinguish systems

---

### Instance ID (optional)

```
{app-id}-{host-or-location}
```

Examples:

* `bb-golab-air-quality-pi01`
* `bb-golab-air-quality-cleanroom`

Use instance IDs for logging, debugging, and multi-device deployments.

---

## What To Avoid

* Hardcoding sensor logic in the backend
* Device code performing logging, networking, or visualization
* Backend exposing hardware-specific fields
* Skipping protocol validation
* Inventing alternate normalized field names
* Letting raw sensor output bypass normalization

---

## Network Access

Bard Box deployments are internal systems and are not exposed to the public internet.

### Standard Access Model

* Raspberry Pi connected via ethernet to Bard network
* Static IP assigned by Bard IT
* Dashboard accessible on Bard network or via Bard VPN
* No public-facing ports

### Deployment Requirements

* Coordinate with Bard IT for static IP assignment
* Access via browser on Bard network or VPN
* No additional client software required

---

## Starting a New Project

1. Register a UID for each device — see `uid-registry.md`
2. Assign an App ID for the system
3. Write device firmware using `device-instructions.md`
4. Write a Pi driver using `pi-driver-instructions.md`
5. Reuse existing drivers where possible
6. Use `channel-names.md` for all field naming
7. Use an AI assistant with these documents as context to generate code

---

## Final Principle

If something breaks, it is almost always because one of the three contracts was violated:

* device protocol
* driver interface
* channel naming

Fix the contract — not the symptom.
