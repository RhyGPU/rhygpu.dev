---
title: "Mnemosyne"
slug: "mnemosyne"
featured: true
order: 1
subtitle: "Local-first memory architecture for persistent AI characters."
status: "Active Alpha"
summary: "A desktop AI narrative engine that separates character memory, world state, prompt context, and debugging traces so LLM-driven characters can change without losing continuity."
repo: "https://github.com/RhyGPU/mnemosyne"
stack:
  - Tauri
  - React
  - TypeScript
  - Rust
  - SQLite
  - OpenAI-compatible APIs
highlights:
  - Designed a separation between subjective character memory and objective world continuity.
  - Built a context compiler to avoid raw-chat bloat while preserving recent scene texture.
  - Added payload inspection to debug exact model inputs instead of guessing why continuity failed.
  - "Added recovery workflows for bad generations: regenerate, fix, variants, restore pressure, and patch traceability."
  - Added fresh-session boundaries to prevent cross-session relationship and world-state contamination.
  - Refined narrator prompting so characters can act without resolving user reactions.
  - Designed a paper/terminal UI split for fiction surfaces and developer tools.
architecture:
  - User input
  - Context Compiler
  - Narrator model
  - Visible narration + hidden state
  - Parser / validator
  - Soul / World / relationship updates
  - Payload inspector / debug logs
  - Next turn
media:
  - title: Home dashboard
    type: screenshot
    src: /projects/mnemosyne/home-dashboard.png
    alt: Mnemosyne home dashboard showing living worlds, recent sessions, and engine status.
    caption: App shell and session entry point for persistent worlds, recent sessions, and engine status.
    status: available
  - title: Play view
    type: screenshot
    src: /projects/mnemosyne/play-view.png
    alt: Mnemosyne play view with the turn pipeline, message composer, model mode, and dev controls.
    caption: The main writing surface where the user interacts with the narrator while the engine maintains state behind the scene.
    status: available
  - title: State Map / Continuity View
    type: screenshot
    src: /projects/mnemosyne/state-map-or-soul-view.png
    alt: Mnemosyne State Map showing scene state, characters, relationships, objects, timeline, and memory inspector.
    caption: Inspectable continuity state separated from the visible transcript.
    status: available
  - title: Payload inspector
    type: screenshot
    src: /projects/mnemosyne/payload-inspector.png
    alt: Mnemosyne terminal developer UI showing pipeline logs, memory cycle, API debug, LLM payload counts, repair controls, and benchmark runner.
    caption: Developer view for model payload, pipeline state, repair controls, and benchmark diagnostics.
    status: available
  - title: Library scene launcher
    type: screenshot
    src: /projects/mnemosyne/library-scene-launcher.png
    alt: Mnemosyne library launcher showing scene selection, primary character selection, and session start controls.
    caption: Scenario and session launch flow with explicit world, character, and isolated-session boundaries.
    status: available
  - title: Repair / regenerate flow
    type: placeholder
    caption: Planned screenshot slot for recovery workflows around bad generations and state repair.
    status: planned
  - title: Settings / provider profile
    type: placeholder
    caption: Planned screenshot slot for model/provider configuration once the public UI is capture-ready.
    status: planned
proofNotes:
  - Devlogs document the design evolution from raw state blocks to inspectable session architecture.
  - GitHub repo contains the working alpha source.
  - README documents current implemented systems and known limitations.
showHighlightsPanel: false
tags:
  - local-first
  - AI roleplay
  - memory systems
  - state engine
---

## Problem

LLM characters lose continuity because normal chat is the wrong storage layer.

Raw chat history looks simple at first: keep sending the conversation back to the model and let the context window do the work. That fails as the session grows. Old prose gets the same weight as current state, completed actions can replay, hidden-state residue can leak back into the prompt, and the most dramatic line can overpower the most accurate fact.

Summaries fail in the opposite direction. They are smaller, but they flatten emotional rhythm. A summary can say `trust improved` or `the scene moved to the kitchen` without preserving the pressure, hesitation, timing, and last exchange that made the next response feel alive.

Mnemosyne also had to solve a harder split: character memory and world state are not the same thing. A Soul should remember subjective history, fear, trust, shame, attachment, and changed expectations. A World Log should remember locations, objects, plot threads, time, and objective continuity. If those buckets mix, characters become omniscient or world facts start behaving like emotional memories.

Fresh sessions add another failure mode. A new setup can inherit stale relationship warmth, old props, previous locations, or scenario-specific memories unless the app knows what should persist and what should reset.

Then there is the prompt problem. Every bug invites another rule. Too many prompt rules can make the narrator worse: cautious, overexplained, less alive. Mnemosyne's job is not to bury the model under machinery. It is to put the right machinery in the right layer.

## Core Idea

> The narrator writes. The state map remembers.

Mnemosyne separates visible narration from memory, world state, relationship state, and debugging machinery. The model writes the next scene from a compiled brief. The app carries the continuity, records what changed, and keeps the machine-readable parts out of the player's transcript.

That means the narrator can focus on prose while the engine handles state: Soul memory, World Log facts, relationship pressure, recent events, hidden patches, payload history, and repair trails.

## Architecture

