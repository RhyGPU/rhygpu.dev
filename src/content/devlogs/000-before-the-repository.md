---
number: "000"
title: "Before the Repository"
subtitle: "I got tired of AI RP forgetting what mattered."
slug: "000-before-the-repository"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "The origin of Mnemosyne, before the repo, the roadmap, and the app."
tags:
  - mnemosyne
  - origin
  - ai-rp
  - memory
commits: []
---

Mnemosyne started before the repo, before the roadmap, and before the app.

It started with AI RP scenes that could write drama, but could not live through drama properly. Trust moved too fast. Fear disappeared when the scene needed convenience. A character could go through something heavy, then act like the emotional cost had already been paid off three messages later.

At first I did not think I needed software.

I thought I needed a better prompt.

<div class="section-label">The crude block</div>

My first workaround was a code block at the end of the chat.

It tracked the current scene, status, atmosphere, character position, physical condition, sensory details, and whatever memories seemed important enough to carry forward.

It was ugly. It was manual. It was not an engine. It was just a compact state tracker duct-taped to the bottom of a roleplay.

But it worked better than nothing.

That was the annoying part.

If a crude status block could improve continuity, then the problem was not only bad writing. The problem was that the AI had no reliable structure for carrying the scene forward.

<div class="section-label">What felt wrong</div>

JanitorAI, Character.AI, and similar platforms all had the same weakness in different forms. Memory was unreliable. Platform summaries were hit or miss. The system could remember random details and miss the moment that actually changed the character.

SillyTavern gave more control and could handle memory better if you were willing to configure it, feed it lore, manage context, and burn tokens. That was better, but it still did not solve the part I cared about.

Remembering more is not the same as feeling more human.

A character can have a longer context and still feel hollow. The model can drag a bigger pile of text behind it and still fail to understand which detail should hurt, which one should soften trust, and which one should fade.

<div class="section-label">The actual problem</div>

The first real break came from looking back at my own RP tests.

The progression was too sudden. The AI jumped to the next interesting emotional state because that made the current scene easier to write. It did not make the character earn the change.

I did not want a better transcript summary.

I wanted a system that could track whether a character had actually changed.

> Make the AI remember like a character, not like a transcript.

That meant emotional variables had to be separate. Trust is not love. Fear is not shame. Affection is not commitment. A character can like someone and still distrust them. They can feel safe in one room and terrified in another.

Some moments should stick forever because they hit the right nerve. Whole stretches of normal conversation should fade because nothing actually changed.

<div class="section-label">The Soul.md moment</div>

I was already using manual summaries because I did not trust platform auto-summaries. I would copy a whole chat, paste it into DeepSeek, and make it summarize the session myself. That worked better, but it proved the same point again: the platform memory was not enough.

Then the Soul.md idea hit.

I do not remember it as some grand technical revelation. It was more like a simple shape snapping into place.

> The character's inner continuity could live in a file.

Not a perfect engine. Not a finished architecture. Just a living file that could carry scars, preferences, memories, trust, fear, and the slow changes that happen after enough scenes.

The crude code block stopped looking like only a hack. It started looking like the first ugly version of a Soul file.

> A narrator writes the scene.
>
> A Soul remembers what mattered.

That was the point where Mnemosyne stopped feeling like a better prompt and started feeling like something I could build.
