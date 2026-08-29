---
number: "025"
title: "Pulse Swallowed the Clock"
subtitle: "World time, countdowns, a stopwatch, and Pomodoro entered one cockpit; only some of them survived leaving the screen."
slug: "omni-025-pulse-swallowed-the-clock"
project: "OmniPlanner"
date: 2026-07-05
status: "published"
summary: "Pulse v4.2 expanded from alarms into a five-tab clock and focus suite with shared Pomodoro state and selectable alarm audio. Its UI breadth was real, but countdown and stopwatch lifecycles remained renderer-bound rather than joining Electron's persistent scheduler."
tags:
  - omniplanner
  - pulse
  - timers
  - pomodoro
  - world-clock
  - web-audio
  - electron
commits:
  - hash: "b465659277be10df7cfab210773dacfe5a399aba"
    title: "feat: Pulse v4.2 fully-featured premium Clock App with World Clock, Countdown Timers, Precision Stopwatch, synced Pomodoro dashboard, sound synthesis presets, and custom audio upload"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/b465659277be10df7cfab210773dacfe5a399aba"
---

Pulse began July 5 as OmniPlanner's alarm and reminder surface.

By 14:36, its subtitle had changed from “Alarms · Reminders · Nudges” to “Clock · Alarms · Focus Utilities.” A new tab bar divided the screen into Alarms, World Clock, Timer, Stopwatch, and Pomodoro.

The commit called the result a fully featured premium Clock App. It added 1,730 lines, removed 529, and introduced four large React components plus a shared sound engine.

The expansion was visually coherent. It also exposed a deeper architectural split: the alarm tab used Electron's persistent main-process scheduler, while most of the new clock tools measured time inside whichever renderer component happened to be mounted.

Pulse had become a suite before all five tabs agreed on what it meant for time to continue.

<div class="section-label">One surface collected five different time models</div>

The redesigned Pulse header retained a master Alarms Active switch, but the switch did not govern the other utilities. The World Clock, countdown timers, stopwatch, and Pomodoro remained usable as separate tools.

That distinction was sensible. Turning off notifications should not make Seoul disappear or prevent someone from measuring a lap.

The tab architecture was equally straightforward. `AlarmsView` held a local `activeTab`, and mounted exactly one of the four utility components when selected. The original reminder and custom-alarm interface remained under Alarms.

That conditional mounting detail determined the lifetime of each tool:

- World Clock persisted its selected city list;
- Timer persisted remaining values but deliberately restored everything paused;
- Stopwatch held all state only in its mounted component;
- Pomodoro lifted state into the root app and therefore survived navigation inside OmniPlanner;
- recurring alarms continued in Electron's main process even when the window was hidden.

They looked like siblings. They did not yet share one clock service.

<div class="section-label">World time was local, live, and almost timezone-correct</div>

The World Clock updated a single `Date` every second and formatted it through `Intl.DateTimeFormat` for up to twelve named IANA timezones.

Five cities appeared by default: Seoul, Tokyo, New York, London, and San Francisco. The user could add Paris, Sydney, Singapore, Berlin, Dubai, Mumbai, or Hong Kong and remove any selected card. The list was stored under `omni_world_clock_cities`, so leaving the tab or restarting the app preserved the chosen grid.

Using IANA identifiers was the right foundation. Daylight-saving changes belonged to the runtime's timezone database instead of a hand-maintained table. Each card also derived a local date and a day/night state rather than merely applying a fixed offset to the system clock.

The displayed relative offset was less precise. The component calculated an offset in minutes and then rounded it to an integer number of hours. A city such as Mumbai could therefore show a three-hour difference where the real difference from Seoul was three and a half. The data source supported fractional offsets; the label discarded them.

The list also bypassed OmniPlanner's registered storage-key abstraction and wrote directly to `localStorage`. It was harmless non-sensitive data, but another one-off key made backup and migration coverage easier to miss.

<div class="section-label">The countdown persisted its number, not its deadline</div>

The Timer tab supported multiple labeled countdowns.

A user could enter hours, minutes, and seconds or choose a quick preset, then independently pause, resume, reset, or delete each timer. A progress line and `HH:MM:SS` display updated every tenth of a second. Reaching zero opened a full-screen stop-sound dialog, played the default chime, and requested a desktop toast.

The timer list was written to local storage after every state update. On mount, it restored the records and intentionally forced every `running` flag to false “for safety.”

That meant the feature did not restore elapsed time. It restored a paused remaining-duration snapshot.

More importantly, `TimerTab` itself existed only while the Timer subtab was selected. Switching to Alarms, World Clock, Stopwatch, or Pomodoro unmounted it. The interval was cleared, the last state had already been stored, and returning created a new component with every countdown paused.

The same thing happened when leaving Pulse for another OmniPlanner screen. A “Pasta” timer could silently stop because the user checked the calendar.

Even while mounted, the ticker subtracted a fixed 100 milliseconds on every callback rather than calculating `deadline - Date.now()`. Renderer throttling, a busy event loop, sleep, or a hidden window could make it run slow. Persisting the entire timer array ten times per second also turned a display refresh into constant storage traffic.

