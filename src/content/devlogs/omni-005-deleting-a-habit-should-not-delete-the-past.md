---
number: "005"
title: "Deleting a Habit Should Not Delete the Past"
subtitle: "Week isolation had turned one habit into many copies."
slug: "omni-005-deleting-a-habit-should-not-delete-the-past"
project: "OmniPlanner"
date: 2026-03-11
status: "published"
summary: "Habit deletion first affected one week, then every week, then only future weeks — until inheritance resurrected it again. The fix required identity, history, and tombstones to agree."
tags:
  - omniplanner
  - habits
  - data-modeling
  - local-first
  - migration
  - debugging
commits:
  - hash: "829b26dca9c86656d30ede67647ab0d3aa3fd0d7"
    title: "Fix habit deletion to propagate across all weeks"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/829b26dca9c86656d30ede67647ab0d3aa3fd0d7"
  - hash: "d22cc7ef1a207e7b9613dcca5ffb12ef999ddcca"
    title: "Fix habits and add per-tab zoom, configurable goals, and email retrieval"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/d22cc7ef1a207e7b9613dcca5ffb12ef999ddcca"
  - hash: "d928569197e77837ead91251341b0d3b83c816e2"
    title: "Add forward-only habit deletion and cross-week streaks"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/d928569197e77837ead91251341b0d3b83c816e2"
  - hash: "b3557b6f5ea93f4f46697e70350406733f591dcc"
    title: "Fix habit propagation, streak calculation, and workspace clearing"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/b3557b6f5ea93f4f46697e70350406733f591dcc"
  - hash: "9c36c59d513b67f4ade6637067cd8e23cd135857"
    title: "Replace milestones with a five-year streak chart"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/9c36c59d513b67f4ade6637067cd8e23cd135857"
  - hash: "d21c70b37cd54ff81261ed9dacb0f057b5cb29df"
    title: "Prevent deleted habits from leaking into new weeks"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/d21c70b37cd54ff81261ed9dacb0f057b5cb29df"
---

Deleting a habit from one week did not delete it from the next.

That was not a simple missing loop. It was the consequence of OmniPlanner's central architectural choice.

Every `WeekData` object stored its own `habits` array. When a new week was opened, `getOrCreateWeek` searched backward through as many as 520 weeks, collected active habits by ID, copied them into the new week, and reset their completions.

This preserved weekly history. Monday's checkmarks belonged to Monday's week. It also meant that one conceptual habit existed as a family of records distributed across time.

From March 11 through March 13, deletion moved through four definitions:

1. mark only the current week's copy;
2. mark every stored copy;
3. mark the current and future copies while preserving the past;
4. preserve that forward deletion when old copies are later used to construct a new week.

Each version fixed the failure directly in front of it. Each exposed a domain rule the previous version had not represented.

This article is reconstructed from those commits. There is no continuous exported conversation for the sequence, but the diffs preserve the argument in code.

<div class="section-label">One ID, many records</div>

Habit copies retained the same ID across weeks.

That was the right starting point. It allowed completions from separate week records to be recognized as belonging to the same behavior. It also made deduplication possible when a future week inherited habits from several earlier weeks.

But identity alone did not provide lifecycle.

The original delete action found the habit in the visible week and added `deletedAt` to that copy. If the user had already opened a future week, its cached copy remained unmarked. Navigating there made the deleted habit reappear.

The first fix moved deletion into `App.tsx` where the full `allWeeks` store was available. It iterated every stored week and marked every matching ID with the same deletion timestamp.

The resurrection stopped.

History disappeared with it.

Although the confirmation text said “this week and all future weeks,” the first implementation did not compare week keys. It marked past copies too. Looking backward no longer showed the habit as it had existed then.

For a task list, global removal can be a reasonable default. For a historical habit tracker, it rewrites the record.

<div class="section-label">Deletion is a boundary in time</div>

Two days later, the delete operation learned where the user was standing.

OmniPlanner's week storage keys included an ISO start date. Because the date component was ordered `YYYY-MM-DD`, the code could compare a stored week key with the current week key and skip every earlier week.

Deletion now meant:

- past weeks retain the habit and its checkmarks;
- the visible week receives the deletion;
- already-created future weeks receive the same deletion;
- later weeks should not inherit the habit.

That is a much more precise model than “remove habit.” It is an effective-date operation.

The habit had a creation time, a stable ID, per-week completions, and a deletion time. A week before creation should not display it. A week after deletion should not display it. A week inside that interval should preserve what happened.

The interface did not need to explain temporal databases. It did need the result to behave like one.

<div class="section-label">The filter hid a habit that had just been added</div>

Between the two deletion fixes, habit creation failed for a different reason.

The weekly view called a lifecycle filter that parsed `weekStartDate`, calculated a seven-day boundary, and compared that range with millisecond creation and deletion timestamps. The combination was sensitive to how a date-only string became a local `Date` and to which week the user was viewing.

A newly added habit could be present in the current week's stored array and absent from the rendered active list.

