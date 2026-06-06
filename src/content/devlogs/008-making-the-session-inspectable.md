---
number: "008"
title: "Making the Session Inspectable"
subtitle: "Visible chat export, payload history, and the first real state diagnosis."
slug: "008-making-the-session-inspectable"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "Visible chat export, payload history, and the first real state diagnosis."
tags:
  - mnemosyne
  - debugging
  - logs
  - payload
  - state
commits:
  - hash: "TBD"
    title: "Debug Log Export V1, visible chat export and LLM payload history"
    repo: "RhyGPU/mnemosyne"
---

Regenerate made bad outputs recoverable.

That helped, but recovery is not the same as diagnosis.

If the narrator gives a bad response, I can retry it now. I can fix the last response with instructions. I can stop one bad continuation from becoming the end of the test.

But that still leaves the bigger question:

Why did the response go bad in the first place?

Before this, debugging continuity was still too much guessing.

Maybe the model invented the detail.

Maybe the prompt caused it.

Maybe the World Log was stale.

Maybe the Soul carried old relationship state.

Maybe recent chat had the wrong anchor.

Maybe the visible scene looked fine, but the backend was feeding the model garbage.

I needed receipts.

Not vibes.

<div class="section-label">What changed</div>

This pass added exportable logs.

Two kinds.

The first was the visible chat log.

That is the clean transcript: what the user saw, what the narrator said, and nothing else. No hidden state. No backend payload. No debug junk. Just the readable RP conversation.

The second was backend payload history.

Not just the current payload in the inspector.

The actual history of what the app sent to the model over multiple turns.

That matters because a single payload snapshot is useful, but it is not enough. A consistency bug can build over several turns. A stale memory can enter the context once, then echo later. A world snapshot can be wrong from the beginning and keep poisoning the scene quietly.

So the app needed to remember its own model inputs.

Not forever as character memory.

As debugging evidence.

<div class="section-label">Why I touched this</div>

The immediate reason was consistency.

A character could suddenly change clothing. A scene could start in the wrong place. A new test could feel weirdly warm, like the character already trusted the user. The model could act like it was continuing an old emotional relationship inside a supposedly new setup.

Without logs, all of that is hard to prove.

You can argue with the output forever:

The model is dumb.

The prompt is bad.

The memory is stale.

The context is wrong.

The state engine failed.

Maybe all of those are partly true. But without records, it is just guessing.

So the next tool had to answer two questions:

```txt
What did the player see?
```

and:

```txt
What did the model receive?
```

Once both exist, a continuity bug becomes traceable.

<div class="section-label">Visible chat export</div>

The visible chat export is the story-facing record.

It should contain only the conversation as it appeared in the UI:

```txt
User:
...

Narrator:
...
```

No hidden state blocks.

No encoded payload tails.

No memory patches.

No provider metadata.

No token estimates.

No API data.

Just the RP transcript.

That is useful because sometimes I need to read the session like a normal scene. If the visible chat already contradicts itself, then the problem is in the narrative output. If the visible chat is clean but the next model response goes sideways, then the problem may be in the backend context.

That separation matters.

The visible log tells me what happened in the story.

The payload history tells me what the system told the model.

Those are not the same thing.

<div class="section-label">Payload history</div>

The payload history is the backend-facing record.

It should capture the actual final input used for generation:

```txt
provider
mode
model
base_url
system_message
user_message
context_text
estimated_system_tokens
estimated_user_tokens
estimated_total_tokens
created_at
```

The rule is hard:

Never store the API key.

Never export the API key.

Model name, provider, mode, and base URL are useful debugging metadata. The key is not.

The export should show multiple payloads, not only the latest one. That lets me check the progression of the session:

Did the stale object appear in Payload 1?

Did the relationship values drift in Payload 2?

Did the World Log start wrong?

Did a retry or fix response create duplicate context?

Did the model receive one version of the scene while the visible chat showed another?

