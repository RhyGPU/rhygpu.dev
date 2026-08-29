---
number: "001"
title: "The Web Planner Became a Desktop App"
subtitle: "The repository began by taking ownership of its own shell."
slug: "omni-001-the-web-planner-became-a-desktop-app"
project: "OmniPlanner"
date: 2026-02-25
status: "published"
summary: "OmniPlanner's first repository captured an already substantial weekly planner, then replaced its browser assumptions with a local Electron shell, provider-neutral AI, and reproducible desktop builds."
tags:
  - omniplanner
  - electron
  - local-first
  - desktop
  - ai
  - ci
commits:
  - hash: "d00a0efa2e391f7b55d3c37f258cea1add5b4287"
    title: "Initial repository import"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/d00a0efa2e391f7b55d3c37f258cea1add5b4287"
  - hash: "725ced45e1f4132dbec9a064ff5fde656beb3a65"
    title: "Fix upload, Electron crash, AI service, and build issues"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/725ced45e1f4132dbec9a064ff5fde656beb3a65"
  - hash: "4a7463119ee5146f7cfe78f3c63180eb47e375fb"
    title: "Convert from web app to local Electron desktop app"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/4a7463119ee5146f7cfe78f3c63180eb47e375fb"
  - hash: "daf14d39528bebef57b985d4e7ea4bb2cae1e03f"
    title: "Add multi-AI provider system with settings UI"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/daf14d39528bebef57b985d4e7ea4bb2cae1e03f"
  - hash: "0dcfd9163e5533d4bb1d6fc9f7dfb11264a2da13"
    title: "Remove dead code and optimize WeeklyPlannerView"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/0dcfd9163e5533d4bb1d6fc9f7dfb11264a2da13"
  - hash: "2ecc8d06583c05b877ff6417121096bb14a76a23"
    title: "Add desktop build workflow and fix launcher"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/2ecc8d06583c05b877ff6417121096bb14a76a23"
---

On February 25, OmniPlanner acquired a history.

The first Git commit did not contain a blank application or a minimal scaffold. It imported 33 files and more than ten thousand lines: the weekly planner, monthly and data views, goals, email, habits, events, backup utilities, a week manager, Gemini integration, an Electron main process, three launchers, and several hundred lines of architecture notes.

The repository started in the middle of the story.

The surviving direct conversation resumes before that point on February 10 and then much later. I do not have a continuous exported message log for the commits in this entry. This chapter is therefore a reconstruction from commit timestamps, diffs, and the documentation checked into the repository — not a recreation of dialogue I can no longer quote.

That distinction is useful because the commits show something the old phase summary compressed too neatly. OmniPlanner did not simply “become Electron” in one operation. Its first evening was a rapid sequence of finding browser assumptions, repairing them, replacing them, and then removing the paths that were no longer true.

<div class="section-label">The first commit was already version two</div>

The imported package still called itself version `0.0.0`, but its architecture document called the planner v2.0.

The central idea was week isolation. Each Monday-to-Sunday page owned its goals, daily plans, meetings, notes, habits, and timestamps. The monthly view aggregated those weeks instead of maintaining a competing global calendar. Local storage held the working state. Backup and restore were meant to be the path out.

This was the architectural response to the bugs found two weeks earlier. A planner could not preserve history if editing the present rewrote adjacent weeks. The initial repository did not solve every lifecycle problem, but it made the week a first-class stored object.

The imported app was also caught between identities.

Its README still described an AI Studio web app and instructed the user to start a Vite development server. Its package already included Electron and `electron-builder`. `electron-main.cjs` existed, but the browser-facing UI still reached toward Node through `window.require`. Styling and fonts arrived through remote CDNs. The launcher opened a web server. The product wanted to be local desktop software while several of its operational assumptions still belonged to a hosted browser demo.

<div class="section-label">Seven minutes of damage control</div>

The first follow-up commit landed 22 minutes after the import.

It was not a grand desktop conversion. It repaired the things that failed under ordinary use: a backup upload could crash the browser-facing view by requiring Electron directly; uploading the same file twice did not retrigger the input; invalid or empty JSON produced an unhelpful generic error; a successful import could erase existing emails when the backup omitted them.

Gemini had its own boundary failures. The code looked for one environment variable while the surrounding configuration could provide another. It targeted a preview model and failed quietly when no key was present. The patch accepted both legacy key names, moved to a stable model, and returned a useful disabled state instead of pretending that an empty key was a working integration.

The weekly planner also contained an effect that could rerun whenever its own update changed the render. Stale-habit archival was changed from repeated per-habit updates to one batched update.

The repository was only minutes old, but its first lesson was already clear: importing a working-looking interface was not the same thing as importing working boundaries.

