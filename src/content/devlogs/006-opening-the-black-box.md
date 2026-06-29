---
number: "006"
title: "Opening the Black Box"
subtitle: "LLM Payload Inspector, Latest Exchange, and the tail excerpt bug."
slug: "006-opening-the-black-box"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "LLM Payload Inspector, Latest Exchange, and the tail excerpt bug."
tags:
  - mnemosyne
  - payload
  - debugging
  - context
commits:
  - hash: "7985475"
    title: "Clean up LLM payload context and latest exchange"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/7985475596fcbcb1f7f2e22dbb7e809539745113"
  - hash: "a543e1c"
    title: "Improve chat navigation and payload copy feedback"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/a543e1c8651dbb9149716081fddfc1c0bc18ca65"
---

Context Priority Stack looked like the right direction.

It gave the model a hierarchy. Latest user input mattered more than old chat. Scene state and world state were supposed to outrank stale prose. Recent chat was supposed to help tone, not override continuity.

But the same kind of failure still showed up.

The model could still continue from the wrong physical moment.

At first, the obvious answer looked like Scene State V1. Track current physical state, completed beats, object locations, do-not-replay lists, and time state directly in the engine.

That sounded clean.

It was also too much.

I did not want Mnemosyne to become a giant object tracker. I did not want to track every fork, chair, door, shirt, phone, fridge, and microwave just because the model failed one scene. That would fight the whole point of the project:

> Less tokens, better outcome.

So I pushed back.

Before adding more state, I needed to know what the model was actually seeing.

<div class="section-label">What changed</div>

The next fix was not more memory.

It was inspection.

The context order became more intentional:

```txt
SYSTEM RULES
WORLD / STORY SNAPSHOT
CHARACTER SNAPSHOT
RELEVANT MEMORIES
LOWER-PRIORITY RECENT CHAT
LATEST EXCHANGE, HIGH PRIORITY
CURRENT USER MESSAGE
```

The important part was `LATEST EXCHANGE, HIGH PRIORITY`.

That section was supposed to sit near the end of the compiled context, right before the current user message. It should tell the model:

> Continue from the final state of the last narrator response.
>
> Then respond to the latest user input.
>
> If older context conflicts with this, ignore the older context.

That was the cheaper fix.

Not full Scene State.

Not object tracking.

Just feed the model the most recent anchor correctly.

Then came the second piece: the LLM Payload Inspector.

I needed to see the actual text going into the API call.

Not a fake preview.

Not a simplified context panel.

The real payload:

```txt
system message = narrator prompt + compiled context
user message = current user input
```

Without that, I was guessing.

<div class="section-label">Why I touched this</div>

The phone scene was still the test case.

The previous narrator response ended with the character moving past the phone reveal and turning toward the kitchen. The next user message accepted the food and added a new emotional beat.

The next response should have continued from that.

Instead, the model acted like the phone was still central.

That made the problem look like bad memory, but I was not convinced.

The model may not have been ignoring the latest exchange.

It may have been receiving the wrong latest exchange.

That distinction matters.

If the model is ignoring correct context, that is a model behavior problem.

If the app is sending the wrong anchor, that is my bug.

The only way to know was to open the black box.

<div class="section-label">Payload Inspector</div>

The inspector needed to show the exact LLM input.

It had to include:

- final system message text
- current user message text
- compiled context
- estimated tokens
- provider mode
- model name
- base URL

It also had one hard rule:

> Never show the API key.

This was not a fancy UI feature. It was debugging equipment.

If continuity breaks, I need to inspect the prompt and ask:

- Is Latest Exchange actually near the bottom?
- Did the final state survive?
- Is Recent Chat duplicating old material?
- Is the world snapshot too vague?
- Is the current user message duplicated?
- Is the model being told two different things at once?

Once I can copy the exact payload, the problem stops being mystical.

It becomes inspectable.

<div class="section-label">The real bug</div>

The inspector worked.

And it exposed the actual problem.

`[LATEST EXCHANGE, HIGH PRIORITY]` was supposed to give the model the final state of the previous narrator response.

But it was feeding the beginning.

That is a brutal bug.

The beginning of a long narrator response often contains the dramatic setup. In the phone scene, the beginning was the phone reveal. The ending was the actual current state: the character had already reacted, moved on, and turned toward the kitchen.

So the app was saying:

> Continue from the final state.

