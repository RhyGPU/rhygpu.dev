---
title: "Devlog 000, The Math Soulslike Was a Card Game"
date: 2026-05-30
phase: Pre-origin, concept, tool chain, scope
---

There was no code when this started. No Unreal project. No Codex session. There was a problem and a tool chain.

---

## The Problem

I had a game idea fighting inside my head for a while. A math-themed fantasy action RPG where enemies are defeated by solving equations through combat. Not a math game with combat bolted on. A real action game where the damage system is algebra, the armor system is arithmetic, and the execution finisher is a judge's gavel.

The working name was already locked: Pythagorean Harmony.

But there was a gap between what I wanted to think about and what I could actually produce. I am not a C++ wizard. I have never shipped a commercial game. Unreal Engine 5 is enormous. The distance between "cool math combat idea" and "compiling C++ project where a cube displays x + 5 = 10" is measured in weeks, or months, or never. Most game ideas die in that gap.

The tool chain was supposed to close it. Unreal Engine 5 for the engine. OpenAI Codex as the coding agent, running locally, reading project files, writing C++. Cursor available as backup but not paid yet, so Codex would be the primary workhorse. NVIDIA Kids' model generation tools for assets later, after gameplay was proven. And me: the designer, the tester, the person who decides what feels right.

The question was: what exactly do I tell Codex to build?

---

## Round 1: The Card Game Pitch

The very first design document started in the wrong genre entirely.

I asked for help structuring a math fantasy game concept, and the tool talked me into the safest possible starting point: a turn-based card battler. React and TypeScript. Browser-based. A single battle screen. The player is a math mage with spell cards. There is a variable called x. Cards like Arithmetic Bolt (deal 6 damage), Linear Spell (deal 2x + 3 damage), Increase X, Factor Shield, Probability Strike. The enemy has 50 HP and attacks for 8 per turn.

It was clean. It was scoped. It was implementable in one Codex session.

It was also not the game I wanted to make.

The card game prototype has math in it, but math is just damage numbers. The player clicks a card and watches a number go down. There is no moment where the player sees an equation, feels the pressure of an enemy winding up an attack, and has to solve under threat. That moment -- combat and math happening simultaneously, neither one spared -- was the entire reason the project existed.

So the card game was scrapped before it started. But it was useful. It forced the first design questions: what does "math combat" actually mean? What does the player do? What does the enemy do? How do you fail?

---

## Round 2: The Stupid Fun Ideas

The real concept emerged in a brainstorming session that started with "give me stupid but actually fun ideas for a math soulslike."

The ideas that mattered:

Enemies scream wrong math answers. A liar mage variant puts fake answers floating around the arena. When the player inputs a wrong answer, the enemy gets a morale buff and the game insults the player with medieval scholar energy: "The Academy weeps." "Your arithmetic has dishonored the realm."

A troll enemy that does not understand math. It sees 12 + 9 = ? and starts smashing numbered rocks on the ground until the correct one appears. The player dodges wrong numbers and attacks the right one.

The X Weapon. Not a sword. An execution finisher. The enemy is groggy, the equation is x + 7 = 19, the player inputs x = 12, and the screen says: VARIABLE ISOLATED.

Armor made of equations. Helmet: x + 3 = 10. Chestplate: 4 x 7. To break armor, you solve or attack each piece with the correct operation.

A mimic treasure chest that asks 2 + 2 = ? Answer wrong and it bites you. Answer 8 to 2 + 2 x 2 = ? and it attacks: "ORDER OF OPERATIONS, FOOL."

These were not systems yet. They were vibes. But they told me what the game needed to feel like: funny, aggressive, constantly blurring the line between being threatened and being amused.

---

## Round 3: The Two-Axis Difficulty Breakthrough

The single best design moment in the pre-development phase was realizing that enemy difficulty could split into two independent axes.

In most games, difficulty scales one way: stronger enemy equals more HP plus more damage plus faster attacks. Boring. Linear. Predictable.

What if it did not?

What if one enemy had the easiest equation imaginable -- x = 1, the answer is right there -- but an insane combat pattern? Delayed attacks, roll catches, fake windups, instant gap closers, parry bait. The answer is insultingly obvious. The enemy physically will not let you submit it. That enemy type says: "Can you survive long enough to answer?"

