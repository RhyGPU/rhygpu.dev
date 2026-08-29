---
number: "012"
title: "Nothing Writes Until Confirm"
subtitle: "First-run trust came from honest empty states, gates, and previews."
slug: "omni-012-nothing-writes-until-confirm"
project: "OmniPlanner"
date: 2026-03-23
status: "published"
summary: "OmniPlanner taught a blank workspace how to explain itself, disabled actions that could not run, and added read-only previews before backup restore or email-to-calendar writes."
tags:
  - omniplanner
  - onboarding
  - ux
  - backup
  - email
  - trust
commits:
  - hash: "a4156aec7a48455a3bb044a3fa5c4eacad51a7e7"
    title: "Add onboarding clarity and first-run trust"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/a4156aec7a48455a3bb044a3fa5c4eacad51a7e7"
  - hash: "c3046f9102f76a9c7cf6a3283bc1c95cce7ea7df"
    title: "Add empty-state guidance across planner views"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/c3046f9102f76a9c7cf6a3283bc1c95cce7ea7df"
  - hash: "c4e85257133c5428ce7b0831a93b561bbd2c1099"
    title: "Add AI readiness gating and settings clarity"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/c4e85257133c5428ce7b0831a93b561bbd2c1099"
  - hash: "747efd8bb4c8f303daddca5254b82162025a0562"
    title: "Add backup preview and two-step restore"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/747efd8bb4c8f303daddca5254b82162025a0562"
  - hash: "5a44949af84d46d5044750bf35265b2aa39487bb"
    title: "Polish the email-to-calendar confirmation flow"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/5a44949af84d46d5044750bf35265b2aa39487bb"
---

A blank planner can look broken.

By late March, OmniPlanner had goals, week isolation, calendar intelligence, backups, reminders, AI providers, email, and three platform shells. A new installation showed almost none of that context. It opened into an empty planning surface and expected the user to infer where data lived, which view to visit first, and why some integrations did nothing.

Phases 14–18 changed the product without changing its core model. The app learned to explain emptiness, expose capability before action, preview destructive imports, and require confirmation before converting an email into stored time.

This entry is reconstructed from five commits across March 23 and 24. Their shared principle was not “add more guidance.” It was more specific:

> Show the user what is true before asking them to change state.

<div class="section-label">First run was not the same as no data</div>

The welcome card did not appear merely because the current week was empty.

OmniPlanner already generated blank weekly scaffolds. A restored user might open a new week with no tasks while still owning years of goals and history. Treating either case as a new user would turn onboarding into recurring interruption.

`hasPlannerData` conservatively searched for meaningful content: non-empty goals, todos, events, focus text, or active habits. The card appeared only when no meaningful data existed and the device-local dismissed flag had not been set.

That flag deliberately remained outside backup data. Restoring a backup did not reset the current device's onboarding choice. Moving to a genuinely fresh device showed the explanation again.

The card kept the sidebar visible and offered one dismissal action. It stated the storage model directly: data lives on this device; there is no account, server sync, or tracking. Platform-specific copy explained desktop, mobile, or browser behavior. Suggested first steps pointed toward goals, the weekly planner, and settings without forcing a tour.

It also did not request notification permission. Reminders remained opt-in inside settings. Onboarding was orientation, not a pretext for acquiring capabilities.

<div class="section-label">Empty space became a question</div>

After dismissal, individual views still contained silent blank panels.

Phase 15 added one-line prompts at the point where an action belonged. The weekly business list asked what should advance professionally. The personal list asked what should be protected. Each goal timeframe received a short question appropriate to its horizon.

The monthly goal grid showed guidance only in the current empty month. Filling all twelve empty cells with instructions would have created more noise than clarity.

These were not generated examples or default data. OmniPlanner did not seed fake goals that a user might mistake for their own. It described the purpose of the empty container and left ownership blank.

<div class="section-label">Unavailable stopped looking clickable</div>

**AI Optimize Week** had always appeared active.

With no provider or key, clicking it wrote a configuration message into a focus field. The feedback arrived after the action and in a location meant for planner data.

The readiness service introduced three states: ready, missing key, or disabled. Keyless custom local models counted as ready. Network failure remained a runtime error rather than being confused with configuration readiness.

When AI could not run, the button lost its click handler, changed visual state, and displayed a small route to Settings & Data. The settings panel showed the same status live while the provider form changed, including whether the displayed state came from unsaved edits.

Phase 18 applied the same gate to **Add to Calendar** in the inbox.

The rule was simple: a button should not advertise an operation the current configuration cannot attempt.

<div class="section-label">Restore became read-only first</div>

Backup restore already validated before writing, but selecting a file still led directly into the import flow.

Phase 17 separated preview from mutation.

`previewBackupFile` parsed and validated without touching storage. The Data view displayed:

- backup version and export date;
- week, goal, and email counts;
- legacy-format status;
- non-fatal warnings.

Only **Confirm Restore** called the existing write path. Canceling discarded the preview.

The same screen stopped using vague language around export. It listed what a backup contained — planner data, goals, and emails — and what it excluded — API keys, email passwords, and notification preferences.

This mattered because “backup” often implies a complete clone. OmniPlanner's security model intentionally excluded credentials. The interface now told the user before restore, not after discovering that an account needed to be configured again.

The old footer claim **Real-Time Sync — Month & Week Unified** was replaced with **Local-Only Storage — No server, no account** and a credential-exclusion note. Internal views sharing one state object was no longer described with language that suggested cloud synchronization.

<div class="section-label">Email extraction became a draft</div>

The first email-to-calendar path called AI and immediately appended the returned event after an alert.

Phase 18 inserted an explicit preview.

The extracted title, date, time, and duration appeared inside the inbox. Nothing entered `allWeeks` until the user selected **Confirm**. **Cancel** removed the draft.

This was necessary because AI extraction is interpretive. A message can contain several dates, quoted history, a deadline rather than a meeting, or a timezone the model misunderstands. A syntactically valid event is not automatically the user's intended plan.

The preview did not yet provide a full editor for every event field. It established the ownership boundary first: AI proposes; the user commits.

The inbox also replaced alert-driven capability failures with inline states. Web and mobile explained that IMAP required the desktop shell. A missing account, an empty inbox, and an unavailable platform no longer shared one blank result. Partial account-fetch failures appeared as amber warnings instead of disappearing into the developer console.

The placeholder recipient `you@omniplan.ai` was removed. When account provenance existed, the interface displayed the real address. Otherwise it showed nothing rather than inventing identity.

<div class="section-label">Trust was implemented as timing</div>

These phases did not introduce a new database or platform.

They changed when information appeared relative to an action:

- storage truth appeared before onboarding dismissal;
- a contextual question appeared before the first item;
- AI readiness appeared before the button could run;
- backup contents appeared before restore could write;
- extracted event details appeared before the calendar changed;
- platform limits appeared before an email operation failed.

That sequence is the product work.

Local-first software asks users to trust a device-local state they cannot inspect as easily as a cloud account page. AI-assisted software asks them to trust an interpretation. Restore asks them to replace the current workspace. Each boundary benefits from the same pattern: reveal, preview, confirm.

OmniPlanner's empty screen did not need more decoration. It needed to say what it was, what could happen next, and which actions would remain entirely under the user's control.
