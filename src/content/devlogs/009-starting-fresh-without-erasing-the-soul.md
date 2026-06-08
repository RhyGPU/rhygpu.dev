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

The logs worked.

That was the problem.

Once visible chat export and payload history existed, the bug stopped being a feeling. I could finally compare what the player saw against what the model received.

And the answer was ugly:

New sessions were not actually new.

A fresh test could look new in the chat window, but the backend still carried old scene state. The payload could still remember old relationship warmth, old location, old objects, and old active plots.

So the model was not always being stupid by itself.

Sometimes I was handing it a dirty brief and expecting a clean scene.

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

That distinction matters.

The Soul can persist. The character can still be the same person. Their long-term personality, core memories, trauma patterns, preferences, and emotional tendencies can remain.

But a scenario is different.

A new test should not automatically inherit:

- old location
- old key objects
- old active plots
- old recent events
- old relationship temperature
- old scene-specific emotional momentum

A character can be persistent without every new scene starting inside the last room.

That was the boundary I needed.

<div class="section-label">Why I touched this</div>

The test case was obvious.

A new debt collector or random threat scene should not inherit trust over 100, affection over 100, and a kitchen-counter setup from an earlier scenario.

If the payload tells the model:

```txt
Location: Aurora's kitchen counter
Key objects: wine glass, couch, phone
Relationship: high trust, high affection
```

then the model will write from that.

It will make the character warmer than she should be. It will pull the scene back toward the apartment. It will reuse the old phone or wine glass because the context says those objects matter.

That is not a mysterious LLM failure.

That is stale state.

The logs made that clear.

So the fix was not Memory Retrieval V1.

It was not object tracking.

It was not full Scene State.

The fix was simpler:

```txt
Make fresh sessions actually fresh.
```

<div class="section-label">Persistent Soul vs scenario state</div>

This became one of those boundaries that seems obvious after the bug exposes it.

The Soul is long-term character continuity.

Scenario state is current-session continuity.

They should not be the same reset lever.

If I delete all Soul continuity every time I start a fresh scene, the character becomes shallow again. That defeats the point of Mnemosyne.

But if I preserve every scene detail forever, the character gets haunted by old tests. Every new scene starts with leftover objects, stale relationship warmth, and active plots that no longer belong.

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

That lets the character remain herself without forcing every new test to continue the last setup.

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

Unless the user chooses persistent continuity.

That last part is important.

Sometimes I want the relationship to continue. Sometimes I want a fresh test with the same character but not the same relationship state.

Those are different user intentions.

The UI should make that visible:

```txt
Using persistent Soul continuity
```

or:

```txt
Fresh scenario state
```

The model should not have to guess what kind of session this is.

The user should know.

The engine should know.

The payload should reflect it.

<div class="section-label">What got better</div>

The first fix helped.

The relationship state no longer started completely insane in fresh tests. Instead of carrying huge trust and affection values from old scenes, the new session started closer to neutral.

That mattered immediately.

A cold or threatening opener should not inherit romantic warmth by default. A character facing a dangerous stranger should not behave like she is continuing a vulnerable kitchen scene.

The payload became less contaminated.

The visible chat export still worked.

The payload history still worked.

The app could now prove that the relationship reset was moving in the right direction.

That was progress.

Not complete, but real.

<div class="section-label">What still failed</div>

The world snapshot was still not clean enough.

Even after the relationship reset improved, fresh sessions could still carry the default Aurora apartment setup:

```txt
Location: Aurora's kitchen counter
Active plots: Establish the first scene
Key objects: Half-empty wine glass; Couch with rumpled blankets; Phone
```

That meant the fresh session was only half fresh.

The relationship was cleaner, but the setting still dragged the model back into the default scenario.

That explains why a random opener could still become kitchen-counter based.

The user says something broad, the model looks at the payload, and the payload says Aurora is basically in her apartment with wine, couch, and phone.

So the model follows the brief.

Again, not pure model stupidity.

Dirty context.

