---
number: "009"
title: "Starting Fresh Without Erasing the Soul"
subtitle: "Fresh scenario state, stale world cleanup, and the first reset boundary."
slug: "009-starting-fresh-without-erasing-the-soul"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "Fresh scenario state, stale world cleanup, and the first reset boundary."
tags:
  - mnemosyne
  - fresh-session
  - scenario-state
  - world-state
  - prompt-cleanup
commits:
  - hash: "TBD"
    title: "Fresh Session / Reset Scenario State V1"
    repo: "RhyGPU/mnemosyne"
---

The logs did what I built them to do.

They made the lie obvious.

A new session looked clean from the chat window. New opening. New direction. New test. But the exported payload told a different story. Under the surface, Mnemosyne was still dragging old scene state into the next run: leftover relationship warmth, stale location, old objects, and active plots that belonged to another setup.

So the model was not always failing in a vacuum.

Sometimes I was handing it a dirty brief and then acting surprised when the scene came out dirty.

<div class="section-label">What changed</div>

This pass added the first real fresh-session boundary.

A new chat needed a choice:

```txt
Continue Soul continuity
```

or:

```txt
Start fresh scenario state
```

The distinction is small in the UI, but huge for the engine.

The Soul can persist. The character can still be herself: long-term personality, core memories, trauma patterns, preferences, emotional tendencies, the slow drift that makes her feel lived-in.

A scenario is not that.

A new test should not automatically inherit old location, key objects, active plots, recent events, relationship temperature, or scene-specific emotional momentum. A character can stay persistent without every fresh scene starting inside the previous room.

That was the boundary I needed.

<div class="section-label">Why I touched this</div>

The test case was blunt.

A debt collector scene, or any random threat opener, should not start with trust over 100, affection over 100, and a kitchen-counter setup from a completely different run.

If the payload says:

```txt
Location: Aurora's kitchen counter
Key objects: wine glass, couch, phone
Relationship: high trust, high affection
```

the model has every reason to write from that. It will make Aurora warmer than she should be. It will pull the setting back toward the apartment. It will resurrect the phone or wine glass because the context says those objects are relevant.

That is not some mysterious LLM curse.

It is stale state with a narrator attached to it.

The logs made the fix narrower. Not Memory Retrieval V1. Not object tracking. Not full Scene State.

Just this:

```txt
Make fresh sessions actually fresh.
```

<div class="section-label">Persistent Soul vs scenario state</div>

This became one of those boundaries that seems obvious only after the bug embarrasses you.

The Soul is long-term character continuity.

Scenario state is current-session continuity.

They should not share the same reset lever.

If I wipe the Soul every time I start a new scene, the character becomes shallow again. That defeats the whole point of Mnemosyne. But if I preserve every scene detail forever, the character gets haunted by old tests. Every new opening arrives with someone else's props, emotional temperature, and plot residue.

So the split became:

```txt
Persistent:
character identity
core memories
slow personality drift
long-term emotional patterns
durable relationship history, if selected
```

and:

```txt
Volatile:
current location
time elapsed
active plots
key objects
recent events
scene-specific memories
current relationship temperature, if starting fresh
```

That lets the character remain herself without turning every test into a sequel.

<div class="section-label">Fresh scenario state</div>

The first reset target was volatile state.

Fresh scenario mode should clear or neutralize things like:

```txt
world.location
world.time_elapsed
world.active_plots
world.key_objects
world.recent_events
recent scenario-specific memories
relationship warmth toward the user
```

unless the user deliberately chooses persistent continuity.

Sometimes I want the relationship to continue. Sometimes I want the same character in a clean room, with no old emotional debt attached. Those are different user intentions, and the app should not blur them together.

The UI needs to make the mode visible:

```txt
Using persistent Soul continuity
```

or:

```txt
Fresh scenario state
```

The model should not have to guess what kind of session this is. Neither should the user. The payload should carry that decision clearly.

<div class="section-label">What got better</div>

The first fix helped.

Fresh tests no longer started with completely insane relationship values. Instead of inheriting huge trust and affection from old scenes, the new session moved closer to neutral.

That changed the tone immediately.

A cold opener should feel cold. A threat scene should not carry romantic warmth by default. A dangerous stranger should not be treated like the continuation of a vulnerable kitchen conversation.

The payload was still imperfect, but less contaminated. Visible chat export kept working. Payload history kept working. Most importantly, the app could now prove that the relationship reset was moving in the right direction.

Progress, but not victory.

<div class="section-label">What still failed</div>

The world snapshot was still too sticky.

Even after the relationship reset improved, fresh sessions could still inherit the default Aurora apartment setup:

```txt
Location: Aurora's kitchen counter
Active plots: Establish the first scene
Key objects: Half-empty wine glass; Couch with rumpled blankets; Phone
```

So the session was only half fresh. The relationship state cleaned up, while the setting kept dragging the model back into the old default scenario.