The existing Electron alarm engine already solved most of these lifecycle problems with absolute timestamps, persisted schedules, sleep recovery, and main-process timers. v4.2 did not connect countdowns to it. The desktop toast at completion was real only if the renderer component stayed alive long enough to decide that completion had happened.

<div class="section-label">The stopwatch was precise in display, temporary in ownership</div>

The Stopwatch used `requestAnimationFrame()` for display updates and derived elapsed time from `Date.now()` minus a captured start time.

That was better than incrementing a counter on every frame. If rendering paused briefly, the next frame caught up to wall-clock time. The interface displayed centiseconds, recorded laps, calculated each split from prior lap totals, and highlighted the fastest and slowest once at least two existed.

Its “Precision Stopwatch” label described the presentation more than a durable measurement system. `Date.now()` is a wall clock rather than a monotonic high-resolution clock, and operating-system time corrections can affect it. `performance.now()` would be a stronger basis for precision timing.

All stopwatch state was component-local and unpersisted. Switching Pulse tabs unmounted it and discarded the running measurement and every lap. A utility meant to compare laps should not reset because the user briefly inspected an alarm.

The difference from the countdown was revealing: one persisted too frequently without preserving elapsed time; the other preserved elapsed time while mounted but persisted nothing. A shared time-domain model could have given both tools explicit start timestamps, pause accumulation, and restoration rules.

<div class="section-label">Pomodoro finally had one state across two controls</div>

Pomodoro moved in the opposite architectural direction.

Its mode, duration, time remaining, and running flag were lifted into `App.tsx`. The root memoized one props object and passed it to both the persistent sidebar timer and the new large Pulse dashboard.

Changing a 25-minute focus session to a 50-minute session in either interface updated the other. Starting, pausing, and resetting also stayed synchronized. The Pulse version added a circular progress display and a custom-duration slider, while the sidebar kept the compact always-visible control.

There was only one ticking effect. It remained inside `PomodoroTimer` in the sidebar; `PomodoroTab` was a second control and visualization, not a second interval. Because React still mounted the sidebar timer even when CSS hid its container on a small viewport, this avoided double-decrementing the shared state.

That was a practical reuse of the existing component, but it made the time engine depend on a presentation component remaining mounted. The Pomodoro state was not persisted and still decremented once per interval callback, so renderer suspension or app restart could lose or stretch a session.

On focus completion, the sidebar component played a chime, wrote an `ActualEventLog`, and automatically switched to a five-minute break. This preserved the earlier planner integration: focus time became execution history rather than an isolated clock statistic.

The log inferred the start by subtracting the configured duration from the completion time. Pauses were not represented, and the existing identity rule for multiple unplanned actuals on one day could still cause one session to replace another. The shared dashboard fixed control duplication; it did not yet produce a robust session ledger.

<div class="section-label">Alarm sound became a reusable subsystem</div>

v4.2 extracted the overlay's two-note chime into `soundSynth.ts` and added four generated presets:

- a rising sine-wave chime;
- a short square-wave double beep;
- a sawtooth frequency pulse;
- a slower C-major-seventh arpeggio.

Each custom alarm stored its selected preset. The main process persisted that name, included it in the trigger event, and preserved it when scheduling the next recurrence. `AlarmMissionOverlay` then delegated playback and cleanup to the shared module.

The alarm creator could preview a sound for four seconds. It could also import an audio file, convert the complete file to a data URL, and store the base64 string with the notification settings. Custom playback decoded that buffer in the renderer, looped it, and fell back to the chime when decoding failed.

Keeping synthesis local fit OmniPlanner's offline direction. It avoided shipping sound assets and kept the presets reproducible.

The custom-upload path needed stronger boundaries. It accepted whatever the file input returned, with no size ceiling or format validation before reading the entire file into memory and application storage. Base64 adds roughly one third to the original byte size. A large song could inflate the settings record, slow every settings save or backup, and exceed a browser-backed storage quota.

The imported bytes were not copied into Electron's alarm schedule. Only the preset name crossed to the main process; the overlay read the current `customSoundData` from renderer settings when triggered. This kept the main-process file small, but made custom audio depend on the renderer successfully loading the same settings when the alarm restored the window.

The sound module was a global singleton. Starting any new preview, timer sound, or alarm stopped the currently active source before playing its own. That prevented overlapping noise, although it also meant an ordinary countdown completion could replace a still-active mission alarm sound.

<div class="section-label">The commit proved breadth, not background reliability</div>

The v4.2 commit changed 13 files. No test file changed, and no direct session record survives after the earlier 13:28 conversation. Its history can be reconstructed from the commit and implementation, but there is no captured user-side acceptance result for the new clock suite.

The feature was not fake. The world clocks used real timezone formatting. Multiple countdowns existed. The stopwatch calculated laps. Pomodoro controls shared state and logged focus work. Alarm presets flowed through persistence and IPC.

But “clock app” raises a stricter expectation than “clock screen.” Time should keep its meaning when the user changes tabs, closes a window, sleeps the machine, or restarts the application.

Only the Electron alarm scheduler had begun to meet that standard. v4.2 assembled an attractive cockpit around several separate notions of time. The next architectural step was not another tab. It was one durable timing service beneath all of them.
