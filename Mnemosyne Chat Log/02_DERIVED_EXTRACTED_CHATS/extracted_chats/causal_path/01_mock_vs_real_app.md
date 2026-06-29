# 01. Mock vs Real App

Source messages: `001` to `012`
Time span: `2026-06-26T14:44:04.740Z` to `2026-06-26T15:14:29.597Z`

## Why This Chunk Exists

The user asks to compare the current Mnemosyne UI with the uploaded design handoff. The first causal fork is that the mock has a strong flow, but it was made without knowing the real app.

## Decisions / Causal Facts

- Current app is functional but reads like a dense settings/control panel.
- Mock is not a reliable implementation spec by itself; it is a vision of UX flow and atmosphere.
- Real app concepts are Souls, Settings/Worlds, Sessions, Editor/Workshop, Chat, Settings drawer, and richer backend state.

## Bridge To Next Chunk

This leads to the user clarifying that the skin itself is not the goal. The desired thing is the mock's easier, more intuitive UX flow, adapted to the actual app.

## Raw Messages In This Segment

### 001. USER | 2026-06-26T14:44:04.740Z

`uuid: a7cbec25-3db0-461f-bf71-c2473127cfe7`

<uploaded_files>
<file><file_path>C:\Users\T-ROBOTICS\AppData\Roaming\Claude\local-agent-mode-sessions\5e07596b-7436-46f1-8ec4-f9d42f21dc8a\ea1dab66-1c27-4a7e-bc56-f1dd2a113ddc\local_0f147b87-079c-450e-a003-4f0a0c6dd81b\uploads\Mnemosyne_ AI roleplay state engine-handoff.zip</file_path><file_uuid>8e882bc4-5bff-4773-859d-8649fcb4b23c</file_uuid></file>
</uploaded_files>

I don't like the current ui design. Compare the current UI and the UI exmaple zip file and lets talk

---

### 002. ASSISTANT | 2026-06-26T14:44:08.277Z

`uuid: ce1c68c9-26d0-45b1-b875-91ee8db3f7ff`

Let me look at both the uploaded example and your current project.

---

### 003. ASSISTANT | 2026-06-26T14:44:16.897Z

`uuid: 0b528d02-1f6f-436f-b903-3f12f604a81e`

Let me extract the zip and look at the current UI source.

---

### 004. ASSISTANT | 2026-06-26T14:44:25.415Z

`uuid: 37548597-6154-4952-8353-7d9b991e3e38`

The example is a single-file HTML mockup. Let me look at it, the current screenshot, and the current UI code.

---

### 005. ASSISTANT | 2026-06-26T14:44:32.588Z

`uuid: ac72e78a-dcec-413c-95d7-04673bb9a204`

Let me read the design mockup and the current UI source.

---

### 006. ASSISTANT | 2026-06-26T14:44:36.457Z

`uuid: 10881082-9b4b-4e25-a704-0bde05306d9e`

I'll copy the extracted files into the workspace folder so I can read them.

---

### 007. ASSISTANT | 2026-06-26T14:44:48.356Z

`uuid: 95222776-2984-40f0-8c5c-522d7faee219`

This is a rich, fully-realized design. Let me see the rest of it and the current app's main component.

---

### 008. ASSISTANT | 2026-06-26T14:44:53.645Z

`uuid: d75b612c-8a0e-4be7-b1a5-ea5f98a636d8`

Now let me see the current UI's actual structure to compare.

---

### 009. ASSISTANT | 2026-06-26T14:45:24.586Z

`uuid: c1d18965-79ed-47c1-b724-f1a57a09bf7e`

I've read both in full. Here's how they compare.

**The gist:** your current UI is a *light, dense control panel* — one long scroll of stacked cards (Launcher → World → Primary Character → Ready → Active Chats), each crammed with button rows (New / Import / Export / .mne / Save / Archive…). It's functional but reads like a settings screen. The mockup is a *dark, literary app* organized around a left nav rail with five distinct destinations: Campaigns, Play, State Map, Characters, Settings.

Where they diverge most:

**Aesthetic.** Current: cream/white, system sans, utilitarian. Mockup: warm dark (`#1a1714`), Spectral serif for prose, IBM Plex Mono for labels/metadata, a single orange accent (`#d98a5a`). The mockup treats the fiction as the product — prose is set like a book; chrome recedes.

**Structure.** Current collapses everything onto one launcher you scroll. Mockup splits by *intent*: a Home that surfaces "Continue" + a campaign grid, a clean Play view (transcript + composer + per-turn token/cost line), and separate management screens. Far less visible at once, much less button soup.

