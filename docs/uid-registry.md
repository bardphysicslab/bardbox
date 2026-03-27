# Bard Box UID Registry

Every Bard Box device must have a unique identifier (UID).

---

## UID Format
```
bb-0001, bb-0002, bb-0003, ...
```

---

## Rules

- UIDs are globally unique across all Bard Box deployments
- Once assigned, a UID must never be reused
- UIDs must remain stable — do not change a UID after deployment
- Do not use project-local names as UIDs (e.g. `sensor_01`, `golab_pms`)

---

## Where the UID Lives

**Programmable devices (Arduino, ESP32):**
- Store in firmware as `#define DEVICE_UID "bb-0001"`
- Physically label the device with the UID

**Non-programmable devices (instruments, external systems):**
- Assign in Pi driver configuration
- Physically label the device with the UID if possible

---

## How to Assign a UID

1. Check the registry below for the next available UID
2. Add your device with a description
3. Commit the update to this file

---

## Registry

| UID | Description | Project | Status |
|-----|-------------|---------|--------|
| bb-0001 | GT-521S particle counter | GoLab Monitor | Active |