But the text it provided was:

> She is still reacting to the phone.

That means the model was not randomly failing.

It was following the wrong anchor.

The high-priority section was high-priority garbage.

The bug was easy to miss because the label was correct.

The payload said "latest exchange." The prompt language said "final state." The section sat in the right priority position. From far away, the architecture looked right.

But the excerpt function was taking the front of the previous assistant message.

That meant the system was prioritizing the opening image of the last response, not the place where the response landed. In a short answer, that difference might not matter. In a long narrator answer, it matters constantly.

A narrator often opens with the thing being reacted to and ends with the new physical/emotional position. The head is setup. The tail is state.

So the model was being told to continue from the ending while being shown the beginning.

<div class="section-label">Head vs tail</div>

The fix was simple once the payload made the bug visible.

For the latest assistant response, use the tail.

Not the head.

The latest assistant excerpt should preserve the ending because the ending usually contains the current physical state.

The rules became:

```txt
latest assistant excerpt = tail / end of the last assistant message
latest user input = full if reasonable, otherwise capped
recent chat = older messages only
```

Before taking the tail, the app should strip machine noise:

- status blocks
- hidden state blocks
- markdown status artifacts

Then cap safely:

- latest assistant tail around 1200 characters
- latest user input around 1000 characters
- UTF-8 safe truncation
- prefix tail truncation with `...` so it is obvious this is the ending

That small detail matters.

If the excerpt starts with `...`, I know I am reading the end of the message, not the beginning.

<div class="section-label">Recent chat cleanup</div>

The same bug existed in a weaker form inside lower-priority recent chat.

Older assistant excerpts were also taking the head of responses. That meant even the lower-priority context could keep reintroducing old physical states.

It did not break the output after the priority fix, but it was still noisy.

The rule became clearer:

> User messages should be preserved more directly.
>
> Assistant messages should often preserve the final state.

That does not mean every assistant message needs a huge tail excerpt. But for continuity, the end of the assistant response is often more important than the opening prose.

A narrator response can start with atmosphere and end with movement.

The ending is usually where the scene actually lands.

<div class="section-label">Time cleanup</div>

The payload also showed a smaller bug.

Time formatting was malformed.

A line like `Session startLate evening` means two time fields got glued together. That kind of malformed state gives the model permission to invent time.

Then it starts saying things like `three minutes later` or `twenty minutes ago` even when nothing established that.

The fix was not a full time engine.

Just clean the formatting.

If exact time is not known, do not invent it. If two time strings get joined, separate them properly or only show one clean value.

Again, small bug.

Expensive consequences.

<div class="section-label">What got better</div>

After the tail fix, the important test improved.

The model stopped resurrecting the phone reveal. It continued from the food, the vulnerability, and the latest user joke. That is what I wanted to see.

This was not a magical memory breakthrough.

It was simpler and more useful:

> The model finally saw the right anchor.

The architecture was not wrong. The implementation was pointing the model at the wrong part of the previous response.

That is why the inspector mattered.

Before the inspector, I could only argue with the output.

After the inspector, I could inspect the input.

That changes the whole debugging loop.

<div class="section-label">What is still rough</div>

The fix worked in the important way, but the logs still showed cleanup work.

The payload inspector visually duplicated context. The actual model probably was not receiving duplicate context, but the debug display made it look confusing.

The current user input also appeared inside `LATEST EXCHANGE`, then again as the actual user message. That is not fatal, but it wastes tokens and muddies priority.

Lower-priority recent chat could still include stale assistant head excerpts.

Relevant memories were also getting polluted by generic filler. Things like `neutral exchange added texture` are not memories. They are debug-flavored garbage. They cost tokens and teach the model nothing.

So the next cleanup pressure is clear:

- make payload display labels clearer
- stop duplicating current user input
- use better assistant excerpts in recent chat
- filter generic memory filler
- keep the payload lean

<div class="section-label">Next</div>

Next is cleanup, not a new grand architecture.

The payload is now visible.

The latest exchange is closer to correct.

The model can continue from the right anchor when the right anchor is actually fed to it.

Now the problem moves to hygiene:

```txt
do not duplicate the current user message
do not let stale assistant heads pollute recent chat
do not store generic debug filler as memory
do not let the debug UI misrepresent the actual API payload
```

That is the next layer.

Not more magic.

Better plumbing.
