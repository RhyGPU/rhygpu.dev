---
number: "002"
title: "The Last Week of February Disappeared"
subtitle: "A calendar is not linked if only one view can write."
slug: "omni-002-the-last-week-of-february-disappeared"
project: "OmniPlanner"
date: 2026-02-26
status: "published"
summary: "A seven-day iterator skipped the final partial week, exposing a deeper problem: OmniPlanner's monthly calendar could display planning data but could not reliably create or edit it."
tags:
  - omniplanner
  - calendar
  - date-time
  - ux
  - electron
  - debugging
commits:
  - hash: "819814023b5a1b56f99dd08f2728a0f6cc4539d0"
    title: "Fix calendar bugs: uninteractable dates, read-only monthly, todo layout, habits"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/819814023b5a1b56f99dd08f2728a0f6cc4539d0"
---

The last week of February existed in the weekly planner and disappeared in the monthly calendar.

The cause was a loop that looked completely reasonable:

1. start on the first day of the month;
2. load the week containing that day;
3. move forward seven days;
4. stop after the end of the month.

For February 2026, that sequence visited February 1, 8, 15, and 22. It never visited February 28. Because the 22nd was a Sunday, its week belonged to February 16–22. The final week beginning Monday the 23rd was never loaded.

The calendar still drew the dates. It simply could not find the `WeekData` behind them. To the user, the final six days looked present and behaved as if they did not exist.

This entry, like the previous one, is reconstructed from the repository rather than a continuous exported conversation. The diff is unusually clear: one date-range bug exposed a second problem in the product's architecture. The two calendar views shared data in theory, but only one of them was allowed to behave like a planner.

<div class="section-label">A range is not a sequence of seven-day samples</div>

The fix to `getWeeksInRange` was small.

After the weekly loop finished, it explicitly loaded the week containing the range's end date and appended it if that week was not already present. The function stopped assuming that stepping from an arbitrary start by seven days would cover both boundaries.

The bug was a reminder that calendar ranges are not just arithmetic intervals. They overlap semantic buckets. A month can begin or end halfway through a week, and the set of weeks intersecting that month must include both partial edges.

That sounds obvious when written as a rule. It was much less obvious inside a loop whose increments were the same size as its buckets.

The disappearing dates also showed why a visual calendar needs empty data to be a valid state. A day with no plan is not a missing day. It is a day the user has not planned yet.

<div class="section-label">The monthly view was a display case</div>

Before this patch, clicking a date opened a polished detail modal.

It showed the day's focus, notes, and time blocks. It labeled the data “Real-Time Sync” and displayed an edit icon beside each event. But focus and notes were rendered as read-only blocks. The edit icon produced an alert telling the user to switch to the weekly planner. Dates without an existing daily plan could not open a meaningful editor at all.

The data was synchronized in one direction: the monthly view could observe what the weekly view had written.

That was technically shared state, but it was not the user-facing meaning of a linked calendar. From the user's perspective, two views of the same day should not disagree about whether that day is editable.

The patch added an application-level operation for updating the week containing any date. `MonthlyView` received that operation instead of managing a second store. When the user edited a daily focus, changed notes, added a time block, or deleted one, the monthly modal updated the same `allWeeks` record used by the weekly planner.

The monthly view became another editor over the same model, not a screenshot of the model.

<div class="section-label">Empty days became editable days</div>

The old lookup returned either a stored daily plan or nothing.

The new lookup separated two questions:

- does a stored daily plan already exist for this date?
- what should the editor show if it does not?

For display, a missing day received an empty shape: no focus, todos, notes, or events. On the first edit, `getOrCreateWeek` found or created the parent week, copied the daily plan, and sent the updated week through the shared application callback.

This eliminated an accidental permission rule where only previously populated days were interactive.

The date modal then gained the operations it had visually implied. Focus and notes became text areas. Events could be added with a title, start time, and duration, then removed from the same surface. **Open in Planner** switched to the weekly tab and moved the current date with it.

There was no special monthly copy to reconcile later. Both paths converged on `allWeeks`.

<div class="section-label">Seven columns cannot shrink forever</div>

The same bug-fix commit repaired the weekly grid.

Its desktop columns could shrink to zero because the layout used flexible widths with `min-w-0`. Long todos were forced into increasingly narrow cells, and an invalid utility class failed to provide the intended wrapping behavior.

Each day received a 160-pixel minimum width. The planner container became horizontally scrollable when the window could not fit all seven columns. Todo text used explicit `overflowWrap` and `wordBreak` rules.

Horizontal scrolling was not as visually elegant as compressing the entire week into every window size. It was more honest. Seven usable day columns require space. Below that threshold, preserving the content is better than pretending the layout still fits.

This was also a desktop-shell problem. Once the app had a resizable Electron window, “desktop” no longer meant one browser viewport chosen during development. The planner had to remain usable across window widths controlled by the user.

<div class="section-label">Replace the browser prompt</div>

Habit creation still used `prompt()`.

It was expedient in a browser prototype and unreliable in Electron. It also pulled the user out of the planner's interaction model into a blocking platform dialog.

The habit panel gained an inline input with visible confirm and cancel controls. Enter saved, Escape canceled, and the empty state itself invited the first habit. Creating a habit no longer depended on a browser primitive the desktop app could not consistently own.

This was not the end of the habit work. The new habit was added only to the current week's data. Deleting it, carrying it into future weeks, and calculating a truthful streak across weeks would become the next set of failures.

But the interaction now belonged to OmniPlanner rather than the browser shell it had just left behind.

<div class="section-label">One calendar, two perspectives</div>

The patch was filed as four bug fixes: skipped dates, a read-only month, collapsed todos, and broken habit entry.

Together they completed a larger transition.

The repository already claimed that the monthly and weekly views synchronized through a central store. After this change, that claim became operational:

- every date could be opened, including a date with no existing plan;
- both views could mutate the same daily focus, notes, and events;
- moving from month to week preserved the selected date;
- a partial week at the edge of a month could no longer fall outside the lookup;
- the weekly grid preserved usable columns instead of collapsing its contents.

Week isolation had been introduced to protect one week from another. This patch proved that isolation did not mean fragmentation. Multiple views could still share one stored week as long as they went through the same update boundary.

The last week of February did not need special treatment because it was February. It needed the calendar to understand that a visible date is always a real date, an empty plan is still a planable day, and synchronization means every supported view operates on the same truth.
