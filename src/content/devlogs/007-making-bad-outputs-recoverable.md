---
number: "007"
title: "Making Bad Outputs Recoverable"
subtitle: "UX comfort, regenerate/fix response, and the road to real branching."
slug: "007-making-bad-outputs-recoverable"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "UX comfort, regenerate/fix response, and the road to real branching."
tags:
  - mnemosyne
  - ux
  - regeneration
  - correction
  - branching
commits:
  - hash: "a543e1c"
    title: "Improve chat navigation and payload copy feedback"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/a543e1c8651dbb9149716081fddfc1c0bc18ca65"
  - hash: "13f8dbe"
    title: "Anti-replay retry payload metadata fix"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/13f8dbe177655a66f408d7c40cc9c90640394634"
---

After the payload cleanup, the backend finally looked stable enough to breathe.

The latest exchange was being fed from the right end of the previous narrator response. Recent chat was lower priority. The payload inspector was no longer misleading me. The model was finally seeing the right anchor more often.

The obvious next backend task looked like Memory Hygiene V2.

Less duplicate memory.

Less irrelevant memory.

Better retrieval.

That was all good.

But it was not the thing making the app uncomfortable to use.

The problem was simpler:

The app still made it annoying to recover from bad outputs.

And bad outputs are not going away.

<div class="section-label">What changed</div>

This pass shifted from backend memory to app comfort.

First came the small friction fixes:

- keep Return to Library visible while scrolling
- make the chat header sticky
- show feedback when copying the LLM payload

Small stuff.

But small stuff matters when the app is something I actually use.

If I have to scroll to the top just to leave a chat, that is friction. If I click Copy LLM Payload and get no feedback, I have to wonder whether it worked. If the app feels annoying during testing, I will avoid testing it.

That is bad for the project.

So the next feature was not smarter memory.

It was making the app less irritating.

Then came the bigger comfort feature:

Regenerate / Fix Last Response.

Because even with better context, the narrator can still mess up.

It can repeat a scene beat.

It can misread who said what.

It can invent time.

It can continue from the wrong emotional tone.

It can give an answer that is almost good, but wrong in one specific way.

The app needed a fast correction loop.

<div class="section-label">Why I touched this</div>

The payload fixes made the system more stable, but they did not make the model perfect.

That is the important difference.

A better context compiler can reduce failure.

It cannot eliminate LLM behavior.

So the question changed again.

Not:

> How do I prevent every bad response?

But:

> What happens when a bad response appears?

Before this, the answer was ugly. I had to manually retry, edit around the problem, or keep pushing the scene forward and hope it recovered.

That is not good enough for long-form RP.

The user needs to be able to say:

```txt
Regenerate this.
```

or:

```txt
Fix this response.
Do not replay the phone reveal.
Continue from the kitchen.
```

without destroying the session.

That is the real product need.

<div class="section-label">UX Comfort Pass</div>

The first comfort pass was intentionally small.

The Return to Library button needed to stay visible. I should not have to scroll back to the top of a long RP session just to leave the chat.

The payload copy button needed feedback. If I copy the LLM payload, the app should confirm it.

Not with a giant modal.

Just:

```txt
Copied!
```

or:

```txt
Payload copied.
```

Then it disappears.

That is not a deep feature. It is just basic usability.

But it made the app feel less like a prototype and more like something I could keep open while debugging.

The rule was simple:

Do not touch the backend.

Do not change hidden state.

Do not change provider behavior.

Just reduce friction.

<div class="section-label">Regenerate</div>

Regenerate is the first real recovery tool.

The behavior is simple:

The latest user message stays the same.

The app asks the model for a new narrator response.

The old narrator response gets replaced, or at least clearly treated as discarded.

V1 does not need full branching yet.

That matters because full branching is a different system. Regenerate is a practical fix. It gives me a way to recover from a bad continuation without building a whole timeline tree immediately.

The point is speed.

