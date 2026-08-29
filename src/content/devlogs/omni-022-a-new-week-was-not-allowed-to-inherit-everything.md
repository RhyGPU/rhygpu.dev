---
number: "022"
title: "A New Week Was Not Allowed to Inherit Everything"
subtitle: "Goal-linked commitments earned a decision ritual; ordinary backlog still stopped at Sunday."
slug: "omni-022-a-new-week-was-not-allowed-to-inherit-everything"
project: "OmniPlanner"
date: 2026-07-05
status: "published"
summary: "v4 repaired six Dashboard mutations that used the wrong week key, then added a once-per-week carry-forward decision for unfinished goal-linked tasks without abandoning OmniPlanner's week-isolation rule."
tags:
  - omniplanner
  - weekly-planning
  - carry-forward
  - data-model
  - react
  - bug-fix
commits:
  - hash: "0e1699dd0c0c34d79f3c2b730d89c92052ed972b"
    title: "feat: Monday carry-forward ritual + Dashboard week-key fix (v4.0)"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/0e1699dd0c0c34d79f3c2b730d89c92052ed972b"
  - hash: "af8c21da2ee18a317dc1d6908de326bbc7850f72"
    title: "docs: v4.0 consolidation — all-in-one thesis, resolved security findings, version 4.0.0"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/af8c21da2ee18a317dc1d6908de326bbc7850f72"
---

OmniPlanner was built around a refusal to create one immortal backlog.

Each week is its own planning page. Unfinished work does not automatically flood the next Monday. The boundary forces a new decision instead of letting stale tasks accumulate until the list becomes meaningless.

That rule created a difficult exception.

An ordinary task can expire with the week. A task explicitly linked to a long-running goal represents a commitment beyond that week. Letting it disappear without review makes the weekly surface clean by silently starving the goal system above it.

v4 added a carry-forward ritual for that exception — immediately after repairing the Dashboard actions that had been writing to no week at all.

<div class="section-label">The missing prefix affected six different actions</div>

The previous entry traced the persistence failure to a string convention.

`allWeeks` used canonical keys such as `omni_week_2026-07-06`. New Dashboard callbacks computed only `2026-07-06`. TypeScript saw two strings; the store saw two different addresses.

The July 5 patch replaced the hand-built Monday strings with `getWeekStorageKey()` across six mutation paths:

- log an actual event;
- toggle a habit and its daily actual;
- toggle a todo;
- quick-add a todo;
- quick-add a habit;
- set the Morning Briefing focus theme.

The repair also replaced in-place mutation of nested week objects with new arrays and objects. That was important for React as well as persistence. A correct key still does not guarantee a render if state references are quietly reused.

When a week did not exist, creation went through `getOrCreateWeek()` instead of borrowing `currentWeek` under a new address. The Pomodoro could finally write its `ActualEventLog`, and the Morning Briefing could finally persist its focus banner.

One actual-log edge case remained. The update path matched existing records by `plannedEventId` and date. Unplanned sessions such as Pomodoros have no `plannedEventId`, so two on the same date both compare as `undefined` and the later session can replace the earlier one. The week address was fixed; the identity rule for multiple unplanned actuals was not.

<div class="section-label">Only goal-linked work crossed the boundary</div>

The new domain module scanned exactly one previous week.

It collected unfinished todos from the weekly business and personal goal sections, followed by daily plans in date order. A todo qualified only when it had a `parentGoalId` and was not done.

Unlinked work never appeared in the dialog.

That filter preserved the product's original week-isolation rule. Carry-forward was not a global rollover switch. It was a review of work that had already declared a relationship to a longer-lived goal.

Candidates were grouped under the current goal text. If the referenced goal had since been removed, the group remained visible under an “Unlinked goal (removed)” fallback instead of silently dropping the task.

For each item, the user could choose:

- Carry to the new week's Monday;
- Move to a specific day in the new week;
- Drop, leaving it only in the old week.

Bulk controls supported Carry all and Drop all. The default for every untouched choice was Carry.

That default optimized for continuity, but it also made the primary Apply action potentially aggressive. Opening the ritual and clicking through without review copied every candidate to Monday. A no-default or explicit review requirement would favor deliberation over speed.

<div class="section-label">Carry meant copy, not move</div>

`buildCarriedTodo()` created a new task with a fresh ID.

It preserved text, goal link, and priority; reset completion; and intentionally removed old scheduling metadata. The previous week's source task stayed untouched as historical evidence.

This was consistent with immutable weekly history. A reschedule did not rewrite what had been planned last week. It created a new-week commitment derived from that record.

The new ID was based on the source ID and current timestamp. The copy did not retain an explicit `carriedFromId`, so lineage could only be inferred from the generated ID string. Backup normalization or future ID changes could erase that inference.

The candidate collector's comment mentioned de-duplication, but the implementation did not actually maintain a seen set. If the same logical todo ID appeared in both a weekly goal section and a daily plan, both sources became separate candidates because the dialog key included source plus ID. Applying both could copy the same work twice.

The ritual protected historical weeks. It did not yet formalize task lineage or duplicate identity.

<div class="section-label">“Monday” meant the first launch of the week</div>

The feature was named the Monday carry-forward ritual, but it did not require the current day to be Monday.

On the first application launch for a canonical week key, it inspected the week seven days earlier. If candidates existed, the dialog appeared before the Morning Briefing. If none existed, the current week key was recorded immediately so startup would not scan again.

This made the ritual resilient to missed days. Opening OmniPlanner on Wednesday still forced the weekly decision rather than skipping it because Monday had passed.

The once-per-week flag also controlled dismissal. Choosing “Don't show this week” wrote the same completion marker without applying any decisions. The candidates remained in last week's history, but the dialog did not return that week.

That is a reasonable interpretation of dismissal, though stronger copy such as “Skip this review for the week” would make the persistence explicit.

The trigger used a startup snapshot by design. Changes to goals or weeks after mount did not re-open the dialog in the same session.

<div class="section-label">The model finally named the focus it was already storing</div>

The same commit declared `focusTheme` on `DailyPlan`.

The Morning Briefing had already been writing this field through object spreads, which can bypass a useful excess-property signal depending on context. The Dashboard read it, but the domain interface did not acknowledge it.

Adding the optional field closed that type hole and distinguished it from the existing daily `focus` field: one belonged to the weekly column editor; the other powered the briefing and Dashboard banner.

AI cost estimates also became model-keyed instead of provider-keyed. Unknown and local models contributed zero dollars rather than borrowing an arbitrary provider price, and the UI labeled the result as a rough estimate.

<div class="section-label">v4 stated its actual thesis after fixing its store</div>

Four minutes later, the documentation consolidation changed the package version from 2.2.0 to 4.0.0 and stated the product thesis directly: alarms, planner, todos, and email in one always-open cockpit.

It also updated stale security findings to reflect encrypted desktop credentials, retained open web and OAuth concerns, and documented the alarm engine, tray lifecycle, carry-forward ritual, and week-key repair.

The feature commit added 498 lines and removed 95 across 11 files. No automated test file changed. Its message records an end-to-end web preview of carry to Monday, move to Wednesday, and drop; the following manual checklist broadened verification to the desktop shell.

The most important v4 change was not the modal itself. It was the restored meaning of a week:

- Dashboard actions now write to the canonical week;
- historical weeks remain historical;
- routine backlog stays behind;
- goal-linked unfinished work receives an explicit human decision;
- carrying creates a new record rather than falsifying the old one.

OmniPlanner did not solve backlog by moving everything forward. It made continuity conditional on declared purpose.