**The State Map is the real differentiator.** The mockup has a whole screen the current UI doesn't: Scene State, Characters (knows / misbelieves), Relationships (signed trust/fear/affection bars), Objects, Timeline, and a Memory Inspector with provenance — every memory traces to the turn and the evidence quote that created it, with pin/invalidate. That visualizes what your engine actually does. Right now that's invisible.

**Dev mode.** Current has a "Dev Console" button up top. Mockup folds dev into Play as a green CRT terminal with a live pipeline rail (SEND → CONTEXT → NARRATOR → GUARD → EVALUATOR → PATCH → REPAIR → COMMIT) and a command line.

**Action density.** Current exposes every export/import/archive button inline. Mockup hides those in Settings/menus and keeps the main surfaces calm.

One caveat: the screenshot I have shows only the Launcher (top of the current app). My read of the current app's *visual language* is solid, but if there are other current screens you want weighed in, point me at them.

So — what do you want to do with this? A few directions:

- **Adopt the mockup wholesale** (dark literary + nav rail + State Map) as the target and plan a migration.
- **Cherry-pick** — e.g. keep your current flow but steal the State Map + dark theme.
- **Just the visual reskin** (colors/fonts/spacing) without restructuring navigation.

Which way are you leaning, and is there anything in the current UI you specifically *don't* want to lose?

---

### 010. USER | 2026-06-26T15:13:22.129Z

`uuid: 9dcdef9b-0418-413f-bd3a-d8a5772d7643`

Idk. we need to discuss this. I personally am applealed to the zip file ver but honestly my project UI tells me im not there yet. Cause the zip file didn't have any context of the project when working on it.

---

### 011. ASSISTANT | 2026-06-26T15:13:36.282Z

`uuid: 417b7fd3-e940-448b-853f-6536a1685bbb`

You've put your finger on the real tension, so let me ground it rather than guess. The mockup is a *vision* drawn without knowing what your engine actually does today — it invented campaigns, a State Map full of relationship bars, memory provenance, a dev pipeline. The useful question isn't "is it pretty" (it is) but "how much of what it shows is real in your project right now, and how much is fiction the UI is writing checks for." Let me check what actually exists.

---

### 012. ASSISTANT | 2026-06-26T15:14:29.597Z

`uuid: 4d7ca5bf-4523-4310-9d08-d12483d38958`

That instinct is right, and now I can make it concrete. I looked at what your project actually is under the hood, and the mismatch isn't really "my UI is behind the mockup" — it's that the mockup was drawn against an *imagined* product that's both ahead of yours in some places and behind it in others.

Here's the actual map. Your real app has three views — **Library** (the launcher in your screenshot), **Editor** (workshop), **Chat** — plus a Settings *drawer* with ai/chat/dev tabs. Your core concept is the **Soul** (mentioned 581 times) — core/recent memories, avatar, continuity. That's your screenshot's "1 core / 0 recent / no av…". You already have relationships, variants, checkpoints, snapshots, a live dev terminal, benchmarks, and session repair.

The mockup, meanwhile, talks about **campaigns**, **evaluators**, a token/cost meter, and memory **provenance with evidence quotes** — and your codebase has *zero* of those words. So the mockup is three different things stacked together, and the trick is to stop treating it as one decision:

**1. The skin — take it today, no risk.** Dark `#1a1714`, Spectral serif for prose, Plex Mono for labels, the single orange accent. This is pure visual language. It doesn't assume any feature you don't have. This alone would close most of the gap you're feeling, and it's the cheapest thing on the list.

**2. The State Map — the one genuinely worth building.** This is the mockup's best idea *and* you already have the data for it: memories, core/recent, relationships, scene, continuity all exist. You just have no screen that shows them. This is where the mockup is legitimately pulling you forward, not writing fiction.

**3. The fiction — leave it until the engine backs it.** The token/cost line, the evidence-quote provenance, the "evaluator" naming — those are the parts that made you feel "I'm not there yet." You're right not to build UI that promises them before they're real, because then the interface lies.

And one thing worth saying plainly: in places **your project is more sophisticated than the mockup.** The mockup flattens your "Soul + continuity" idea into a generic "character," and your existing dev terminal is conceptually richer than its pretty CRT. So this isn't you catching up to a better design — it's you having a real engine and a nice-looking sketch that doesn't fully understand it.

So the "am I there yet" framing dissolves: the skin you can take now, the State Map is the one real build, and the rest you ignore until the backend earns it.

Where do you want to push on this? Two things I'm curious about: does a dedicated **State Map view** actually fit how you think about the product, or is that drawer/inline territory for you — and is **"Soul"** the identity you want the UI built around, or were you tempted by the mockup's simpler "campaign/character" language?

---
