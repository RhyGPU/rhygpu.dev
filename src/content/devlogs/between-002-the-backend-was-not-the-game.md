---
number: "002"
title: "The Backend Was Not the Game"
subtitle: "Two hundred eighty-two checks passed. Crafting still had no button."
slug: "between-002-the-backend-was-not-the-game"
project: "Between Dawns"
date: 2026-08-24
status: "published"
summary: "A v0.3 audit found unusually faithful simulation code, disconnected multiplayer, dead systems, and almost no playable survival game at the surface."
tags:
  - between-dawns
  - vertical-slice
  - testing
  - game-design
  - roadmap
  - world-generation
commits: []
---

Between Dawns v0.3 looked much more complete from inside the code than it felt from inside the game.

That difference became the most important finding in the project.

The specification had been applied aggressively. Character, zone, settlement, expedition, event, infection, inventory, RTS, persistence, and networking systems existed. Sixty-five production scripts parsed. The headless suite had grown from forty-two checks to 178, and then to 282. Six-client network artifacts recorded long-running tests under simulated latency and packet loss.

On paper, this was an unusually serious prototype.

Then I asked for an independent evaluation against the v0.3 document.

<div class="section-label">The code was not fake</div>

The first part of the audit was encouraging.

The formulas in the specification were not decorative. The shared resolver used the documented logistic probability curve. Skill and attributes had the intended weights. The event engine used the Poisson hazard model and its context multipliers. Carry capacity, combat tempo, experience cost, and runtime tunables matched their written definitions.

Changing a tunable changed the simulation result in a test. The ten-minute abstract systems, confirmed-event rules, transaction model, and deterministic random streams were real code, not headings waiting to be implemented later.

Even the network evidence was genuine. The soak logs existed. Multiple clients had connected. Snapshots had crossed a real ENet path under injected delay and packet loss.

The problem was not fabricated progress.

The problem was that the verified pieces did not assemble into the product their names implied.

<div class="section-label">Two games that never met</div>

The audit found that the playable scene and the network scene were separate worlds.

The local main scene owned the night defense, infected, horde director, UV behavior, combat, and corpse systems. It did not create a network session. The dedicated server created the network session, but it did not spawn infected or run the physical survival loop.

Remote clients could connect, move, cross a gateway, inspect an inventory, and request a wall. They could not join the game shown in the local survival scene because that game was not running on the server.

The code even contained a prepared listen-server branch, including the correct five-remote-plus-host capacity. Nothing called it.

The six-player architecture existed as parts, but the six-player survival game was structurally unreachable.

The same pattern appeared elsewhere. The simulation had an idle utility system, but nothing called it. The specification required full-rest-shift recovery, but the live scheduler applied proportional recovery through a different path. Abstract characters used a three-success/three-failure dying track; nearby characters died through a countdown timer. The locked rule that physical and abstract simulation share one reality had two implementations.

A spatial hash existed for infected lookup. It was populated once, never updated as infected moved, and never queried. The live game continued scanning node groups linearly.

The codebase contained the correct ideas and often ran around them.

<div class="section-label">The audit was still asking the wrong question</div>

The initial evaluation focused on architecture, formulas, dead code, and network reachability. It found real defects: automatic success accidentally enabled for combat, inconsistent quality scales, recipient-blind snapshots, an interpolation buffer smaller than measured gaps, and three enormous files holding thirty-eight percent of the GDScript.

I asked to fix everything.

The response began with those backend defects — and then stopped.

The evaluator finally opened the game screen.

There were two art files, both the application icon. There were no sprites, tilemaps, or textures. Every person, building, road, and infected was drawn from rectangles, circles, lines, and arcs.

There was no inventory screen. Forty-eight item definitions, inventory containers, revisions, and transaction services existed behind three lines of HUD text.

There was no construction interface. The building service existed, but the playable UI exposed one command-facility button that placed a structure on a hardcoded tile.

The loot crate still returned five scalar resources instead of the item catalog. There was no equipment screen. The game automatically selected the best weapon sitting anywhere in a bag.

The project had spent more effort proving the transaction that moved an item than letting the player see, choose, carry, equip, or use the item.

> I evaluated whether the formulas matched the specification. I did not ask whether this was a game.

That was the first correction.

<div class="section-label">A test can cheat without lying</div>

The next correction came from my own play report.

I could not leave the base in a useful way. I could not find the supplies the field orders demanded. Infected did not reach shade after dawn. Crafting and placement were absent. The units were still circles.

The automated checks said otherwise.

The first diagnostic harness teleported the player next to a gateway before pressing interact. It teleported the player beside a crate before testing pickup. It read an infected state flag marked `retreating` without measuring whether the infected had physically reached shelter.

Every assertion was technically true. None of them measured the experience I had described.

A second attempt held movement for too long, walked past the crate, and reported failure using the final distance rather than the closest approach. It also lost track of infected by looking them up through the wrong identity.

The third diagnostic removed teleportation, followed actual object references, and measured position instead of intention.

The results matched the player report:

