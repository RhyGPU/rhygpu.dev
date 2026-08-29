---
number: "024"
title: "Dismissing an Alarm Became Work"
subtitle: "v4.1 connected repeating alarms to wake missions, planner tasks, and calendar movement — then left recurrence and snooze semantics unfinished."
slug: "omni-024-dismissing-an-alarm-became-work"
project: "OmniPlanner"
date: 2026-07-05
status: "published"
summary: "OmniPlanner v4.1 added custom weekly alarms, three interactive dismissal missions, synthesized fade-in chimes, and Smart Snooze calendar shifts. The integration was ambitious, but pausing could erase a recurring alarm and snoozing stripped the mission from the next ring."
tags:
  - omniplanner
  - electron
  - alarms
  - planner-integration
  - react
  - scheduling
  - product-design
commits:
  - hash: "deb983cedf0f41d8a587eada8a2d9e9cae849b0f"
    title: "feat: custom alarms, repeat scheduling, wake missions, and Smart Snooze calendar rescheduling (v4.1)"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/deb983cedf0f41d8a587eada8a2d9e9cae849b0f"
---

Eleven minutes after repairing the first failed tray test, OmniPlanner's alarm system changed scope.

It was no longer only a way to keep a planning reminder alive after the window closed. v4.1 introduced named alarms with weekly repetition, selectable snooze and fade-in durations, and a mission that could stand between the ring and the Dismiss button.

The mission could ask for three arithmetic answers, require the day's focus theme, or turn two planner todos into the price of silence. Snoozing could also move a matching calendar block later.

This was the point where Pulse stopped being a passive reminder list and began behaving like a small alarm application attached to the planner.

It was also a single 878-line feature commit with no new automated tests, made while the desktop acceptance gate from the previous entry was still open.

<div class="section-label">A custom alarm became persisted scheduler state</div>

The new `CustomAlarm` model stored more than a time.

Each record had a string ID, title, hour, minute, enable flag, selected days of the week, mission type, snooze duration, and fade-in duration. It lived inside the existing non-sensitive notification settings, so the renderer owned the editable definition while Electron's main process owned the live timers.

The Alarms screen added a compact creator for that model:

- a label and native time input;
- seven day-of-week pills, defaulting to Monday through Friday;
- None, Math, Planner Checklist, or Daily Theme missions;
- 5, 10, 15, or 30 minute snooze;
- instant, 10, 20, or 30 second sound fade-in.

Saving updated local settings. `syncReminders()` then sent the entire custom-alarm array across the preload bridge. The main process cancelled every existing ID in the `custom-` namespace and rebuilt enabled schedules from the latest definitions.

That full replacement strategy was simple and idempotent. Toggle, delete, and edit paths could all converge on one operation instead of trying to patch individual timers across process boundaries.

It was not especially efficient: cancelling each custom alarm persisted the schedule file, and adding each replacement persisted it again. For the intended personal-scale list, correctness was more important than minimizing a handful of small writes.

The scheduler extended its on-disk records with mission, snooze, fade, original clock time, and repeat days. Those fields survived restart alongside the next occurrence timestamp. Numeric IDs from the older notification tracks and string IDs from custom alarms could now share the same map.

<div class="section-label">Firing an alarm crossed from the main process into the planner</div>

When a custom alarm became due, the main process first removed its current occurrence from the map and persisted the change. It showed a native Windows notification, restored and focused the main window, then emitted `alarm:trigger` to the renderer with the mission configuration.

After delivery, a `custom-` alarm calculated its next selected weekday and scheduled itself again.

This separated two responsibilities well:

- Electron kept time while the renderer was hidden;
- React rendered the interactive experience after Electron brought the window back.

The preload API exposed only a callback registration and custom-alarm update method, rather than giving the renderer raw Electron access. The app registered one listener on mount and converted each trigger into `activeAlarm` state. That state mounted a full-screen `AlarmMissionOverlay` above the planning interface.

The main process also retained the earlier ten-minute missed-alarm policy. A recently missed occurrence fired after restart or resume; an older one was discarded as stale. That policy was sensible for one-shot reminders, but v4.1 reused it without giving recurring alarms a separate path.

If a recurring custom alarm was more than ten minutes late at restore time, the code deleted it and did not calculate its next occurrence. Its future series disappeared from the live schedule until a later renderer synchronization rebuilt it from settings.

The same failure existed for Pause Alarms. `fireAlarm()` deleted the due occurrence before checking the global pause flag. A paused alarm returned early, before the recurring reschedule block. Pause therefore suppressed more than one ring: it could remove the series from the main-process schedule for the rest of the session.

The persisted definition still existed in renderer settings, so relaunching or another reminder sync could recover it. But a tray action labeled Pause should not depend on an unrelated future synchronization to preserve tomorrow's alarm.

<div class="section-label">The Dismiss button acquired three gates</div>

