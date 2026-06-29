---
number: "010"
title: "Prompt Cleanup V2"
subtitle: "Less machinery in the narrator's face, cleaner action doctrine, and the first UI-flow reset."
slug: "010-prompt-cleanup-v2"
project: "Mnemosyne"
date: 2026-05-29
status: "published"
summary: "How Mnemosyne moved from adding more prompt rules to cleaning the narrator brief, preserving character agency, and separating player paper UI from terminal dev machinery."
tags:
  - mnemosyne
  - prompt-cleanup
  - narrator
  - ux
  - state-map
  - dev-console
commits:
  - hash: "TBD"
    title: "Prompt Cleanup V2 and UI flow reset"
    repo: "RhyGPU/mnemosyne"
---

Fresh sessions fixed one kind of contamination.

They did not fix the bigger pattern.

By this point, Mnemosyne had a lot of correct machinery: Soul continuity, World Log, recent events, relationship pressure, latest exchange priority, payload inspection, visible chat export, payload history, regenerate, and fresh scenario state.

The backend was getting smarter.

The narrator prompt was getting worse.

<div class="section-label">What changed</div>

This pass was the first time the answer was not another rule.

The system prompt had become a pile of defensive instructions:

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

Each rule had a reason. None of them were random.

A rule existed because the model had once stolen the user's action. Another existed because it invented elapsed time. Another existed because it touched the user's phone too aggressively. Another existed because it confused narrator prose with user dialogue. Another existed because stale world state poisoned a new scene.

The problem was that all of those local fixes were now competing with the core job:

```txt
Write the next scene well.
```

The model was being briefed, but it was also being lawyered.

<div class="section-label">Why I touched this</div>

The most revealing comparison was outside the app.

A simpler Janitor-style setup could sometimes produce more natural prose than Mnemosyne, even when Mnemosyne had better state. That was uncomfortable, because the whole point of Mnemosyne was not to make the model worse in exchange for continuity.

That told me the bug was not only memory.

It was presentation.

The engine had useful context, but it was throwing too much machinery into the narrator's face. The narrator was not only receiving a scene brief. It was receiving a legal document, a psychology note, a state schema, a continuity checklist, and a debugging protocol all at once.

The character stopped feeling careful.

She started feeling constrained.

<div class="section-label">The wrong instinct</div>

The wrong instinct was to keep adding narrower prohibitions.

```txt
Do not touch the phone.
Do not infer objects.
Do not invent time.
Do not move too much.
Do not act too strongly.
Do not control the user.
Do not change state too aggressively.
```

That kind of prompt can stop some failures.

It also sedates the narrator.

A living character needs to be able to act. She should be able to reach, interrupt, refuse, challenge, retreat, escalate, hesitate, grab for her own phone, or use the room around her.

The real boundary is not:

```txt
The character must not act.
```

The real boundary is:

```txt
The character may act.
The user's response belongs to the user.
```

That is a cleaner doctrine.

<div class="section-label">Action doctrine</div>

The device rule exposed the distinction.

Bad:

```txt
Aurora takes the phone from his hand, unlocks it, scrolls through the messages, and reads everything.
```

That resolves the user's side of the interaction. It steals the result.

Good:

```txt
Aurora lunges for the phone, fingers closing toward the edge of the screen. "Give me that."
```

That creates pressure. It gives the character agency. It still leaves the user room to pull back, let go, resist, speak, or change the scene.

So the prompt needed fewer object-specific bans and more general action law:

```txt
Portray decisive character attempts.
Do not resolve the user's reaction.
Describe what the character perceives.
Do not claim the user's internal state unless the user gave it.
Concrete time requires evidence.
```

Those rules are shorter, broader, and closer to the real boundary.

<div class="section-label">Prompt cleanup</div>

Prompt Cleanup V2 meant separating the narrator brief from the engine internals.

The narrator needs:

```txt
role
scene state
character state
relationship pressure
relevant memory
latest exchange
current user message
action doctrine
```

The narrator does not need every piece of mechanical explanation every turn.

It should not be forced to read a long lecture about the whole architecture before writing a single response. The state engine can remain strict underneath. The visible prompt can be calmer.

That became the new direction:

```txt
Less machinery in the narrator's face.
More useful state in the right place.
Cleaner hierarchy.
Shorter rules.
Better writing.
```

<div class="section-label">What this did not mean</div>

This was not giving up on structure.

