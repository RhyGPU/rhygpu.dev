---
number: "001"
title: "Deleting the First Game"
subtitle: "The first playable build was the wrong product."
slug: "between-001-deleting-the-first-game"
project: "Between Dawns"
date: 2026-08-23
status: "published"
summary: "How Between Dawns discarded a browser prototype, became a native Godot project, and learned to separate a playable foundation from a finished system."
tags:
  - between-dawns
  - godot
  - mobile
  - architecture
  - prototyping
  - testing
commits: []
---

The first playable version of Between Dawns lasted about twenty minutes before I killed it.

At 18:59, immediately after finishing the first design document, I gave it to Codex with a direct request:

> Build the game from this.

The fastest interpretation was a browser game. That made sense if the goal was to prove the loop with almost no setup: open a page, walk around a top-down map, gather supplies, reinforce a barricade, assign NPCs, and survive the night.

It was also the wrong product.

<div class="section-label">A prototype optimized for the wrong thing</div>

The first implementation choice optimized for immediate execution. A browser could provide a playable vertical slice without installing an engine or producing platform builds.

When I clarified that it was a phone game, the browser version gained landscape layout, twin-stick touch controls, large action buttons, orientation handling, and a PWA shell. The prototype became more mobile-friendly without becoming a mobile game.

That distinction should have been obvious.

At 19:23, I asked the question that ended the first build:

> Why is it in a browser? I said mobile and PC.

The browser was not a harmless delivery detail. It changed the assumptions around input, exports, filesystem access, performance, networking, dedicated servers, and what it meant to own the project after the coding session ended.

So the web build was deleted.

<div class="section-label">One native project</div>

The replacement was a Godot 4 project with Android and Windows as the first targets.

The same codebase would support touch, keyboard and mouse, and gamepad input. Mobile was not a desktop interface squeezed onto a smaller screen. It had a left movement stick, a right aiming stick, separate firing and interaction controls, safe-area-aware UI, and landscape presentation. PC kept direct mouse aiming and keyboard movement.

More importantly, the engine choice matched the game that had been designed the hour before. Between Dawns needed a persistent simulation, direct-IP networking, headless server support, deterministic world generation, local save data, and the ability to run without a browser between the player and the game.

The first native vertical slice contained the shortest version of the loop:

- collect supplies;
- reinforce the north and east entrances;
- assign NPCs through an operation table;
- survive the night spawn director;
- rescue downed survivors before they die;
- use UV as a limited defensive tool;
- reach the next dawn.

It was not the design document. It was one night at one outpost, built to prove that the basic pressure could be played.

<div class="section-label">“Implement everything”</div>

The next request was exactly what it sounds like:

> Implement all of it.

That forced a change from scene scripting to production architecture.

The current build was audited against the design. The gap was enormous: no persistent Zone Graph, no full construction or crafting loop, no six-player physical replication, no distant squads, no procedural materialization, no settlement economy, and no complete NPC simulation.

The plan therefore separated a playable vertical slice from a systems-complete alpha. The game assembly script would become thin. Core rules, simulation, networking, UI, and data would become separate modules. Listen servers and headless dedicated servers would run the same shared simulation. The server would own movement validation, combat, random outcomes, inventory, buildings, NPCs, zones, and saves.

The first technical review also caught several choices that looked reasonable on paper but would fail at the intended scale.

A 64×64-meter zone was too small for six players, NPCs, roads, farms, buildings, and a horde. The world moved to 256×256 logical tiles divided into 16×16 chunks. Zone edges received canonical seeds so an exit generated from either direction would still describe the same connection.

Randomness was split into independent streams. Firing one extra bullet could not be allowed to shift a global random sequence and change the biome or loot in a distant zone.

Player death became an explicit world policy instead of an accidental game-over screen. Disconnects became part of simulation too: after a short defensive AI window, the abandoned character would continue through abstract risk instead of teleporting safely home.

<div class="section-label">Building the foundation under the slice</div>

The implementation kept the playable outpost while adding the systems beneath it.

Input devices became adapters that produced the same input intent. The touch aiming stick stopped secretly firing and returned to doing one job; shooting became a separate action. Inventory items gained unique identities, revisions, idempotent transactions, and explicit rejection reasons so repeated network requests could not silently duplicate equipment.

The world gained deterministic coordinates, canonical edge generation, chunked zones, and separate random streams. Persistence moved toward immediate journal append, periodic compressed checkpoints, and backup recovery instead of repeatedly rewriting one giant save.

The data catalog was no longer a note in a plan. Forty-eight items, twenty-eight recipes, and fourteen structures entered the project as definitions. Services appeared for construction, contamination, NPC growth, shifts, RTS orders, direct control, confirmed events, and encounter materialization.

This was still not all connected to finished player-facing interfaces. But it changed the project from one scene containing every idea into a game that could accept those systems without being rewritten for each one.

<div class="section-label">The engine had to judge the engine</div>

Static checks were not enough.

A portable Godot 4.3 runtime was added to the local project tooling so the actual parser and headless runner could inspect the build. It immediately found problems that a file-level validator had missed: a hash function colliding with Godot's global `seed()` function, type-inference warnings promoted to errors, and an invalid audio resource header.

After those fixes, the project compiled in the real engine. The integration suite first reached thirty-one passing checks and then forty-two. The main scene booted without a runtime error.

The network path was tested as two separate processes: a dedicated server and a client connecting over ENet, negotiating the protocol, submitting an authoritative request, and receiving the response. That test also exposed a node-path assumption that differed between the server and client scene trees. The session root was unified and the test was run again.

This was the first point where “server-authoritative” meant more than a sentence in the vision document.

<div class="section-label">A game I could run without the agent</div>

When the build was ready, I asked how to run it. The game window was launched for me.

That was not good enough.

> Am I supposed to make you run it every time?

The result was mundane and necessary: `게임실행.bat` to start the game and `게임편집.bat` to open the project. A local project is not really handed over if its owner still needs the coding session to operate it.

The launchers were a small feature. They marked a much larger boundary between a demonstration and a usable development workspace.

<div class="section-label">The honest completion line</div>

Later that night, I compared the implementation against the expanding system specification and asked whether all of it had actually been built.

The honest answer was no.

What existed was a playable Gate A vertical slice plus the beginnings of the architecture: combat, loot, NPC assignment, down and rescue, input paths, transactions, persistence, deterministic world services, an ENet request path, and data catalogs.

What did not yet exist was equally important: full six-player character replication, multi-zone physical streaming, the complete settlement economy, production-ready expedition UI, the final text-simulation formulas, the full infection ecology, and every service connected back into play.

> A foundation can be implemented without the whole design being implemented.

That correction became part of the project discipline. Test counts and service files would no longer be allowed to imply that a feature was playable merely because its backend shape existed.

Between Dawns ended its first implementation session as a native Godot game that could boot, play one survival loop, run headless tests, and prove an authoritative client/server exchange.

The browser prototype had been faster.

Deleting it was still the first correct implementation decision.
