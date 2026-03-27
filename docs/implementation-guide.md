# Bard Box Implementation Guide

This guide walks through deploying a new Bard Box project from scratch.

## Overview

A Bard Box deployment has three parts:

1. **Device node** — a microcontroller (ESP32 or Arduino) collecting sensor data
2. **Pi gateway** — a Raspberry Pi running drivers and a FastAPI app
3. **Dashboard** — a web UI served by the Pi

Each part follows the standards in this repo so that knowledge and code from one project carries into the next.

---

## Step 1 — Assign a UID

Every device gets a unique Bard Box UID in the format `bb-XXXX` (e.g. `bb-0001`).

Register the UID in [`uid-registry.md`](uid-registry.md) before writing firmware.

---

## Step 2 — Set up the device node

See [`device-instructions.md`](device-instructions.md).

- Choose sensors and microcontroller
- Wire sensors and verify readings
- Flash firmware that streams CSV over serial using the standard format
- Assign channel names per [`channel-names.md`](channel-names.md)

---

## Step 3 — Set up the Pi driver

See [`pi-driver-instructions.md`](pi-driver-instructions.md).

- Install the relevant driver from `drivers/`
- Configure serial port, baud rate, and channel mapping
- Verify the driver parses incoming data correctly
- Integrate with the FastAPI app

---

## Step 4 — Build the dashboard

- Use the existing GoLab Monitor (`golab-monitor` repo) as a reference
- Serve a FastAPI app from the Pi
- Follow Bard visual style (see `docs/` for display standards — coming soon)

---

## Step 5 — Deploy as a service

```bash
sudo systemctl enable <service-name>
sudo systemctl start <service-name>
journalctl -u <service-name> -f
```

---

## Reference

| Doc | Purpose |
|---|---|
| [`channel-names.md`](channel-names.md) | Standard channel name conventions |
| [`uid-registry.md`](uid-registry.md) | Registry of all deployed device UIDs |
| [`network-access.md`](network-access.md) | How to reach deployed Pi gateways |
| [`device-instructions.md`](device-instructions.md) | Device node setup |
| [`pi-driver-instructions.md`](pi-driver-instructions.md) | Pi driver setup |
