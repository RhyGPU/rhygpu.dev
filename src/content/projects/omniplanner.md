---
title: "OmniPlanner"
slug: "omniplanner"
featured: false
order: 2
subtitle: "Desktop-first planning workspace for goals, weeks, habits, calendar blocks, and AI-assisted organization."
status: "Active App"
summary: "An Electron desktop app for personal planning workflows, built around local data, weekly structure, goals, habits, and optional AI assistance."
icon:
  src: /projects/omniplanner/app-icon.png
  alt: OmniPlanner app icon.
ogImage: /projects/omniplanner/dashboard-overview.png
repo: "https://github.com/RhyGPU/OmniPlanner"
devlog: "/projects/omniplanner/devlog/"
devlogLabel: "Devlogs"
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
  - title: Dashboard overview
    type: screenshot
    src: /projects/omniplanner/dashboard-overview.png
    alt: OmniPlanner dashboard showing upcoming events, habits, quick todos, recent email state, and local sync status.
    caption: Daily execution surface combining events, habits, todos, email status, and local-only state in one desktop workspace.
    status: available
  - title: Pulse reminders
    type: screenshot
    src: /projects/omniplanner/pulse-reminders.png
    alt: OmniPlanner Pulse view showing daily reminders, event alarms, sleep alarm rules, and reminder toggles.
    caption: Reminder and nudge layer for morning planning, habit check-ins, focus alerts, and sleep-related routines.
    status: available
  - title: Priority inbox
    type: screenshot
    src: /projects/omniplanner/priority-inbox.png
    alt: OmniPlanner Priority Inbox showing an email-style planning message and disabled calendar action until provider setup.
    caption: Inbox workflow for planning-relevant messages, with calendar actions gated by provider configuration instead of fake availability.
    status: available
  - title: Month view
    type: screenshot
    src: /projects/omniplanner/month-view.png
    alt: OmniPlanner monthly calendar view for July 2026 with tasks distributed across days.
    caption: Month-level planning view for scanning scheduled work and task distribution across the calendar.
    status: available
  - title: Deep planner week
    type: screenshot
    src: /projects/omniplanner/deep-planner-week.png
    alt: OmniPlanner Deep Planner weekly view with business goals, well-being goals, focus goals, habits, time blocks, and week review.
    caption: Weekly operating surface combining goals, focus, habits, todos, calendar blocks, and plan-versus-actual review.
    status: available
  - title: Life Vision board
    type: screenshot
    src: /projects/omniplanner/life-vision-board.png
    alt: OmniPlanner Life Vision Board showing monthly focus cards and a selected July goal.
    caption: Longer-horizon planning surface for annual or monthly focus areas beyond the immediate week.
    status: available
  - title: Settings and local data
    type: screenshot
    src: /projects/omniplanner/settings-data.png
    alt: OmniPlanner Settings and Data page showing AI provider selection, email accounts, local notifications, backup export, restore, calendar import, and zero-knowledge storage.
    caption: Local-first infrastructure view for provider setup, email connection, notifications, backup, restore, calendar import, and local storage messaging.
    status: available
proofNotes:
  - Desktop-first app rather than a web-only planner.
  - App data is stored locally on the device.
  - Windows launcher flow exists through run.bat and create-shortcut.bat.
  - Real screenshots show the current dashboard, inbox, calendar, deep planning, reminders, vision, and settings/data surfaces.
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

## Development Journal

