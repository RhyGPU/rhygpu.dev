---
number: "010"
title: "Prompt Cleanup V2 and the UI Reset"
subtitle: "Action doctrine, paper UI, terminal dev mode, and the feature-parity correction."
slug: "010-prompt-cleanup-v2"
project: "Mnemosyne"
date: 2026-06-27
status: "published"
summary: "Prompt Cleanup V2, action doctrine, State Map visibility, and the UI-flow reset after the mock-vs-real-app mistake."
tags:
  - mnemosyne
  - prompt-cleanup
  - ui
  - state-map
  - feature-parity
commits: []
---

Fresh Scenario State cleaned the room.

It did not clean the narrator's head.

The next failure was not stale location or old relationship warmth. It was pressure from the prompt itself. The model was being asked to write a scene while carrying too much machinery in its face: agency warnings, device warnings, time warnings, attribution warnings, hidden-state requirements, context hierarchy, memory instructions, relationship stats, world state, recent chat, latest exchange, and repair language.

That was not discipline anymore.

It was weight.

The narrator could follow more rules and still write worse.

<div class="section-label">Prompt Cleanup V2</div>

Prompt Cleanup V2 was the correction.

The goal was not to remove boundaries. The goal was to stop explaining the engine to the narrator every turn.

The model still needed a role:

```txt
You are the narrator.
Write the scene.
Do not speak as the user.
Do not reveal engine state.
Respect the current Soul and World context.
```

But it did not need the whole design philosophy stapled to the front of every response. The app should carry the structure. The prompt should brief the writer.

That is the difference.

<div class="section-label">Action doctrine</div>

The device rule exposed the bigger problem.

I had tried to protect user agency by adding a restriction around phones and props. The intention was right. The wording was wrong.

A character should not resolve the user's action without permission. But a character should absolutely be allowed to act.

Aurora can reach for the phone. She can interrupt. She can lunge, refuse, challenge, retreat, grab her own coat, slam a door, step closer, or make the situation worse.

What she cannot do is decide the user's completed response.

Good:

```txt
Aurora reaches for the phone, fingers closing toward the edge. "Give me that."
```

Bad:

```txt
Aurora takes the phone from his hand, unlocks it, and reads everything.
```

That became the action doctrine:

> Characters may initiate pressure.
>
> The user's reaction belongs to the user.

That rule is smaller than a pile of prop prohibitions and stronger than a timid narrator.

<div class="section-label">The UI-flow reset</div>

The next mistake came from the UI side.

A design handoff mock looked good. It had a calmer app flow: a left rail, a home surface, Play, State Map, Characters, Settings, and dev progress details. It felt more like a real product than the dense launcher that had grown out of the engine work.

But the mock did not know Mnemosyne.

It did not know the real app's Souls, Settings, conversations, archive behavior, .mne import/export, editor, payload tools, dev mode, benchmark scars, or the difference between player-facing state and GM/dev state.

So the useful lesson was not "copy the mock."

The useful lesson was:

> Use the mock's flow.
>
> Keep the real app's features.

I got that wrong once.

A separate mock-data V2 prototype made the app look cleaner while leaving real functionality behind. That was the exact wrong artifact. Mnemosyne did not need a fake prettier app. It needed the existing app reorganized.

The correction was feature parity first.

<div class="section-label">Paper/editorial human UI</div>

The visual direction also got clarified.

Not the dark mock skin.

The app wants a book/editorial paper direction: warm paper, ink, hairline rules, restrained accent, enough editorial hierarchy to organize a complex engine without turning it into a dashboard.

The reason is not only taste.

Mnemosyne is reading-first. The user spends time inside scenes, memories, state, and session records. A paper surface makes redaction feel native too. Hidden State Map fields can read like a declassified document instead of a broken UI.

That matters because State Map visibility is not binary.

<div class="section-label">Terminal dev UI</div>

The human UI should be paper.

The dev UI should not.

Dev mode is the machine room: pipeline traces, evaluator status, repair attempts, payload inspection, benchmark residue, logs, and commands. It should feel separate. Terminal language fits there because the user is not reading a scene in that mode. They are operating the engine.

That split became part of the design:

```txt
Human surface: paper/editorial.
Dev surface: terminal/machine room.
```

Mixing them makes both worse.

<div class="section-label">State Map redaction</div>

State Map also changed shape.

The first instinct was to ask whether showing everything would break immersion. It can.

But deleting the view is not the answer.

The better answer is a single State Map with visibility rules.

Realistic mode shows little. Reader mode can show more Soul-facing information. GM or god mode can show the whole operational map: who knows what, who misbelieves what, plot state, relationship numbers, memory, objects, timeline, and hidden state.

The backend should keep all of it.

The UI decides what the current seat may see.

That means redaction is a presentation layer, not data loss.

<div class="section-label">Feature parity</div>

This became the hard requirement.

The UI overhaul is not a mock app creation task.

Every existing feature has to land somewhere in the new flow:

- Home for resuming and selecting sessions
- Play for the actual RP surface
- State Map as the full state hub
- Library or Workshop for Souls, settings, import/export, and editing
- Settings as a real destination, not a buried drawer
- Dev mode as a clear terminal-styled entry

The mock's "Campaigns" becomes Home.

The mock's Play remains Play.

The mock's State Map becomes Mnemosyne's state hub, backed by real Soul and World data.

The mock's Characters cannot be copied literally, because Mnemosyne's real objects are Souls, Settings, sessions, and editor surfaces.

That mapping matters more than the mock's labels.

<div class="section-label">What the logs corrected</div>

The causal logs make the public history sharper.

The mock provider did not prove real model behavior. It proved the pipe.

Raw chat and dead summaries both failed, which is why Context Compiler V2 and patch protocol mattered together.

The latest exchange bug was not a mystical model failure. It was the app feeding the head of the previous narrator response while claiming to feed the final state.

Fresh Scenario State fixed part of the dirty-brief problem.

Prompt Cleanup V2 fixed the next layer: too much machinery in the narrator's face.

The UI reset fixed the product layer: do not replace the real app with a pretty mock. Reorganize the real app without losing features.

<div class="section-label">Next</div>

The next public phase should not claim that the UI mock proved backend truth.

It did not.

The backend truth still comes from payloads, state exports, visible chat logs, and real model runs.

The UI truth is different:

Can the user find the right surface?

Can they resume a session without hunting?

Can they see the Soul without reading debug sludge?

Can they enter Dev mode without polluting Play?

Can State Map reveal or redact based on mode?

Can the new flow carry every old feature?

That is the bar.

Not prettier.

Accurate.
