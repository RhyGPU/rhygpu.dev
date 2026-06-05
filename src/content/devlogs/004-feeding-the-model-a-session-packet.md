---
number: "004"
title: "Feeding the Model a Session Packet"
subtitle: "Context Compiler V2, clean recent chat, and state injection."
slug: "004-feeding-the-model-a-session-packet"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "Context Compiler V2, clean recent chat, and state injection for provider payloads."
tags:
  - mnemosyne
  - context
  - payload
  - state
commits:
  - hash: "af5f3ae"
    title: "Add patch protocol v1 foundation"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/af5f3ae"
  - hash: "b4ad92a"
    title: "Merge pull request #2 from RhyGPU/feat/patch-protocol-v1"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/b4ad92a"
  - hash: "187763a"
    title: "Commit and push Context Compiler V2"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/187763a"
---

After the app started hiding and parsing model output, the next problem was input.

The model could write a scene. The app could catch the hidden state. But before the next response, the model still needed the session back.

Not as raw chat history forever.

That was the bloat I was trying to avoid.

But also not as one dead summary that cuts the rhythm out of the scene.

I needed a session packet.

> The whole session, but carried forward as state.

<div class="section-label">What changed</div>

Context Compiler V2 started building the next provider payload from actual session pieces instead of treating the prompt as a loose pile.

The packet centered on:

- `CURRENT STATE`
- `CHARACTER MEMORY`
- `RECENT EVENTS`
- `RELATIONSHIP`
- `WORLD`
- clean recent messages

The recent messages stay clean. No hidden block. No machine JSON. No encoded state being fed back into the model raw.

The hidden state is for the engine. The visible narration is for the chat history. The compiled packet is what the model gets next.

That separation is the whole point.

<div class="section-label">Why I touched this</div>

The external API tests made the pressure obvious.

Without the right input shape, the model drifts back into normal RP chatbot behavior. It talks as the character. It forgets that it is supposed to be a narrator. It treats prompt instructions like vibes instead of rules.

It can also start mixing character knowledge, narrator knowledge, and user action if the payload is sloppy.

That was not acceptable for Mnemosyne.

The app has to hold the session together. The model writes from the state, but the model should not be trusted to carry the whole state by itself.

<div class="section-label">How the packet works</div>

The loop started to look like this:

```txt
Soul
World Log
Recent Events
Relationship State
Clean Recent Messages
        ↓
Context Compiler V2
        ↓
Provider Payload
        ↓
Model Response
        ↓
Visible Narration + Hidden State
        ↓
Strip / Parse
        ↓
Soul / World Patch
        ↓
Updated Session State
        ↓
Compile again
```

The model still does the writing. The app carries the session.

Clean recent messages keep the prose alive. They preserve the last exchange, the tone, and the immediate rhythm.

The compiled state carries the long-term part: what the character remembers, where the scene is, what recently happened, and what the current relationship pressure looks like.

One side keeps the writing from going cold. The other keeps the session from going empty.

<div class="section-label">What got better</div>

The model is no longer starting from only a few recent chat turns.

It gets a compact version of the session before writing: current scene, character memory, world state, recent events, relationship pressure, and the last clean messages.

That makes failures easier to inspect.

If the next response goes wrong, I can check the payload. Maybe the model ignored the instructions. Maybe the compiled packet missed something important. Maybe the recent chat window was too short. Maybe the world state was stale.

That is still annoying, but it is better than just saying the AI forgot.

Now there is a place to look.

<div class="section-label">Why the categories matter</div>

The Soul and World Log split only works if the compiler preserves it.

A character memory is not the same kind of thing as a room fact. Relationship pressure is not the same thing as active plot. Recent dialogue is not the same thing as long-term identity.

If those get mashed together, the model will mash them together too. That is how a character starts knowing narrator-only information, or how old emotional tension keeps bleeding into every scene.

So the packet needs sections.

Soul stays Soul-shaped. World stays World-shaped. Relationship stays relationship-shaped. Recent messages stay as actual chat texture.

That is where the earlier split starts paying rent. The memory layers are no longer only design notes. They are becoming something the app can feed into a model call.

<div class="section-label">Patch protocol entering the same range</div>

Patch protocol started showing up here because compiled state creates another problem.

If the app sends state forward every turn, then state changes need to be traceable.

A memory should not just appear. A world event should not just mutate. A relationship shift should not become permanent without knowing which turn caused it.

Regenerate, correction, restore, and branch logic all need that trail later.

The input side and the patch foundation belong near each other. One decides what the next model call sees. The other starts making state changes explicit enough to survive edits.
