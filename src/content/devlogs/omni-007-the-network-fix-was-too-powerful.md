---
number: "007"
title: "The Network Fix Was Too Powerful"
subtitle: "CORS, Windows focus, and administrator mode converged on one boundary."
slug: "omni-007-the-network-fix-was-too-powerful"
project: "OmniPlanner"
date: 2026-03-16
status: "published"
summary: "AI and email connections failed inside Electron, native dialogs froze input, and the first repair elevated the whole app while proxying network traffic through the main process — effective, but broader than the product should require."
tags:
  - omniplanner
  - electron
  - windows
  - security
  - networking
  - ipc
commits:
  - hash: "cc5ec0dcf445695d30f65386690398654b3282f8"
    title: "Fix admin permissions, dialog freeze, habit deletion, and connection errors"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/cc5ec0dcf445695d30f65386690398654b3282f8"
  - hash: "d0738cc3528d314bdd71be3d4ec055606f403772"
    title: "Route AI traffic through the Electron main process"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/d0738cc3528d314bdd71be3d4ec055606f403772"
---

OmniPlanner could connect to an IMAP server in code and fail to connect as a Windows application.

AI requests had a parallel problem. The renderer loaded from `file://`, external APIs enforced browser-origin rules, the page's content policy constrained destinations, and Windows could interrupt first-run network access with an operating-system prompt.

The first repair made the application more permissive. The second moved all AI traffic into Electron's main process and made the entire app request administrator privileges.

The features could reach the network afterward. The solution also became more powerful than a personal planner should need to be.

This entry is reconstructed from two March 16 commits. Their implementation is worth preserving without pretending it was the final security architecture. Later phases introduced explicit platform services, secure credentials, and narrower capability boundaries precisely because this solution had demonstrated both the value and the danger of centralizing privileged work.

<div class="section-label">A dialog could freeze every input</div>

The connection failures were not the only desktop-shell bug.

OmniPlanner still used `window.alert()` and `window.confirm()` for restore errors, missing settings, email failures, calendar extraction results, habit deletion, and the destructive workspace reset.

Inside this Electron setup, a native dialog could take keyboard focus from the renderer and fail to return it cleanly. After dismissing the prompt, text inputs remained unresponsive until the application restarted.

The patch replaced those calls with React-owned `AlertDialog` and `ConfirmDialog` components. The dialog lived inside the renderer's focus system, moved focus to a safe button when opened, supported Escape, and gave dangerous confirmation a visually distinct action.

This was not only styling. A blocking browser primitive had become a desktop lifecycle bug. Owning the dialog meant owning focus restoration and keyboard behavior too.

The main process also attempted to refocus the renderer after operating-system focus events such as UAC prompts. The two changes addressed the same class of failure from opposite sides: one removed avoidable OS-level focus transitions; the other tried to recover from the unavoidable ones.

<div class="section-label">The content policy opened completely</div>

OmniPlanner's AI provider list was intentionally extensible.

That made a fixed `connect-src` list awkward. Gemini, OpenAI, Anthropic, OpenRouter, a local LM Studio endpoint, an Ollama server, and a user-defined compatible API could all have different destinations.

The first March 16 patch changed Electron response headers so the renderer's content security policy allowed `connect-src *`.

It removed the immediate policy block. It also removed a meaningful allowlist.

For custom local endpoints, some form of configurable destination was necessary. A wildcard for every renderer request was the broadest possible expression of that requirement. If renderer code were ever compromised, the same permission would let it connect anywhere the process could reach.

The patch also moved documentation links through a small `openExternal` IPC operation that accepted only HTTP and HTTPS URLs. That operation was much closer to the capability shape the app ultimately needed: expose one controlled action rather than the entire underlying platform.

<div class="section-label">The app began demanding elevation</div>

The packaged Windows configuration added `requestedExecutionLevel: requireAdministrator`.

That handled newly built executables. It did not affect an existing build or a development launch, so the next commit added a runtime check. On Windows, the main process ran `net session`; if it was not elevated, it invoked a hidden PowerShell process that relaunched Electron with `Start-Process -Verb RunAs`, then exited the original instance.

The commit's reasoning was that AI and email needed network permission granted to the elevated process by Windows Firewall.

Requiring elevation made that assumption operational, but it coupled ordinary planning to administrator access. Viewing a week, checking a todo, or writing a note now began from a process with privileges unrelated to those actions.

It also made the focus problem more likely because every launch could cross a UAC boundary.

Administrator mode can be a useful diagnostic: if elevation changes the result, permissions or policy are part of the failure. It is a poor permanent default for a local productivity app. The safer target is to grant the application only the network and storage capabilities it actually needs while leaving routine UI work unprivileged.

The March implementation had not reached that target yet.

<div class="section-label">Fetch moved out of the renderer</div>

The more durable half of the second commit was `electronFetch`.

In a browser build, it fell back to normal `fetch`. In Electron, it serialized the method, headers, and body across the preload bridge. The main process used Electron's `net` module, collected the response, and returned status, headers, and text to the renderer as a reconstructed `Response`.

OpenAI, Anthropic, and OpenAI-compatible providers switched to this wrapper. Gemini was rewritten from its SDK to a direct REST call because the SDK's internal transport could not be redirected through the new boundary.

This removed browser CORS from desktop AI calls and gave every provider one transport seam. It also kept the web version viable through the fallback.

The first IPC shape was again too broad. The renderer could supply an arbitrary URL, headers, and body to a generic main-process request handler. That was convenient for provider extensibility and dangerous as a privileged capability. A compromised renderer could ask the main process to make requests far beyond daily-focus generation.

A mature boundary would validate destinations or expose domain operations such as `generateSchedule` rather than raw network authority. The later platform-service work moved in that direction.

<div class="section-label">Deletion finally learned the actual time</div>

The first March 16 commit also corrected the habit tombstone logic from the previous entry.

The global set of deleted IDs stopped resurrection, but it treated deletion as timeless. If a past week had never been saved and needed reconstruction after the habit was deleted, the set excluded that habit even though the deletion occurred after the historical week ended.

The week manager replaced the set with the earliest deletion timestamp for each habit ID. When reconstructing a week, it compared that timestamp with the end of the target week.

A habit deleted in March could still be reconstructed into an unsaved February week because it had been alive then. It remained excluded from April.

This completed the temporal rule more accurately than a boolean tombstone could. “Deleted somewhere” and “was active during this week” are not opposite facts; both can be true.

<div class="section-label">The right boundary was visible, not finished</div>

March 16 produced real improvements:

- renderer-owned dialogs stopped native focus loss;
- historical habit reconstruction respected deletion time;
- AI providers shared one desktop/web transport abstraction;
- Gemini no longer depended on an SDK transport the app could not control;
- external links and network work moved behind preload IPC.

It also created security debt:

- every Windows launch sought administrator privileges;
- the renderer's connection policy allowed every destination;
- a generic IPC handler gave the renderer main-process network reach.

Both sets of facts belong in the devlog.

The implementation had discovered the correct architectural direction — browser-like UI should ask the desktop shell for platform capabilities — while choosing an overly permissive first version of that shell.

The next productization phases would turn that discovery into named storage, credential, email, network, notification, and shell services. March 16 was the less elegant precursor: the day the network started working by making the boundary impossible to ignore.
