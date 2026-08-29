---
number: "004"
title: "Five Checkmarks, Two Flames"
subtitle: "Weekly completion was being labeled as a streak."
slug: "omni-004-five-checkmarks-two-flames"
project: "OmniPlanner"
date: 2026-03-10
status: "published"
summary: "A habit completed five times could display a streak of two. Fixing the label led into a broader adaptability pass: wider planning columns, zoom controls, and local or provider-neutral AI."
tags:
  - omniplanner
  - habits
  - metrics
  - accessibility
  - local-ai
  - electron
commits:
  - hash: "ee260ed93ab8fd86615d4fe2172c06762bf71438"
    title: "Fix habit streak, widen todo columns, add zoom and local AI providers"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/ee260ed93ab8fd86615d4fe2172c06762bf71438"
---

A habit had five completed days and the flame beside it displayed `2`.

The number was not random. It was the current consecutive run inside the week. If Monday, Tuesday, Thursday, Friday, and Saturday were checked, five completions and a two-day streak were both mathematically defensible descriptions.

Only one of them matched what the interface appeared to promise.

At this stage, the weekly habit panel was not a long-term behavior analytics screen. It was seven checkboxes showing how much of the visible week had been completed. Placing a flame and one unexplained number beside those boxes made the user read `2` as “two of the seven,” even though five boxes were visibly checked.

On March 10, the badge changed from current streak to total completed days: `5/7`.

This entry is reconstructed from the commit rather than an exported conversation. The commit bundled the metric correction with three other adaptability changes: more room for todos, interface zoom, and more ways to run AI. They look unrelated in a file list. In use, all four removed an assumption about the one correct way to operate the planner.

<div class="section-label">Name the number the user can verify</div>

The old habit utility already calculated several values: current streak, longest streak, total completed days, and percentage.

The interface selected the current streak for its primary badge. That made sense if the badge represented continuity. It made less sense inside a weekly row where the user's immediate evidence was a count of checked dates.

The replacement displayed `totalDays/7`. The tooltip named the value explicitly and retained the best streak as secondary context. The flame color moved through neutral, amber, and orange as weekly completion increased.

This did not solve cross-week streaks. It did something more basic first: it stopped presenting one valid metric as if it answered a different question.

The difference matters in any planning interface:

- **completion** asks how many intended actions happened in a period;
- **streak** asks how long actions remained consecutive;
- **consistency** asks how completion behaves across many periods.

One number cannot carry all three meanings. For the visible weekly row, completion was the number the user could audit by looking left to right.

<div class="section-label">A todo needs more than leftover width</div>

The previous calendar fix had protected each day column with a 160-pixel minimum. Real todos showed that the threshold was still too narrow.

The minimum grew to 200 pixels. The checkbox, text size, and delete affordance became more compact so controls did not consume the space meant for the task itself.

This was not an attempt to fit all seven days without scrolling. That constraint had already been abandoned. The grid now preferred legible content and horizontal movement over seven compressed columns.

The planner was beginning to distinguish information density from information loss. A dense interface can still be useful. A textarea reduced to the space left after its controls cannot.

<div class="section-label">Zoom became application state</div>

The app also gained zoom controls in the sidebar and the keyboard shortcuts users expect from desktop software: increase, decrease, and reset.

Electron routed those operations through its main process and preload bridge. The browser path used a CSS fallback. The sidebar displayed the current percentage instead of making zoom an invisible transform.

The first implementation was global. A later commit would replace it with per-tab zoom because the weekly grid, goals, inbox, and settings did not share the same useful scale. It would also move the transform inside the viewport container after the outer layout began shrinking with the content.

Those later corrections do not make the first control pointless. They reveal the right domain boundary. Zoom was not merely a browser shortcut; it was a user preference that the planner needed to expose, persist, and eventually scope to the surface being viewed.

<div class="section-label">Local AI joined the provider list</div>

The February provider interface had separated Gemini, OpenAI, and Anthropic from the planner's own AI actions.

March tested whether that interface was actually extensible.

OpenRouter joined as a configurable provider for many hosted models. A second OpenAI-compatible path accepted a custom endpoint and model name. It was designed for LM Studio on port 1234, Ollama on port 11434, or another server implementing the same request shape. The API key became optional for local endpoints.

The weekly planner did not gain separate “Ask Ollama” or “Ask OpenRouter” buttons. It continued to call the same schedule and daily-focus operations. Provider selection remained in settings.

That was the proof that the earlier abstraction worked. Adding local inference required a new adapter and configuration fields, not a rewrite of the planning UI.

It also strengthened the local-first direction. Planner data had been stored locally from the beginning, but AI assistance still implied sending context to a hosted API. A configurable local endpoint made it possible for the model boundary to remain on the user's machine too.

<div class="section-label">Adaptability is not polish</div>

The March 10 commit can be read as a miscellaneous feature batch:

- change one habit number;
- widen a few columns;
- add zoom buttons;
- add two AI provider modes.

The common result was that fewer choices were imposed by the initial implementation.

The habit panel stopped insisting that a streak was the most useful weekly metric. The layout stopped insisting that every day fit into the available width. The interface stopped insisting on one visual scale. The AI layer stopped insisting on a short list of hosted vendors.

None of those changes finished its subject. Cross-week habit identity was still broken. Zoom still had the wrong scope. Local AI configuration still needed the broader credential and platform work that came later.

But the product moved toward a useful rule: where a personal planner can preserve user choice without corrupting its domain, it should.

Five checkmarks should be allowed to mean five completed days. A model should be replaceable. A grid should be readable. And the person using the planner — not the original viewport or provider — should determine how it fits.
