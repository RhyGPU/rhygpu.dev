---
number: "017"
title: "The Dashboard Arrived Before It Could Render"
subtitle: "The new cockpit expanded the product by 3,800 lines and broke at the first React render."
slug: "omni-017-the-dashboard-arrived-before-it-could-render"
project: "OmniPlanner"
date: 2026-06-22
status: "published"
summary: "OmniPlanner replaced its weekly-grid entry point with a today dashboard, actual-event logging, Pulse alarms, and plan-vs-actual review — but the large integration passed Vite while failing TypeScript and crashing at render until a direct July 2 repair."
tags:
  - omniplanner
  - dashboard
  - alarms
  - react
  - typescript
  - product-design
commits:
  - hash: "efb3b2a94f59f78b1519dfe3e67772e258d6bdb3"
    title: "local match?"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/efb3b2a94f59f78b1519dfe3e67772e258d6bdb3"
  - hash: "7d3b89fec9d1d67248abd075abc641f25e153e72"
    title: "render error fixed"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/7d3b89fec9d1d67248abd075abc641f25e153e72"
---

By late May, OmniPlanner's weekly planner was no longer the whole product.

The first repository devlog described a different opening question:

> Nobody opens a planner to see a grid — they open it to know what's next.

That retrospective, committed on May 29, announced a Dashboard, event Start/Skip/Snooze actions, a Pulse tab, sleep tracking, priority stars, undo, storage recovery, and plan-versus-actual review. At that point, the committed application still did not contain the new Dashboard or Pulse components.

The implementation reached Git on June 22 in a single commit titled `local match?`.

It changed 21 files, added 3,805 lines, removed 1,474, and made Dashboard the default tab. It also introduced a render-time failure that survived both the production build and the test suite.

The next surviving direct conversation began ten days later with four words:

> why not work rn?

<div class="section-label">The planner acquired a “today” layer</div>

Before this change, the weekly view was the primary operating surface. It was good at editing a plan but weak at answering the moment-to-moment question: what should happen now?

`DashboardView` added that layer.

The screen collected upcoming events, habits due today, top todos, and recent email into one entry point. Event cards offered Start, Skip, Done, and Snooze-shaped interactions. Quick-add forms could create a todo or habit without navigating back into the full planner. Priority values ranked work, and a five-second undo toast made habit deletion recoverable.

The important model addition was not the cards. It was `DailyActuals`.

A planned calendar event could now be connected to an `ActualEventLog`: scheduled time, actual start and end, whether it was attended, how often it was snoozed, where the observation came from, and when it was logged. Daily plans also gained actual habit completion and sleep fields.

OmniPlanner was beginning to distinguish intention from observation.

That distinction supported a new `WeekReview`. The comparison engine counted attended, missed, rescheduled, and unplanned events; computed habit completion; estimated sleep debt; and combined those inputs with todo completion into an adherence score.

This was a meaningful product boundary. A planner that only stores what should happen can organize. A planner that stores what did happen can review and adapt.

<div class="section-label">The calendar became the proposed alarm source</div>

The new Pulse tab presented daily planner reminders, habit reminders, focus-block reminders, and alarms derived from calendar events.

The accompanying rules engine treated alarms as projections of the plan rather than a second manually maintained list:

- a sleep event produces a wind-down reminder one hour before and a wake reminder eight hours after start;
- a meeting produces a preparation reminder 30 minutes before;
- a focus block produces a five-minute warning;
- an optional catch-all rule can warn before any event.

Each derived alarm retained the source event ID and a stable descriptive ID. The view previewed alarms for today and the next two days, while reminder synchronization scheduled the current day's future alarms through the platform notification interface.

The architecture was ahead of the desktop implementation.

The type documentation in the same commit still stated that Electron used `nullNotifications`. Pulse could display rules and toggle settings, but the desktop adapter did not yet deliver those alarms through Electron's operating-system notification APIs. That bridge would not become real until the July v4.0 work.

