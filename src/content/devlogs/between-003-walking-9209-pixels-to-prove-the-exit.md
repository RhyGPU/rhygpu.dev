---
number: "003"
title: "Walking 9,209 Pixels to Prove the Exit"
subtitle: "No teleporting, no hardcoded base, and no passing on flags."
slug: "between-003-walking-9209-pixels-to-prove-the-exit"
project: "Between Dawns"
date: 2026-08-26
status: "published"
summary: "The procedural district rewrite replaced the old base, proved real gateway travel, closed the M1 starting gaps, and survived a belated commit audit."
tags:
  - between-dawns
  - procedural-generation
  - district
  - godot
  - playtesting
  - git
commits:
  - hash: "c86482c8bd8b40551f9939a0eaeccd115c2ccf55"
    title: "Initial commit"
    repo: "between_dawns"
    url: "https://github.com/RhyGPU/between_dawns/commit/c86482c8bd8b40551f9939a0eaeccd115c2ccf55"
  - hash: "1b06cc4e4c8c4787f681929a05e64d3462b05c70"
    title: "feat(district): separate the procedural district generator"
    repo: "between_dawns"
    url: "https://github.com/RhyGPU/between_dawns/commit/1b06cc4e4c8c4787f681929a05e64d3462b05c70"
  - hash: "3cacdbc301019d80e4a1e6eee2d8772034914059"
    title: "feat(m1): close the four remaining starting-line gaps"
    repo: "between_dawns"
    url: "https://github.com/RhyGPU/between_dawns/commit/3cacdbc301019d80e4a1e6eee2d8772034914059"
---

The first map in Between Dawns was not really a world.

It was a 2,200-by-1,500-pixel yard with seven hardcoded buildings, a fixed intersection, fixed fields, a fixed player spawn, fixed NPC positions, and enough backend systems to describe a much larger game.

The v0.3 audit had established the new standard: if the player could not reach a result through ordinary input, the result was not playable. The next work applied that rule to the map itself.

The project stopped repairing the old base.

It replaced it.

<div class="section-label">People before terrain</div>

The visual rewrite started with the actors because the old circles made every later screenshot dishonest. A larger district would not feel more alive if its survivors and infected still looked like debug markers.

The replacement was procedural, but not a rotating paper doll.

The generator treated each actor as simple projected geometry, then baked eight distinct directions and eight frames per direction: idle, six walking frames, and an action pose. Guards, scavengers, clinic workers, builders, farmers, operators, drivers, and infected received different silhouettes and palettes.

The first sheets looked better at full size and failed where it mattered. The walk cycle disappeared at game scale. A weapon facing the camera collapsed into a dot. A standing infected seen from behind was almost indistinguishable from a survivor.

Those were geometry problems, so they were measured and fixed as geometry problems. Weapon depth was intentionally exaggerated. The carry angle moved away from the body. The infected received a rounded hunch that remained visible from the rear.

The readability probe reduced the actors to game size and grayscale. It did not pretend every survivor profession could be identified from a twenty-eight-pixel silhouette. It separated the survival-critical requirement instead:

> Can I tell a survivor from an infected before the mistake reaches melee range?

The final actor set produced twenty-four sheets. Bodies, holding poses, and weapons were separated into layers so an unarmed character actually had empty hands. The visual read from the authoritative equipment slots; a rifle sitting in a backpack could no longer appear in the character's hands.

The new sprites passed the real-window interaction probes. That qualification mattered because the headless runner had briefly reported every mouse control as broken: its zero-sized window transformed click coordinates by twenty times. The game was fine; the instrument was not. The failure was recorded in the roadmap so a broken runner could not certify or condemn future UI work.

<div class="section-label">A district-sized ground test</div>

The terrain could not continue as thousands of immediate drawing commands.

A generator baked a 192-by-480-pixel atlas containing fifteen terrain types with six variants each. Grass, dirt, road, concrete, floors, walls, and other surfaces wrapped their detail across tile boundaries so repetition did not create visible seams. Ground had no heavy outline; outlines remained the language of objects, not the floor beneath them.

Godot assembled the TileSet at runtime. `world_map.gd` stopped drawing ground primitives and kept only objects such as buildings, trees, walls, and labels.

Then the proposed district scale was tested rather than assumed.

The first timing result was useless because vertical synchronization locked the frame near sixteen milliseconds. With VSync disabled, a map containing 168,960 tiles added approximately 0.73 milliseconds. `TileMapLayer` culled to the visible viewport, so the cost followed screen area instead of the entire district.

That measurement allowed the project to keep the large district without inventing a custom chunk renderer prematurely.

<div class="section-label">The generator owns the world</div>

The old map had procedural fragments mixed with manual scenery. That was worse than either a fully authored map or a fully generated one because no file clearly owned the result.

The rewrite established a single boundary:

> `DistrictGenerator.generate()` creates terrain, roads, buildings, gateways, and placement data. `world_map.gd` renders the result.

The reference density provided a numeric target. Dead Town's measured world contained 1,658 placed instances across its map, approximately 3.14 objects per screen. A generated Between Dawns district averaged 631 objects, or 3.36 per screen — close enough to use as a baseline without copying the map.

The previous base was removed completely:

- the seven building array;
- the fixed base rectangle;
- the intersection, field, and workstation overlays;
- the manual gate creation path;
- old NPC and construction coordinates;
- hand-scattered clutter and duplicate biome labels;
- test assumptions tied to the original yard.

