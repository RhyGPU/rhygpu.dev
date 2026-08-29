---
number: "023"
title: "The Background Process Was Not a Tray"
subtitle: "The first desktop smoke test passed launch-at-login and failed everything the user could actually see."
slug: "omni-023-the-background-process-was-not-a-tray"
project: "OmniPlanner"
date: 2026-07-05
status: "published"
summary: "A direct Windows smoke test exposed an invisible tray, no usable alarm-time control, and an exit path that bypassed confirmation. The repair made those paths testable, but the surviving record does not prove that the second smoke test passed."
tags:
  - omniplanner
  - electron
  - windows
  - system-tray
  - smoke-testing
  - release-gate
  - bug-fix
commits:
  - hash: "9935aa5ab71ded5a326c40f4983afd95edbee6b7"
    title: "docs: add Phase 7 UI backlog, manual verification checklist, and focusTheme type-hole note"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/9935aa5ab71ded5a326c40f4983afd95edbee6b7"
  - hash: "bfa191cd55ae741765f2afdcd6dda0f358f6bd0"
    title: "fix: tray icon loading, quit confirmation bridge, and alarm time settings UI"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/bfa191cd55ae741765f2afdcd6dda0f358f6bd0"
---

At 10:55 on July 5, the system documentation made an unusually careful distinction.

The desktop alarm shell was “code-verified,” not “done done.” Its build passed, TypeScript was clean, and all 138 tests passed, but a packaged-app checklist still had to prove that closing the window left a visible tray icon, an alarm fired while the window was hidden, the icon restored the app, and Quit displayed a warning.

Less than an hour later, the first direct Windows test justified every word of that caveat.

The app asked whether it should launch when the computer started. That part worked. Closing the window also left an OmniPlanner process in Task Manager.

Everything after that failed from the user's point of view.

There was no icon in the taskbar notification area or its hidden-icon panel. With no icon, there was no visible way to reopen the hidden window, pause alarms, or quit. Pulse displayed reminder states but did not expose a time control that could be moved a few minutes into the future. The most important notification scenario — a toast arriving while the window was closed — could not even be attempted.

A background process was alive. That did not make it a tray application.

<div class="section-label">The first acceptance test had one pass and three blockers</div>

The 11:33 checklist was deliberately small and ordered:

1. launch the development build and answer the launch-at-login prompt;
2. close the window and find OmniPlanner in the system tray;
3. schedule a near-future reminder and receive it with the window closed;
4. reopen the app from the tray;
5. quit through the tray and see a confirmation dialog.

At 11:54, the direct report reduced the result to observable facts:

- the launch-at-login prompt appeared;
- closing the window left a process running;
- no tray icon was visible, including among hidden icons;
- no clear reminder-time setting existed in Pulse.

The process result explained why the implementation could look correct during review. Electron's close handler was hiding the window instead of terminating the application. The timer and tray code could exist, and Task Manager could confirm that the main process survived.

But a hidden window without a usable icon is a lockout, not an always-running shell. The user cannot distinguish it from a hung or orphaned process. They also cannot exercise the Open, Pause Alarms, and Quit affordances that make background residency understandable.

The test correctly stopped the release sequence. The advice at the time was not to push the local feature stack and not to begin the email OAuth phase. Building more features on top of an unverified lifecycle would only make the eventual repair harder to isolate.

That was release discipline, not pessimism. A manual gate had found a class of failure the automated suite did not represent.

<div class="section-label">The icon existed as a path, not as pixels Windows could display</div>

The original `getTrayIcon()` searched two locations for `favicon.ico` and passed the first existing path to Electron's `nativeImage.createFromPath()`.

That was concise, but it assumed that an asset reachable by an application path would also decode correctly from the packaged ASAR context. On the tested Windows run, the tray object could be created without producing a visible icon.

The 11:58 repair broadened the candidates to both ICO and PNG resources, then changed the loading boundary:

- read the asset into memory with `fs.readFileSync()`;
- create the native image from the buffer;
- reject an image when `isEmpty()` reported that decoding failed;
- resize PNG fallbacks to the 16×16 tray size;
- log the candidate path and exception when loading failed.

This addressed the packaged-resource failure more directly than adding another guessed path. It also made future failures diagnosable instead of silently returning an unusable image.

There was still a final fallback to `nativeImage.createEmpty()`. If every candidate were absent or undecodable, the application could still enter the same invisible-tray state. The new logs narrowed that risk; they did not eliminate the need to inspect the actual Windows notification area.

<div class="section-label">A displayed reminder time became an editable reminder time</div>

The alarm settings UI had rendered the Morning Planner and Habit Check-In times as formatted text. The values existed in settings, but the user had no control suitable for a two-minute smoke test.

The repair replaced both read-only labels with native time inputs. Changing one split the `HH:MM` value and wrote the hour and minute back through `updateSettings()`. The controls and their individual toggles became disabled when notifications were globally off, so the visual state matched the effective state.

The Focus Block Alert also gained a lead-time selector: at start, or 5, 10, 15, or 30 minutes before the block.

This was a small interface change with a large verification effect. Before it, the notification engine could only be argued about from code. After it, a person could deliberately schedule a near-future event, close the window, and observe whether the main process delivered anything.

The distinction between Pulse and Alarms also mattered. The original checklist called the surface Pulse, while the follow-up work increasingly described a dedicated alarm application. A feature that technically moved to a new screen was still missing if the person following the documented path could not find it. Discoverability was part of the acceptance test.

<div class="section-label">The in-app exit button had bypassed its own warning</div>

The tray's Quit item already called `confirmQuit()`. The renderer's `quit-app` IPC did not.

It set `isQuitting` and called `app.quit()` immediately, bypassing the dialog that warned that alarms and background checks would stop. Two buttons with the same user-facing meaning therefore had different safety behavior.

The repair routed the IPC event through `confirmQuit()` as well. This made the exit policy belong to the main process rather than to whichever interface happened to request it.

That centralization mattered for an alarm app. Closing the planning window was supposed to keep the service alive; choosing Exit was supposed to terminate it only after an explicit confirmation. If one renderer path could skip the warning, the lifecycle contract was only partially implemented.

<div class="section-label">Green checks described the code, not the desktop</div>

The completion report later that day listed a clean production build, 138 passing tests, zero TypeScript errors, and a clean working tree. Those were real results. They covered compilation, unit behavior, and repository state.

They did not show a Windows tray icon.

No test file changed in the 11:58 repair. The commit touched two files, adding 93 lines and removing 24. Its most important behaviors depended on Electron packaging, Windows shell presentation, and a human-visible notification path — precisely the layer outside the existing automated checks.

The report therefore retained the manual gate and explicitly called the alarm phases “code-verified” until the packaged test passed. That wording was more valuable than turning the four green checks into a release claim.

The surviving conversation also contains a useful communication failure. When the post-repair walkthrough was shared, it was initially misread as another claim that contradicted the earlier test. It was actually the response to the user's request for a fix. Once corrected, the next instruction was simple: run the smoke test again, now looking under the Alarms surface for a near-future custom alarm.

The record ends without the result of that second run.

So the honest state of v4.0 at this point was neither “still broken” nor “fully verified.” The first manual test failed. A focused commit repaired the icon-loading boundary, exposed testable time controls, and unified the quit confirmation path. The documentation preserved the remaining acceptance gate.

The repair made the test possible. It was not proof that the test passed.
