---
title: "Pythagorean Harmony"
slug: "pythagorean-harmony"
featured: false
order: 3
subtitle: "Equation-duel combat prototype for a fantasy third-person action RPG."
status: "Playable Prototype"
summary: "A UE5 prototype exploring math-based combat, where enemies are defeated by transforming equations with operation weapons and executing with the correct value of x."
repo: "https://github.com/RhyGPU/PythagoreanHarmony"
stack:
  - Unreal Engine 5
  - C++
  - Blueprint tuning
  - Third Person Template
highlights:
  - Designed a combat loop where the learning object is the enemy state, not a separate quiz.
  - Turned algebra operations into weapon interactions.
  - Scoped the project around proving the core loop before building a full game.
  - Used UE5 third-person foundations with C++ core systems and Blueprint tuning.
  - "Built around readable player feedback: equation state, operation effects, correct answer execution, and wrong-answer consequences."
showHighlightsPanel: false
tags:
  - game prototype
  - UE5
  - math combat
  - lab
---

## Problem

Educational games often become homework with graphics or trivia pasted onto combat.

That is not the interesting version of the idea. The interesting version is making math part of the combat grammar itself: visible, physical, tactical, and legible under pressure.

The design problem for Pythagorean Harmony is whether equation solving can become a combat loop instead of an interruption. The player should not stop playing the game to answer a worksheet prompt. The equation should be the enemy state, and combat should be how the player transforms it.

## Core Idea

Enemies are not just HP bars.

Each enemy has an equation. The player reads that equation, survives the enemy, uses operation weapons to transform it, then uses the X weapon to execute once the correct value is known.

Wrong answers should not merely say "incorrect." They should create combat consequences, such as enemy evolution or a changed enemy state. The math has to matter inside the fight.

## Prototype Combat Loop

1. Read the enemy equation.
2. Survive enemy attacks.
3. Input numbers or choose operation weapons.
4. Use operation weapons to simplify or transform the equation.
5. Identify the correct value of x.
6. Land the X weapon execution.
7. If the answer is wrong, the enemy state changes or evolves.

## Example Encounter

An enemy displays:

```txt
x + 5 = 10
```

The player reasons:

```txt
x = 5
```

Then the player lands the X weapon with `5` to execute the enemy.

A more advanced enemy could require multiple operation steps before the X weapon is safe. The prototype direction is not only "type the answer." It is operation choice, timing, reading, pressure, and execution.

## Core Systems

<div class="case-grid">
  <article>
    <h3>Equation Enemy</h3>
    <p>The enemy's state is an equation, making the learning object part of the combat target instead of a separate quiz layer.</p>
  </article>
  <article>
    <h3>Operation Weapons</h3>
    <p>Weapon actions represent algebraic operations, letting the player transform the enemy equation through combat interactions.</p>
  </article>
  <article>
    <h3>X Weapon Execution</h3>
    <p>Once the correct value is known, the player uses the X weapon to execute the enemy with the answer.</p>
  </article>
  <article>
    <h3>Wrong Answer Evolution</h3>
    <p>Incorrect answers create combat consequences, such as enemy evolution or changed state, instead of ending at a simple failure message.</p>
  </article>
  <article>
    <h3>Combat Readability</h3>
    <p>The prototype depends on readable equation state, visible operation effects, clear execution timing, and understandable failure feedback.</p>
  </article>
  <article>
    <h3>UE5 Third-Person Prototype</h3>
    <p>The first playable prototype uses Unreal Engine 5's Third Person Template as the movement and camera foundation.</p>
  </article>
  <article>
    <h3>C++ Core / Blueprint Tuning</h3>
    <p>Core systems live in C++, with Blueprint used for tuning and simple linking where iteration speed matters.</p>
  </article>
</div>

## Technical Highlights

- Designed a combat loop where the learning object is the enemy state, not a separate quiz.
- Turned algebra operations into weapon interactions.
- Scoped the project around proving the core loop before building a full game.
- Used UE5 third-person foundations with C++ core systems and Blueprint tuning.
- Built around readable player feedback: equation state, operation effects, correct answer execution, and wrong-answer consequences.

## Current Status

Pythagorean Harmony is a first playable prototype and lab project.

The current focus is proving whether equation-duel combat can feel readable, tactical, and physical enough to justify deeper game development. It is not a full RPG yet. A full world, progression system, enemy roster, and long-term content are out of scope for the current prototype.

The working frame is "Math Souls Prototype: Equation Duel": prove the duel, then decide whether the larger game deserves to exist.

## What This Demonstrates

<div class="proof-list">
  <span>Gameplay systems design</span>
  <span>Educational mechanic design</span>
  <span>Unreal Engine prototyping</span>
  <span>C++ gameplay architecture</span>
  <span>Combat loop design</span>
  <span>Scope control</span>
  <span>Abstract math into interactive systems</span>
</div>
