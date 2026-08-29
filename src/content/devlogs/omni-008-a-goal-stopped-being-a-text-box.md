---
number: "008"
title: "A Goal Stopped Being a Text Box"
subtitle: "Life goals became identities that weekly work could point to."
slug: "omni-008-a-goal-stopped-being-a-text-box"
project: "OmniPlanner"
date: 2026-03-18
status: "published"
summary: "OmniPlanner replaced long-range goal text blobs with migrated GoalItem records, then linked weekly work in one direction through Todo.parentGoalId so progress could be derived without duplicated state."
tags:
  - omniplanner
  - goals
  - domain-modeling
  - migrations
  - local-first
  - architecture
commits:
  - hash: "2485faf61a8868168daac889a7ba764e7beefd46"
    title: "Add product docs, storage abstraction, and migration scaffolding"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/2485faf61a8868168daac889a7ba764e7beefd46"
  - hash: "62577c804e4eeedb8a51fa1eae810206bd07391f"
    title: "Add GoalItem domain model and migrate life goals"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/62577c804e4eeedb8a51fa1eae810206bd07391f"
  - hash: "46a547e716727a9b201e8b1b0dfbb903832a84bb"
    title: "Fix white screen with a null-safe migration"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/46a547e716727a9b201e8b1b0dfbb903832a84bb"
  - hash: "3e79bbe6f6a1401deff3513f4e57014b2d967708"
    title: "Link weekly todos to life goals"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/3e79bbe6f6a1401deff3513f4e57014b2d967708"
---

OmniPlanner had ten-year goals before it had a goal domain.

The Goals view stored long-range intention as nested text. A year key pointed to a string, or in the five-year section to an object containing a goal and an action note. Monthly entries used month abbreviations. Checked state, lifecycle, parent relationships, and stable identity did not exist.

The screen could hold aspirations. The weekly planner could not reliably point back to them.

On March 18, the project paused visible feature work long enough to define what a goal was, how stored data could evolve, and which direction the relationship between life goals and weekly execution should run.

The first migration crashed on a real null value and produced a white window. The correction landed 36 minutes later. One hour after that, weekly work could link to long-range goals without copying progress into both sides.

This sequence is reconstructed from repository history. The commits call the linking work “Phase 3,” while the first product roadmap used that label for cross-platform shell work. The implementation sequence had already outrun the document's initial numbering. The domain decisions are clearer than the labels, so this entry follows what shipped.

<div class="section-label">Write the non-negotiables before the adapter</div>

The productization pass began with three documents: a product roadmap, a v3 architecture, and a security model.

The roadmap named the product philosophy directly: privacy-first, calm, local-first, open source, and free at the core. AI remained optional and user-controlled. Basic planning could not depend on a server. Existing user data could not be broken without a migration.

Its most practical non-negotiable was already overdue:

> No secrets in localStorage long-term.

The previous entries had shown why. AI keys and IMAP passwords had been made functional before the secure credential boundary existed. The roadmap did not pretend otherwise; it recorded the current vulnerability and made migration part of the architecture.

The contribution rules were equally concrete: types before UI, migrations for format changes, storage through an adapter, optional AI, and a manual verification path for each change.

Those rules turned the phase plan from a feature list into constraints on how new features were allowed to arrive.

<div class="section-label">One registry for every local key</div>

The first implementation phase intentionally changed nothing visible.

A `StorageAdapter` defined get, set, remove, keys, and clear operations. `LocalStorageAdapter` implemented it. Every `omni_*` key moved into one registry instead of being repeated across `App.tsx`, settings, the week manager, and backup utilities.

This was not abstraction for the sake of replacing a short API with a longer one. It created one seam where IndexedDB, file storage, tests, schema inspection, and platform-specific persistence could later enter.

The ad hoc weekly-goal conversion also moved into a numbered migration registry. `omni_schema_version` recorded progress. Each migration was required to be idempotent and persisted its version only after running.

The application called the runner before React mounted.

That ordering protected components from seeing mixed schemas. It also meant a migration exception could prevent the entire interface from appearing — a failure the very next phase demonstrated.

<div class="section-label">A goal acquired identity and lifecycle</div>

