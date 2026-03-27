\# Bard Box

Bard Box is a modular platform developed at Bard College that makes it easy   
for faculty, staff, and students to deploy sensor monitoring and display systems   
across campus — without requiring specialized engineering expertise.

\#\# The Problem

Departments at Bard have real needs for environmental monitoring, sustainability   
reporting, research data collection, and public-facing data displays. The current   
options are:

\- Expensive vendor systems with proprietary cloud subscriptions  
\- Complex open-source platforms that require significant technical expertise  
\- One-off solutions that can't be reused across projects

\#\# The Solution

Bard Box packages proven, affordable open-source hardware and software into a   
standardized system that any department can adopt. Each deployment follows the   
same architecture, the same communication standards, and the same visual design   
language — so knowledge and code from one project carries directly into the next.

\#\# How It Works

A typical Bard Box deployment has three parts:

\*\*1. Sensor Node\*\*  
A small microcontroller (ESP32 or Arduino) connected to one or more sensors.   
It collects data and streams it in a standard format. Uses affordable,   
well-documented components from suppliers like Adafruit and SparkFun.

\*\*2. Gateway (Raspberry Pi)\*\*  
A Raspberry Pi receives data from sensor nodes, stores it, and serves it via   
a web API. Uses existing Bard Box drivers — one per sensor type. Adding a new   
sensor means adding or adapting a driver, not rewriting the system.

\*\*3. Dashboard or Display\*\*  
A web-based dashboard presents the data in Bard's visual style. The same   
backend can power a technical lab dashboard, a public sustainability display,   
or a data export for research — depending on the application.

\#\# Who Can Deploy It

You don't need to be an engineer. A typical new project requires:

\- Someone who understands the need (faculty, staff, student)  
\- Basic familiarity with Raspberry Pi and Arduino (or a student who has it)  
\- This documentation  
\- An AI assistant (Claude, ChatGPT) to help write project-specific code

The READMEs in this repo, combined with the existing drivers from deployed   
projects, provide enough context for an AI assistant to generate most of the   
project-specific code correctly. A Bard Box-experienced person is available   
for guidance but does not need to build each project from scratch.

\#\# What This Repo Contains

This repository defines the standards that all Bard Box deployments follow:

\- \*\*Hardware protocol\*\* — how sensor nodes communicate with the Pi  
\- \*\*Sensor driver interface\*\* — how drivers are structured on the Pi  
\- \*\*Dashboard standards\*\* — how data is presented visually  
\- \*\*Display and signage standards\*\* — for public-facing installations  
\- \*\*Energy and sustainability standards\*\* — for deployments that report   
  environmental impact

\#\# Current Deployments

| Project | Department | Description | Status |  
|---------|-----------|-------------|--------|  
| GoLab Monitor | Physics | Air quality monitoring in the Go Lab | Active |

\#\# Design Philosophy

\- \*\*Reuse over rebuild\*\* — every new project starts from existing code  
\- \*\*Standards over flexibility\*\* — consistency makes maintenance easier  
\- \*\*Open hardware\*\* — no vendor lock-in, no cloud subscriptions required  
\- \*\*Student-accessible\*\* — the whole stack should be understandable by a   
  motivated undergraduate  
\- \*\*Honest about complexity\*\* — some technical help is needed, but it should   
  be the exception not the rule

\#\# Maintained By

Bard College Physics Department  