Mnemosyne still needs state. It still needs memory routing. It still needs relationship deltas, world snapshots, payload logs, and repair tools. The lesson was not that prompts should be vague.

The lesson was that the narrator prompt and the developer/debug machinery are different surfaces.

The model should receive the smallest useful brief that preserves continuity and behavior.

The developer should be able to inspect the full machinery somewhere else.

That distinction became a UI problem too.

<div class="section-label">The UI-flow reset</div>

Around the same time, the interface problem became obvious.

The current UI worked, but it looked like a dense control panel. Too many buttons, too many backend concepts, too much machinery visible at once. That matched the prompt problem almost perfectly.

The product was doing the same thing in two places:

```txt
The prompt showed too much machinery to the narrator.
The UI showed too much machinery to the player.
```

The mock UI helped, but not because it was a complete product spec. It did not know Mnemosyne's actual features. It invented some things, flattened others, and missed parts of the real app.

Its useful lesson was flow.

One surface should not do every job.

<div class="section-label">Paper and terminal</div>

The visual split became clear:

```txt
Player-facing fiction: paper / book / editorial-lite.
Developer and GM machinery: terminal.
```

Paper fits the story layer. It makes the transcript, Soul view, and records feel like reading, journals, dossiers, and case files. It also makes redaction natural. Hidden knowledge can appear as blacked-out text in reader/god modes instead of looking like a broken app.

Terminal fits the machine layer. The Dev console, payload trace, pipeline stages, benchmark output, and raw diagnostics should feel like the back room. That is where the engine can be explicit without contaminating the fiction surface.

This is the same architectural split expressed visually:

```txt
Soul / Play / readable records = paper.
Pipeline / payload / repair / debug = terminal.
```

<div class="section-label">State Map without spoiling the story</div>

The State Map needed the same treatment.

A full state view is useful, but not every user should see every field in every mode. A player in realistic mode should not get a god-view of secret beliefs, hidden knowledge, or offscreen plot truth. That spoils the story.

So State Map became a visibility problem, not a deletion problem.

The backend keeps the state.

The mode decides how much is visible:

```txt
Realistic: omit hidden knowledge entirely.
Reader: redact sensitive fields with optional reveal.
God / GM / Dev: show the full machine-readable truth.
```

Omit and redact are not the same.

If realistic mode shows `misbelieves — censored`, it still leaks that a secret exists. In realistic play, even the existence of the hidden field may be too much. In reader mode, the redaction is part of the pleasure. In god mode, the whole map is allowed.

That made the mock's State Map idea usable without turning solo immersive RP into a spoiler dashboard.

<div class="section-label">What got better</div>

The direction became cleaner.

Prompt side:

```txt
Do not add more cages.
Clarify the actual boundary.
Keep the narrator brief compact.
Move debug machinery out of the narrator's face.
```

UI side:

```txt
Do not make one mega-control-panel.
Split by user intent.
Let Play read like a book.
Let records read like dossiers.
Let Dev look like a terminal.
```

The same design law applied to both:

```txt
The fiction surface should feel alive.
The machine surface should be inspectable.
Do not confuse the two.
```

<div class="section-label">What stayed rough</div>

This did not finish the product.

It created a clearer direction, but the actual app still needed hard work:

- State Map had to render real loaded Soul/session data, not mock data.
- Library and Workshop had to preserve every existing creation/editing feature.
- Settings needed to become a real page, not just a drawer.
- Play needed a calm pipeline indicator without turning into Dev mode.
- Home needed a clear Continue flow and honest shelves.
- Redaction needed to be mode-aware instead of just decorative.
- Dev needed to stay reachable without overwhelming normal play.

The important part was the standard:

```txt
No fake mock-data victory.
No pretty UI that lies about what the backend can do.
No hiding real features just to make the screen calmer.
```

The mock was inspiration.

The real app was the source of truth.

<div class="section-label">Next</div>

The next work is not one single feature.

It is convergence.

The engine needs to keep becoming safer and more inspectable: restore tools, provenance, memory inspector, better retrieval, entity separation, and payload timing.

The interface needs to expose that power without dumping the machinery on the player.

So the next product direction is:

```txt
Paper for play.
Editorial-lite for records.
Terminal for Dev.
Real State Map data.
Mode-aware redaction.
Feature parity before polish.
```

Mnemosyne should not become a prettier control panel.

It should become a readable fiction surface with a serious engine underneath.

That is the actual cleanup.

Not only shorter prompts.

A cleaner boundary between story and machine.