The immediate fix made the visible weekly row use the truth closest to its scope: habits already stored in `currentWeek`, excluding only records explicitly deleted or archived. The more elaborate cross-week lifecycle logic remained in the week manager where inheritance happened.

This reduced duplicated interpretation. Once a `WeekData` record had been constructed for a date, the view did not need to decide again whether its contents belonged there.

<div class="section-label">Future weeks can already exist</div>

Forward deletion solved only half of propagation.

The user could navigate ahead before creating a new habit. That future week would be cached without it. Adding the habit to the current week did not modify the already-created future record, so the habit vanished when moving forward.

`addHabitGlobally` mirrored forward deletion. It added the new habit to the current week and every existing future week, keeping completions only in the current copy.

That covered cached weeks at write time. It did not cover every ordering of operations, imported data, or older caches.

The week reader therefore gained reconciliation. When an existing week was opened, it scanned earlier weeks for habit IDs missing from the cache and injected active copies with empty completions.

This was a useful local-first pattern: repair derived duplication at the boundary where it is read. The canonical information was spread across user-owned historical records, so a cached future projection could be healed without a server migration.

It also reopened the deletion bug.

<div class="section-label">The past resurrected the future</div>

Consider a habit that existed in January and was deleted in March.

The January copy correctly had no `deletedAt`; it needed to remain visible in January. A new April week looked backward, found that active-looking January record, and copied it forward. The March tombstone existed in another weekly copy, but the inheritance loop had not seen it yet — or discarded it because it was looking only for a non-deleted source.

Past preservation had become a resurrection source.

The final fix in this sequence first built a set of every habit ID marked deleted in any stored copy. Both paths — reconciling an existing week and constructing a new one — consulted that set before inheriting an older record.

The older copy remained historically visible in its own week. It simply lost the authority to create a new future copy.

That distinction is the heart of the design:

> A historical record can be true about the past without being an instruction for the future.

The code did not yet have a separate canonical habit registry and event log. It derived a tombstone set from distributed week records. Within the architecture that existed, that was enough to stop deletion leakage without erasing history.

<div class="section-label">A streak also needs one identity</div>

Once habit IDs survived across weeks, streak calculation could move beyond the visible seven days.

The new calculation visited every week, found the matching habit ID, and collected completed date keys into a set. Duplicate copies could not double-count one date. Sorting those dates produced total completed days and the longest consecutive run.

The first version anchored the current streak to today, or yesterday if today was not complete. That made a historical week display a number judged from the wall clock rather than from the page being viewed.

An hour later, the calculation accepted the viewed week's end date. The metric now traveled with the planner's temporal perspective.

This was the same rule learned by deletion: the current screen's week is not decorative context. It changes the meaning of the operation.

<div class="section-label">From fifteen milestones to 1,825 days</div>

The streak UI immediately grew a reward layer.

It began with 15 thresholds, from three days through 1,500, each selecting a message, color, and occasional animation. Later the same day, that table expanded into a five-year chart ending at day 1,825, with more than one hundred named thresholds and a deterministic pool of filler titles between them.

The tone moved from encouragement into amused obsolescence. Early days celebrated momentum. Later years asked whether the tracker had outlived its purpose. At day 1,825, the tracker declared itself out of commission.

The joke carried a product position: the goal of a habit tracker is not eternal dependence on the tracker. A behavior can eventually become ordinary enough to retire.

The milestone system would have been meaningless if one habit's completions were still fragmented into unrelated weekly counts. Gamification sat on top of the identity repair, not in place of it.

<div class="section-label">The data surface kept growing</div>

This period added more local-storage keys for per-tab zoom, goal base years, email accounts, and AI settings. The old **Nuke Workspace** action still removed only the original three keys.

One fix enumerated all seven known keys. The next replaced that list with a prefix rule: remove every key beginning with `omni_`.

It was the same maintainability lesson at a different scale. A destructive operation that promises “all” should not silently preserve whatever features were added after its hardcoded list.

Weekly goals received a migration for a similar reason. They changed from plain strings to todo-shaped objects so checked state could persist. Existing local storage and backups were normalized on read instead of being abandoned.

Local-first software cannot treat schema evolution as a deployment detail. The database is already on the user's machine, in every version the app has ever written.

<div class="section-label">What deletion finally meant</div>

By the end of March 13, a habit was no longer merely an object inside the visible week.

It was a stable identity projected across week records, with historical completions, an effective deletion boundary, a derived global tombstone, and a streak assembled from dates across those projections.

The implementation arrived through reversals:

- local deletion was too narrow;
- global deletion was too broad;
- forward deletion preserved history but missed future caches;
- reconciliation healed caches but revived deleted identities;
- the tombstone set separated historical truth from future inheritance.

This is why the bug took more than one fix. The button said **Delete**, but the real question was temporal:

> From which week onward should this habit stop existing, and which older records must remain evidence that it once did?

Once OmniPlanner could answer that, the past stopped changing and the future stopped resurrecting it.