<div class="section-label">Local meant removing the network from startup</div>

Six minutes later, the actual desktop conversion landed.

The change did more than wrap the Vite output in a window. It removed Tailwind, Google Fonts, import maps, and other presentation dependencies from remote CDNs. Tailwind, PostCSS, Autoprefixer, and Inter became build-time or bundled dependencies. `index.html` was reduced to a local shell. Vite received a relative base path so its assets could load through `file://` instead of assuming an HTTP origin.

That was the practical meaning of local-first at this stage. The user's planner data had already lived in local storage, but the application itself still depended on the network to assemble its interface. A desktop planner that cannot render its font or CSS offline is only locally stored, not locally operable.

Electron's boundary was repaired at the same time.

The quit IPC handler had accidentally been nested inside the macOS `activate` callback, so it was not registered as a normal application handler. A six-line preload script exposed only `quitApp()` through `contextBridge`. Node integration remained disabled and context isolation remained enabled. The renderer stopped calling Electron through an unguarded runtime require.

The window gained minimum dimensions, a hidden menu bar, a proper preload path, and separate development and packaged loading paths. The build declared Windows NSIS and portable targets, macOS DMG, and Linux AppImage.

This was the moment OmniPlanner became more than a website shown inside a desktop window. The application took responsibility for how it booted, what it loaded, and which operating-system capabilities the renderer was allowed to reach.

<div class="section-label">AI became a provider, not the product</div>

Five minutes after the Electron conversion, the single Gemini service was replaced by a provider interface.

Gemini, OpenAI, and Anthropic each implemented the same two planner operations: predict a daily focus and generate a schedule from todos. A dispatcher read the selected provider and key from settings. The Data tab gained controls for choosing a provider, storing a key, and disabling AI entirely. Existing environment-based Gemini configuration remained a compatibility path.

This was a surprisingly durable product decision for such an early commit.

OmniPlanner was not going to define itself as a client for one model vendor. AI was an optional service behind the planner's own actions. With no key, the planner still existed. With a different provider, the planning domain did not have to change.

The implementation was not yet secure enough for the product it would become. API keys were stored in `localStorage`; encrypted desktop credentials arrived later. But the dependency direction was right: the weekly planner called an application capability, and the capability selected its provider behind a boundary.

<div class="section-label">Delete the interface that lies</div>

Twenty-five minutes later, the new provider system made the old Gemini service dead code, so it was deleted.

The cleanup also removed the redundant shell launchers, unused metadata, unreferenced date helpers, a duplicate week update function, and an email search box that looked interactive but had no state, change handler, or filtering behavior.

That search field is the smallest change in the sequence and one of the most representative. A control that suggests a capability it does not perform makes the product less truthful. Removing it was better than preserving the appearance of completeness.

Several frequently recreated planner callbacks were memoized, but the larger optimization was conceptual: after a fast architectural replacement, the repository removed the obsolete routes instead of keeping both generations indefinitely.

<div class="section-label">The next morning, the build left the machine</div>

The old retrospective described repository creation, desktop conversion, and CI as one day. The timestamps are slightly less tidy.

The initial import through dead-code cleanup occurred between 6:19 PM and 7:18 PM Korea time on February 25. The build workflow arrived at 8:46 AM on February 26.

GitHub Actions built the desktop app on Windows, macOS, and Linux. Ordinary pushes produced downloadable artifacts; version tags assembled them into a release. The workflow did not prove the resulting apps worked on real hardware, but it made packaging reproducible outside the development machine.

The cross-platform `run.js` changed roles too. It stopped starting a Vite server. On first use it installed dependencies, built the application when `dist/index.html` was absent, launched Electron as a detached process, and let the terminal close.

That launcher was still developer-shaped. It assumed Node and npm, and later work would add double-click entry points and a desktop shortcut. But it expressed the correct destination: launch the planner, not the environment used to develop the planner.

<div class="section-label">What the repository changed</div>

In less than a day, OmniPlanner established four boundaries that the pre-repository folder had only implied:

- weeks were stored as independent planning records;
- the renderer reached desktop capabilities through a narrow preload bridge;
- AI providers sat behind planner operations instead of owning them;
- packaged outputs could be built away from the original machine.

It also preserved several unfinished problems. Credentials were not encrypted. Local storage was still doing too many jobs. The weekly planner remained the structural center of gravity. Calendar and habit behavior would reveal more ways that “week isolation” and “recurrence” could disagree.

Those problems belong to the next entries.

The achievement of February 25 was narrower and more important: OmniPlanner stopped being a folder that happened to run. It became a repository with an owned desktop shell, replaceable external services, and a build that could leave the machine where it was created.