This is why the June feature should be read as a product and data-model expansion, not as proof that desktop alarms were already working end to end.

<div class="section-label">Safety work arrived beside product work</div>

The June synchronization also expanded the shell around the planner.

Window position and size were persisted under Electron's user-data directory. An auto-backup path attempted to capture `omni_` localStorage keys at quit and retain the ten newest snapshots. Update checks, IPC declarations, and preload methods expanded. Startup gained a storage integrity check before migrations.

The integrity check validated whether four critical localStorage values contained parseable JSON. If corruption was detected, startup offered to remove only the damaged keys and reset the schema version so migrations could recreate clean structures.

That is narrower than erasing all local data, but it is still destructive recovery. The detector checked JSON parseability, not the full shape or relationships of the stored objects. A structurally wrong but valid JSON value would pass; accepting repair would permanently remove a corrupt critical key. The backup path therefore remained important.

The commit also advanced the schema registry to version 4 for optional todo scheduling fields. The migration itself was intentionally a no-op because the new properties were optional.

<div class="section-label">The integration had no coherent green gate</div>

The size of the change obscured several mismatches.

`App.tsx` defined Dashboard callbacks before it initialized `allWeeks` and derived `currentWeek`. One callback captured `currentWeek` during render. JavaScript's temporal dead zone made that an immediate runtime error: the variable existed lexically but could not be read before initialization.

The same file used `getWeekDays` and the `Todo` type without importing them.

The comparison engine had a second contract failure. `DayComparison.habits` was declared as an object containing a habit list and completion rate. In the no-actuals branch, `compareDay()` returned the array directly and added a separate `habitCompletionRate` field that did not belong to the interface.

The new Dashboard displayed todo priority, but `Todo` itself did not declare that property.

These were exactly the failures a complete typecheck would expose. Yet Vite transpiled and bundled the TypeScript without enforcing type correctness, and the existing 138 tests did not exercise the new render path. The June commit added new alarm and comparison engines without dedicated test files for them.

The result was a dangerous split signal:

- the tests passed;
- the production build passed;
- TypeScript failed;
- React could blank at runtime.

Build success once again described artifact creation, not application health.

<div class="section-label">The repair took two minutes because the compiler already knew</div>

The July 2 diagnostic session ran the launcher's actual dependencies: Node availability, typecheck, tests, and build.

The contradiction appeared immediately. Tests and build were green, while TypeScript named the broken symbols and model shapes. Inspection then found the runtime-critical ordering error.

The repair was deliberately small:

1. import `getWeekDays` and `Todo`;
2. initialize `allWeeks` and `currentWeek` before Dashboard callbacks use them;
3. add the optional one-to-five `priority` field to `Todo`;
4. return a proper `HabitComparison` object when a day has no actuals.

The patch changed three files with 16 insertions and 12 deletions. Typecheck, all 138 tests, and the production build then passed together, and the app was launched through the same path as `run.bat`.

The fix restored rendering. It did not certify every new Dashboard action.

Several handlers still derived a plain Monday date such as `2026-07-06`, while the week store used its canonical prefixed key. Those mutations could look up no week and quietly return the previous state. That functional integration bug survived until the July 5 v4.0 work.

<div class="section-label">A cockpit needs evidence at every boundary</div>

The June-to-July sequence produced three distinct artifacts:

- a May retrospective that stated the desired product direction;
- a June bulk synchronization that introduced the model and UI;
- a July direct repair that made the expanded app render.

They should not be collapsed into one claim that “Dashboard and alarms shipped in May.” The dates and levels of completion were different.

The useful lesson was not merely to move a hook upward in `App.tsx`. OmniPlanner had added an execution cockpit, an actuals model, an alarm rules engine, storage recovery, and shell behavior in one integration. The old tests covered established planner logic, while the new failure lived at the seam between React initialization, shared types, and the default route.

After July 2, the app could reach the Dashboard. The next work had to prove that the Dashboard could reach the stored week, and that Pulse could reach the operating system.