The founder now spawned at a shelter produced by the district seed. The first attempt exposed several hidden dependencies: a generated building could become fifteen by seventy-nine tiles, the leader still appeared at `(1100, 790)`, placement logic still believed the map was sixty-eight by forty-six tiles, and supply crates could appear behind or inside inaccessible buildings.

Each bug was evidence that the old base still owned part of the game. The fixes moved that ownership into generated anchors, open-ground placement, and district dimensions until a world-coordinate scan found no remaining literals from the old map.

<div class="section-label">A gateway is an agreement between two maps</div>

The first gateway implementation treated the entire thirty-pixel outer rim as an exit. On a fifteen-thousand-pixel-wide map, the player could leave from places that had no visual opening.

The replacement used edge identity.

Two neighboring district coordinates were sorted into the same canonical pair and hashed. Both districts independently derived the same set of openings from that shared edge seed. No saved handshake was required. If the eastern border of one district opened at a particular offset, the western border of its neighbor produced the corresponding opening.

Travel used the nearest real opening and placed the arriving character at the matching offset. Multiple openings on one border were allowed. Returning through the same edge preserved the route.

The first walking probe stalled after 3,731 pixels. It was not a timeout; the character remained motionless for 170 seconds against generated geometry. The detour logic could not route around a large building.

The probe and navigation were corrected without teleporting the actor to the answer.

The successful run walked 9,209 pixels across the generated district, reached the actual opening, crossed into the adjacent district, and retained a valid route home.

That is why the distance belongs in the title. A gateway method returning the correct neighbor had already been easy to prove. Walking the world to reach it proved something else.

<div class="section-label">Daylight had to remove the actors, not the problem</div>

The old dawn behavior changed an infected state and left it colliding with a wall. The generated world removed that wall trap, but the full day/night cycle still exposed several errors.

Infected reached a doorway and stopped because the retreat target was the threshold while the shelter test required them to be fourteen pixels inside. Once their daylight exposure became severe, their movement stopped completely, freezing them just short of safety. Even those that reached cover remained live nodes standing inside the building throughout the day.

The corrected path used two retreat stages: reach the entry, then continue toward the interior. At dawn's end, sheltered infected were absorbed into the building's abstract population instead of remaining physical actors. Unsheltered infected were removed by sunlight. At night, the building could release its stored infected back into the district.

The measured cycle was:

> Seven infected at night → two reach shelter → five perish in sunlight → zero remain on the daytime map → two emerge the following night.

This matched the world-resolution rule better than simply hiding sprites. A building interior could carry a number while the exterior district stopped paying for actors the player could not observe.

<div class="section-label">No gun until the world gives you one</div>

The old start handed pistols and ammunition to the founder, joining players, and default NPCs. That skipped the first survival decision and contradicted the scavenging loop.

The start moved through a crowbar phase and then to the stricter choice: empty hands.

Firearms became loot tied to eligible POI families. A probe started without a firearm and searched five kinds of location; three could produce one through play.

Finding a gun was still not enough. The first probe picked one up, left it in the backpack, and discovered that firing logic still used a weapon definition independent of the visible equipment. The renderer had been fixed earlier, but the action had not.

The final equipment gate made the slot authoritative for both presentation and use. A weapon in the bag was not in the hands. Equipping it changed the active weapon. An empty slot did not silently select the best item available.

The M1 starting-line audit now closed four concrete gaps:

- real district travel;
- full daylight retreat and re-emergence;
- unarmed starts with firearms found through scavenging;
- equipment slots controlling actual weapon use.

This did not mean M1 was complete. It meant the project had finally reached the line from which the Dead Town milestone could be judged honestly.

<div class="section-label">Committing only after the wrong order was exposed</div>

The project became a Git repository on August 26. Before the first push, generated artifacts, external research clones, caches, and conversation data were excluded. The initial private repository contained 294 project files and roughly 16.4 megabytes of source, documents, and real assets.

Three days later, the district and M1 work still existed as thirty-seven uncommitted changes. They were separated into two logical commits: the district generator in one, the remaining M1 starting-line changes in the other.

The first commit audit made a familiar mistake. It ran the static project validator, failed to find a system-wide Godot installation, noted that runtime tests were unverified, and pushed anyway.

That contradicted the user's condition: commit if the changes were not broken.

The portable Godot runtime had been inside `.tools/godot/` the entire time. It was ignored by Git, so the shallow search missed it. The README even documented the command.

The corrected audit ran the actual engine:

- static validation across seventy-eight GDScript files, invariants, and resource paths;
- `PASS: 283 checks` in the headless integration runner;
- a district generator probe averaging 631 objects and 3.36 objects per screen;
- a 9,209-pixel travel probe with district creation and return-route preservation;
- a daylight probe measuring seven infected down to zero and two returning at night;
- an armament probe proving an unarmed start and firearm acquisition through POIs.

The pushed commit messages still claimed the engine had been unavailable. After explicit approval, the two commits were recreated with the verified results, their trees were compared byte-for-byte with the originals, and the corrected history was force-pushed with a lease. The content did not change; the evidence attached to it did.

The current history ends at `3cacdbc`, local and remote aligned, with a clean worktree.

<div class="section-label">The next honest gap</div>

After the starting line closed, the game was run against the full Dead Town adoption matrix.

Seven gaps remained. The largest was immediate and embarrassing: firing a gun did not attract infected. Noise existed only as a scalar feeding a spawn budget. There was no physical sound event, no visible radius, and no hearing response in nearby actors.

That was good news in the only way a measured failure can be good news.

The district was no longer a fixed yard pretending to be a world. The player could cross it, leave it, return, survive its dawn, and earn the weapon used in the next test.

The remaining failures were finally failures inside the game.