The overlay synthesized a two-note A5/E6 chime through Web Audio every 2.2 seconds. With fade-in enabled, the gain rose linearly from 0.01 to 0.12 over the selected duration. Unmounting the overlay cleared the interval and closed the audio context.

Then the chosen mission controlled whether Dismiss was enabled.

The Math mission generated addition, subtraction, or multiplication problems. Three correct answers cleared it. A wrong answer retained the current stage and displayed an error.

The Theme mission displayed the day's Focus Theme and required it to be typed back. Comparison trimmed whitespace and ignored case. If no theme existed, the mission automatically passed. This was less a memory test than an attention ritual: the answer was visible directly above the input, which made the point repetition rather than recall.

The Checklist mission read active todos from the selected day's plan. Checking an unfinished item invoked the same Dashboard mutation that persisted normal todo completion. Two newly completed items cleared the mission, or one item cleared it when it was the last unfinished task.

That made dismissal produce real planner state instead of maintaining a disposable alarm-only checklist. It was the strongest product connection in the release.

There was an edge case. `activeTodos` included tasks that were already done. If every active task was complete when the alarm opened, the list was non-empty, completed items could not be clicked, and Dismiss remained disabled because the automatic empty-list escape only checked `activeTodos.length === 0`. A checklist intended to prove action could trap a user who had already done the work.

The overlay also did not make missions unavoidably blocking. Snooze remained enabled before mission completion. Closing or killing the desktop process remained an operating-system escape. This was an interaction gate, not tamper-resistant alarm enforcement — an appropriate distinction for a personal planner, but different from the walkthrough's phrase “blocks dismiss.”

<div class="section-label">Snooze moved work by matching words</div>

Snooze performed two actions.

First, it scheduled a new one-shot main-process notification for the chosen number of minutes. Second, it searched the current planner day for a calendar event whose title appeared inside the alarm title or body. Every match had its `startHour` shifted by the snooze fraction, capped at 23.75.

That was the first time an alarm response edited the schedule itself. Snoozing “Focus Block” could acknowledge a real execution delay rather than leaving the calendar to claim the original start time.

The heuristic was intentionally lightweight, but it was also fragile:

- matching was substring-based rather than linked by an event ID;
- short or repeated event titles could shift the wrong block or several blocks;
- the lookup used the app's selected `currentDate`, not necessarily the wall-clock date on which the alarm fired;
- only the start time moved, with no collision or end-of-day validation beyond clamping the start to 23:45;
- the state update reused a captured `dayPlan`, so a concurrent edit could be overwritten.

Most importantly, the snoozed notification used the basic `notificationSchedule()` path. That path assigned `missionType: none`, a five-minute default snooze, and no fade-in. The next ring therefore did not preserve the original mission or sound configuration.

A user could postpone a Math alarm once and receive a freely dismissible alarm afterward. Smart Snooze connected the alarm to the calendar, but disconnected the alarm from its own rules.

<div class="section-label">Repeat-day semantics still needed a contract</div>

`getNextOccurrenceMs()` began with the chosen time today, advanced to tomorrow if that moment had passed, and then walked forward until it found a selected weekday.

For a normal Monday-to-Friday alarm, that produced the expected next occurrence. The original clock fields stayed with the record, allowing the series to reschedule from its definition instead of adding a fixed 24-hour duration.

The UI allowed all seven day pills to be deselected. The scheduler interpreted an empty array as no weekday filter and scheduled the alarm for the next day. In other words, selecting no repeat days behaved like repeating every day.

Neither behavior is inherently wrong — an empty set could mean a one-shot alarm or a daily alarm — but the creator labeled the control “Repeat Days” and did not explain that fallback. The data model needed an explicit one-shot/daily/repeating mode rather than assigning three meanings to an array's shape.

There were also no timezone or daylight-saving rules beyond JavaScript's local `Date` construction. For a Windows-only personal build in Korea, that was a practical starting point. It was not yet a portable alarm contract.

<div class="section-label">The feature expanded before its gate closed</div>

The direct checklist after this commit asked for a custom alarm one minute in the future with a Math mission, followed by a Smart Snooze test against a calendar block. The completion report still described both Phase 1 and v4.1 as code-verified pending that packaged manual run.

No surviving message records the final result.

That does not erase what v4.1 accomplished. It created a real cross-process alarm pipeline, persisted repeat metadata, made the planner participate in dismissal, and treated snooze as an execution change instead of a private timer event.

It also revealed the cost of combining an alarm clock and planner in one jump. Recurrence, pause, missed-alarm recovery, mission continuity, calendar identity, and already-completed tasks all became one product contract.

The best idea in v4.1 was not that an alarm could demand arithmetic. It was that an alarm could acknowledge the work it interrupted. The unfinished part was making that acknowledgement reliable enough to survive pause, restart, snooze, and the messy state of a real day.
