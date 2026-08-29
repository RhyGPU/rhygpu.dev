---
number: "000"
title: "Before OmniPlanner Had a Repository"
subtitle: "The first feature request was a code audit."
slug: "omni-000-before-omniplanner-had-a-repository"
project: "OmniPlanner"
date: 2026-02-10
status: "published"
summary: "OmniPlanner began as one sentence joining personal planning, iCalendar, todos, self-improvement goals, and email — followed immediately by a request to inspect what was already broken."
tags:
  - omniplanner
  - origin
  - planning
  - local-first
  - refactoring
  - debugging
commits: []
---

OmniPlanner existed before its repository.

Fifteen days before the first commit, it lived in a folder called `Desktop\Planner` under the less memorable working name `omniplan-ai---executive-life-os`.

The first surviving description was not a pitch deck or a roadmap. It was one unfinished sentence:

> A personal planner merged with iCalendar, a personal todo calendar, self goals and improvement, and email.

The grammar was rough. The product boundary was already there.

The goal was not another task list. It was one place where long-term intention, weekly execution, calendar time, recurring behavior, and incoming obligations could meet.

<div class="section-label">The first request was not a feature</div>

The obvious next question was which part to build first: calendar import, email sync, goals and habits, weekly recurrence, or local-first storage.

I chose none of them.

> First, look at my code. Check what I have, what is imperfect or redundant, and what can be modularized. Start there.

That decision established a pattern OmniPlanner would repeat for months. The app grew quickly, but the useful work often began by finding where the visible interface and the stored behavior had drifted apart.

The first audit found several examples immediately.

<div class="section-label">A streak that could only be perfect</div>

The habit completion percentage divided `totalDays` by `totalDays`.

Any non-empty habit therefore reported one hundred percent. It was a mathematically valid expression with no useful relationship to the user's behavior.

The active-habit filter had a different problem. It accepted a week start date and then ignored it, returning every habit that was not currently deleted. A habit created after the week could appear in the past. A habit deleted before that week could remain present.

The compiled `dist` output contained better lifecycle logic than the source. That was not reassurance; it meant the editable source and the running artifact disagreed.

This was the first version of a problem that would later become central to the app:

> A week is not just a date range. It is a historical state that must not be rewritten by the present.

Habits, events, and goals needed creation, deletion, and recurrence semantics that respected the week being viewed.

<div class="section-label">Two backups that could not restore each other</div>

Backup and restore existed twice.

One path exported a version and date with all planner data nested under `data`. Another exported a timestamp with weeks, email, and life goals at the top level. Their importers expected their own shapes. A backup created from one surface could fail when restored through the other.

The types had drifted too. One helper described email as an array of strings while the application used structured email objects.

Delete behavior was duplicated across the app component, the data screen, and a utility. One UI path called `localStorage.clear()` directly while another wrapped a central helper.

For a local-first planner, this was not a secondary refactor. Export and restore were the user's ownership boundary. If the app could write two incompatible versions of the truth, “your data stays local” was not yet a trustworthy promise.

The fix created one backup path, normalized old and new formats on import, refreshed application state after restore, and removed the competing implementations.

<div class="section-label">An event that repeated because the code decided</div>

Editing an existing calendar event always set `repeating: true`.

The interface did not ask. The stored event could be one-time, but touching it converted it into a weekly recurrence.

The first patch stopped overwriting the value and preserved the event color. It fixed the silent mutation without yet giving the user a recurrence control.

That distinction mattered a few hours later.

When I used the app again, the issue was still visible from the other direction: adding a new weekly event repeated it without a choice. Preserving an existing value was not the same as designing the input that created the value.

The event editor gained an explicit **Repeat Weekly** checkbox. New events defaulted to one-time. Editing retained the stored decision.

Recurrence became user intent instead of an implementation default.

<div class="section-label">The first fix broke the build</div>

The initial cleanup touched the backup layer, week manager, weekly planner, data view, and app shell. It unified formats, corrected lifecycle filtering, changed streak calculations, and removed unused paths.

Then I asked to run the tests.

There was no test script.

The closest available gate was the production build, but it was not run during the first patch. Several hours later, Vite found an unterminated JSX tree in `DataView.tsx`.

The refactor had fixed the data model and left the app unable to compile.

The nesting error was repaired, but the episode set another early rule:

> A cleanup that is not built is still a hypothesis.

The codebase would eventually reach 138 automated tests and a clean TypeScript gate. The first session began at zero, with a build error discovered by opening the app.

<div class="section-label">The first streak fix was also wrong</div>

The original percentage was obviously broken. The first replacement used a broader habit history and looked more reasonable.

It still did not match how this version of the planner worked.

Habit completion reset with each week. The streak shown inside the weekly planner therefore needed to be calculated from that week's dates, not from an assumed continuous lifetime history.

After real use exposed the mismatch, the calculation was corrected again. Current streak, longest streak, and percentage were derived from the visible week.

This was not the final habit architecture. Cross-week streaks and deletion propagation would become recurring problems in later commits. But the first correction clarified the domain question:

> Is this number describing the habit's life, or this week's execution?

Without that answer, even a correct formula could measure the wrong thing.

<div class="section-label">The oversized week</div>

The audit also identified the structural center of the app: `WeeklyPlannerView`.

It handled responsive layout, week navigation, habit state, event creation and editing, AI actions, and most of the rendering. Storage was spread across the app component, week utilities, and data helpers. `getOrCreateWeek` could scan as far as 520 weeks to reconstruct habits and events each time it ran. Date helpers mixed local time, UTC noon, and local weekly calculations.

The suggested decomposition was straightforward: one storage boundary, one versioned backup service, smaller weekly components, and hooks for events, habits, and navigation.

That decomposition was not completed in the first session. The important part was naming the pressure before adding iCalendar and email — two systems that would make inconsistent time and persistence much harder to unwind.

<div class="section-label">What already existed</div>

The pre-repository app was rough, but it was not empty.

It already had a weekly planner, habits, events, email data, life goals, backup and restore, and an AI surface. The problem was that each feature carried its own assumptions about time, recurrence, persistence, and shape.

The first day of work did not make OmniPlanner impressive. It made the existing app more honest:

- backups shared one format and could normalize older data;
- habit visibility began respecting creation and deletion dates;
- weekly progress stopped being permanently perfect;
- event editing stopped silently enabling recurrence;
- new events gave recurrence back to the user;
- the build error caused by the cleanup was found and repaired.

There was still no repository, desktop shell, release pipeline, or formal phase plan.

There was, however, already a product thesis: planning data should belong to the user, weeks should retain their own history, and the app should never silently turn one intention into another.

Fifteen days later, that folder became a Git repository.

The problems found on February 10 became the first layer beneath everything that followed.
