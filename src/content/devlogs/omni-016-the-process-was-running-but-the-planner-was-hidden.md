---
number: "016"
title: "The Process Was Running, but the Planner Was Hidden"
subtitle: "The first fix launched Electron. The second made it behave like an app."
slug: "omni-016-the-process-was-running-but-the-planner-was-hidden"
project: "OmniPlanner"
date: 2026-05-06
status: "published"
summary: "A broken Windows launcher, an unreliable shortcut, forced elevation, stale Electron processes, and a hidden window produced a convincing false positive: every technical check passed while the planner still appeared not to launch."
tags:
  - omniplanner
  - electron
  - windows
  - launcher
  - debugging
  - refactoring
commits:
  - hash: "0534b6c5e666ee25b1082eda33fc64e8d399bdd9"
    title: "Fixed infini load time/ clean up"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/0534b6c5e666ee25b1082eda33fc64e8d399bdd9"
---

On May 6, OmniPlanner had a particularly desktop-shaped failure.

The launcher did not launch. The shortcut could not be trusted. After the first round of fixes, Electron processes existed and every automated check passed — but the calendar still did not appear to open.

The user's correction was more useful than the process list:

> It still doesn't run the app itself. It's a calendar/planner app. More like it takes forever to launch.

The distinction changed the investigation. Starting an Electron process was not the same as presenting a usable application window.

This entry is backed by two recovered direct conversations from working copies under `Downloads`. The first repaired the Windows launch path and then followed the false positive into Electron itself. The second, 23 minutes later, performed the requested behavior-preserving cleanup. Both landed together in one commit.

<div class="section-label">The launcher had several independent failures</div>

There was no single launch bug.

`run.js` used CommonJS `require()` calls inside a package declared as `"type": "module"`. Running the file directly therefore failed before it could launch Electron.

Windows added another trap. PowerShell selected `npm.ps1`, which the local execution policy blocked. A launcher meant for double-click use could not depend on whichever npm shim a shell happened to resolve.

The desktop package also forced an administrator relaunch on every start. That logic had been introduced as a network workaround, but the planner did not require elevated privileges. It inserted a UAC transition into ordinary startup, closed the original process, and made failures harder to follow.

The shortcut creator had its own path assumptions. A Windows Desktop may live under the profile directory, OneDrive, or a shell-resolved location. In the verification environment, the shell API even returned an empty Desktop path. The generated `.lnk` also passed through a sandbox alias instead of the real checkout path.

The first repair addressed each boundary:

- convert `run.js` to an actual ES module;
- invoke `npm.cmd` explicitly on Windows;
- remove forced administrator elevation;
- make packaged builds run as the current user;
- search normal and OneDrive Desktop locations;
- target `cmd.exe` with the real `run.bat` path as an argument;
- add root wrappers for the repository's nested app directory;
- replace the mistyped root `README.mdI` with `README.md`.

TypeScript passed. The production build passed. All 138 tests passed. The shortcut was created under the OneDrive Desktop and pointed to the intended launcher.

`node run.js` also left Electron processes running.

That last result looked like success. It was not yet proof that the planner was visible.

<div class="section-label">A process list produced the wrong conclusion</div>

The first response declared the launch fixed because Electron stayed alive.

The user tried the actual product and reported that it still did not open. For a moment, the window appeared late enough to prompt “never mind, it worked.” A second attempt clarified the real behavior: startup felt effectively infinite, and repeated attempts left more Electron processes behind.

This was the useful failure in the session. The acceptance test moved from “does a process exist?” to “does the planner window paint, become visible, and respond like one desktop app?”

Foreground diagnostics showed multiple Electron processes with blank window titles. The launcher hid their output, so a stalled or invisible renderer looked exactly like a successful detached launch.

The main process was changed to request Electron's single-instance lock. A second launch now restores, shows, and focuses the existing window instead of creating another pile. The window begins hidden only until `ready-to-show`, then receives explicit `show()` and `focus()` calls after both readiness and renderer load.

Load failures, renderer termination, and renderer console errors gained visible diagnostics. Debug inspection finally confirmed that Electron had loaded `dist/index.html` and that the document title was `OmniPlanner`.

The most direct launcher bug was self-inflicted: the child process had been spawned with `windowsHide: true`. That option was intended to suppress a console window, but in this launch shape it could also prevent the application window from appearing normally. It was changed to `false`.

The process had been running. The product surface had been missing.

<div class="section-label">Startup state was isolated, not truly migrated</div>

Two broader Windows workarounds were added during the investigation.

Hardware acceleration was disabled to avoid a class of blank or slow Electron windows. Electron's user-data and cache paths were also moved to `LocalAppData\\OmniPlanner`, separating the app from the stale or inaccessible state involved in the failed launches.

Those changes made the test launch stay alive and paint, but they are not a complete root-cause analysis.

Disabling GPU acceleration globally trades away acceleration for predictability. Moving `userData` changes where Chromium storage and the app's encrypted credential file live. The commit did not include a migration from the former profile directory, so an existing installation could leave old browser state or credentials behind in the previous location.

The session also did not record a cold-start benchmark before and after the fix. “Infinite load time” was the observed symptom and commit title, not a measured performance claim.

For the working checkout, a clean profile was a practical recovery. For a packaged release, the same transition would need detection, migration, and a narrower decision about whether GPU acceleration was actually responsible.

<div class="section-label">Cleanup was constrained by “keep every feature”</div>

The follow-up request was not for a redesign:

> Clean up useless and repetitive stuff without getting rid of functions or features. More like a tidy up.

The working tree already contained the launch repairs, so the cleanup stayed deliberately small.

Repeated empty daily-plan literals became `createEmptyDailyPlan()`. Email-derived calendar events and ICS imports began sharing one `addEventToWeek()` path rather than maintaining two nearly identical insertion routines. Monthly view code reused the same daily-plan factory, and damaged restore-flow copy and comments were cleaned up.

This mattered beyond line count. A default daily plan contains focus text, todos, notes, and calendar events. Repeating that object in several insertion paths creates a quiet schema problem: the next field can be added in one place and omitted in another. Centralizing the factory made the empty state part of the model rather than incidental syntax.

The repository wrapper was tidied at the same time: the README typo was corrected, an empty root lockfile was removed, and the useful launch entry points remained available at both root and app-directory levels.

The consolidated commit changed 15 files, with 219 insertions and 185 deletions. It was not a broad codebase purge. It preserved the calendar, email import, weekly planning, storage, and desktop features while reducing a few high-confidence duplications around them.

<div class="section-label">The real verification path ended at the window</div>

The May 6 repair passed four different layers:

1. `npm.cmd run typecheck` validated the TypeScript surface;
2. 7 test files and 138 tests passed;
3. the Vite production build completed;
4. Electron inspection showed the built planner document loaded inside the desktop window.

Only the fourth check addressed the user's actual complaint.

The episode left a durable distinction in OmniPlanner's history: launch infrastructure is not finished when the wrapper exits cleanly, the child process exists, or a shortcut file has been written. A desktop app has launched when the intended window appears, contains the intended renderer, and a second invocation returns the user to that same surface.

On May 6, the tests were already green before that definition was met.