<div class="flow-diagram" aria-label="Mnemosyne turn architecture">
  <span>User input</span>
  <span>Context Compiler</span>
  <span>Narrator model</span>
  <span>Visible narration + hidden state</span>
  <span>Parser / validator</span>
  <span>Soul / World / relationship updates</span>
  <span>Payload inspector / debug logs</span>
  <span>Next turn</span>
</div>

The loop is intentionally inspectable. If a response goes wrong, the failure can be traced to the compiled input, the model output, the hidden-state parse, the applied patch, or stale state carried into the next turn.

## Core Systems

<div class="case-grid">
  <article>
    <h3>Soul Memory</h3>
    <p>Subjective character continuity: what the character experienced, misread, feared, wanted, trusted, resisted, and emotionally carried forward.</p>
  </article>
  <article>
    <h3>World Log</h3>
    <p>Objective story continuity: location, active objects, plot threads, time pressure, recent events, and facts the narrator needs without making the character omniscient.</p>
  </article>
  <article>
    <h3>Context Compiler</h3>
    <p>Builds the model payload from clean recent chat plus structured state, avoiding raw-chat bloat while preserving immediate scene texture.</p>
  </article>
  <article>
    <h3>Hidden State / Patch Protocol</h3>
    <p>Separates visible prose from machine-readable state changes so memory, world, and relationship updates can be traced, rejected, regenerated, or restored.</p>
  </article>
  <article>
    <h3>Payload Inspector</h3>
    <p>Shows the exact prompt and state packet sent to the model, turning continuity bugs into debuggable input/output problems.</p>
  </article>
  <article>
    <h3>Regenerate / Fix / Variants</h3>
    <p>Recovery workflows for bad generations, including the harder state question: discarded responses should not quietly mutate the Soul.</p>
  </article>
  <article>
    <h3>Fresh Scenario State</h3>
    <p>Lets long-term Soul continuity persist while clearing volatile scenario residue: stale locations, old props, recent events, and relationship temperature from prior tests.</p>
  </article>
  <article>
    <h3>Prompt Cleanup V2 / Action Doctrine</h3>
    <p>Refines the narrator brief so characters can initiate pressure and act decisively without resolving the user's reaction or stealing user agency.</p>
  </article>
  <article>
    <h3>State Map Direction</h3>
    <p>A mode-aware visibility layer for player, reader, GM, and developer views, with redaction instead of deleting useful state.</p>
  </article>
</div>

## Technical Highlights

- Designed a separation between subjective character memory and objective world continuity.
- Built a context compiler to avoid raw-chat bloat while preserving recent scene texture.
- Added payload inspection to debug exact model inputs instead of guessing why continuity failed.
- Added recovery workflows for bad generations: regenerate, fix, variants, restore pressure, and patch traceability.
- Added fresh-session boundaries to prevent cross-session contamination.
- Refined narrator prompting so characters can act without resolving user reactions.
- Designed a paper/terminal UI split for fiction surfaces and developer tools.

## Development Journal

<div class="journal-links">
  <a href="/devlog/000-before-the-repository/"><strong>000</strong><span>Origin: the first crude state block and the moment Mnemosyne became a memory problem.</span></a>
  <a href="/devlog/002-splitting-memory-in-two/"><strong>002</strong><span>Soul vs World: subjective character memory separated from objective continuity.</span></a>
  <a href="/devlog/004-feeding-the-model-a-session-packet/"><strong>004</strong><span>Context Compiler: clean recent chat plus structured session state.</span></a>
  <a href="/devlog/006-opening-the-black-box/"><strong>006</strong><span>Payload Inspector: debugging the exact inputs sent to the narrator model.</span></a>
  <a href="/devlog/008-making-the-session-inspectable/"><strong>008</strong><span>Inspectable Session: visible chat export, payload history, and state diagnosis.</span></a>
  <a href="/devlog/009-starting-fresh-without-erasing-the-soul/"><strong>009</strong><span>Fresh Scenario State: persistent Soul continuity without stale world contamination.</span></a>
  <a href="/devlog/010-prompt-cleanup-v2/"><strong>010</strong><span>Prompt Cleanup V2: action doctrine, less machinery in the narrator brief, and UI-flow reset.</span></a>
</div>

## Current Status

Mnemosyne is a working alpha, not a polished public release.

The core memory/state/payload/debug loop exists: local desktop shell, structured continuity concepts, compiled model payloads, hidden-state parsing, inspection surfaces, recovery flows, and fresh-session boundaries.

The active work is long-session stability, memory provenance, cleaner entity separation, safer state import/export, and State Map V1. The product direction is becoming clearer too: fiction surfaces should feel paper/editorial; developer surfaces should feel terminal and inspectable.

## Roadmap

- State Map V1 with mode-aware visibility and redaction.
- Memory Inspector and provenance trails for why a memory exists.
- Entity separation so characters, objects, scenes, and world facts do not blur together.
- Safer import/export for local sessions, Souls, and state bundles.
- Local model runtime later, after the state loop is reliable.
- Better alpha documentation for setup, limits, and debugging workflows.

## What This Demonstrates

<div class="proof-list">
  <span>LLM systems design</span>
  <span>Stateful app architecture</span>
  <span>Local-first desktop development</span>
  <span>Debugging and instrumentation</span>
  <span>Prompt/context engineering</span>
  <span>Product thinking under ambiguity</span>
</div>
