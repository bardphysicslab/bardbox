# Bard Box Implementation Guide

## Purpose

This document explains the core architecture of Bard Box and how the pieces 
fit together.

For writing code, use the specific instruction documents:
- `device-instructions.md` — for Arduino/ESP32 sensor nodes
- `pi-driver-instructions.md` — for Raspberry Pi drivers
- `channel-names.md` — normalized channel name reference

---

## Core Architecture

A Bard Box deployment has two essential parts:

**1. Sensors / Devices**
One or more sensors collect data. These may be connected directly to the 
Raspberry Pi (via I2C, SPI, USB, or serial) or through an intermediate 
device (such as an Arduino or ESP32) when distance or isolation requires it.
The right connection method depends on the specific situation.

**2. Raspberry Pi**
The Pi is the hub. It reads from sensors, stores data, serves a web API, 
and powers the dashboard or display. All sensor communication goes through 
a standardized driver interface — so the rest of the system doesn't care 
how a sensor is physically connected.

The key standard is **how the Pi talks to sensors** — defined in the driver 
and device instruction documents. Everything else follows from that.

---

## Design Principles

1. **Interface-first** — define the contract before the implementation
2. **Strict separation of concerns** — devices collect data, Pi normalizes and serves it
3. **Data is the interface** — the serial output format is the most critical standard
4. **Protocol versioning** — always validate version, reject mismatches
5. **Hardware independence** — backend must never depend on specific sensors, 
   wiring, or transport
6. **Reuse over rebuild** — every new project starts from existing code
7. **Student-accessible** — the whole stack should be understandable by a 
   motivated undergraduate

---

## What To Avoid

- Hardcoded sensor logic in the backend
- Device code that does logging, networking, or visualization
- Backend endpoints that expose hardware-specific fields
- Skipping protocol version validation
- Merging untested code to `main`
- Inventing alternate normalized field names

---

## Network Access

Bard Box deployments are intended for internal use and are not exposed to the 
public internet.

**Standard access model:**
- Raspberry Pi connected to Bard network via ethernet
- Static IP assigned in coordination with Bard IT
- Dashboard accessible on Bard internal network or via Bard VPN
- No public-facing ports

**What this means for new deployments:**
- Coordinate with Bard IT to get a static IP assigned to the Pi
- Users access the dashboard via browser on the Bard network or Bard VPN
- No special software required beyond the Bard VPN client

---

## Starting a New Project

1. Register a UID for each new device — see `uid-registry.md`
2. Write device firmware using `device-instructions.md`
3. Write a Pi driver using `pi-driver-instructions.md`
4. Use existing drivers from current deployments as a starting point
5. Use `channel-names.md` to ensure consistent field naming
6. Use an AI assistant (Claude, ChatGPT) with the relevant documents as context
   to generate project-specific code