That is the point.

The payload history turns the app from a black box into a record.

<div class="section-label">What got better</div>

The logging fix worked.

Now I could export the visible transcript and the backend payload history, then compare them.

That changed the debugging process immediately.

Before, I would look at a bad output and wonder what happened.

After, I could check:

- did the visible chat contain the contradiction?
- did the payload contain stale world state?
- did the context include old relationship values?
- did the model receive conflicting scene information?
- did the current user message get duplicated?
- did the backend send the right model and provider?
- did the app accidentally keep old scenario state?

The answer was no longer hidden.

That is a big shift.

It does not make the model smarter by itself.

It makes the failure inspectable.

<div class="section-label">The first diagnosis</div>

The logs did their job.

They showed the real problem.

The new test session was not actually clean.

The visible chat looked like a new scenario, but the backend payload still carried old state.

The character was entering a new setup with stale relationship values and stale world context. A scene that should have started cold could inherit warmth from an older scenario. A new situation could still carry location details from the previous one.

That explains a lot.

If a new scene starts with high trust and affection, the narrator will write the character too warmly.

If the World Snapshot still says the character is at the kitchen counter, the model will keep pulling the scene toward that location.

If old objects remain in key objects, the narrator may resurrect them even when the new scenario never introduced them.

That is not a retrieval problem yet.

That is not a clothing tracker problem yet.

That is not a reason to add a giant object system.

The logs showed something simpler:

Fresh sessions were not fresh enough.

<div class="section-label">Why this mattered</div>

This is exactly why I wanted logs before more architecture.

Without logs, the tempting fix would be to add more tracking.

Track clothes.

Track props.

Track objects.

Track scene state harder.

Track everything.

But that can become bloat fast.

The logs showed that the issue was not necessarily missing tracking. The issue was stale state leaking into a new test.

That is a different fix.

If the session starts dirty, adding more memory only gives the model more dirty context.

So the correct move is not:

```txt
Add more tracking.
```

It is:

```txt
Make new sessions actually start clean.
```

That is a better diagnosis.

And it only became obvious because the logs existed.

<div class="section-label">What stayed rough</div>

The payload history was useful, but still not perfect.

Multiple payloads can appear from retries, variants, and fixes. That is expected, but the export needs stronger metadata to make them easier to map back to the visible chat.

The next useful metadata would be:

```txt
message_id
variant_id
source: normal / regenerate / fix
selected: true / false
```

Without that, I can still inspect the payloads, but it takes effort to know which payload produced the currently visible narrator response.

That is not fatal.

It is just the next layer of debug hygiene.

The visible chat tells me what happened.

The payload history tells me what was sent.

The missing piece is a clean bridge between them.

<div class="section-label">What not to overbuild yet</div>

The logs also prevented another bad instinct.

A clothing issue showed up, but the answer should not be full outfit tracking right away.

Same with props.

Same with physical scene state.

A lightweight appearance pin might make sense later, something like:

```txt
[APPEARANCE CONTINUITY]
Current outfit: ...
Do not change outfit unless the user action or narrator event explicitly changes it.
```

But not before checking the payload.

If the payload already contains contradictory clothing state, fix the context.

If the payload is clean and the model still invents changes, then add a small continuity pin.

Inspect first.

Then build.

<div class="section-label">Next</div>

The logs worked.

And because they worked, they exposed the real next problem:

New sessions were not actually new.

The next fix is Fresh Session / Reset Scenario State.

Not full Scene State.

Not object tracking.

Not clothing tracking.

A smaller, cleaner boundary:

```txt
same persistent Soul continuity
```

or:

```txt
fresh scenario state
```

The user should be able to choose whether a new chat continues the existing Soul or starts with clean volatile state.

Relationship warmth, recent scene objects, stale location, active plots, and recent events should not leak into a new scenario unless the user wants continuity.

That is the next layer.

The session is inspectable now.

Next, it needs to start clean.
