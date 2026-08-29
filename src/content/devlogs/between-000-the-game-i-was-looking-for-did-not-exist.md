---
number: "000"
title: "The Game I Was Looking For Did Not Exist"
subtitle: "A controller-game search turned into a six-player survival strategy game."
slug: "between-000-the-game-i-was-looking-for-did-not-exist"
project: "Between Dawns"
date: 2026-08-23
status: "published"
summary: "How the search for a better Dead Town became Between Dawns: a shared survival world designed around authority, territory, and the next sunrise."
tags:
  - between-dawns
  - origin
  - game-design
  - co-op
  - survival
  - networking
commits: []
---

I was not trying to make a game.

I had bought a controller and wanted something good to play with it: online co-op if possible, preferably on Android, and substantial enough that it did not feel like another disposable mobile game.

The search kept circling back to *Dead Town*. Its appeal was easy to describe — top-down scavenging, building, shared survival, and a night that actually gave the day a purpose. Finding a modern replacement was harder. One game had the survival loop but weak multiplayer. Another had co-op but felt cheap. Others had action, crafting, or zombies without creating a persistent world that a group could defend together.

The failed recommendations gradually became a design brief.

<div class="section-label">The sentence that started it</div>

At 16:12, after another dead end, I wrote:

> If I make my own version of Dead Town, the multiplayer will probably be bad too.

That was the turn.

The answer was not that networking would be easy. It was that this kind of game could be manageable if multiplayer was treated as the foundation instead of a feature added later.

The first shape was small: a 2D top-down survival game, a shared world, scavenging, containers, construction, combat, and nightly hordes. The host would own the truth. Clients would send intent. Item movement would be a server-approved transaction instead of every phone editing its own copy of an inventory.

Before there was a title, an engine, or a repository, there was already one rule:

> The world must have one authority.

<div class="section-label">Six players made the architecture real</div>

Two minutes later, the target became six-player co-op.

Tailscale, Radmin, or another virtual LAN could handle the awkward path between machines. The game did not need to begin with accounts, matchmaking, or a custom relay service. It only needed to treat that connection as transport — never as the game architecture itself.

That distinction mattered. The design separated the server authority from the player so the same core could support a listen server, a headless dedicated server, and direct-IP clients. A PC could run the authoritative world while six phones remained clients, avoiding the battery, heat, and background-process limits of making one phone host everything.

The scope guardrail was blunt. First prove two players. Then prove six. Do not build skill trees, vehicles, quests, NPCs, or weather until six people can move items at the same time without duplication or loss.

It was the first important technical decision in the project, made before the project existed.

<div class="section-label">The survival game became a settlement game</div>

Once the camera was top-down, RTS control felt natural. That immediately threatened to turn the idea into *RimWorld + Project Zomboid + RTS + Factorio*.

The way out was not to build a second game on top of the first. NPCs and robots would use the same world, items, movement, and combat rules as directly controlled characters. The RTS layer would only add a command interface: move, follow, defend, attack, and work.

Robots came first because their behavior could be narrow and legible — haul supplies, repair structures, defend an entrance, scavenge a marked area. Human survivors could become deeper later, with professions, fatigue, mental state, relationships, and permanent loss.

From there, the systems began connecting faster than I could name the project.

The world became an infinite graph of finite zones. Each zone could have its own biome, entrances, resources, arable land, and zombie pressure. Expansion would create its own cost: more territory meant more frontier entrances to defend.

Food would not be limited by an arbitrary population cap. It would be limited by safe, productive land. Wood and food could come from the living world; metal, machinery, firearms, and electronics would have to be recovered from the dead one. A fertile zone might feed a settlement while exposing it to a city that pushed hundreds of infected toward its northern gate.

The map itself became the expansion penalty.

<div class="section-label">A world at two resolutions</div>

The same idea also solved a problem that usually separates strategy games from action games.

Nearby events could run as physical gameplay. Distant expeditions could run as text and backend simulation. If the player drove to a distress call, the unresolved parts of that event could materialize into a playable location — but facts already established by the simulation could not be rerolled for convenience.

That meant direct control, RTS orders, and distant text events were not three unrelated modes. They were three views of the same characters, equipment, injuries, resources, and world state.

Later, a sufficiently developed operations center could let the player directly control a selected NPC during a rescue or withdrawal. A veteran would stop being a number in a roster and become someone the player had trained, equipped, commanded, and personally risked.

The settlement was no longer background decoration. The long-term reward was a community that could survive without requiring the founder to personally perform every dangerous job.

<div class="section-label">The first document, then the name</div>

By 18:26, the conversation had become a nineteen-page game vision and system design document. At 18:52, revision 0.2 expanded it to twenty pages and clarified a central risk: the founder's death still ended the run, while direct NPC control let the player delegate danger without making loss meaningless.

Five minutes later, the project finally received a name.

The loop had already written it:

> Survive the dawn. Scavenge, rescue, and expand during the day. Withdraw at sunset. Hold through the night. Reach the next dawn.

**Between Dawns** meant the entire game could fit inside the distance between two sunrises.

The name did not come first and pull a design behind it. It arrived after the networking model, the settlement, the territory economy, the expeditions, and the night had already converged on the same rhythm.

I started that morning looking for a controller game.

By the end of the day, I had the first specification for the game I could not find.
