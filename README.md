# Bard Box

Bard Box is a modular platform developed at Bard College that makes it easy
for faculty, staff, and students to deploy sensor monitoring and display systems
across campus — without requiring specialized engineering expertise.

---

## The Problem

Departments at Bard have real needs for:

* environmental monitoring
* sustainability reporting
* research data collection
* public-facing data displays

Current options are:

* Expensive vendor systems with proprietary cloud subscriptions
* Complex open-source platforms that require significant technical expertise
* One-off solutions that cannot be reused across projects

---

## The Solution

Bard Box packages proven, affordable open-source hardware and software into a
standardized system that any department can adopt.

Each deployment follows:

* the same architecture
* the same communication standards
* the same visual design language

This allows knowledge and code from one project to carry directly into the next.

---

## How It Works

A typical Bard Box deployment has three parts:

### 1. Sensor Node

A microcontroller (ESP32 or Arduino) connected to one or more sensors.
It collects data and streams it in a standard format using affordable,
well-documented components.

### 2. Gateway (Raspberry Pi)

A Raspberry Pi receives data from sensor nodes, stores it, and serves it via
a web API.

It uses Bard Box drivers (one per sensor type). Adding a new sensor means
adding or adapting a driver — not rewriting the system.

### 3. Dashboard or Display

A web-based dashboard presents the data in Bard’s visual style.

The same backend can power:

* a technical lab dashboard
* a public sustainability display
* a research data export

---

## Who Can Deploy It

You do not need to be an engineer.

A typical project requires:

* someone who understands the need (faculty, staff, or student)
* basic familiarity with Raspberry Pi and Arduino (or access to someone who has it)
* this documentation
* an AI assistant (Claude, ChatGPT) for project-specific code

The documentation and existing drivers provide enough structure for an AI
assistant to generate most of the implementation.

---

## What This Repo Contains

This repository defines the standards all Bard Box deployments follow:

* **Device protocol** — how sensor nodes communicate with the Pi
* **Driver interface** — how data is normalized on the Pi
* **Channel naming standard** — how measurements are represented
* **System architecture** — how components fit together

---

## Current Deployments

| Project       | Department | Description                     | Status |
| ------------- | ---------- | ------------------------------- | ------ |
| GoLab Monitor | Physics    | Air quality monitoring in GoLab | Active |

---

## Design Philosophy

* **Reuse over rebuild** — every project builds on existing work
* **Standards over flexibility** — consistency enables scale
* **Open hardware** — no vendor lock-in, no required cloud services
* **Student-accessible** — understandable by a motivated undergraduate
* **Practical simplicity** — minimal complexity required to deploy

---

## Maintained By

Bard College Physics Department
