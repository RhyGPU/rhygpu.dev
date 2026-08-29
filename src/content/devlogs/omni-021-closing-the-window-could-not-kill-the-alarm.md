---
number: "021"
title: "Closing the Window Could Not Kill the Alarm"
subtitle: "Pulse stopped being a settings screen and became a main-process service."
slug: "omni-021-closing-the-window-could-not-kill-the-alarm"
project: "OmniPlanner"
date: 2026-07-04
status: "published"
summary: "OmniPlanner v4 replaced Electron's no-op notification adapter with persisted main-process timers, wake recovery, a system tray, close-to-tray behavior, and opt-in launch at login — finally allowing reminders to outlive the renderer window."
tags:
  - omniplanner
  - electron
  - alarms
  - notifications
  - system-tray
  - desktop
commits:
  - hash: "1f954f0da98b7cb51ccf9ecbb0a3a19d90c13d0a"
    title: "feat: working desktop alarms — tray, main-process notifications, launch at login (v4.0)"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/1f954f0da98b7cb51ccf9ecbb0a3a19d90c13d0a"
---

Pulse existed before desktop alarms did.

The rules engine could derive a wind-down reminder from a sleep block, a preparation reminder from a meeting, and a five-minute warning from a focus event. The settings screen could enable those rules. The platform abstraction even exposed a notification service.

On Electron, that service was `nullNotifications`.

It reported itself unavailable, returned false from scheduling, and performed no cancellation. Closing the only window also ended the application. Pulse described an alarm system that the desktop build could not deliver.

At 17:00 on July 4, v4.0 connected the missing operating-system layer.

<div class="section-label">The timer moved out of React</div>

An alarm tied to the renderer is only as reliable as the renderer.

React can reload. The window can be hidden. Chromium can suspend work. The machine can sleep. A browser-style `setTimeout` is useful for an open page, but it is the wrong owner for a desktop alarm that claims to survive ordinary app use.

v4 placed scheduled alarms in the Electron main process.

The renderer sent a numeric ID, title, body, and fire timestamp through the preload bridge. The main process stored the entry in a map, replaced any previous entry with the same ID, persisted the serializable fields to `scheduled-alarms.json`, and armed a timer.

Long delays were explicitly handled. JavaScript timers have an approximately 24.8-day ceiling, so the scheduler chained timers until the remaining delay fit within that range.

When a timer fired, Electron created a native `Notification`. Clicking the toast reopened or focused the planner window.

The platform factory then replaced `nullNotifications` with `electronNotifications`, allowing the existing reminder synchronization code to use the same interface as web and Capacitor while receiving desktop-specific durability.

Pulse had become connected plumbing rather than an availability mock.

<div class="section-label">Persistence covered restart and sleep</div>

On startup, the main process read `scheduled-alarms.json`, reconstructed valid numeric entries, and armed them again.

System sleep required a separate path. A `setTimeout` does not continue counting normally while the machine is suspended. On `powerMonitor.resume`, OmniPlanner recalculated every remaining delay.

Past alarms received a bounded grace policy:

- less than ten minutes late: fire immediately;
- ten minutes or more late: discard as stale.

That policy prevented a morning alarm from suddenly appearing in the afternoon while still recovering from a short laptop sleep or process gap.

The JSON file used restricted file mode where the platform honored it. Writes were synchronous, which simplified ordering between mutation and re-arming. They were not atomic replacements, and restore treated a malformed file as one failed collection. A crash during write could therefore lose the schedule file until the renderer synchronized reminders again.

The implementation made alarms persistent. It did not yet make the schedule a transactional database.

<div class="section-label">The X button changed meaning</div>

Keeping timers in the main process would not help if closing the window still quit Electron.

v4 created a system tray with three actions:

- open OmniPlanner;
- pause alarms;
- quit OmniPlanner.

The window's close event now called `preventDefault()` and hid the window unless a real quit was already in progress. A one-time native notification explained that OmniPlanner was still running and that the tray menu owned full exit.

Quit became deliberate. The tray command opened a confirmation dialog warning that alarms and notifications would stop. The normal `before-quit` event set the same flag so operating-system shutdown and explicit application quit could close the window rather than hide it again.

This changed OmniPlanner from a document-like app into a resident service with a window.

That distinction had UX cost. Users expect X to close many Windows applications. The one-time explanation and visible tray menu were necessary, not decorative.

The quit dialog also mentioned background email checks. This commit established the resident process required for such work, but its concrete implementation centered on alarm timers; the message was broader than the evidence in this change.

<div class="section-label">Startup remained opt-in</div>

A resident alarm app cannot recover after a reboot until it starts again.

OmniPlanner added Electron IPC around `getLoginItemSettings()` and `setLoginItemSettings()`. On the first desktop launch after v4, the renderer asked whether the user wanted the planner to start at login. The answer was recorded once, and Settings retained a reversible toggle.

The default was not silently changed.

This respected the difference between a useful recommendation and permission to add a login item. Enabling startup makes alarms more dependable, but it also changes system behavior and resource use outside the immediate session.

The notification settings panel updated its desktop status from “not available” to “full support” and explained close-to-tray behavior beside the toggle.

<div class="section-label">Pause meant suppress and forget</div>

The tray's Pause Alarms checkbox had a non-obvious semantic.

When a scheduled time arrived, `fireAlarm()` removed the entry from the map and persisted the reduced schedule before checking whether alarms were paused. If paused, it logged suppression and returned without showing a toast.

The alarm was not deferred. Unpausing did not replay it.

That may be appropriate for a “do not disturb” control, but the label “Pause Alarms” can imply suspended delivery. The implementation behaved more like “silence alarms while checked.” A clearer label or explicit missed-alarm history would make the consequence visible.

The paused state itself was in memory. It was not persisted across app restart.

<div class="section-label">The main-process boundary became the product boundary</div>

The commit changed 14 files, with 444 insertions and 39 deletions. It also centralized the AI usage and morning-briefing storage keys introduced by v3.

No automated test file changed with the alarm bridge. The critical checks were inherently cross-process and time-dependent:

1. schedule a near-future alarm through the renderer adapter;
2. hide the window and confirm the native toast still fires;
3. restart before fire time and confirm the schedule restores;
4. suspend and resume across fire time and verify the ten-minute rule;
5. click the notification and verify window focus;
6. close with X, then explicitly quit from the tray;
7. toggle launch at login and read back the operating-system state.

The following day's checklist did exactly this kind of practical verification because typecheck and unit tests could not prove a Windows notification appeared.

v4.0 completed a pillar that earlier devlogs had overstated. Before this commit, OmniPlanner had notification settings, derivation rules, and platform interfaces. After it, the Electron build had a persistent timer owner, a native delivery mechanism, and a lifecycle that could keep both alive without an open window.

The alarm no longer depended on the page staying visible.