<div class="section-label">Threat severity</div>

The fresh session test also exposed another state problem.

Threat scenes were not scaling hard enough.

Trust could drop, but fear stayed too low. A scene could describe Aurora as terrified or cornered, while the numeric state still treated fear like a mild concern.

That mismatch matters.

If the state says fear is low, the next prompt may soften the character too quickly. If affection or desire remain active in a violent threat context, the narrator can start writing emotional tones that feel completely wrong.

A threat should not only reduce trust.

It should push fear hard.

It should suppress romance-adjacent values unless the scene strongly justifies otherwise.

That does not need a giant trauma system yet.

It just needs the state engine to respect severity.

<div class="section-label">Time and POV still leaked</div>

The same tests also showed smaller prompt issues.

Time discipline still failed. The narrator invented concrete durations even when the user or World Log never established them.

That kind of detail sounds natural in prose, but it is dangerous for continuity.

If the system does not know the duration, the narrator should not make one up.

The rule needs to be shorter and harder:

```txt
Never invent concrete durations.
Do not say minutes, hours, days, or years passed unless the user or World Log established it.
```

There was also mild POV leakage.

The narrator could write as if it knew exactly what the user felt, saw, or aimed. Sometimes that is a reasonable inference. Sometimes it crosses into controlling the user.

The better rule is not to make the narrator timid.

The better rule is:

```txt
Describe what the character perceives.
Do not claim the user's internal experience or exact action unless the user gave it.
```

<div class="section-label">The overcorrection</div>

This is where I made a wrong turn.

To stop the narrator from controlling the user's device, a device/prop agency rule got added.

The intention made sense.

If the user shows a phone, the narrator should not decide that Aurora takes it, unlocks it, searches it, and reads everything unless the user allows that.

But the rule was too rigid.

It made the narrator cautious around phones and props in general. Worse, it started pushing against the thing I actually wanted: a character who can act.

Aurora should be allowed to use her own phone.

She should be allowed to reach for things.

She should be allowed to interrupt, step forward, grab for something, refuse, challenge, retreat, escalate, or use her own environment.

The problem is not character action.

The problem is resolving the user's reaction without permission.

That is the real boundary.

Good:

```txt
Aurora lunges for the phone, fingers closing toward the edge of the screen. "Give me that."
```

Bad:

```txt
Aurora takes the phone from his hand, unlocks it, scrolls through the messages, and reads everything.
```

The first one creates pressure.

The second one steals the user's response.

That distinction matters more than a blunt device rule.

<div class="section-label">What this taught me</div>

This pass exposed a pattern.

When the model behaves badly, the tempting fix is to add another restriction.

Do not touch the phone.

Do not infer objects.

Do not invent time.

Do not move too much.

Do not act too strongly.

But too many rules make the narrator worse.

The model starts writing like it is filling out a compliance form instead of writing a living character.

That is not Mnemosyne.

The engine should make the narrator smarter, not more timid.

The right fix is usually a cleaner boundary, not a bigger cage.

For fresh sessions, the boundary is:

```txt
persistent Soul continuity vs fresh scenario state
```

For action, the boundary is:

```txt
character may act, but user reaction stays with the user
```

For time, the boundary is:

```txt
concrete duration requires evidence
```

Those are cleaner than piling up mechanical restrictions.

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

That last one matters too.

If the model is weak at instruction following, continuity, and nuance, the backend can only help so much. A cleaner payload gives the model a better chance, but it does not turn a weak model into a great writer.

Still, the backend had obvious cleanup left.

So the next move was not to blame the model first.

It was to clean the prompt and the brief.

<div class="section-label">Next</div>

Fresh sessions got cleaner.

But the next diagnosis was bigger:

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

The engine should not bury the narrator under rules.

It should brief the model, preserve continuity, and then let the character act.

So the next pass is Prompt Cleanup V2.

Not more restrictions.

Less machinery in the narrator's face.

Cleaner role.

Cleaner action doctrine.

Shorter prompt.

Better writing.
