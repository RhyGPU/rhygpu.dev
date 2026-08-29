---
title: "Between Dawns"
slug: "between-dawns"
featured: false
order: 3
subtitle: "Six-player survival strategy across the dangerous space between two sunrises."
status: "Playable Vertical Slice"
summary: "A Godot survival game combining direct top-down action, settlement command, and distant expedition simulation in one authoritative persistent world."
repo: "https://github.com/RhyGPU/between_dawns"
devlog: "/projects/between-dawns/devlog/"
devlogLabel: "Devlogs"
stack:
  - Godot 4.3
  - GDScript
  - ENet
  - Android
  - Windows
highlights:
  - Built direct control, RTS command, and distant text simulation on the same character and world state.
  - Designed a six-player authoritative network model with listen-server and headless dedicated-server paths.
  - Made territorial expansion expose new entrances and raise the cost of defending a settlement.
  - Connected finite procedural zones into a persistent deterministic world graph.
  - Turned distant expedition outcomes into immutable facts that can materialize as playable rescue scenes.
architecture:
  - Direct player input / RTS orders / expedition plans
  - Authoritative world and inventory state
  - Character / Zone / Settlement simulation
  - Physical or abstract resolution by observation distance
  - Persistent journal and checkpoints
  - Replicated client presentation
media:
  - title: Night defense vertical slice
    type: placeholder
    caption: Planned capture of the playable settlement defense loop from dusk through dawn.
    status: planned
  - title: Tactical zone map
    type: placeholder
    caption: Planned capture of connected zones, gateways, pressure, expeditions, and retreat routes.
    status: planned
  - title: Operations UI
    type: placeholder
    caption: Planned capture of shifts, work orders, squads, expeditions, and direct NPC control.
    status: planned
proofNotes:
  - The public repository contains the current Godot project, specifications, implementation status, and automated validation tools.
  - The current build is a vertical slice; real-device controller and broader multiplayer playtesting remain separate validation steps.
showHighlightsPanel: false
tags:
  - survival strategy
  - co-op
  - simulation
  - godot
  - procedural world
---

## Problem

Most co-op survival games split apart under one of two pressures. Either multiplayer is attached after the single-player systems already own the truth, or the settlement layer becomes a disconnected management screen whose people and resources do not behave like the world the player actually visits.

Between Dawns starts from the opposite direction. Multiplayer authority comes first, and every scale of play uses the same persistent state.

## Core Idea

> Survive one dawn, use the day to prepare, and hold the world together until the next.

The player directly explores finite top-down zones, scavenges the remains of civilization, and defends a growing settlement at night. The same survivors can receive RTS orders nearby or run distant expeditions through abstract simulation. If the player reaches an unresolved incident, it can become physical gameplay without erasing outcomes that already happened.

Expansion is useful and dangerous. Safe arable land supports more people, but every newly exposed gateway can become another route the infected use to reach the settlement.

## Shared Simulation

<div class="flow-diagram" aria-label="Between Dawns shared simulation architecture">
  <span>Direct control / RTS / expedition plan</span>
  <span>Authoritative Character + Zone + World state</span>
  <span>Physical or abstract simulation</span>
  <span>Immutable outcomes</span>
  <span>Persistence + replication</span>
  <span>Next decision</span>
</div>

Direct action, command, and text events are different resolutions of one simulation. Characters keep the same equipment, injuries, fatigue, mental state, experience, and relationships when they move between them.

## Current Playable Scope

- A dusk-to-dawn settlement defense loop with scavenging, fortification, shifts, and horde pressure.
- Deterministic finite zones connected as an expanding persistent graph.
- Physical combat, injuries, rescue, treatment, infection pressure, and permanent death.
- RTS field commands, work orders, squads, expeditions, radio distress, and NPC direct control.
- Persistent resources, equipment, vehicles, structures, world facts, journals, and checkpoints.
- A maximum-six-player ENet authority path with dedicated-server and remote-client presentation.
- Keyboard and mouse, Android touch, and Android/XInput gamepad input paths.

## Development Journal

<div class="journal-links">
  <a href="/devlog/between-000-the-game-i-was-looking-for-did-not-exist/"><strong>000</strong><span>Origin: the controller-game search that became a six-player survival strategy game.</span></a>
  <a href="/devlog/between-001-deleting-the-first-game/"><strong>001</strong><span>Implementation: deleting the browser prototype and rebuilding the project as a native Godot game.</span></a>
  <a href="/devlog/between-002-the-backend-was-not-the-game/"><strong>002</strong><span>Audit: 282 passing checks, disconnected systems, and the discovery that the backend was not the game.</span></a>
  <a href="/devlog/between-003-walking-9209-pixels-to-prove-the-exit/"><strong>003</strong><span>World rewrite: procedural districts, real gateway travel, daylight ecology, and a verified M1 starting line.</span></a>
</div>

## Current Status

Between Dawns is a playable vertical slice under active development. The project has automated validation and multiplayer smoke coverage, but that does not replace broader real-device controller, Android, and six-player playtesting.

The next work is not to invent another disconnected layer. It is to keep proving that the existing layers — action, command, expedition simulation, persistence, and networking — agree on the same world.

## What This Demonstrates

<div class="proof-list">
  <span>Multiplayer authority design</span>
  <span>Simulation architecture</span>
  <span>Godot game development</span>
  <span>Procedural world systems</span>
  <span>Strategy and action integration</span>
  <span>Scope control</span>
</div>
