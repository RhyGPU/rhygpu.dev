---
number: "013"
title: "The First Release Gate Had 138 Tests"
subtitle: "Typecheck came first; then the boundaries around user state received evidence."
slug: "omni-013-the-first-release-gate-had-138-tests"
project: "OmniPlanner"
date: 2026-03-24
status: "published"
summary: "OmniPlanner normalized IDs through a migration, extracted its calendar editor, enforced TypeScript, added 138 focused tests, and replaced ambiguous email failures with stable codes and operation IDs."
tags:
  - omniplanner
  - testing
  - typescript
  - migrations
  - email
  - release
commits:
  - hash: "326dcf0681f6aa59c10c16ceed08e47b5ac3eaa2"
    title: "Enforce typecheck, normalize IDs, and extract the event editor"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/326dcf0681f6aa59c10c16ceed08e47b5ac3eaa2"
  - hash: "24634e4ff21eb5ac3051d381d6f5610782a26242"
    title: "Make reminder state visible in the planner"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/24634e4ff21eb5ac3051d381d6f5610782a26242"
  - hash: "451faea759eaa20bee75c9e226f2ae280bc2071c"
    title: "Add 138 tests and a release checklist"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/451faea759eaa20bee75c9e226f2ae280bc2071c"
  - hash: "6ea2c38dbd41221758a8014305407828e7044aa7"
    title: "Add email error taxonomy and operation diagnostics"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/6ea2c38dbd41221758a8014305407828e7044aa7"
---

OmniPlanner's first session had no test command.

The production build was the nearest available check, and the first cleanup shipped an unterminated JSX tree before that build was run.

Six weeks later, the project had an explicit zero-error TypeScript gate, a versioned ID migration, a release checklist, and 138 automated tests across seven files. A week after that, email failures stopped being arbitrary strings and became stable codes with traceable operation IDs.

The hardening did not attempt to test everything at once. It began with the pure functions and state boundaries most likely to corrupt local data or misrepresent whether an action was safe.

This entry reconstructs Phases 19–22 through April 3. The old summary placed OAuth in this same range, but repository history puts the OAuth foundation on April 6 and token lifecycle on April 8. Those belong to the next entry.

<div class="section-label">A union type had spread into identity</div>

Todos and calendar events accepted IDs as `string | number`.

Early records used timestamps as numbers. Later code used prefixed strings and `crypto.randomUUID()`. Comparisons, goal links, event links, and component keys all had to remember that `42` and `'42'` might refer to the same conceptual record while strict equality treated them as different.

Phase 19 chose one representation: string.

Migration v3 traversed every stored week and converted numeric IDs in:

- weekly business and personal goals;
- meetings;
- daily todos;
- calendar events;
- event-to-todo links.

New event creation stringified timestamps. Types and planning selectors stopped carrying the union. Backup format moved to 3.1, and modern imports recorded the new schema level.

This was not cosmetic type cleanup. Identity comparisons sit underneath scheduling coverage and goal progress. A number on one side and a string on the other could make a real link appear absent.

<div class="section-label">TypeScript became a separate gate</div>

`npm run typecheck` was added as `tsc --noEmit`.

The first clean run required several small corrections: textarea style props, explicit `Object.entries` shapes, and careful casts at migration boundaries where legacy data intentionally violated current types.

Running Vite was no longer expected to stand in for full static checking. The release process could fail on a type error without producing artifacts first.

The same phase extracted the calendar event modal from the already oversized weekly planner. Its state changed from `any` to a named `EventEditorState`. Event-kind metadata moved with the component; planner-specific color behavior stayed in the planner.

The AI provider interface also gained a generic completion operation. Email event extraction stopped misusing “predict daily focus” as a transport for unrelated prompts. Every provider implemented the operation it was actually being asked to perform.

Hardening here meant reducing accidental flexibility: one ID type, one editor state shape, one completion capability, one typecheck command.

<div class="section-label">Reminder configuration became visible where time was edited</div>