That explains why a broad opener could still collapse into kitchen-counter staging. The user gives a loose start, the model checks the payload, and the payload quietly says: Aurora is basically in her apartment with wine, couch, and phone.

Of course the model follows the brief.

Dirty context again.

<div class="section-label">Threat severity</div>

The fresh session test also exposed a second state problem: threat scenes were not scaling hard enough.

Trust could drop, but fear stayed too low. The prose could describe Aurora as terrified or cornered, while the numeric state still treated fear like a mild concern.

That mismatch matters because the next prompt reads those numbers. If fear stays low, the narrator may soften her too quickly. If affection or desire remain active in a violent threat context, the emotional tone can turn wrong fast.

A threat should not only reduce trust.

It should push fear hard, and it should suppress romance-adjacent values unless the scene strongly justifies otherwise.

No giant trauma system yet. Just severity that respects the scene.

<div class="section-label">Time and POV still leaked</div>

The same tests showed smaller prompt problems.

Time discipline still failed. The narrator invented concrete durations even when neither the user nor the World Log established them. In prose, that kind of detail sounds natural. In a continuity engine, it creates fake facts.

The rule needed to be shorter and harder:

```txt
Never invent concrete durations.
Do not say minutes, hours, days, or years passed unless the user or World Log established it.
```

There was also mild POV leakage. The narrator could write as if it knew exactly what the user felt, saw, or aimed. Sometimes it was a reasonable inference, sometimes it crossed the line into steering the player.

The better boundary is not to make the narrator timid. The better boundary is:

```txt
Describe what the character perceives.
Do not claim the user's internal experience or exact action unless the user gave it.
```

That keeps the character active without stealing the user's side of the scene.

<div class="section-label">The overcorrection</div>

This is where I made a wrong turn.

To stop the narrator from controlling the user's device, a device/prop agency rule got added. The intention was reasonable: if the user shows a phone, the narrator should not decide Aurora takes it, unlocks it, searches it, and reads everything unless the user allows that.

But the wording was too rigid.

It made the narrator cautious around phones and props in general. Worse, it pushed against the thing I actually wanted: a character who can act.

Aurora should be allowed to use her own phone. She should be allowed to reach for things, interrupt, step forward, grab for something, refuse, challenge, retreat, escalate, or use her own environment.

The problem is not character action.

The problem is resolving the user's reaction without permission.

Good:

```txt
Aurora lunges for the phone, fingers closing toward the edge of the screen. "Give me that."
```

Bad:

```txt
Aurora takes the phone from his hand, unlocks it, scrolls through the messages, and reads everything.
```

The first creates pressure.

The second steals the response.

That distinction is cleaner than a blunt device rule.

<div class="section-label">What this taught me</div>

A pattern started showing up.

When the model behaves badly, the tempting fix is to add another restriction. Do not touch the phone. Do not infer objects. Do not invent time. Do not move too much. Do not act too strongly.

Stack enough of those rules and the narrator stops feeling careful. It starts feeling sedated.

The model writes like it is filling out a compliance checklist instead of portraying a living character.

That is not Mnemosyne.

The engine should make the narrator smarter, not more timid. Most of the time, the answer is a cleaner boundary, not a bigger cage.

For fresh sessions:

```txt
persistent Soul continuity vs fresh scenario state
```

For action:

```txt
character may act, but user reaction stays with the user
```

For time:

```txt
concrete duration requires evidence
```

Those rules are still rules, but they aim at the real boundary instead of choking the scene.

<div class="section-label">What stayed rough</div>

Fresh Session V1 improved the worst contamination, but it did not finish the job.

Still rough:

- default world snapshot can leak into fresh sessions
- default objects can appear without being established
- active plots can start stale
- threat severity is too weak
- time discipline still needs sharper wording
- device/prop agency rule overcorrected
- model quality may still depend heavily on provider choice

That last one matters. If the model is weak at instruction following, continuity, and nuance, the backend can only help so much. A cleaner payload gives the model a better chance, but it does not turn a weak model into a great writer.

Still, the backend had obvious cleanup left. Blaming the model first would be too easy.

The next move was to clean the prompt and the brief.

<div class="section-label">Next</div>

Fresh sessions got cleaner, but the next diagnosis was bigger.

Mnemosyne was becoming over-prompted.

The system prompt had accumulated too much mechanical language:

```txt
agency rules
device rules
time rules
attribution rules
psychology explanation
hidden-state schema
status reports
context priority
memory instructions
relationship stats
world snapshot
recent memories
recent chat
latest exchange
```

The model was being briefed, but also lawyered.

That is why the same model could sound more natural in a simpler Janitor-style setup and dumber inside Mnemosyne.

The engine should not bury the narrator under rules. It should brief the model, preserve continuity, and then let the character act.

So the next pass is Prompt Cleanup V2.

Not more restrictions.

Less machinery in the narrator's face.

Cleaner role.

Cleaner action doctrine.

Shorter prompt.

Better writing.
