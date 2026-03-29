# Bard Box UID Registry

Every Bard Box device must have a unique identifier (UID).

---

## UID Format

```
bb-0001, bb-0002, bb-0003, ...
```

Rules:

* Prefix is always `bb-`
* Numeric portion is zero-padded to 4 digits
* Do not invent alternate formats

---

## Core Rules

* UIDs are globally unique across all Bard Box deployments
* Once assigned, a UID must never be reused
* UIDs must remain stable — do not change a UID after deployment
* Do not use project-local names as UIDs (e.g. `sensor_01`, `golab_pms`)

---

## Source of Truth

The authoritative UID registry is maintained in Google Sheets:

**[INSERT UID REGISTRY LINK HERE]**

Rules:

* Always check the registry before assigning a new UID
* Do not assign UIDs outside the registry
* Do not rely on local copies of this file for UID assignment

---

## Where the UID Lives

### Programmable Devices (Arduino, ESP32)

Store in firmware:

```cpp
#define DEVICE_UID "bb-0001"
```

* Physically label the device with the UID

---

### Non-Programmable Devices (instruments, external systems)

* Assign UID in the Raspberry Pi driver configuration
* Physically label the device with the UID if possible

---

## Assignment Process

1. Open the UID registry (Google Sheet)
2. Find the next available UID
3. Assign it to the device
4. Add the device entry to the registry
5. Commit and deploy

---

## Example Entries

| UID     | Description              | Project       | Status |
| ------- | ------------------------ | ------------- | ------ |
| bb-0001 | GT-521S particle counter | GoLab Monitor | Active |

---

## Status Definitions

* **Active** — currently deployed and in use
* **Retired** — no longer in use, UID remains reserved
* **Reserved** — assigned but not yet deployed

---

## Notes

* The Google Sheet is the single source of truth
* This document defines rules and workflow only
* Do not reuse retired UIDs
* Always assign UIDs before flashing or deploying devices
