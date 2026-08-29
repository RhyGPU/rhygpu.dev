---
number: "020"
title: "The Pomodoro Chimed, but the Week Stayed Empty"
subtitle: "The execution UI arrived before its callbacks learned the canonical week key."
slug: "omni-020-the-pomodoro-chimed-but-the-week-stayed-empty"
project: "OmniPlanner"
date: 2026-07-04
status: "published"
summary: "v3.2 added a focus timer, morning briefing, event checklists, and plan-vs-actual overlays, but its new Dashboard mutations addressed weeks by a plain Monday date instead of OmniPlanner's prefixed storage key, so important actions could silently fail to persist."
tags:
  - omniplanner
  - pomodoro
  - dashboard
  - react
  - persistence
  - ux
commits:
  - hash: "772e20f35d0b32721cd046d2a8b818742447d575"
    title: "feat: premium planner UI, Pomodoro timer, and morning briefing (v3.0-v3.2)"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/772e20f35d0b32721cd046d2a8b818742447d575"
---

The last v3 commit on July 4 tried to close the distance between planning and doing.

The Dashboard gained a daily briefing. The sidebar gained a Pomodoro timer. Calendar events gained internal checklists. The weekly grid could place actual execution beside the original plan, and the Week Review moved into a collapsible drawer instead of occupying permanent space.

Visually, OmniPlanner became more like an operating cockpit.

Functionally, the new execution controls inherited a key mismatch from the Dashboard integration. A focus timer could reach zero, play its completion chime, switch into break mode, construct a valid actual-event record — and then fail to store it in any week.

There is no direct conversation attached to this commit. Its success and failure paths are both visible in the code, and the persistence bug was explicitly fixed the following day.

<div class="section-label">A timer became part of the actuals model</div>

`PomodoroTimer` was not implemented as an isolated countdown widget.

It offered 25- and 50-minute focus presets, 5- and 15-minute break presets, pause, reset, a progress layer, and a two-tone Web Audio chime. Finishing a focus session created an `ActualEventLog`:

- a unique `actual-pomodoro-*` ID;
- a title containing the completed duration;
- today's date key;
- calculated actual start and end hours;
- manual source and attended status;
- a logged timestamp.

Because the timer was not necessarily attached to a scheduled calendar event, the log omitted `plannedEventId`. The comparison engine could therefore treat it as unplanned work — exactly the kind of activity a plan-versus-actual system should reveal.

Break completion did not write an execution record. Both modes switched automatically when the timer ended.

This was the right conceptual integration. Focus time was no longer only a UI utility; it was evidence about how the day had actually been spent.

<div class="section-label">Morning planning became a once-per-day ritual</div>

The new `MorningBriefing` modal assembled a lightweight daily review:

- yesterday's habit completion rate;
- up to three unfinished todos for today;
- today's focus and task blocks;
- a field for one daily focus theme.

On the first open for a date, the modal appeared automatically. Dismissing it stored that date under `omni_last_briefing_date`, and a Dashboard button could reopen it later. Submitting the form wrote `focusTheme` into the day's plan before closing.

The UI connected three time horizons without AI generation: yesterday's behavior, today's existing commitments, and one explicit statement of intent.

Closing the modal with the X used the same dismissal path as completing it. That prevented repeated interruption, but it also marked the ritual done even if no focus theme had been set.

The new storage key was written as a raw string rather than through the central `LOCAL_STORAGE_KEYS` registry. The subsequent v4 commit moved it into the registry with the AI usage key.

<div class="section-label">Calendar blocks acquired internal structure</div>

`CalendarEvent` gained a typed `subEvents` collection. Each child carried an ID, title, and completion state.

The event editor could add, remove, and edit those checklist items. The weekly calendar rendered them inside the parent block and allowed in-place completion without opening the editor again.

This made a time block capable of representing more than one opaque label. A two-hour release block could retain the checks that made it complete; a meeting could carry agenda items; a routine could expose its sequence.

Unlike placing more separate todos on the calendar, sub-events remained owned by the block. That preserved the visual schedule while adding executable detail.

The same weekly view added an Actuals mode. Planned blocks with actual logs became visually subdued, attended execution appeared as a solid comparison block, and skipped items gained a red treatment. A Week Review drawer summarized the comparison on demand.

The product direction was coherent: plan, execute, record, compare.

<div class="section-label">The canonical key included more than the date</div>

OmniPlanner did not index `allWeeks` by a bare Monday such as `2026-07-06`.

Its canonical helper returned:

`omni_week_2026-07-06`

The new Dashboard handlers repeatedly reimplemented only the date portion:

1. calculate the Monday for an action date;
2. format it as `YYYY-MM-DD`;
3. look up `updated[weekStart]`.

That lookup could not find a normally stored week.

`handleLogActual` responded by returning the previous state unchanged. The completed Pomodoro record disappeared silently. Event Start and Skip actions used the same callback and could fail the same way.

`handleSetFocusTheme` had the same structure. The morning briefing could accept a focus, close, and still leave the day unchanged.

Habit completion, quick todo creation, and other Dashboard mutations repeated variations of the mismatch. Upcoming-event and todo selectors also used the plain key, then fell back to `currentWeek`; across a week boundary, that fallback could search the wrong week for a future date.

No exception appeared. The mutation code treated “week not found” as a safe no-op, so the UI offered no failure state.

This is the kind of bug TypeScript cannot identify. Both the canonical key and plain date were strings. The missing information lived in a naming convention and a helper that the new code bypassed.

<div class="section-label">The UI shipped without a matching behavior test</div>

The commit added 817 lines and removed 67 across 11 files. It created two substantial components and altered the core weekly planner. No test file changed with it.

A focused integration test could have exposed the key mismatch with a small fixture:

1. seed `allWeeks` under `getWeekStorageKey(date)`;
2. complete a one-second focus session or invoke its actual-log callback;
3. assert that the target day's `actuals.events` contains the new record;
4. submit a morning focus and assert the same canonical week changed;
5. cross Sunday into Monday and verify upcoming items come from the next week.

The timer itself behaved visibly. The chime played. The mode changed. The failure was behind that feedback, in the state transition users could only discover after reopening or reviewing the week.

<div class="section-label">Premium polish made persistence more important</div>

The rest of the commit tightened the working surface: fewer upcoming cards, expired events filtered from today's Dashboard, stronger grid alignment, denser day columns, refreshed icons, and a collapsible review panel.

Those changes made the app feel more immediate. They also raised the trust cost of a silent no-op. A rough prototype invites verification; a polished button and completion chime imply that the action is finished.

The v3.2 implementation established the right execution loop in the model:

`focus session → ActualEventLog → DailyActuals → Week Review`

The connection from callback to week store was wrong.

The next day's v4.0 work replaced the hand-built Monday strings with `getWeekStorageKey()` across the affected handlers. Only then could the new cockpit reliably write into the planner it was presenting.
