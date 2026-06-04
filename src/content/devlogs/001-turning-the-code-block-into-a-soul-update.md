---
number: "001"
title: "Turning the Code Block Into a Soul Update"
subtitle: "The status block stopped being a summary and started looking like a packet."
slug: "001-turning-the-code-block-into-a-soul-update"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "How the crude code block started becoming an update packet for a human-like Soul system."
tags:
  - mnemosyne
  - soul
  - memory
  - psyche
commits: []
---

After the Soul.md idea hit, I started looking at the crude status block differently.

Before that, it was just a workaround. A code block at the end of the chat, holding whatever the model needed so the next reply did not lose the scene.

Then the shape changed.

> The code block could be an update packet.

The AI did not need to carry the whole character inside normal prose. It could write the scene, then report what changed. Another layer could read that report and update the Soul.

That was the first useful split in my head:

> The narrator writes what happened.
>
> The packet reports what changed.
>
> The Soul absorbs the change.

<div class="section-label">The packet idea</div>

The original block tracked status, scene information, memories, atmosphere, physical condition, sensory details, and position. That was enough to prove the basic point.

But if it was going to feed a Soul, it needed more than facts.

It needed to say what the scene did to the character.

Not just:

> She is scared.

But why. What caused it. Whether it was new or familiar. Whether it touched an old wound. Whether it raised distrust, reinforced a pattern, or should fade after the moment passed.

That was when the block stopped feeling like a summary. It started feeling like a bridge between narration and persistent character state.

<div class="section-label">Building the psyche</div>

The next question was what the Soul should actually contain.

A list of facts was not enough. That would make the same mistake again, only with cleaner formatting. Facts can say what happened. They do not say what the character became because of it.

So I started treating the character less like a bot and more like a psyche.

I asked DeepSeek to help research psychology, memory, emotional states, and how people retain or lose experiences. I was not trying to pretend this was neuroscience. I was trying to build a usable foundation for believable character change.

The early variables were simple, but they gave the system a shape:

- Trust
- Fear
- Shame
- Affection
- Openness
- Attachment
- Desire
- Resolve

Those axes mattered because they are not interchangeable. Trust is not affection. Fear is not shame. Desire is not commitment. A character can warm up to someone and still not feel safe with them.

<div class="section-label">Memory with meaning</div>

The memory side had the same problem.

People do not remember everything equally. They remember what hurt, what comforted them, what broke an expectation, and what touched a need or fear. They forget boring repetition, but repetition can still become a pattern if it changes how they see the world.

A repeated meal is forgettable. Repeated kindness can become trust. Repeated silence can become abandonment.

So forgetting could not just be a timer.

It needed meaning.

The packet had to flag moments based on salience: emotional shift, broken expectation, important decision, core fear, core desire, relationship pressure.

The Soul would not save everything. It would keep what changed the character.

<div class="section-label">Character card vs Soul</div>

The more I worked through it, the less the Soul felt like a character card.

A character card says:

> This is who the character is.

A Soul says:

> This is what the character has become.

That distinction became the foundation.

A static prompt can describe someone as guarded. A Soul can carry why they became guarded, what weakens that guard, what reinforces it, and which memories still shape their reactions.

That is why the packet mattered. It was the first mechanism for turning a scene into a change.

<div class="section-label">What this set up</div>

I did not have the final app yet.

I did not have the full engine.

But I had the shape of the problem.

> The AI should not be trusted to remember everything by itself.

It should describe the scene and report candidate changes. The Soul should decide what those changes mean.

That moved Mnemosyne away from prompt engineering and toward an actual system.

The prompt was still there. The code block was still there. But now I was designing the thing that would read it.
