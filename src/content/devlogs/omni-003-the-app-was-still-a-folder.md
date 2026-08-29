---
number: "003"
title: "The App Was Still a Folder"
subtitle: "Desktop software needs an entrance, not a command sequence."
slug: "omni-003-the-app-was-still-a-folder"
project: "OmniPlanner"
date: 2026-03-10
status: "published"
summary: "OmniPlanner could build as an Electron app, but opening it still required repository knowledge. Double-click launchers and a shortcut creator turned the development folder into something re-enterable."
tags:
  - omniplanner
  - electron
  - windows
  - launcher
  - distribution
  - ux
commits:
  - hash: "ba451c3275a361d4e463c9caf7e2c88b1d69053d"
    title: "Add repository field to package.json for electron-builder CI"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/ba451c3275a361d4e463c9caf7e2c88b1d69053d"
  - hash: "5bc2ca29c217f38ba0288e06d0dc2959937c0592"
    title: "Add double-click launchers and desktop shortcut creator"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/5bc2ca29c217f38ba0288e06d0dc2959937c0592"
---

By March, OmniPlanner was a desktop application that still opened like a source repository.

Electron had a main process. The app could be packaged for three operating systems. A GitHub Actions workflow knew how to produce installers and portable artifacts.

Locally, however, the ordinary entrance was still a command: find the nested application directory, open a terminal there, install the right dependencies, build the renderer, and launch Electron.

That was acceptable for development. It was a poor ritual for a personal planner meant to be opened every day.

This is another Git-based reconstruction; the direct March conversation is not in the exported corpus. The commits show a small distribution story in two parts: first make the remote builder understand where the repository lives, then make the local user stop needing to understand the repository at all.

<div class="section-label">The build knew the files but not the project</div>

OmniPlanner's application lived one directory below the Git root.

The Actions workflow already set its working directory to `omniplan-ai---executive-life-os`, but `electron-builder` also tried to infer repository metadata. In CI, it could not reliably discover that metadata from the nested package and failed with `Cannot detect repository by .git/config`.

The first March 10 commit added an explicit `repository` object to `package.json`.

It was four lines, but it described a recurring difference between a successful local build and a reproducible build. A developer's checkout contains ambient context: Git remotes, parent directories, cached dependencies, and a shell already positioned in the right place. A clean runner knows only what the project declares.

If the build requires information, that information belongs in the build input.

<div class="section-label">Double-click is an interface</div>

Fifty minutes later, the local entrance changed.

Windows received `run.bat`. Linux and macOS received `run.sh`. Both launchers followed the same state machine:

1. move into the launcher's own directory;
2. verify that Node.js exists;
3. install dependencies if `node_modules` is missing;
4. build if `dist/index.html` is missing;
5. start Electron;
6. close the launcher after the app opens.

The important operation was not any one shell command. It was relocating setup knowledge from the user's memory into a file beside the application.

The scripts also treated failures as part of the interface. Missing Node did not become a cryptic “command not found.” Install and build failures stopped the sequence and remained visible. First-run work announced itself instead of looking like a frozen app.

This was still a source-based launcher. The user needed Node, npm, the repository, and an internet connection for the first dependency installation. It was not a substitute for the installers produced by CI.

But it served a different purpose: it made the working checkout usable as a daily application while development continued.

<div class="section-label">The shortcut pointed to the ritual</div>

Windows also received `create-shortcut.bat`.

The script created a temporary VBScript, used Windows Script Host to place **OmniPlan AI.lnk** on the desktop, set the working directory to the application folder, and pointed the shortcut at `run.bat`.

The shortcut did not bypass the launch checks. It pointed to the file that knew how to perform them.

That detail mattered. If the shortcut had launched Electron or a generated `dist` file directly, first-run installation and missing-build recovery would have existed only in the repository entrance. Instead, every supported local entrance converged on the same startup sequence.

The icon and polish could wait. Re-entry could not. A planner that disappears back into a nested source directory after every use will not become part of a routine.

<div class="section-label">A launcher can preserve stale code</div>

The first launcher had an intentional shortcut: it rebuilt only when `dist/index.html` did not exist.

That made repeat launches fast. It also meant an existing build could remain stale after source files changed. The launcher knew the difference between “built” and “not built”; it did not know the difference between “current” and “out of date.”

This was reasonable for a first daily entrance and insufficient as a final update strategy. Later sessions would revisit startup delay, duplicate launch paths, and the cost of rebuilding too often or too little.

The early script reveals the trade-off clearly:

- always rebuilding makes every launch feel like development tooling;
- never checking freshness can open yesterday's application;
- installing a packaged release avoids both, but slows iteration during active development.

OmniPlanner was still on the third path's way, not at its destination.

<div class="section-label">From executable to re-enterable</div>

The February desktop work answered whether OmniPlanner could run outside a browser. The March launcher work answered whether I could return to it without reconstructing the development environment each time.

Those are different definitions of “working.”

After these commits:

- the remote packager had explicit repository context;
- each desktop platform had a discoverable local launcher;
- first-run dependency and build work was automated;
- Windows could create a desktop shortcut without manual path setup;
- startup failures appeared as guided states rather than vanished terminals.

The result was not a polished consumer installation. It was something more immediately useful during development: the repository had a front door.

That front door would later need renovation. For now, OmniPlanner no longer required me to remember how it was made before I could use what I had made.