Reminder settings already existed in the Data view. Phase 20 surfaced their effect inside planning.

Focus and task blocks showed an inline reminder toggle and minutes-before selection when the current platform could support it. Electron, which still had no notification adapter, hid the control. A disabled master switch produced an enable-notifications hint instead of saving a setting that could not run.

Calendar blocks with active reminders displayed a bell and timing label. The habit area showed its reminder status too.

Pure `reminderStatus` helpers defined formatting, active-state predicates, and labels. That separation made the feature's visible truth testable without scheduling an operating-system notification.

<div class="section-label">The first 138 tests targeted invariants</div>

Phase 21 installed Vitest with a jsdom environment and added seven suites:

- 27 reminder-status tests;
- 28 backup-validator tests;
- 19 onboarding-data detection tests;
- 25 planning-intelligence tests;
- 12 AI-readiness tests;
- 10 migration tests;
- 17 calendar-editor tests.

The selection followed the recent failure history.

Backup tests rejected primitives and malformed collections while accepting modern and legacy shapes. Onboarding tests distinguished an empty scaffold from meaningful planner data. Planning tests checked unscheduled work, goal support, coverage, and scheduled minutes. Readiness tests preserved the keyless local-model path. Migration tests verified version gating, old weekly goal conversion, string ID normalization, and idempotence.

The calendar editor tests exercised conditional UI: event kind, platform, notification master state, missing props, and whether **Delete** appeared only for an existing event.

These tests did not prove that Electron launched, IMAP authenticated, IndexedDB survived quota pressure, native reminders fired, or a packaged mobile app rendered correctly. They concentrated on deterministic rules and one component boundary.

That was an appropriate first layer, provided the scope remained explicit.

<div class="section-label">The release checklist named what tests could not</div>

`RELEASE_CHECKLIST.md` added ten sections beyond `vitest run`.

It covered migrations, backup and restore, reminder behavior, AI gating, onboarding, platform smoke tests, regression surfaces, pre-merge rules, and version bumps.

The checklist did not convert manual verification into automation. It prevented automated confidence from silently replacing platform work the suite did not perform.

This was the first coherent release gate:

> typecheck + automated invariants + manual platform matrix

Earlier commits often mentioned a successful Vite build. Phase 21 defined what confidence required beyond compilation.

<div class="section-label">Email failure stopped being one string</div>

On April 3, Phase 22 added 27 stable email error codes.

Connection, authentication, mailbox, body loading, AI extraction, parsing, and other failure classes received identifiers separate from user-facing messages. Retryability became a function of the code rather than a guess based on text.

Every IMAP operation received an operation ID. Main-process logs recorded phases such as start, connected, mailbox opened, and failed. Service responses returned the code and operation ID to the UI.

That made two audiences possible:

- the user received calm, actionable copy;
- a diagnostic report retained a stable code and correlation ID.

AI email extraction changed semantics too. It returned `null` only when no event genuinely existed. Provider failure, invalid JSON, or missing required fields threw a typed `EmailError` instead of being swallowed into the same empty result.

This distinction prevented the interface from telling the user “there was no event” when the actual problem was “the model response could not be parsed.”

Per-account connection errors moved inline. Body-load failures appeared in the message view rather than leaving an indefinite loading placeholder.

<div class="section-label">Confidence became layered</div>

By April 3, OmniPlanner had four different forms of evidence:

- TypeScript proved current source shapes were internally consistent;
- migrations transformed older stored shapes into those current shapes;
- tests verified pure rules and conditional component behavior;
- operation IDs made external failures traceable after the fact.

None could replace the others.

A typecheck cannot prove a migration preserves real user data. A unit test cannot prove Windows focus behavior. A successful IMAP connection cannot prove an error message is classified correctly. A checklist cannot catch a regression automatically.

The project moved from “the build passed” to a release model where each layer had a named responsibility and an admitted limit.

The number 138 was not proof that OmniPlanner was finished. It was proof that the core rules finally had somewhere to fail before the user's local workspace became the test environment.
