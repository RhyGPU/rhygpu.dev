---
number: "003"
title: "Hiding the Machine"
subtitle: "Mock provider, encoded hidden state, and the first real model test."
slug: "003-hiding-the-machine"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "Mock provider, encoded hidden state, real model testing, and the first output-side Mnemosyne loop."
tags:
  - mnemosyne
  - hidden-state
  - tauri
  - diagnostics
commits:
  - hash: "f26cbfe"
    title: "Add AGPL-3.0 license"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/f26cbfead602bea6003dc6445337c8b73ba77bc4"
  - hash: "a642953"
    title: "Scaffold Tauri desktop client"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/a6429539c7fb38ec92f790ad3c3ee6afaf753903"
  - hash: "b0697fa"
    title: "Wire mock provider turn flow"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/b0697faee12dbac371a443caea62ca99e6b70086"
  - hash: "aee7972"
    title: "Encode mock hidden state"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/aee79720d2c325d1bc55f704ae82a633cbd5fbcc"
  - hash: "365d105"
    title: "Surface memory cycle diagnostics"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/365d105634de01d784884622766279c83c60a987"
  - hash: "21f5efd"
    title: "Add turn debug panel"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/21f5efdf29fe70955561eab4ee10183fbda4f7c1"
---

The first app problem was output control.

The model could write a scene, but the app had to catch the machine part before the player saw it.

That was the job here: visible narration for the player, hidden state for the engine.

The old crude code block was useful because I could inspect it. I could see trust move, fear move, a memory get flagged, or the scene state change. But if that block stayed visible after every message, the RP experience was dead.

No raw JSON under the dialogue. No trust deltas sitting in the scene. No memory tags breaking the mood. No system residue reminding the player that the character is being calculated.

> The player sees the story. The engine reads the state.

<div class="section-label">What changed</div>

The desktop app started becoming more than a prompt experiment.

Tauri gave the project a body: a window, a chat interface, Rust behind it, React in front of it, local Soul files, provider settings, and a place for the state loop to run.

The output loop started taking shape:

```txt
User Message
        ↓
Compiled Context
        ↓
Model Response
        ↓
Visible Narration + Hidden State
        ↓
Strip / Parse
        ↓
Soul / World Update
        ↓
Save
```

That was the first version of the app actually breathing.

<div class="section-label">Why the mock existed</div>

The mock provider was not real RP testing.

It was scaffolding.

It proved that the UI could send a turn, the backend could return a response, the response could include hidden state, and the app could update the chat. That mattered. But it was not testing narration, psychology, or model behavior.

The mock did not surprise me. It did not drift. It did not forget the format. It did not leak state because a model got confused. It returned what the code told it to return.

Useful for the pipe. Useless as proof that the RP experience worked.

That distinction became important later because it is easy to overclaim a mock.

The mock proved that Mnemosyne could move data through the desktop app. It did not prove that a real model would obey the narrator role, preserve the hidden-state boundary, keep user agency clean, or update a Soul without smearing scene facts into character memory. It did not prove emotional pacing. It did not prove that the parser could survive a model trying to be helpful in the wrong shape.

So this pass should not be read as "the engine worked."

It should be read as:

> The pipe existed.
>
> Now it needed to survive an actual model.

<div class="section-label">The first real model test</div>

The useful failures came from actual LLMs.

I was already using OpenRouter models for AI RP testing, so using free OpenRouter models inside the app was the obvious next step. I needed real generations to see whether the system survived contact with a model that could misunderstand, improvise, ignore formatting, or write something good for the wrong reason.

The first real test felt good in a way the mock never could.

A real model answered. The chat moved. The scene had atmosphere. The narration had texture. It was not finished, but the product stopped feeling imaginary for a moment.

Then the warning showed up.

The output was nice, but it was also wrong in a dangerous way: the model wanted to talk like the character instead of staying as the narrator.

That mattered because Mnemosyne is not supposed to be another character impersonator. The narrator should describe the character. The Soul and World Log should carry continuity underneath. If the model collapses into being the character, knowledge boundaries collapse with it.

The first real test proved two things at once:

> It could feel good.
>
> Feeling good was not enough.

<div class="section-label">Encoded hidden state</div>

Plain hidden JSON was easy to inspect, but too fragile for the actual path.

It could leak into the visible response. It could get wrapped in prose. It could be malformed by the model. It also made the boundary between narration and machinery feel weaker than it should.

So the hidden state moved toward an encoded payload.

The app needed a recognizable marker, a compact body, and a parser that could support the new format without destroying older test transcripts.

That is where the `mne1.<base64url>` style payload started to matter.

The narration is for the player. The encoded hidden state is for the engine.

<div class="section-label">Diagnostics</div>

Once the state became hidden, debugging got harder.

If the Soul updated wrong, I needed to know why. If parsing failed, I needed to know where. If a memory got added, scored, discarded, or consolidated, I needed a place to inspect the cycle without dumping the machinery into the player's chat.

That made the turn debug panel and memory cycle diagnostics necessary.

Not as polish.

As survival.

The player should not see the machinery. The developer absolutely needs to.

<div class="section-label">What this exposed</div>

This pass made the first hard boundary visible.

The model should write and propose.

The app should catch, parse, validate, and manage.

At this stage I was still asking one model response to do too much: write the scene, stay in narrator mode, respect user agency, output hidden state, flag memory, judge importance, update relationship values, and remember to forget.

That burden was already showing cracks.

But the app now had somewhere to put the cracks. The mock gave the pipe a shape. Real models gave it failure cases. Encoded hidden state gave the engine something safer to parse. Diagnostics gave me a way to see behind the curtain.

That was enough to move forward.