<div class="journal-links">
  <a href="/devlog/omni-000-before-omniplanner-had-a-repository/"><strong>000</strong><span>Origin: the pre-repository planner, its first code audit, and the bugs that defined the data model.</span></a>
  <a href="/devlog/omni-001-the-web-planner-became-a-desktop-app/"><strong>001</strong><span>Foundation: the first repository, local Electron shell, provider-neutral AI, and reproducible desktop builds.</span></a>
  <a href="/devlog/omni-002-the-last-week-of-february-disappeared/"><strong>002</strong><span>Calendar truth: restoring the missing final week and making monthly and weekly views edit the same data.</span></a>
  <a href="/devlog/omni-003-the-app-was-still-a-folder/"><strong>003</strong><span>Re-entry: double-click launchers, first-run setup, and a desktop shortcut for the working checkout.</span></a>
  <a href="/devlog/omni-004-five-checkmarks-two-flames/"><strong>004</strong><span>Adaptability: truthful weekly habit progress, readable columns, zoom, and local AI providers.</span></a>
  <a href="/devlog/omni-005-deleting-a-habit-should-not-delete-the-past/"><strong>005</strong><span>Habit identity: forward deletion, future-week reconciliation, cross-week streaks, and preserved history.</span></a>
  <a href="/devlog/omni-006-an-email-became-a-time-block/"><strong>006</strong><span>Integration: IMAP retrieval, email-to-calendar extraction, and ICS events entering the shared week store.</span></a>
  <a href="/devlog/omni-007-the-network-fix-was-too-powerful/"><strong>007</strong><span>Desktop boundary: fixing focus and connectivity while exposing the cost of elevation and generic network IPC.</span></a>
  <a href="/devlog/omni-008-a-goal-stopped-being-a-text-box/"><strong>008</strong><span>Goal domain: versioned migrations, GoalItem lifecycle, and one-way links from weekly execution.</span></a>
  <a href="/devlog/omni-009-the-password-left-localstorage/"><strong>009</strong><span>Credential hardening: safeStorage, migrated secrets, daily goal links, and the first fallback failures.</span></a>
  <a href="/devlog/omni-010-a-goal-had-tasks-but-no-time/"><strong>010</strong><span>Execution coverage: goal-aware calendar blocks, deterministic focus gaps, and derived weekly trends.</span></a>
  <a href="/devlog/omni-011-the-planner-outgrew-electron/"><strong>011</strong><span>Cross-device foundation: platform services, IndexedDB PWA, Capacitor, reminders, and resilient restore.</span></a>
  <a href="/devlog/omni-012-nothing-writes-until-confirm/"><strong>012</strong><span>First-run trust: honest empty states, readiness gates, and previews before restore or calendar writes.</span></a>
  <a href="/devlog/omni-013-the-first-release-gate-had-138-tests/"><strong>013</strong><span>Release confidence: typecheck, ID migration, 138 tests, manual gates, and traceable email failures.</span></a>
  <a href="/devlog/omni-014-oauth-worked-on-a-branch/"><strong>014</strong><span>Feature-branch email: bounded IMAP, PKCE OAuth, token refresh, and explicit unmerged status.</span></a>
  <a href="/devlog/omni-015-the-license-named-the-wrong-project/"><strong>015</strong><span>Publication: history-aware secret scanning, AGPL-3.0-or-later, and the corrected copied notice.</span></a>
  <a href="/devlog/omni-016-the-process-was-running-but-the-planner-was-hidden/"><strong>016</strong><span>Desktop launch truth: Windows wrappers, single-instance Electron, a visible planner window, and scoped deduplication.</span></a>
  <a href="/devlog/omni-017-the-dashboard-arrived-before-it-could-render/"><strong>017</strong><span>Execution cockpit: Dashboard, actuals, Pulse rules, a render-time failure, and the July 2 repair.</span></a>
  <a href="/devlog/omni-018-the-local-model-was-not-part-of-the-repository/"><strong>018</strong><span>Local-first v3: file-backed planner state, untracked llamafiles, local server control, and usage estimates.</span></a>
  <a href="/devlog/omni-019-rich-email-was-not-the-same-as-safe-email/"><strong>019</strong><span>MIME inbox: text and HTML alternatives, iframe containment, plaintext fallback, and unfinished remote-content policy.</span></a>
  <a href="/devlog/omni-020-the-pomodoro-chimed-but-the-week-stayed-empty/"><strong>020</strong><span>Execution UI: Pomodoro actuals, morning briefing, event checklists, and the silent week-key persistence failure.</span></a>
  <a href="/devlog/omni-021-closing-the-window-could-not-kill-the-alarm/"><strong>021</strong><span>Desktop alarms: persisted main-process timers, wake recovery, system tray, and opt-in launch at login.</span></a>
  <a href="/devlog/omni-022-a-new-week-was-not-allowed-to-inherit-everything/"><strong>022</strong><span>Week transition: canonical key repair and explicit carry, reschedule, or drop for goal-linked work.</span></a>
  <a href="/devlog/omni-023-the-background-process-was-not-a-tray/"><strong>023</strong><span>Desktop acceptance: the invisible tray, missing time controls, repaired quit path, and an unclosed smoke-test gate.</span></a>
  <a href="/devlog/omni-024-dismissing-an-alarm-became-work/"><strong>024</strong><span>Alarm integration: weekly repeats, wake missions, planner-backed dismissal, and Smart Snooze's unfinished semantics.</span></a>
  <a href="/devlog/omni-025-pulse-swallowed-the-clock/"><strong>025</strong><span>Pulse v4.2: five clock utilities, shared Pomodoro state, custom alarm audio, and renderer-bound timer lifecycles.</span></a>
</div>

## What This Demonstrates

<div class="proof-list">
  <span>Desktop app development</span>
  <span>Product design for personal workflows</span>
  <span>Local-first data thinking</span>
  <span>Practical launcher/setup design</span>
  <span>AI-assisted productivity design</span>
  <span>UX structure for planning systems</span>
</div>
