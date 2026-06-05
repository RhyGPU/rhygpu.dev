---
number: "005"
title: "Keeping the Scene From Replaying"
subtitle: "Immediate continuity, attribution guard, and the first context priority stack."
slug: "005-keeping-the-scene-from-replaying"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "Immediate continuity, attribution guard, and the first context priority stack."
tags:
  - mnemosyne
  - continuity
  - attribution
  - context
commits:
  - hash: "70ed66a"
    title: "Add narrator attribution guard"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/70ed66a7fd862af321346426da8d058cb3690fdb"
  - hash: "38018a"
    title: "Add narrator response integrity guard V1"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/38018a6ce17f9b729e47efb9e5528f1d08e24b7e"
  - hash: "71b04d1"
    title: "Verified code snapshot containing CONTEXT PRIORITY, SCENE STATE, and DO NOT REPLAY"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/71b04d10fe693b9ae6ca3b539488fdfb5b3d78a7"
---

Context Compiler V2 gave the model a session packet.

That helped, but it exposed the next problem fast: the model could still continue from the wrong part of the scene.

The packet had Soul, World, relationship state, recent events, and recent chat. On paper, that sounded like enough. In practice, the model could still grab the wrong anchor. It could treat old dramatic prose as current physical state. It could replay a completed beat because that beat was emotionally loud. It could treat its own character dialogue like the user said it.

The issue was not just memory anymore.

It was priority.

The model needed to know which part of the context was legally binding.

> A session packet is not enough if the narrator follows the wrong part of it.

<div class="section-label">What changed</div>

This pass started with continuity guards and ended with a stronger context priority structure.

The first fix was `[IMMEDIATE CONTINUITY]`.

Recent chat was useful, but it was not strict enough. It preserved what was said, but the model could still treat it like background. I needed a section that told the model where the scene currently was.

Not just:

> Here is what was said.

But:

> Here is where the scene is now. Continue from here. Do not replay.

That created a cleaner split:

```txt
Recent Chat = dialogue and prose continuity
Immediate Continuity = action-state continuity
World Log = scene and plot continuity
Soul Memory = character and emotional continuity
```

That was the first useful improvement.

Then the attribution issue showed up.

The model wrote a character joke, then later acted like the user had said the joke. That is not long-term memory failure. That is local speaker ownership failure.

So I added the narrator attribution guard.

The rule was simple: user facts come from user messages. Character dialogue is not user dialogue. Narrator prose is not user action. The narrator cannot invent user thoughts, motives, actions, or dialogue just to smooth the scene forward.

After that, the continuity problem still was not fully solved.

The model got better, but it could still resurrect stale physical facts. It could bring an old object back into the character's hand because the old prose was more vivid than the current state. It could invent unsupported elapsed time because that made the scene flow better.

That is when the priority problem became obvious.

> A guard says: please do not mess this up.
>
> A priority stack says: this section outranks that section.

That is the stronger fix.

<div class="section-label">Why I touched this</div>

The test case was simple.

A scene had already moved past a phone reveal and into the kitchen. The user accepted food and added a new emotional beat. The next response should continue from the kitchen, react to the new user input, and leave the completed reveal behind.

Instead, the model pulled the phone back into focus.

That told me the context packet was not authoritative enough.

It had the information, but the model did not know how to rank it. Recent chat, status prose, world events, character emotion, and the latest user message were all competing inside the same prompt. The model followed the most dramatic thing, not necessarily the most current thing.

That is bad for RP continuity.

A long scene cannot keep replaying whatever detail was most intense two turns ago. If a character already saw something, reacted, set it down, and moved to the kitchen, that state needs to be current fact. It should not be re-discovered because the prose was vivid.

So the goal became narrower:

> Feed less clutter.
>
> Rank the state harder.
>
> Make recent chat support the scene, not override it.

<div class="section-label">Immediate continuity</div>

`[IMMEDIATE CONTINUITY]` was the first version of that fix.

The idea was to promote the latest action state above recent chat.

Recent chat still matters. It keeps tone, rhythm, and dialogue texture alive. But it is not always a safe source of physical continuity. Prose can be long. It can contain metaphors, old actions, sensory detail, and status text. The model may latch onto the wrong part.

Immediate continuity was supposed to give the model a short checkpoint:

```txt
Completed scene facts:
Aurora has already seen and reacted to the phone reveal.
She moved toward the kitchen for food.

Latest user input:
The user accepted food and admitted loneliness/attraction.

Continue forward.
Do not replay completed beats.
```

It tells the model where the scene is instead of asking it to infer everything from prose.

<div class="section-label">Attribution guard</div>

The attribution bug was a different failure class.

The model did not forget. It confused ownership.

A character made a joke. Later, the same character reacted as if the user had said it. That is small in one response, but dangerous for an RP engine because the same pattern can become worse:

- character speech becomes user speech
- narrator metaphor becomes world fact
- user intent gets invented
- the narrator moves the user to keep the scene smooth
- the model reacts to its own setup instead of the player's actual input

So the guard had to be compact.

Not a giant prompt lecture.

Just enough pressure to remind the narrator:

> User facts only come from user messages.
>
> Character dialogue is character dialogue.
>
> Narrator prose is not user action.
>
> Do not invent user thoughts, motives, actions, or dialogue.

That was worth doing because it targets a common RP failure without spending many tokens.

The point was not perfection. The point was cheap damage reduction.

<div class="section-label">Time discipline</div>

The next bug was time.

The model invented a concrete duration that the scene never established.

That is the same kind of issue as attribution drift. It fills a gap because the prose wants to move smoothly. For normal writing, that might be fine. For a continuity engine, it is dangerous.

If the World Log or user did not establish a timestamp or elapsed duration, the narrator should not make one up.

Vague pacing is fine.

Concrete time claims need support.

So the time rule stayed compact too:

> Do not invent exact elapsed time, timestamps, or scene transitions unless the user or World Log supports them.

Again, this is not a full time engine. It is a small guard against an expensive class of mistakes.

<div class="section-label">Context Priority Stack</div>

The bigger fix was the Context Priority Stack.

At this point, adding more guard text was not the right move. The model already had instructions. The problem was that the context did not clearly say what outranked what.

So the compiled context needed a priority order.

The shape became:

```txt
P0 Latest user message
P1 Scene State
P2 Do Not Replay
P3 Active World
P4 Active Soul
P5 Relevant Memory
P6 Recent Chat Excerpt
```

That changed what recent chat was supposed to do.

Recent chat stopped being treated as the main authority. It became tone and dialogue support.

Scene State was introduced as the intended physical-continuity anchor, with Do Not Replay marking completed beats above old prose.

World and Soul state were meant to outrank old chat. The latest user input stayed highest because the user is the new action.

That is the important difference.

Before this, the model could see a lot of context and still choose the wrong anchor. After this, the prompt at least tells it how to rank the context.

> A guard asks the model to behave.
>
> A priority stack gives the model a hierarchy.

<div class="section-label">Recent chat cleanup</div>

Recent chat also needed cleanup.

Full assistant responses are expensive, and for this engine they can be actively harmful. They contain style, sensory detail, status blocks, metaphors, old physical positions, and dramatic phrasing. A lot of that is good for reading, but bad as authority.

So recent chat had to become shorter and lower priority.

The direction was:

- strip assistant status blocks
- strip hidden state if it appears
- cap assistant excerpts
- preserve user messages more strongly
- keep recent chat for tone, not state authority
- avoid breaking UTF-8 while trimming

That matches the project goal better: fewer tokens, better outcome.

Not less context for its own sake.

Less useless context.

<div class="section-label">What got better</div>

The compiler became less dependent on raw prose, but not enough to solve physical continuity by itself.

Instead of throwing a dense recent scene at the model and hoping it infers the current physical state, the app started pushing a ranked state brief:

- latest user input is the new action
- scene state is intended to hold current physical continuity
- completed beats should not replay
- world and Soul state should override older chat
- recent chat exists for tone

That was a better shape for long-form RP, but the next test showed the limit immediately.

It also gives debugging a cleaner target. If the model repeats something, I can check whether the completed beat was missing from Do Not Replay. If it resurrects an object, I can check whether Scene State had the current object location. If it invents time, I can check whether Time State was blank or vague.

The failure gets a place to live.

<div class="section-label">What still failed</div>

The priority stack improved the situation, but it did not fully solve physical continuity.

The same kind of stale-state bug still showed up: the model could continue as if an object was still central after the scene had already moved on. It could also invent unsupported time because it sounded natural.

The obvious answer looked like Scene State V1.

Store current physical state. Store object locations. Store completed beats. Make the engine own more of the scene.

That sounded correct for a moment.

But it also risked becoming exactly the kind of bloat I was trying to avoid.

I did not want to track every tiny physical detail just because one scene failed. If the latest chat was being fed in the wrong order, or if the wrong part of the previous narrator response was being promoted, then adding a bigger state schema would be solving the wrong problem.

So the next move was not to add more memory.

It was to inspect the actual payload.

<div class="section-label">Next</div>

The next step is opening the black box.

Before building heavier scene state, I need to see what the model is actually receiving: the final system message, compiled context, latest exchange, user message, and token estimate.

If the app is feeding the wrong anchor, no amount of prompt discipline will save the output.

That becomes the next debugging layer:

```txt
show the actual LLM payload
verify the context order
check whether Latest Exchange is really near the bottom
check whether the final state of the last narrator response survives
copy the payload for diagnosis
```

The model might not be ignoring the right context.

The app might be sending the wrong one.