And the opposite: an enemy with a brutal equation -- ((3x + 12) / 4)^2 - 9 = 40 -- but a gentle, slow moveset. Three-second windup. Two attacks. If it connects, 90% of your HP is gone. That enemy says: "Can you solve under threat?"

Call them Duelist type (easy equation, hard combat) and Scholar type (hard equation, easy combat). Add Execution type (easy everything, tiny time window), Panic type (medium everything, chaotic), and Fake Difficulty type (looks scary, has a trick). Suddenly, level 10 does not just mean "harder." It means something different every time.

This idea has no equivalent in Slay the Spire, Dark Souls, or any math game I have seen. If the game only ever has one good idea, this should be it.

---

## Round 4: Philosophy Enemies

Then the thematic layer clicked. Some enemies should carry philosophies.

The Simple Truth. Theme: "Truth is simple. Reaching it is not." Equation: x = 1. Combat: extremely difficult.

The Razor Saint. Theme: Occam's Razor, "simple is best." Equation looks complicated but simplifies to something basic. Punishes overthinking.

The Skeptic. Many fake answers, hidden truth.

The Stoic. Slow, calm, relentless. Predictable but punishing.

The Absurdist. Nonsense-looking equations that are solvable underneath.

The Nihilist. Equations that erase themselves. No meaning unless the player assigns one.

The Determinist. Pre-scripted attack fate. Predictable but unavoidable unless understood.

Math gives the mechanic. Philosophy gives the soul. I did not want trolls with numbers on them. I wanted each enemy to represent a way of thinking, and for the player to feel that difference in the fight.

---

## Round 5: Choosing the Engine and Scoping the Prototype

The design settled on a third-person action RPG built in Unreal Engine 5, starting from the C++ Third Person Template. The aesthetic target was stylized fantasy, not realistic. The combat rhythm reference was Dark Souls and Sekiro: deliberate, pattern-based, punishing, readable.

The prototype scope was tight, deliberately hostile to scope creep:

Build a 1v1 combat prototype. Third-person movement. Lock-on. One enemy, a Goblin. The enemy displays an equation. The player enters a number. The player hits the enemy with an X weapon. Correct answer: instant execution. Wrong answer: enemy evolves. That is it. That is the entire first milestone.

Do not implement multiplayer, full inventory, save system, open world, symbolic algebra parser, boss fights, or DLC systems. The cube does not need a face. The Goblin does not need armor yet. The equation does not need to support fractions or trigonometry. x + 5 = 10 is enough to prove the concept.

---

## Round 6: NVIDIA, Kidmo, and the Asset Question

At some point, the question of models and animation came up. I had been thinking about NVIDIA's tools -- Edify 3D for text-to-3D asset generation, Audio2Face for facial animation. The question was whether these should be part of the core pipeline from day one.

The answer was no, and it was clarifying. Those tools are designed for final-asset production: pretty characters, cinematic cutscenes, polished faces. The prototype needs none of it. What the prototype needs is geometry that a player cube and a gray capsule can replace later. Mixamo for base animations. Quaternius universal animation library for CC0 action clips. Maybe Cascadeur for tweaking attack timing. The asset pipeline can wait until the combat loop is fun with placeholder shapes.

The real work is the math-combat system. Everything else is scaffolding.

---

## The Commitment

At the end of the concept phase, before Codex ever wrote a line of C++, the project looked like this:

One idea: enemies are equations, combat is algebra.

One prototype goal: player types 5, hits Goblin with X weapon, screen says AXIOM EXECUTION.

One unique mechanic: two-axis difficulty, where equation threat and combat threat are independent.

One art direction: stylized, readable, enemies wear their math on the outside.

One engine: Unreal Engine 5, Third Person C++ Template.

One coding agent: Codex, running locally, connected to the project folder.

One person: me, playing unfinished builds, reporting what feels wrong, refusing to add features until the core loop works.

That was Pythagorean Harmony before it had a single line of code. The next part of this log is what happened when Codex started writing C++ and the green text appeared.

---

Next: Devlog 001, where the project folder exists for the first time and Codex writes its first five files.