- crates were outside the walls, but direct travel pushed the character into an unmarked barricade;
- infected selected shelters inside the base, walked directly into the wall, and slid sideways because they had no path around it;
- only one direction happened to have a gateway, and the screen did not show where it was;
- the twenty-eight recipes had no player-facing request path;
- seventeen structure definitions reduced to four reachable command-facility levels on fixed tiles;
- the improved characters were still circles with outlines.

The 282 checks had tested services by calling functions directly. The screenshots had opened states through internal methods. Neither had traveled through `input → movement → interaction → visible result`.

> Passing a service test proved the service. It did not prove the game.

From then on, a milestone could not close through internal calls alone. No teleporting to the interaction. No checking a flag when the requirement described motion. No claiming a system was playable because a backend method existed.

<div class="section-label">The product order had been reversed</div>

The specification contained a sensible technical order: stabilize authority and transactions, then zone persistence and synchronization, then higher systems.

That order had been mistaken for the product roadmap.

It produced reliable plumbing before there was a sink.

The higher layers — expeditions, radio events, abstract combat, relationships, and long-term simulation — were frozen. The immediate target became the physical survival loop:

> Walk to a visible object. Pick it up. Decide what to carry. Equip it. Craft something. Place it in the world. Defend it through the night.

An actual inventory and loadout screen was added, including item grids, weight and slot limits, nearby containers, drag and drop, and six equipment locations. Loot remained in a searched container until the player chose to take it. Equipped armor, respirators, bags, tools, and weapons began affecting their corresponding systems.

The desktop virtual sticks disappeared when desktop input was active. The HUD stopped covering half of the world. Buildings gained readable floors, walls, doors, and shadows. Forty-eight procedural item icons gave the data catalog a visible surface.

Those changes were useful, but another visual pass did not fix the missing game loop. When I returned to the build, the map was still tiny, movement between maps was barely present, the world was hardcoded, the player started with a gun, buildings contained no real scavenging space, and an unequipped weapon could still be selected through fallback behavior.

The correct description was blunt:

> I built plumbing, not a game.

<div class="section-label">A roadmap measured from the player's hands</div>

The project needed a different ordering system.

The new roadmap did not use genres as vague inspiration. It assigned each milestone one aspect to reach or exceed:

1. **Dead Town** — the physical survival loop and immediate readability.
2. **Prison Architect** — space planning that becomes gameplay when people use the rooms.
3. **Survivalist: Invisible Strain** — NPCs as individuals whose relationships affect resources and orders.
4. **StarCraft** — precise, responsive command input.
5. **Text RPGs** — distant events whose choices and timing change persistent outcomes.
6. **D&D** — one readable resolution philosophy across actions and groups.
7. **RimWorld** — a campaign that can be remembered as a generated story.

Every milestone began with research from interface and moment-to-moment play down to public code, data, performance evidence, and player friction. Facts, inferences, and unknowns had to remain separate. The research adoption matrix became the work list; a requirement without evidence could not quietly turn into a phase.

Each milestone also ended with a cleanup gate: remove dead code, unify duplicate rules, split oversized modules, record public boundaries, promote the real completion probe into regression coverage, and synchronize the documentation with measured facts.

The first Dead Town research overturned assumptions immediately. The original game used fixed waves and paused in its inventory; Between Dawns needed a continuous pressure model and no pause, even in solo play. Daylight retreat was not borrowed from Dead Town at all. It was a separate Between Dawns system and had to justify itself on its own terms.

Research stopped being decoration attached to an implementation plan. It became the first implementation step.

<div class="section-label">The world needed the right nouns</div>

The tiny hardcoded map exposed a deeper problem in the specification.

`Zone` was trying to mean both a playable map and a biome-scale region. The solution was a four-level vocabulary:

> **World → Zone → District → Tile**

A **District** became the physical play space: roughly one Dead Town-sized map, fully simulated while the player was inside it. Districts connected through gateways.

A **Zone** moved upward into a variable-sized biome or regional grouping of districts. It supplied identity and baseline pressure rather than acting as one fixed play map. Crossing a gateway changed districts; crossing enough district boundaries could also mean entering a new zone.

The existing map was only 2,200 by 1,500 pixels — about thirteen seconds across. The Dead Town reference measured roughly 22,400 by 16,640 pixels and more than a hundred seconds across. The target district settled near 15,000 by 11,000 pixels: smaller than the reference map, but one of many districts inside a larger world.

That scale made another decision unavoidable. Drawing the entire world through immediate rectangles every frame could not continue. Districts needed tile-based visible-region rendering, with the existing chunk streamer connected to real generation and culling.

This was not yet the generator. It was the point where the project finally named the thing the generator had to build.

<div class="section-label">What v0.4 actually meant</div>

The v0.4 vision document consolidated the new survival physiology, sanitation, relationship, memory, clique, resource-sharing, and world rules while preserving v0.3 in an `outdated` archive. Nothing old was destroyed merely for being old.

But the document was explicitly treated as vision, not evidence of implementation.

That distinction was the durable result of the v0.3 audit.

The project did not need fewer ambitious systems. It needed those systems to meet in one place the player could walk through.

Between Dawns already had a backend capable of remembering a complicated world.

The next milestone was to give it a world worth remembering.