`GoalItem` replaced the old text blobs as the working model.

Each goal received:

- a stable string ID;
- a timeframe from ten-year through weekly;
- active, completed, or archived status;
- order, notes, target date, and timestamps;
- optional parent and execution-link fields.

Pure domain functions handled creation, editing, completion, archival, restoration, year selection, and the goals relevant to the current planner view.

The Goals screen was rewritten around those records. It kept the five long-range tabs and year navigation, but each entry now had a lifecycle rather than existing only as text at a coordinate in a form.

The weekly sidebar surfaced active one-year goals and monthly goals matching the current month. Long-range intention entered the execution screen before explicit linking existed.

<div class="section-label">Migration v2 preserved the old language</div>

The old structures could not simply be discarded.

Migration v2 walked each legacy section and created `GoalItem` records:

- ten-year year entries became ten-year items;
- five-year `goal` text became the item and `action` became notes;
- three-year period keys became ordered items;
- monthly strings became monthly goals with target dates in the current year.

The legacy `omni_lifegoals` data remained in storage for backward import compatibility. The new items used a separate key. Backups moved to version 3.0 and included the structured records. Importing an older backup reset the schema version so the goal migration could run again against the restored text.

This was a deliberate asymmetry: migrate forward for use, retain enough old representation to accept data the app itself had previously exported.

<div class="section-label">`typeof null` made the app disappear</div>

The five-year legacy shape was expected to contain objects with `goal` and `action` fields.

Some stored entries were `null`.

JavaScript reports `typeof null === 'object'`, so the migration's object guard passed and the next property access threw. Because migrations ran before React rendered, the exception prevented the root component from mounting. The desktop window opened blank.

The fix added the missing truthiness check before reading the object. More importantly, the migration runner at startup was wrapped in a `try/catch`. A failed migration now logged the error and allowed the app to start with its current storage state instead of converting one malformed record into a completely unusable planner.

That fallback involved a trade-off. Continuing after migration failure can expose components to older data. Refusing to mount can lock a user out of every other feature. For a local-first app with backup tools inside the same UI, remaining accessible was the safer recovery posture.

The same repair added the favicon file expected by the Electron window configuration. A missing window resource and a thrown migration had both been plausible causes of a silent white launch; both were removed.

<div class="section-label">Store the relationship once</div>

The next commit connected goals to weekly execution.

A weekly business or personal todo gained an optional `parentGoalId`. The planner displayed a link control beside an unlinked item and a goal pill beside a linked one. The picker grouped active goals by timeframe. Removing the pill removed the relationship.

The crucial choice was where not to write.

`GoalItem` had briefly included `linkedWeeklyGoalIds`, suggesting a bidirectional relationship. The implementation deprecated that field and never populated it. `Todo.parentGoalId` became the sole persisted link.

Goal progress was derived at read time by scanning business and personal todos across all stored weeks:

- how many point to this goal;
- how many of those are complete;
- whether at least one exists and all are complete.

The Goals view rendered the resulting `completed/linked` badge. It did not automatically mark the life goal complete.

This avoided three synchronization failures:

- linking a todo did not require updating a second list on the goal;
- deleting or restoring weekly data could not leave a stale reverse link;
- completing every current todo did not silently decide that a multi-year goal was finished.

The weekly work held the reference. The goal view calculated evidence from that work. Human intent still owned the goal's lifecycle.

<div class="section-label">Planning acquired a vertical line</div>

Before March 18, goals and weeks were neighboring features. Afterward, they formed a direction:

> life goal → weekly commitment → completed evidence

The storage adapter and migrations made that line safe to introduce into existing local data. `GoalItem` gave its first node an identity. `Todo.parentGoalId` connected execution without duplicating truth. Derived progress brought the result back to the goals screen.

The white-screen regression was part of that work, not an unrelated embarrassment. It showed that local data migration was now on the application's critical startup path and needed the same defensive treatment as rendering or network code.

OmniPlanner had always called itself an “Executive Life OS.” March 18 was when one piece of that name stopped being visual language. A long-term goal was no longer a text box the weekly planner could only display. It was a domain object that weekly work could reference, measure against, and still leave under the user's control.