If the model gives a bad answer, I should not have to repair the whole session manually.

Click regenerate.

Get another attempt.

Move on.

<div class="section-label">Fix with instruction</div>

Regenerate is useful when the answer is generally bad.

Fix with instruction is useful when the answer is close.

Sometimes the model gets the tone right but repeats an old scene beat. Sometimes it writes well but invents time. Sometimes it understands the relationship but forgets the physical state.

In that case, I do not want a blind reroll.

I want to tell it what went wrong.

Example:

```txt
Continue from the kitchen.
Do not replay the phone reveal.
Keep the same emotional beat.
```

That instruction should be high-priority for the next generation.

But it should not become permanent memory.

That is important.

A correction instruction is not character history. It is not Soul memory. It is not a world event. It is a temporary repair command for the next response.

If the app stores it as memory, the system gets polluted.

So Fix with Instruction has to live in a separate category:

```txt
temporary correction context
```

not:

```txt
character memory
```

<div class="section-label">State safety</div>

This feature is not just UI.

The dangerous part is hidden state.

If the model already produced a response, that response may have also produced a hidden-state patch. It may have updated memory, relationship state, world state, or recent events.

If I regenerate and the app simply applies another hidden-state patch on top, the discarded response still affects the Soul.

That is bad.

It means a response I rejected can still change the character.

So regenerate needs state safety.

The preferred behavior is:

```txt
Before generation:
save a snapshot

If regenerating:
restore snapshot
remove or replace old assistant response
generate again
apply only the accepted replacement
```

That is the real difference between a chat UI gimmick and a memory engine feature.

In a normal chatbot, regenerate just means “give me another answer.”

In Mnemosyne, regenerate also means:

> Do not let rejected state become canon.

<div class="section-label">What got better</div>

Bad outputs stopped being dead ends.

That is the real improvement.

Before this, a wrong narrator response created pressure. Either accept it and continue, or manually fight the system.

After this, there is a correction loop.

The model can fail.

The user can push back.

The app can try again.

That makes the whole project more usable.

It also changes how testing feels. I no longer need every response to be perfect. I need the app to make recovery cheap.

That is a healthier expectation for an LLM-based RP engine.

<div class="section-label">What is still rough</div>

This is still not true branching.

That became obvious immediately.

Regenerate / Fix Last Response works for the latest output. But if I go back to an older assistant response and choose a different version, the later messages still belong to the old timeline.

That is not a branch.

That is just response variant selection.

A real branch means each response choice owns its own future.

Something like:

```txt
User 1
  Assistant 1A
    User 2A
      Assistant 2A

User 1
  Assistant 1B
    User 2B
      Assistant 2B
```

If I choose Assistant 1B, the app should not keep showing the later messages from Assistant 1A’s timeline as if nothing changed.

That needs a branch model.

Not just variants.

<div class="section-label">The next problem</div>

The next issue was not only branching.

It was logs.

A consistency issue showed up, and the right move was not to immediately add more tracking.

That would be another overbuild.

The better move was to inspect the evidence first.

I need two kinds of logs:

```txt
visible chat export
```

Only what the user sees. No hidden state. No engine junk. Just the readable RP transcript.

And:

```txt
backend payload history
```

The actual LLM inputs over time, not only the current payload.

That matters because consistency bugs can come from many places:

- character profile
- latest exchange
- status block
- memory section
- world snapshot
- model invention

Before adding more tracking, I need to know which layer is causing the contradiction.

That is the same lesson as the payload inspector.

Inspect first.

Then build.

<div class="section-label">Next</div>

Next is making the session inspectable.

Regenerate makes bad outputs recoverable.

But branching and consistency debugging need better records.

The next layer should export:

```txt
visible chat log
backend payload history
```

Then the app can answer the question that keeps coming back:

```txt
Did the model invent this,
or did we feed it conflicting state?
```

That has to come before full branch timelines.

Bad outputs are recoverable now.

Next, the session needs to become inspectable.
