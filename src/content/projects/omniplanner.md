---
title: "OmniPlanner"
slug: "omniplanner"
featured: false
order: 2
subtitle: "Desktop-first planning workspace for goals, weeks, habits, calendar blocks, and AI-assisted organization."
status: "Active App"
summary: "An Electron desktop app for personal planning workflows, built around local data, weekly structure, goals, habits, and optional AI assistance."
repo: "https://github.com/RhyGPU/OmniPlanner"
stack:
  - Electron
  - Vite
  - React
  - TypeScript
  - JavaScript
  - Local app data
highlights:
  - Built a desktop-first productivity app rather than a web-only planner.
  - Designed around local-first app data.
  - Created a simple Windows launch path with dependency install, build, and launch flow.
  - Structured planning around goals, weeks, habits, calendar blocks, and email instead of one generic task list.
  - Framed AI as optional assistance inside a planning system, not the entire product.
media:
  - title: Weekly planning view
    type: placeholder
    caption: Planned screenshot slot for the weekly planning surface.
    status: planned
  - title: Goals view
    type: placeholder
    caption: Planned screenshot slot for goal organization and review.
    status: planned
  - title: Habits view
    type: placeholder
    caption: Planned screenshot slot for recurring habit tracking.
    status: planned
  - title: Calendar blocks
    type: placeholder
    caption: Planned screenshot slot for time-block planning.
    status: planned
  - title: AI assistance panel
    type: placeholder
    caption: Planned screenshot slot for optional AI assistance inside the planning workspace.
    status: planned
proofNotes:
  - Desktop-first app rather than a web-only planner.
  - App data is stored locally on the device.
  - Windows launcher flow exists through run.bat and create-shortcut.bat.
showHighlightsPanel: false
tags:
  - planning
  - productivity
  - local-first
  - desktop
---

## Problem

Personal planning breaks down when the system is split across too many surfaces.

Goals live in one place. Weekly planning lives somewhere else. Habits become a separate tracker. Calendar blocks sit in a calendar app. Email keeps pulling attention back into the inbox. The result is not a planning workflow. It is a collection of disconnected reminders.

Generic productivity apps can fail from the other direction. They become heavy enough to avoid, or abstract enough that they stop helping with daily execution. A task list is not the same as a week. A week is not the same as a goal system. A calendar block is not the same as a habit.

AI assistance is only useful if it attaches to structure. A floating chatbot can suggest plans, but it does not become the place where the user's week, goals, habits, calendar, and email workflow actually live.

## Solution

OmniPlanner is a desktop-first local planning workspace.

The app is aimed at the practical overlap between weekly structure, goals, habits, calendar blocks, email, and optional AI support. It treats planning as a working surface instead of a passive database.

The product direction is close to an "executive life OS" style app, but grounded in local workflows: open the desktop app, see the planning system, adjust the week, and use AI as assistance inside that structure rather than as the entire product.

## Core Systems

<div class="case-grid">
  <article>
    <h3>Weekly Planning</h3>
    <p>The central planning surface: organize the week as a concrete operating unit instead of a loose pile of tasks.</p>
  </article>
  <article>
    <h3>Goals</h3>
    <p>Goal structure gives the week direction and keeps planning tied to longer-running intent.</p>
  </article>
  <article>
    <h3>Calendar Blocks</h3>
    <p>Time blocks connect plans to execution windows, making the schedule part of the planning workflow.</p>
  </article>
  <article>
    <h3>Habits</h3>
    <p>Habit tracking keeps recurring behavior visible beside goals and weekly execution.</p>
  </article>
  <article>
    <h3>Email Workflow</h3>
    <p>Email is treated as part of the organization surface instead of a separate attention trap.</p>
  </article>
  <article>
    <h3>Optional AI Assistance</h3>
    <p>AI support belongs inside the planning system, helping organize and reason over structure without replacing user ownership.</p>
  </article>
  <article>
    <h3>Local Data / Desktop Launcher</h3>
    <p>App data is stored locally on the device, and the project is built as a desktop app rather than a browser-only planner.</p>
  </article>
  <article>
    <h3>Windows Launch + Shortcut Flow</h3>
    <p><code>run.bat</code> provides the launch path, while <code>create-shortcut.bat</code> creates a desktop shortcut. The launcher installs dependencies on first run, builds if needed, then opens Electron.</p>
  </article>
</div>

## Technical Highlights

- Built a desktop-first productivity app rather than a web-only planner.
- Used Electron with a Vite/React/TypeScript app structure.
- Designed around local-first app data.
- Created a simple Windows launch path with dependency install, build, and app launch behavior.
- Added shortcut creation so the app can be re-entered like a normal desktop workspace.
- Structured planning around goals, weeks, habits, calendar blocks, and email instead of one generic task list.
- Framed AI as optional assistance inside a planning system, not the entire product.

## Current Status

OmniPlanner is a working desktop app and active secondary project.

The Windows launch flow exists: the top-level scripts route into the app folder, `run.bat` launches the app, and `create-shortcut.bat` creates a desktop shortcut. The app stores data locally on the device. The project also has developer commands for install, build, launch, Vite dev server, and Electron start flows.

This is not being presented as a polished public release. Public polish, packaging, and deeper documentation are still ongoing work unless the repo proves otherwise.

## What This Demonstrates

<div class="proof-list">
  <span>Desktop app development</span>
  <span>Product design for personal workflows</span>
  <span>Local-first data thinking</span>
  <span>Practical launcher/setup design</span>
  <span>AI-assisted productivity design</span>
  <span>UX structure for planning systems</span>
</div>
