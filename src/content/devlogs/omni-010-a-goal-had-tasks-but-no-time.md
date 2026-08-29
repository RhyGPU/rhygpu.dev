---
number: "010"
title: "A Goal Had Tasks but No Time"
subtitle: "Calendar support became the missing layer between intention and execution."
slug: "omni-010-a-goal-had-tasks-but-no-time"
project: "OmniPlanner"
date: 2026-03-20
status: "published"
summary: "Goal-linked todos could prove intention without reserving any time. Calendar events gained execution semantics, deterministic focus suggestions, and derived weekly and four-week coverage analytics."
tags:
  - omniplanner
  - calendar
  - goals
  - analytics
  - focus
  - planning
commits:
  - hash: "e43557613d31abccc1a7725acf10bf4d481f038b"
    title: "Add calendar execution and planning intelligence"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/e43557613d31abccc1a7725acf10bf4d481f038b"
  - hash: "945e4c3b0635f22b75ea752aee9c8b857e0378fa"
    title: "Add execution analytics and weekly review"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/945e4c3b0635f22b75ea752aee9c8b857e0378fa"
  - hash: "5a771d5d23a354f83a4687ab022ed6c24f8a48f5"
    title: "Add historical execution trends and reflection analytics"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/5a771d5d23a354f83a4687ab022ed6c24f8a48f5"
---

A life goal could have five linked todos and zero minutes on the calendar.

OmniPlanner now knew that the tasks supported the goal. It knew which tasks were complete. It still could not distinguish a commitment with reserved time from one left in a list.

On the morning of March 20, the calendar acquired that distinction. A time block could identify its kind, the goal it supported, and the todo it scheduled. Within three hours, the same stored relationships produced a weekly review and a four-week execution history.

No AI was required. No analytics table was added. The application derived every result from goals, todos, events, and week records it already owned.

This is a Git-based reconstruction of three consecutive phases. Their common question was simple:

> Did this intention receive time?

<div class="section-label">An event became more than geometry</div>

The original `CalendarEvent` described a rectangle: ID, title, start hour, duration, color, and optional recurrence.

Phase 5 added three optional fields:

- `eventKind`: meeting, focus, task block, or routine;
- `parentGoalId`: the long-range goal supported by the block;
- `linkedTodoId`: the specific weekly or daily todo receiving time.

Making them optional preserved old events and backups. An untyped block still rendered. A new or edited block could carry execution meaning without a schema migration.

The event editor gained four kind controls and kind-specific default colors. Clicking empty calendar space defaulted to a focus block. A goal-linked event showed a small goal indicator in the grid.

The important part was not the color taxonomy. It was that a block could now answer both **what occupies this time?** and **why was this time reserved?**

<div class="section-label">A todo was unscheduled only under specific rules</div>

The new planning selectors defined the missing state deterministically.

A weekly todo counted as unscheduled when it was incomplete, linked to a goal, and had no event in the week matching its todo and goal identity. A daily todo used the same rule inside its own date.

A goal had calendar support when events linking to that goal contributed duration during the visible week. Coverage combined total linked tasks, tasks with matching blocks, and scheduled minutes.

This avoided a vague interpretation where any busy calendar meant progress. A meeting unrelated to a goal did not provide that goal with support. A focus block without a link still counted toward total focus time but not toward a particular goal's coverage.

The relationships remained one-directional:

- todos pointed to goals;
- events pointed to goals and optionally todos;
- coverage was calculated from those pointers.

No progress field was written back into `GoalItem`. No “scheduled” boolean was written onto a todo. The data could not drift between a stored flag and the event that supposedly justified it.

<div class="section-label">Focus Gaps did not call a model</div>

The weekly sidebar gained an amber **Focus Gaps** section for linked weekly work without calendar time.

Each displayed item had a **Block** action. Selecting it opened the normal event editor with the goal and todo already linked, a 90-minute duration, and a suggested hour.

The suggestion algorithm was intentionally small:

- consider incomplete linked weekly todos;
- produce at most one suggestion per goal;
- choose the first chronological day with fewer than four existing events, or the first day as fallback;
- place the block after that day's latest event, capped at 5:00 PM;
- default to 90 minutes and focus kind.

The commit described this as finding the best available day. The actual implementation did not optimize across every day or detect interval collisions. It selected the first day below a simple event-count threshold and used the latest end time.

That was still useful because the suggestion remained visible and editable. It did not need probabilistic confidence or a provider key to transform “I should do this” into a draft reservation.

The planner used AI for optional interpretation elsewhere. Scheduling coverage was domain logic and stayed deterministic.

<div class="section-label">The week review reported facts</div>

Phase 6 extended the same selectors into a collapsed **Week Review** panel.

It reported:

- focus and task-block count;
- total focus and task-block minutes;
- active goals with calendar support;
- active goals with linked work but no blocks;
- completed linked tasks;
- linked tasks still unscheduled.

Day headers received two compact signals: purple when a linked focus block existed, amber with a count when linked daily tasks lacked blocks.

The Goals view displayed calendar coverage beside all-time task progress. A goal could therefore show `3/5` completed tasks and `2h` scheduled this week without collapsing those measurements into one score.

The panel's language was deliberately neutral. It did not call an unscheduled task a failure or turn the data into a productivity grade. The roadmap's “calm” principle appeared here as copy and information hierarchy: show the gap, offer an action, avoid manufacturing guilt.

<div class="section-label">History was the existing week store</div>

Phase 7 looked backward without creating a new analytics database.

For a selected goal, it took up to four stored week keys earlier than the current week and derived one point per week:

- whether the goal had any calendar support;
- supported minutes;
- linked and completed task counts;
- unscheduled linked task count.

From those points it calculated support-week count, total minutes, completed work, and a streak counted backward from the most recent past week.

The Goals view rendered a compact `N/Mw` chip once at least two historical weeks existed. The weekly sidebar summarized how many active goals had support in every considered week, some weeks, or none, and identified the longest current support streak.

This history had a precise limitation: it considered stored weeks, not every calendar week that had elapsed. If no `WeekData` existed for a week, that week was absent from the window rather than counted as a zero-support week.

That matched the architecture's available evidence but made the metric a record-coverage trend, not a complete chronological audit. The distinction belongs in any future interpretation of the streak.

<div class="section-label">Analytics remained disposable</div>

The three phases added hundreds of lines of selectors and UI while adding no analytics persistence.

That was a strength.

If the definition of calendar support changed, the app could recalculate old weeks. If a linked event was edited or removed, the review changed with it. Backup and restore did not need a second set of aggregates. There was no migration for stale totals.

The cost was repeated scanning across `allWeeks`, goals, daily plans, todos, and events. At the scale of a personal local planner, the simpler consistency model was worth it. If performance later required indexing, the derived selectors already defined what an index would have to reproduce.

<div class="section-label">Planning became allocation</div>

The goal work from the previous entries had created a vertical chain:

> life goal → weekly commitment → daily action

Phase 5 added one more step:

> life goal → weekly commitment → daily action → reserved time

Phase 6 described the current state of that chain. Phase 7 asked whether the pattern persisted.

The product did not decide that more scheduled minutes always meant a better week. Meetings, routines, rest, and unlinked work still existed. It did establish that a goal with linked tasks and no reserved time was materially different from one supported by a focus block.

A todo is evidence of intention. A checkmark is evidence of completion. A calendar block is evidence that the week made room.

OmniPlanner could finally show all three without pretending they were the same thing.
